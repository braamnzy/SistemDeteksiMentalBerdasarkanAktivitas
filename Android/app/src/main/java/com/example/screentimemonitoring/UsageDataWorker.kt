package com.example.screentimemonitoring

import android.app.usage.UsageStatsManager
import android.app.usage.UsageEvents
import android.content.Context
import android.util.Log
import android.app.NotificationChannel
import android.app.NotificationManager
import androidx.core.app.NotificationCompat
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException
import java.util.Calendar


class UsageDataWorker(appContext: Context, workerParams: WorkerParameters) :
    CoroutineWorker(appContext, workerParams) {

    companion object {
        private const val TAG = "WorkerDebug"
    }

    override suspend fun doWork(): Result {
        Log.d(TAG, "Worker Started: Checking access and running task.")

        if (!hasUsageAccess()) {
            Log.e(TAG, "Worker Failed: Usage Access not granted. Returning FAILURE.")
            return Result.failure()
        }

        return try {
            val (jsonArray, totalScreenTimeSeconds) = getDailyUsageData()

            sendDataToServer(jsonArray, totalScreenTimeSeconds)

            Log.d(TAG, "Worker SUCCEEDED: Data sent to server.")
            Result.success()

        } catch (e: Exception) {

            Log.e(TAG, "Worker FAILED (Network/Logic Error): ${e.message}", e)
            e.printStackTrace()
            Result.retry()
        }
    }

    private fun hasUsageAccess(): Boolean {
        val appOps =
            applicationContext.getSystemService(Context.APP_OPS_SERVICE) as android.app.AppOpsManager
        val mode = appOps.checkOpNoThrow(
            android.app.AppOpsManager.OPSTR_GET_USAGE_STATS,
            android.os.Process.myUid(),
            applicationContext.packageName
        )
        return mode == android.app.AppOpsManager.MODE_ALLOWED
    }

    private fun getRealScreenTime(
        usageStatsManager: UsageStatsManager,
        startTime: Long,
        endTime: Long
    ): Long {

        val usageEvents = usageStatsManager.queryEvents(startTime, endTime)
        val event = UsageEvents.Event()

        var lastResumeTime = 0L
        var totalScreenTimeMs = 0L
        var currentPackage: String? = null

        while (usageEvents.hasNextEvent()) {
            usageEvents.getNextEvent(event)

            when (event.eventType) {

                UsageEvents.Event.ACTIVITY_RESUMED -> {
                    lastResumeTime = event.timeStamp
                    currentPackage = event.packageName
                }

                UsageEvents.Event.ACTIVITY_PAUSED -> {
                    if (lastResumeTime > 0 && currentPackage == event.packageName) {
                        val duration = event.timeStamp - lastResumeTime
                        if (duration in 1..(60 * 60 * 1000)) {
                            totalScreenTimeMs += duration
                        }
                    }
                    lastResumeTime = 0L
                    currentPackage = null
                }
            }
        }

        if (lastResumeTime > 0) {
            val duration = endTime - lastResumeTime
            if (duration in 1..(60 * 60 * 1000)) {
                totalScreenTimeMs += duration
            }
        }

        return totalScreenTimeMs / 1000
    }

    private fun getDailyUsageData(): Pair<JSONArray, Long> {

        val usageStatsManager =
            applicationContext.getSystemService(Context.USAGE_STATS_SERVICE)
                    as UsageStatsManager

        val calendar = Calendar.getInstance().apply {
            set(Calendar.HOUR_OF_DAY, 0)
            set(Calendar.MINUTE, 0)
            set(Calendar.SECOND, 0)
            set(Calendar.MILLISECOND, 0)
        }

        val startTime = calendar.timeInMillis
        val endTime = System.currentTimeMillis()

        val realScreenTimeSeconds =
            getRealScreenTime(usageStatsManager, startTime, endTime)

        val topApps =
            getTopAppsUsage(usageStatsManager, startTime, endTime)

        Log.d(TAG, "REAL SCREEN TIME: ${realScreenTimeSeconds / 3600.0} hours")

        return Pair(topApps, realScreenTimeSeconds)
    }

    private fun getTopAppsUsage(
        usageStatsManager: UsageStatsManager,
        startTime: Long,
        endTime: Long
    ): JSONArray {

        val usageStatsMap =
            usageStatsManager.queryAndAggregateUsageStats(startTime, endTime)

        val usageMap = mutableMapOf<String, Long>()

        for ((pkg, stats) in usageStatsMap) {
            val sec = stats.totalTimeInForeground / 1000
            if (sec <= 0) continue

            if (pkg.startsWith("com.android.") &&
                !pkg.contains("chrome")) continue

            usageMap[pkg] = sec
        }

        val pm = applicationContext.packageManager
        val jsonArray = JSONArray()

        usageMap.entries
            .sortedByDescending { it.value }
            .take(10)
            .forEach { (pkg, sec) ->

                val appName = try {
                    pm.getApplicationLabel(pm.getApplicationInfo(pkg, 0)).toString()
                } catch (e: Exception) {
                    pkg
                }

                val obj = JSONObject()
                obj.put("package", pkg)
                obj.put("app_name", appName)
                obj.put("foreground_time_s", sec)
                jsonArray.put(obj)
            }

        return jsonArray
    }

    private fun showNotification(message: String) {
        val channelId = "usage_monitor_channel"
        val notificationManager =
            applicationContext.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                channelId,
                "Usage Monitor Alerts",
                NotificationManager.IMPORTANCE_HIGH
            )
            notificationManager.createNotificationChannel(channel)
        }

        val notification =
            NotificationCompat.Builder(applicationContext, channelId)
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle("Peringatan Penggunaan Layar")
                .setContentText(message)
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .build()

        notificationManager.notify(1, notification)
    }

    @Throws(IOException::class)
    private fun sendDataToServer(jsonArray: JSONArray, totalScreenTimeSeconds: Long) {
        val finalPayload = JSONObject()
        val deviceId = android.provider.Settings.Secure.getString(
            applicationContext.contentResolver,
            android.provider.Settings.Secure.ANDROID_ID
        )

        finalPayload.put("device_id", deviceId)
        finalPayload.put("total_screen_time_s", totalScreenTimeSeconds)
        finalPayload.put("usage_data", jsonArray)

        val client = OkHttpClient()
        val mediaType = "application/json; charset=utf-8".toMediaType()
        val body = finalPayload.toString().toRequestBody(mediaType)
        val fullUrl = "${ServerConfig.BASE_URL}/receive_usage"

        val request = Request.Builder()
            .url(fullUrl)
            .post(body)
            .build()

        client.newCall(request).execute().use { response ->

            val responseBody = response.body?.string()
            Log.d(TAG, "Response: code=${response.code}, body=$responseBody")

            if (!response.isSuccessful) {
                throw IOException("HTTP FAILED: ${response.code}")
            }

            if (responseBody != null) {
                val json = JSONObject(responseBody)

                val level = json.optString("level", "rendah")
                val message = json.optString("message", "")
                val prefs = applicationContext.getSharedPreferences(
                    "stress_prefs",
                    Context.MODE_PRIVATE
                )
                prefs.edit()
                    .putString("last_stress_level", level)
                    .putString("last_stress_message", message)
                    .apply()

                if (level.equals("tinggi", ignoreCase = true) && message.isNotEmpty()) {
                    showNotification(message)
                    Log.d(TAG, "Notifikasi ditampilkan (level: tinggi)")
                } else {
                    Log.d(TAG, "Level $level → tidak ada notifikasi")
                }
            }
        }
    }
}