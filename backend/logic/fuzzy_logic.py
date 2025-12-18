import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# 1. Definisi Universe (Semesta Pembicaraan)
screen_universe = np.arange(0, 24.1, 0.1) 
temp_universe = np.arange(15, 35.1, 0.1) 
humid_universe = np.arange(30, 90.1, 0.1) 
aq_universe = np.arange(0, 5.1, 0.1)    
stress_universe = np.arange(0, 100.1, 0.1)

# 2. Antecedents (Input) dan Consequent (Output)
screen = ctrl.Antecedent(screen_universe, "screen") 
temp = ctrl.Antecedent(temp_universe, "temperature")
humid = ctrl.Antecedent(humid_universe, "humidity")
airq = ctrl.Antecedent(aq_universe, "air_quality")
stress = ctrl.Consequent(stress_universe, "stress", defuzzify_method='centroid')

# 3. Membership Functions (Trapmf - Berdasarkan parameter teman Anda)
screen['low'] = fuzz.trapmf(screen_universe, [0, 0, 2, 4])
screen['medium'] = fuzz.trapmf(screen_universe, [3, 5, 7, 9])
screen['high'] = fuzz.trapmf(screen_universe, [8, 12, 24, 24])

temp['cold'] = fuzz.trapmf(temp_universe, [15, 15, 18, 22])
temp['normal'] = fuzz.trapmf(temp_universe, [20, 24, 26, 28])
temp['hot'] = fuzz.trapmf(temp_universe, [26, 30, 35, 35])

humid['low'] = fuzz.trapmf(humid_universe, [30, 30, 40, 50])
humid['medium'] = fuzz.trapmf(humid_universe, [45, 55, 65, 75])
humid['high'] = fuzz.trapmf(humid_universe, [70, 80, 90, 90])

airq['good'] = fuzz.trapmf(aq_universe, [0, 0, 0.5, 1.5])
airq['moderate'] = fuzz.trapmf(aq_universe, [1.0, 2.0, 3.0, 3.5])
airq['poor'] = fuzz.trapmf(aq_universe, [3.0, 4.0, 5.0, 5.0])

stress['very_low'] = fuzz.trapmf(stress_universe, [0, 0, 10, 25])
stress['low'] = fuzz.trapmf(stress_universe, [15, 25, 35, 45])
stress['medium'] = fuzz.trapmf(stress_universe, [35, 45, 55, 65])
stress['high'] = fuzz.trapmf(stress_universe, [55, 65, 75, 85])
stress['very_high'] = fuzz.trapmf(stress_universe, [75, 85, 100, 100])

# 

# 4. Definisi 81 Aturan Secara Eksplisit (ctrl.Rule)
rules = [
    # === SCREEN LOW ===
    ctrl.Rule(screen['low'] & temp['cold'] & humid['low'] & airq['good'], stress['low']),
    ctrl.Rule(screen['low'] & temp['cold'] & humid['low'] & airq['moderate'], stress['low']),
    ctrl.Rule(screen['low'] & temp['cold'] & humid['low'] & airq['poor'], stress['medium']),
    ctrl.Rule(screen['low'] & temp['cold'] & humid['medium'] & airq['good'], stress['very_low']),
    ctrl.Rule(screen['low'] & temp['cold'] & humid['medium'] & airq['moderate'], stress['low']),
    ctrl.Rule(screen['low'] & temp['cold'] & humid['medium'] & airq['poor'], stress['low']),
    ctrl.Rule(screen['low'] & temp['cold'] & humid['high'] & airq['good'], stress['low']),
    ctrl.Rule(screen['low'] & temp['cold'] & humid['high'] & airq['moderate'], stress['low']),
    ctrl.Rule(screen['low'] & temp['cold'] & humid['high'] & airq['poor'], stress['medium']),
    ctrl.Rule(screen['low'] & temp['normal'] & humid['low'] & airq['good'], stress['very_low']),
    ctrl.Rule(screen['low'] & temp['normal'] & humid['low'] & airq['moderate'], stress['very_low']),
    ctrl.Rule(screen['low'] & temp['normal'] & humid['low'] & airq['poor'], stress['low']),
    ctrl.Rule(screen['low'] & temp['normal'] & humid['medium'] & airq['good'], stress['very_low']),
    ctrl.Rule(screen['low'] & temp['normal'] & humid['medium'] & airq['moderate'], stress['very_low']),
    ctrl.Rule(screen['low'] & temp['normal'] & humid['medium'] & airq['poor'], stress['low']),
    ctrl.Rule(screen['low'] & temp['normal'] & humid['high'] & airq['good'], stress['very_low']),
    ctrl.Rule(screen['low'] & temp['normal'] & humid['high'] & airq['moderate'], stress['low']),
    ctrl.Rule(screen['low'] & temp['normal'] & humid['high'] & airq['poor'], stress['low']),
    ctrl.Rule(screen['low'] & temp['hot'] & humid['low'] & airq['good'], stress['low']),
    ctrl.Rule(screen['low'] & temp['hot'] & humid['low'] & airq['moderate'], stress['low']),
    ctrl.Rule(screen['low'] & temp['hot'] & humid['low'] & airq['poor'], stress['medium']),
    ctrl.Rule(screen['low'] & temp['hot'] & humid['medium'] & airq['good'], stress['low']),
    ctrl.Rule(screen['low'] & temp['hot'] & humid['medium'] & airq['moderate'], stress['low']),
    ctrl.Rule(screen['low'] & temp['hot'] & humid['medium'] & airq['poor'], stress['medium']),
    ctrl.Rule(screen['low'] & temp['hot'] & humid['high'] & airq['good'], stress['low']),
    ctrl.Rule(screen['low'] & temp['hot'] & humid['high'] & airq['moderate'], stress['medium']),
    ctrl.Rule(screen['low'] & temp['hot'] & humid['high'] & airq['poor'], stress['medium']),

    # === SCREEN MEDIUM ===
    ctrl.Rule(screen['medium'] & temp['cold'] & humid['low'] & airq['good'], stress['low']),
    ctrl.Rule(screen['medium'] & temp['cold'] & humid['low'] & airq['moderate'], stress['medium']),
    ctrl.Rule(screen['medium'] & temp['cold'] & humid['low'] & airq['poor'], stress['medium']),
    ctrl.Rule(screen['medium'] & temp['cold'] & humid['medium'] & airq['good'], stress['low']),
    ctrl.Rule(screen['medium'] & temp['cold'] & humid['medium'] & airq['moderate'], stress['low']),
    ctrl.Rule(screen['medium'] & temp['cold'] & humid['medium'] & airq['poor'], stress['medium']),
    ctrl.Rule(screen['medium'] & temp['cold'] & humid['high'] & airq['good'], stress['medium']),
    ctrl.Rule(screen['medium'] & temp['cold'] & humid['high'] & airq['moderate'], stress['medium']),
    ctrl.Rule(screen['medium'] & temp['cold'] & humid['high'] & airq['poor'], stress['high']),
    ctrl.Rule(screen['medium'] & temp['normal'] & humid['low'] & airq['good'], stress['low']),
    ctrl.Rule(screen['medium'] & temp['normal'] & humid['low'] & airq['moderate'], stress['low']),
    ctrl.Rule(screen['medium'] & temp['normal'] & humid['low'] & airq['poor'], stress['medium']),
    ctrl.Rule(screen['medium'] & temp['normal'] & humid['medium'] & airq['good'], stress['low']),
    ctrl.Rule(screen['medium'] & temp['normal'] & humid['medium'] & airq['moderate'], stress['medium']),
    ctrl.Rule(screen['medium'] & temp['normal'] & humid['medium'] & airq['poor'], stress['medium']),
    ctrl.Rule(screen['medium'] & temp['normal'] & humid['high'] & airq['good'], stress['medium']),
    ctrl.Rule(screen['medium'] & temp['normal'] & humid['high'] & airq['moderate'], stress['medium']),
    ctrl.Rule(screen['medium'] & temp['normal'] & humid['high'] & airq['poor'], stress['high']),
    ctrl.Rule(screen['medium'] & temp['hot'] & humid['low'] & airq['good'], stress['medium']),
    ctrl.Rule(screen['medium'] & temp['hot'] & humid['low'] & airq['moderate'], stress['medium']),
    ctrl.Rule(screen['medium'] & temp['hot'] & humid['low'] & airq['poor'], stress['high']),
    ctrl.Rule(screen['medium'] & temp['hot'] & humid['medium'] & airq['good'], stress['medium']),
    ctrl.Rule(screen['medium'] & temp['hot'] & humid['medium'] & airq['moderate'], stress['medium']),
    ctrl.Rule(screen['medium'] & temp['hot'] & humid['medium'] & airq['poor'], stress['high']),
    ctrl.Rule(screen['medium'] & temp['hot'] & humid['high'] & airq['good'], stress['medium']),
    ctrl.Rule(screen['medium'] & temp['hot'] & humid['high'] & airq['moderate'], stress['high']),
    ctrl.Rule(screen['medium'] & temp['hot'] & humid['high'] & airq['poor'], stress['high']),

    # === SCREEN HIGH ===
    ctrl.Rule(screen['high'] & temp['cold'] & humid['low'] & airq['good'], stress['medium']),
    ctrl.Rule(screen['high'] & temp['cold'] & humid['low'] & airq['moderate'], stress['high']),
    ctrl.Rule(screen['high'] & temp['cold'] & humid['low'] & airq['poor'], stress['high']),
    ctrl.Rule(screen['high'] & temp['cold'] & humid['medium'] & airq['good'], stress['medium']),
    ctrl.Rule(screen['high'] & temp['cold'] & humid['medium'] & airq['moderate'], stress['high']),
    ctrl.Rule(screen['high'] & temp['cold'] & humid['medium'] & airq['poor'], stress['high']),
    ctrl.Rule(screen['high'] & temp['cold'] & humid['high'] & airq['good'], stress['high']),
    ctrl.Rule(screen['high'] & temp['cold'] & humid['high'] & airq['moderate'], stress['high']),
    ctrl.Rule(screen['high'] & temp['cold'] & humid['high'] & airq['poor'], stress['very_high']),
    ctrl.Rule(screen['high'] & temp['normal'] & humid['low'] & airq['good'], stress['medium']),
    ctrl.Rule(screen['high'] & temp['normal'] & humid['low'] & airq['moderate'], stress['high']),
    ctrl.Rule(screen['high'] & temp['normal'] & humid['low'] & airq['poor'], stress['high']),
    ctrl.Rule(screen['high'] & temp['normal'] & humid['medium'] & airq['good'], stress['high']),
    ctrl.Rule(screen['high'] & temp['normal'] & humid['medium'] & airq['moderate'], stress['high']),
    ctrl.Rule(screen['high'] & temp['normal'] & humid['medium'] & airq['poor'], stress['very_high']),
    ctrl.Rule(screen['high'] & temp['normal'] & humid['high'] & airq['good'], stress['high']),
    ctrl.Rule(screen['high'] & temp['normal'] & humid['high'] & airq['moderate'], stress['high']),
    ctrl.Rule(screen['high'] & temp['normal'] & humid['high'] & airq['poor'], stress['very_high']),
    ctrl.Rule(screen['high'] & temp['hot'] & humid['low'] & airq['good'], stress['high']),
    ctrl.Rule(screen['high'] & temp['hot'] & humid['low'] & airq['moderate'], stress['high']),
    ctrl.Rule(screen['high'] & temp['hot'] & humid['low'] & airq['poor'], stress['very_high']),
    ctrl.Rule(screen['high'] & temp['hot'] & humid['medium'] & airq['good'], stress['high']),
    ctrl.Rule(screen['high'] & temp['hot'] & humid['medium'] & airq['moderate'], stress['very_high']),
    ctrl.Rule(screen['high'] & temp['hot'] & humid['medium'] & airq['poor'], stress['very_high']),
    ctrl.Rule(screen['high'] & temp['hot'] & humid['high'] & airq['good'], stress['high']),
    ctrl.Rule(screen['high'] & temp['hot'] & humid['high'] & airq['moderate'], stress['very_high']),
    ctrl.Rule(screen['high'] & temp['hot'] & humid['high'] & airq['poor'], stress['very_high']),
]

# 5. Inisialisasi Sistem Kontrol
stress_ctrl = ctrl.ControlSystem(rules)
stress_sim = ctrl.ControlSystemSimulation(stress_ctrl)

def calculate_stress(screentime, temperature, humidity, air_quality):
    """
    Menghitung tingkat stres berdasarkan input sensor.
    Mengembalikan stress value, category, message, dan membership degrees.
    """
    # Clamping input
    screentime = float(np.clip(screentime, 0, 24))
    temperature = float(np.clip(temperature, 15, 35))
    humidity = float(np.clip(humidity, 30, 90))
    air_quality = float(np.clip(air_quality, 0, 5))

    try:
        stress_sim.input['screen'] = screentime
        stress_sim.input['temperature'] = temperature
        stress_sim.input['humidity'] = humidity
        stress_sim.input['air_quality'] = air_quality
        stress_sim.compute()
        
        value = float(stress_sim.output['stress'])
    except Exception as e:
        print(f"[FUZZY ERROR] {e}")
        value = 50.0

    # Kategorisasi Output
    if value < 20:
        category = "Very Low Stress"
        message = "Kondisi sangat baik! Tetap jaga pola hidup sehat."
    elif value < 40:
        category = "Low Stress"
        message = "Kondisi baik. Pertahankan keseimbangan aktivitas digital."
    elif value < 60:
        category = "Medium Stress"
        message = "Perlu perhatian. Kurangi screen time dan perbaiki lingkungan."
    elif value < 80:
        category = "High Stress"
        message = "Kondisi tidak ideal. Segera istirahat dan perbaiki lingkungan sekitar."
    else:
        category = "Very High Stress"
        message = "PERINGATAN! Segera kurangi penggunaan HP dan perbaiki kondisi ruangan!"

    # Hitung membership degrees untuk visualisasi
    screen_mf = {
        'low': float(fuzz.interp_membership(screen_universe, screen['low'].mf, screentime)),
        'medium': float(fuzz.interp_membership(screen_universe, screen['medium'].mf, screentime)),
        'high': float(fuzz.interp_membership(screen_universe, screen['high'].mf, screentime))
    }
    
    temp_mf = {
        'cold': float(fuzz.interp_membership(temp_universe, temp['cold'].mf, temperature)),
        'normal': float(fuzz.interp_membership(temp_universe, temp['normal'].mf, temperature)),
        'hot': float(fuzz.interp_membership(temp_universe, temp['hot'].mf, temperature))
    }
    
    humid_mf = {
        'low': float(fuzz.interp_membership(humid_universe, humid['low'].mf, humidity)),
        'medium': float(fuzz.interp_membership(humid_universe, humid['medium'].mf, humidity)),
        'high': float(fuzz.interp_membership(humid_universe, humid['high'].mf, humidity))
    }
    
    aq_mf = {
        'good': float(fuzz.interp_membership(aq_universe, airq['good'].mf, air_quality)),
        'moderate': float(fuzz.interp_membership(aq_universe, airq['moderate'].mf, air_quality)),
        'poor': float(fuzz.interp_membership(aq_universe, airq['poor'].mf, air_quality))
    }

    return {
        "stress_value": round(value, 2),
        "category": category,
        "message": message,
        "fuzzy_details": {
            "total_rules": len(rules),
            "screen_membership": screen_mf,
            "temp_membership": temp_mf,
            "humid_membership": humid_mf,
            "aq_membership": aq_mf
        }
    }

# 6. Bagian Testing (MAIN)
if __name__ == '__main__':
    print("="*60)
    print("TESTING FUZZY LOGIC SYSTEM (SCIKIT-FUZZY ENGINE)")
    print("="*60)
    
    # Test Case 1: Paling stres
    print("\n[TEST 1] Screen Tinggi + Panas + Lembab + AQ Buruk")
    result1 = calculate_stress(18, 33, 85, 4.5)
    print(f"Result: {result1}")
    
    # Test Case 2: Optimal
    print("\n[TEST 2] Screen Rendah + Suhu Nyaman + Humid Ideal")
    result2 = calculate_stress(1.5, 24, 55, 0.2)
    print(f"Result: {result2}")
    
    # Test Case 3: Medium (Screen Sedang)
    print("\n[TEST 3] Screen Sedang + Kondisi Lingkungan Normal")
    result3 = calculate_stress(6, 25, 60, 1.5)
    print(f"Result: {result3}")

    print("\n" + "="*60)
    print("TESTING SELESAI")
    print("="*60)