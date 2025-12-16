from flask import Flask, request, jsonify, render_template
from datetime import datetime
import csv
import os
from logic import fuzzy_logic

app = Flask(__name__)

# === KONFIGURASI ===
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

# State Global untuk data IoT terakhir
LAST_IOT_DATA = {
    "temperature": 25.0,
    "humidity": 60.0,
    "air_quality": 0.25,
    "timestamp": datetime.now()
}

# State Global untuk data HP terakhir
LATEST_PHONE_DATA = {}

# State Global untuk screen time terakhir
LAST_SCREEN_TIME = 0.0

# === ROUTE WEB DASHBOARD ===

@app.route('/')
def dashboard():
    """Halaman utama dashboard"""
    return render_template('dashboard.html')

@app.route('/api/dashboard_data')
def get_dashboard_data():
    """API untuk frontend mengambil data real-time"""
    
    # Default values
    current_device = "Menunggu Data..."
    current_stress = 0
    current_msg = "Sistem Siap"
    current_cat = "-"
    
    # Ambil data HP terakhir jika ada
    if LATEST_PHONE_DATA:
        last_device_id = list(LATEST_PHONE_DATA.keys())[-1]
        data = LATEST_PHONE_DATA[last_device_id]
        current_device = last_device_id
        current_stress = data['stress_val']
        current_msg = data['msg']
        current_cat = data['category']

    return jsonify({
        "iot": {
            "temp": LAST_IOT_DATA["temperature"],
            "humid": LAST_IOT_DATA["humidity"],
            "aq": LAST_IOT_DATA["air_quality"],
            "screen_time": LAST_SCREEN_TIME,  # ✅ TAMBAHAN INI
            "last_update": LAST_IOT_DATA["timestamp"].strftime('%H:%M:%S')
        },
        "analysis": {
            "device_id": current_device,
            "stress_score": current_stress,
            "category": current_cat,
            "message": current_msg
        }
    })

# === ROUTE PENERIMA DATA ===

@app.route('/receive_sensor', methods=['POST'])
def receive_sensor():
    """Menerima data dari IoT sensor (simulator)"""
    global LAST_IOT_DATA
    
    try:
        data = request.get_json(force=True)
        
        LAST_IOT_DATA["temperature"] = float(data.get("temperature", 25))
        LAST_IOT_DATA["humidity"] = float(data.get("humidity", 50))
        LAST_IOT_DATA["air_quality"] = float(data.get("air_quality", 0.1))
        LAST_IOT_DATA["timestamp"] = datetime.now()
        
        print(f"[IoT] T:{LAST_IOT_DATA['temperature']}°C H:{LAST_IOT_DATA['humidity']}% AQ:{LAST_IOT_DATA['air_quality']}")
        
        return jsonify({"status": "updated"}), 200
    
    except Exception as e:
        print(f"[ERROR] receive_sensor: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/receive_usage', methods=['POST'])
def receive_usage():
    """Menerima data screen time dari Android"""
    global LATEST_PHONE_DATA, LAST_SCREEN_TIME
    
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No data"}), 400

        # 1. Identifikasi Device
        device_id = data.get("device_id", "unknown_device")
        total_sec = data.get("total_screen_time_s", 0)
        usage_list = data.get("usage_data", [])
        
        # 2. Konversi ke jam
        total_hours = total_sec / 3600
        LAST_SCREEN_TIME = total_hours  # ✅ TAMBAHAN INI
        
        # 3. Hitung dengan Fuzzy Logic
        fuzzy_result = fuzzy_logic.calculate_stress(
            total_hours, 
            LAST_IOT_DATA["temperature"], 
            LAST_IOT_DATA["humidity"], 
            LAST_IOT_DATA["air_quality"]
        )
        
        # 4. Simpan ke CSV (terpisah per device)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # File summary: data/dataset_{device_id}.csv
        filename_summary = os.path.join(DATA_FOLDER, f"dataset_{device_id}.csv")
        file_exists = os.path.isfile(filename_summary)
        
        with open(filename_summary, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow([
                    "timestamp", "temp", "humid", "aq", 
                    "screen_hours", "stress_val", "category"
                ])
            writer.writerow([
                timestamp,
                LAST_IOT_DATA["temperature"],
                LAST_IOT_DATA["humidity"],
                LAST_IOT_DATA["air_quality"],
                f"{total_hours:.2f}",
                fuzzy_result["stress_value"],
                fuzzy_result["category"]
            ])
        
        # File detail app usage: data/detail_{device_id}.csv (opsional)
        if usage_list:
            filename_detail = os.path.join(DATA_FOLDER, f"detail_{device_id}.csv")
            detail_exists = os.path.isfile(filename_detail)
            
            with open(filename_detail, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not detail_exists:
                    writer.writerow(["timestamp", "app_name", "duration_sec"])
                for app in usage_list:
                    writer.writerow([
                        timestamp,
                        app.get("app_name", "unknown"),
                        app.get("foreground_time_s", 0)
                    ])
        
        # 5. Update state global untuk dashboard
        LATEST_PHONE_DATA[device_id] = {
            "stress_val": fuzzy_result["stress_value"],
            "category": fuzzy_result["category"],
            "msg": fuzzy_result["message"]
        }

        # Log
        print(f"\n✅ [Android:{device_id}] Screen:{total_hours:.1f}h | Stress:{fuzzy_result['stress_value']:.0f} ({fuzzy_result['category']})")
        print(f"   Rules activated: {fuzzy_result['fuzzy_details']['total_rules']}")
        print(f"   IoT: T={LAST_IOT_DATA['temperature']}°C, H={LAST_IOT_DATA['humidity']}%, AQ={LAST_IOT_DATA['air_quality']}\n")

        return jsonify({
            "status": "success",
            "device_id": device_id,
            "level" : fuzzy_result["category"],
            "message": fuzzy_result["message"], 
            "fuzzy_analysis": {
                "stress_value": fuzzy_result["stress_value"],
                "category": fuzzy_result["category"],
                "message": fuzzy_result["message"],
                "activated_rules": fuzzy_result['fuzzy_details']['total_rules']
            }
        }), 200
    
    except Exception as e:
        print(f"[ERROR] receive_usage: {e}")
        import traceback
        traceback.print_exc()  # ✅ Print full error untuk debugging
        return jsonify({"error": str(e)}), 500

# === ENDPOINT UNTUK DEBUGGING ===
@app.route('/test', methods=['GET'])
def test_endpoint():
    """Endpoint untuk test koneksi dari Android"""
    return jsonify({
        "status": "OK",
        "message": "Server is running!",
        "timestamp": datetime.now().isoformat()
    }), 200

# === MAIN ===
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Stress Detection System - Server Started")
    print("=" * 60)
    print("Dashboard: http://localhost:5000")
    print("Test dari HP: http://192.168.1.11:5000/test")
    print("\nAPI Endpoints:")
    print("  - POST /receive_sensor (IoT data)")
    print("  - POST /receive_usage (Android screen time)")
    print("  - GET  /test (Connection test)")
    print("=" * 60)
    
    # Host 0.0.0.0 agar bisa diakses dari jaringan lokal
    app.run(host="0.0.0.0", port=5000, debug=True)