# 🚀 PANDUAN SETUP - Stress Detection System

## 📁 Struktur File yang Benar

```
ProjekSiscer/
├── Android/                    # Folder aplikasi Android (Kotlin)
│   └── (file-file Android kamu)
├── backend/
│   ├── data/                   # Auto-generated saat running
│   │   ├── dataset_{device_id}.csv
│   │   └── detail_{device_id}.csv
│   ├── logic/
│   │   ├── __init__.py         # Kosong (agar jadi package Python)
│   │   └── fuzzy_logic.py      # ⭐ File ini KRUSIAL (81 aturan)
│   ├── static/
│   │   └── style.css           # ⭐ CSS elegant baru
│   ├── templates/
│   │   └── dashboard.html      # ⭐ Dashboard interaktif baru
│   ├── app.py                  # ⭐ Flask backend (updated)
│   ├── config.py               # ⭐ Konfigurasi IP & parameter
│   ├── room_generator.py       # Simulator IoT sensor
│   ├── requirements.txt        # Dependencies Python
│   └── README.md
```

---

## 🔧 LANGKAH 1: Setup Backend (Flask)

### 1.1 Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 1.2 Konfigurasi IP (PENTING!)

Edit file `config.py`:

```python
# Ganti dengan IP komputer kamu!
ANDROID_SERVER_URL = "http://192.168.1.100:5000"  # ⚠️ UBAH INI!
```

**Cara mendapatkan IP komputer:**

**Windows:**
```cmd
ipconfig
```
Cari **IPv4 Address** di adapter yang aktif (WiFi/Ethernet)
Contoh: `192.168.1.100`

**Linux/Mac:**
```bash
ifconfig
# atau
ip addr show
```
Cari `inet` address
Contoh: `192.168.1.100`

### 1.3 Jalankan Flask Server

```bash
python app.py
```

Output:
```
============================================================
🚀 Stress Detection System - Server Started
============================================================
Dashboard: http://localhost:5000
API Endpoints:
  - POST /receive_sensor (IoT data)
  - POST /receive_usage (Android screen time)
============================================================
```

### 1.4 Jalankan Simulator IoT (Terminal Baru)

```bash
python room_generator.py
```

Output:
```
============================================================
🔬 REALISTIC IoT SENSOR SIMULATOR
============================================================
[2025-12-16 10:30:15] Mengirim data Sensor...
  🌡️ Suhu: 23.5°C | 💧 Kelembaban: 65.0% | 🌫️ AQ: 0.4
  ✅ Sent to Server
```

---

## 📱 LANGKAH 2: Setup Android (Kotlin)

### 2.1 Konfigurasi IP di App Android

Di aplikasi Kotlin kamu, tambahkan konstanta untuk server URL:

```kotlin
// Constants.kt atau MainActivity.kt
object Config {
    // ⚠️ Ganti dengan IP komputer tempat Flask berjalan!
    const val SERVER_URL = "http://192.168.1.100:5000"
    
    // Endpoint untuk kirim data screen time
    const val ENDPOINT_USAGE = "$SERVER_URL/receive_usage"
}
```

### 2.2 Permission yang Dibutuhkan

Tambahkan di `AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.PACKAGE_USAGE_STATS" />
```

### 2.3 Format Data yang Dikirim ke Server

```json
{
  "device_id": "samsung_galaxy_s21",
  "total_screen_time_s": 18000,
  "usage_data": [
    {
      "app_name": "Instagram",
      "foreground_time_s": 5400
    },
    {
      "app_name": "WhatsApp",
      "foreground_time_s": 3600
    }
  ]
}
```

### 2.4 Contoh Kode Kotlin untuk Kirim Data

```kotlin
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import org.json.JSONArray

class StressDetectionService {
    private val client = OkHttpClient()
    
    fun sendUsageData(
        deviceId: String,
        totalScreenTimeSec: Long,
        usageList: List<AppUsage>
    ) {
        // Build JSON
        val json = JSONObject().apply {
            put("device_id", deviceId)
            put("total_screen_time_s", totalScreenTimeSec)
            
            val usageArray = JSONArray()
            usageList.forEach { app ->
                val appJson = JSONObject().apply {
                    put("app_name", app.name)
                    put("foreground_time_s", app.durationSec)
                }
                usageArray.put(appJson)
            }
            put("usage_data", usageArray)
        }
        
        // Send POST request
        val mediaType = "application/json; charset=utf-8".toMediaType()
        val body = json.toString().toRequestBody(mediaType)
        
        val request = Request.Builder()
            .url(Config.ENDPOINT_USAGE)
            .post(body)
            .build()
        
        client.newCall(request).execute().use { response ->
            if (response.isSuccessful) {
                val result = JSONObject(response.body?.string() ?: "")
                val stressValue = result.getJSONObject("fuzzy_analysis")
                    .getDouble("stress_value")
                
                // Update UI dengan hasil
                updateStressUI(stressValue)
            }
        }
    }
}

data class AppUsage(
    val name: String,
    val durationSec: Long
)
```

---

## 🌐 LANGKAH 3: Koneksi & Testing

### 3.1 Checklist Koneksi

- [ ] PC dan HP **harus** dalam WiFi yang **sama**
- [ ] Firewall **tidak** memblokir port 5000
- [ ] Flask server running di `0.0.0.0:5000`
- [ ] IP di config.py **sudah benar**
- [ ] IP di Android app **sudah benar**

### 3.2 Test Koneksi dari Browser HP

Buka browser di HP, ketik:
```
http://192.168.1.100:5000
```
(Ganti dengan IP komputer kamu)

Jika berhasil, kamu akan lihat dashboard.

### 3.3 Test dengan Postman/cURL

**Test endpoint IoT:**
```bash
curl -X POST http://localhost:5000/receive_sensor \
  -H "Content-Type: application/json" \
  -d '{"temperature": 28.5, "humidity": 65, "air_quality": 1.2}'
```

**Test endpoint Android:**
```bash
curl -X POST http://localhost:5000/receive_usage \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "test_phone",
    "total_screen_time_s": 21600,
    "usage_data": [
      {"app_name": "Instagram", "foreground_time_s": 7200},
      {"app_name": "WhatsApp", "foreground_time_s": 5400}
    ]
  }'
```

Response:
```json
{
  "status": "success",
  "device_id": "test_phone",
  "fuzzy_analysis": {
    "stress_value": 65.43,
    "category": "High Stress",
    "message": "Kondisi tidak ideal. Segera istirahat..."
  }
}
```

---

## 🔬 LANGKAH 4: Cara Kerja Sistem

### 4.1 Alur Data

```
IoT Sensor → room_generator.py → Flask (/receive_sensor)
                                      ↓
                                 LAST_IOT_DATA
                                      ↓
Android App → HTTP POST → Flask (/receive_usage)
                              ↓
                         fuzzy_logic.py (81 aturan)
                              ↓
                         CSV + Dashboard Update
```

### 4.2 Fuzzy Mamdani - 81 Aturan

**Input (4 variabel × 3 kategori = 81 kombinasi):**
- Screen Time: Low (0-4h), Medium (5-9h), High (10-24h)
- Temperature: Cold (15-22°C), Normal (20-28°C), Hot (26-35°C)
- Humidity: Low (30-50%), Medium (45-75%), High (70-90%)
- Air Quality: Good (0-1.5), Moderate (1-3.5), Poor (3-5)

**Proses:**
1. **Fuzzifikasi**: Input crisp → derajat keanggotaan fuzzy
2. **Inference**: 81 aturan IF-THEN dengan operator MIN (AND)
3. **Defuzzifikasi**: Centroid method → output crisp (0-100)

**Output:**
- Very Low Stress (0-20)
- Low Stress (20-40)
- Medium Stress (40-60)
- High Stress (60-80)
- Very High Stress (80-100)

### 4.3 Contoh Perhitungan

**Input:**
- Screen Time: 6 jam
- Temperature: 28°C
- Humidity: 70%
- Air Quality: 2.5

**Fuzzifikasi:**
- Screen → Medium: 0.67, High: 0.17
- Temp → Normal: 0.50, Hot: 0.50
- Humid → Medium: 0.33, High: 0.67
- AQ → Moderate: 0.50, Poor: 0.17

**Rules yang aktif:**
```
IF Screen=Medium AND Temp=Normal AND Humid=High AND AQ=Moderate
   → Strength = min(0.67, 0.50, 0.67, 0.50) = 0.50 → Output: High

IF Screen=Medium AND Temp=Hot AND Humid=High AND AQ=Moderate
   → Strength = min(0.67, 0.50, 0.67, 0.50) = 0.50 → Output: High

... (total ~12-15 rules aktif)
```

**Defuzzifikasi (Centroid):**
```
Stress = Σ(x × μ(x)) / Σμ(x) ≈ 62.5
Category: High Stress
```

---

## 🐛 TROUBLESHOOTING

### Error: "Connection refused"
- ✅ Pastikan Flask server running
- ✅ Cek firewall tidak block port 5000
- ✅ PC dan HP dalam WiFi yang sama

### Error: "ModuleNotFoundError: No module named 'logic'"
- ✅ Pastikan file `logic/__init__.py` ada (boleh kosong)
- ✅ Jalankan `app.py` dari folder `backend/`

### Error: "ImportError: cannot import name 'fuzzy_logic'"
- ✅ Pastikan `fuzzy_logic.py` ada di folder `logic/`
- ✅ Isi file tidak boleh kosong (pakai code yang sudah dibuat)

### Dashboard tidak update
- ✅ Buka Developer Tools (F12) → Console, cek error
- ✅ Pastikan route `/api/dashboard_data` berfungsi
- ✅ Test: http://localhost:5000/api/dashboard_data

### Data CSV tidak tersimpan
- ✅ Cek folder `data/` sudah dibuat
- ✅ Cek permission write di folder
- ✅ Lihat log di console untuk error

---

## 📊 Output Data

### File CSV yang dihasilkan:

**1. dataset_{device_id}.csv** (Summary)
```csv
timestamp,temp,humid,aq,screen_hours,stress_val,category
2025-12-16 10:30:00,28.5,65.0,1.2,6.0,62.5,High Stress
```

**2. detail_{device_id}.csv** (App Details)
```csv
timestamp,app_name,duration_sec
2025-12-16 10:30:00,Instagram,7200
2025-12-16 10:30:00,WhatsApp,5400
```

---

## 🎯 Checklist Final

- [ ] fuzzy_logic.py sudah diisi dengan 81 aturan
- [ ] config.py sudah disesuaikan dengan IP kamu
- [ ] Flask server berjalan tanpa error
- [ ] room_generator.py mengirim data sensor
- [ ] Dashboard bisa diakses di browser
- [ ] Android app bisa kirim data ke server
- [ ] Data tersimpan di CSV
- [ ] Stress value muncul di dashboard

---

## 📞 Support

Jika ada masalah:
1. Cek log di terminal Flask
2. Cek log di logcat Android
3. Test endpoint dengan Postman/cURL
4. Pastikan semua file ada di struktur yang benar

**Semoga berhasil! 🚀**