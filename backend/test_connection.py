"""
test_connection.py
Script untuk testing koneksi antara Android dan Flask Server
"""

import requests
import json
import time
from datetime import datetime

# ========================================
# KONFIGURASI - UBAH SESUAI SETUP KAMU
# ========================================
SERVER_URL = "http://192.168.1.11:5000"  # Ganti dengan IP laptop kamu

# Test data yang akan dikirim (simulasi Android)
TEST_ANDROID_DATA = {
    "device_id": "test_phone_12345",
    "total_screen_time_s": 18000,  # 5 jam = 18000 detik
    "usage_data": [
        {
            "app_name": "Instagram",
            "foreground_time_s": 7200
        },
        {
            "app_name": "WhatsApp",
            "foreground_time_s": 5400
        },
        {
            "app_name": "YouTube",
            "foreground_time_s": 3600
        },
        {
            "app_name": "TikTok",
            "foreground_time_s": 1800
        }
    ]
}

def print_header(text):
    """Print header dengan border"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"❌ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def test_1_server_reachable():
    """Test 1: Apakah server bisa dijangkau?"""
    print_header("TEST 1: Server Reachability")
    
    try:
        response = requests.get(SERVER_URL, timeout=5)
        print_success(f"Server dapat dijangkau di {SERVER_URL}")
        print_info(f"Status Code: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print_error("Tidak dapat terhubung ke server!")
        print_info("Kemungkinan penyebab:")
        print("   1. Flask server belum dijalankan")
        print("   2. IP address salah")
        print("   3. Firewall memblokir port 5000")
        print("   4. PC dan HP tidak dalam WiFi yang sama")
        return False
    except requests.exceptions.Timeout:
        print_error("Connection timeout!")
        print_info("Server terlalu lama merespons")
        return False
    except Exception as e:
        print_error(f"Error tidak terduga: {e}")
        return False

def test_2_sensor_endpoint():
    """Test 2: Apakah endpoint sensor berfungsi?"""
    print_header("TEST 2: Sensor Endpoint (/receive_sensor)")
    
    test_sensor_data = {
        "temperature": 28.5,
        "humidity": 65.0,
        "air_quality": 1.5
    }
    
    try:
        response = requests.post(
            f"{SERVER_URL}/receive_sensor",
            json=test_sensor_data,
            timeout=5
        )
        
        if response.status_code == 200:
            print_success("Sensor endpoint berfungsi!")
            print_info(f"Response: {response.json()}")
            return True
        else:
            print_error(f"Server returned status code: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Error saat test sensor endpoint: {e}")
        return False

def test_3_usage_endpoint():
    """Test 3: Apakah endpoint usage (Android) berfungsi?"""
    print_header("TEST 3: Android Usage Endpoint (/receive_usage)")
    
    try:
        print_info("Mengirim data simulasi Android...")
        print_info(f"Device ID: {TEST_ANDROID_DATA['device_id']}")
        print_info(f"Screen Time: {TEST_ANDROID_DATA['total_screen_time_s']/3600:.1f} hours")
        print_info(f"Apps: {len(TEST_ANDROID_DATA['usage_data'])} apps")
        
        response = requests.post(
            f"{SERVER_URL}/receive_usage",
            json=TEST_ANDROID_DATA,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print_success("Android endpoint berfungsi!")
            
            result = response.json()
            print("\n📊 HASIL ANALISIS FUZZY:")
            print(f"   Device ID: {result['device_id']}")
            
            analysis = result['fuzzy_analysis']
            print(f"   Stress Value: {analysis['stress_value']:.2f}")
            print(f"   Category: {analysis['category']}")
            print(f"   Message: {analysis['message']}")
            
            return True
        else:
            print_error(f"Server returned status code: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Error saat test usage endpoint: {e}")
        return False

def test_4_dashboard_api():
    """Test 4: Apakah dashboard API berfungsi?"""
    print_header("TEST 4: Dashboard API (/api/dashboard_data)")
    
    try:
        response = requests.get(
            f"{SERVER_URL}/api/dashboard_data",
            timeout=5
        )
        
        if response.status_code == 200:
            print_success("Dashboard API berfungsi!")
            
            data = response.json()
            print("\n🌐 DATA DASHBOARD:")
            print("   IoT Sensor:")
            print(f"      Temperature: {data['iot']['temp']}°C")
            print(f"      Humidity: {data['iot']['humid']}%")
            print(f"      Air Quality: {data['iot']['aq']}")
            print(f"      Last Update: {data['iot']['last_update']}")
            
            print("\n   Analysis:")
            print(f"      Device: {data['analysis']['device_id']}")
            print(f"      Stress: {data['analysis']['stress_score']}")
            print(f"      Category: {data['analysis']['category']}")
            
            return True
        else:
            print_error(f"Server returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error saat test dashboard API: {e}")
        return False

def print_summary(results):
    """Print summary hasil testing"""
    print_header("RINGKASAN HASIL TEST")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    
    print("\nDetail:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    if passed == total:
        print("\n🎉 SEMUA TEST BERHASIL!")
        print("✅ Server siap menerima data dari Android")
    else:
        print("\n⚠️  BEBERAPA TEST GAGAL!")
        print("📝 Periksa log di atas untuk detail error")

def print_next_steps():
    """Print langkah selanjutnya"""
    print_header("LANGKAH SELANJUTNYA")
    
    print("\n1. 📱 Buka browser di HP, ketik:")
    print(f"   {SERVER_URL}")
    print("   Jika berhasil, kamu akan melihat dashboard")
    
    print("\n2. 🔧 Jika gagal, periksa:")
    print("   • Flask server berjalan dengan output:")
    print("     * Running on http://0.0.0.0:5000")
    print("   • Firewall tidak memblokir port 5000")
    print("   • PC dan HP dalam WiFi yang SAMA")
    
    print("\n3. 📝 Di aplikasi Android, set URL:")
    print(f'   const val SERVER_URL = "{SERVER_URL}"')
    
    print("\n4. 🚀 Jalankan room_generator.py untuk simulasi IoT")
    
    print("\n" + "=" * 70)

def main():
    """Main test function"""
    print_header("🧪 FLASK SERVER CONNECTION TEST")
    print(f"Target Server: {SERVER_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Dictionary untuk menyimpan hasil test
    results = {}
    
    # Jalankan semua test
    results["Server Reachable"] = test_1_server_reachable()
    
    if results["Server Reachable"]:
        time.sleep(1)
        results["Sensor Endpoint"] = test_2_sensor_endpoint()
        
        time.sleep(1)
        results["Android Endpoint"] = test_3_usage_endpoint()
        
        time.sleep(1)
        results["Dashboard API"] = test_4_dashboard_api()
    else:
        print_info("\nTest dihentikan karena server tidak dapat dijangkau")
        results["Sensor Endpoint"] = False
        results["Android Endpoint"] = False
        results["Dashboard API"] = False
    
    # Print summary
    print_summary(results)
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()