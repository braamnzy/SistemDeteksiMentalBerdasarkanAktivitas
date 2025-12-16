# config.py
# Konfigurasi untuk Stress Detection System

# ============================================
# NETWORK CONFIGURATION
# ============================================

# Cara mendapatkan IP untuk Flask Server:
# 1. Windows: buka CMD, ketik: ipconfig
#    Cari "IPv4 Address" di adapter yang aktif (WiFi/Ethernet)
# 2. Linux/Mac: buka Terminal, ketik: ifconfig atau ip addr
#    Cari inet address
# 3. Contoh IP: 192.168.1.100

# PENTING: HP dan PC harus dalam jaringan WiFi yang SAMA!

# Ganti dengan IP komputer kamu (tempat Flask berjalan)
SERVER_HOST = "0.0.0.0"  # Biarkan 0.0.0.0 untuk listen semua interface
SERVER_PORT = 5000

# IP yang akan digunakan Android untuk konek
# Ganti dengan IP komputer kamu!
# Contoh: "http://192.168.1.100:5000"
ANDROID_SERVER_URL = "http://192.168.1.11:5000"  # ⚠️ UBAH INI!

# ============================================
# DATA CONFIGURATION
# ============================================
DATA_FOLDER = "data"

# ============================================
# FUZZY LOGIC PARAMETERS
# ============================================

# Input Ranges
SCREEN_TIME_RANGE = (0, 24)      # hours
TEMPERATURE_RANGE = (15, 35)     # celsius
HUMIDITY_RANGE = (30, 90)        # percentage
AIR_QUALITY_RANGE = (0, 5)       # PM2.5 index

# Output Range
STRESS_RANGE = (0, 100)          # stress score

# Membership Function Parameters
# Format: (low_end, low_peak, high_peak, high_end)
MF_SCREEN_TIME = {
    'low': (0, 0, 2, 4),
    'medium': (3, 5, 7, 9),
    'high': (8, 12, 24, 24)
}

MF_TEMPERATURE = {
    'cold': (15, 15, 18, 22),
    'normal': (20, 24, 26, 28),
    'hot': (26, 30, 35, 35)
}

MF_HUMIDITY = {
    'low': (30, 30, 40, 50),
    'medium': (45, 55, 65, 75),
    'high': (70, 80, 90, 90)
}

MF_AIR_QUALITY = {
    'good': (0, 0, 0.5, 1.5),
    'moderate': (1.0, 2.0, 3.0, 3.5),
    'poor': (3.0, 4.0, 5.0, 5.0)
}

MF_STRESS = {
    'very_low': (0, 0, 10, 25),
    'low': (15, 25, 35, 45),
    'medium': (35, 45, 55, 65),
    'high': (55, 65, 75, 85),
    'very_high': (75, 85, 100, 100)
}

# ============================================
# SIMULATION SETTINGS
# ============================================
SIMULATION_INTERVAL = 10  # seconds between sensor updates