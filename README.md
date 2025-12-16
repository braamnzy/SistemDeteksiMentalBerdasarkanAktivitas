# 🧠 Stress Detection Based on Smartphone Activity and Room Quality

Proyek ini bertujuan untuk **mendeteksi tingkat stres pengguna** berdasarkan **aktivitas smartphone** dan **kualitas lingkungan ruangan** menggunakan pendekatan **Fuzzy Logic**.  
Sistem ini menggabungkan data dari **smartphone** (melalui Digital Wellbeing dan sensor internal) serta **IoT device** (sensor suhu, kelembapan, dan kualitas udara) untuk menghasilkan analisis kondisi mental pengguna secara otomatis dan berkelanjutan.

---

## 📱 Sistem Utama

### 1. Pengumpulan Data
- **Smartphone Data:**
  - Durasi aktif penggunaan aplikasi (terutama kategori sosial, hiburan, dan produktivitas)
- **IoT Sensor Data:**
  - Suhu (°C)
  - Kelembapan (%)
  - Kualitas udara (PM2.5)

Data dikirim secara **otomatis dan berkala** ke server Python melalui API, **meskipun aplikasi tidak sedang dibuka**, agar sistem dapat memantau kondisi pengguna secara real-time.

---

### 2. Penyimpanan Dataset
Semua data aktivitas dikombinasikan dan disimpan dalam **dataset_(device_id)`.csv`** agar mudah digunakan untuk:
- Analisis statistik
- Pelatihan model fuzzy
- Monitoring perubahan stres pengguna dari waktu ke waktu

---

### 3. Pemrosesan Data (Server Python)
Server menggunakan **Flask** untuk menerima data dari smartphone dan perangkat IoT.  
Kemudian data diolah menggunakan **Fuzzy Logic System** dengan parameter utama seperti:
- Durasi Aktif Penggunaan Smartphone
- Kondisi lingkungan (panas, lembap, atau udara buruk)

Output sistem berupa **tingkat stres (Very Low, Low, Medium, High, Very High)**.

---

### 4. Hasil Deteksi
Hasil akhir ditampilkan pada perangkat pengguna melalui **pop-up notifikasi**, menyerupai notifikasi sistem.  
Contoh:
> ⚠️ Kondisi tidak ideal. Segera istirahat dan perbaiki lingkungan sekitar.

---

## ⚙️ Arsitektur Sistem
Smartphone ─┬─ IoT Rekayasa
            │
            │ (JSON Request)
            │
       App Server
            │
            │ (Call Fuzzy Function)
            │
    Fuzzy Processing
            │
            │ (Return Message & Level via Server JSON)
            │
 Smartphone Notification

---

## 🧩 Teknologi yang Digunakan
- **Python (Flask, Numpy, Pandas, Scikit-Fuzzy)**  
- **Android (Usage Stats API)**  
- **IoT/Rekayasa IoT (ESP32 / DHT11 / MQ135 atau sensor lingkungan lainnya)**  
- **CSV Dataset Logging**  
- **Fuzzy Logic Inference System**  

---

## 🧠 Metode Fuzzy Logic
Sistem fuzzy digunakan untuk mengubah input numerik menjadi kategori linguistik seperti:
- *Durasi penggunaan tinggi*
- *Suhu ruangan panas*
- *Kelembapan rendah*
- *Kualitas Udara Buruk*

Dengan rule base scikit-fuzzy seperti:
  ctrl.Rule(screen['high'] & temp['cold'] & humid['low'] & airq['good'], stress['medium']),
  ctrl.Rule(screen['high'] & temp['cold'] & humid['low'] & airq['moderate'], stress['high']),
  ctrl.Rule(screen['high'] & temp['cold'] & humid['low'] & airq['poor'], stress['high'])

---

## 📊 Output
- Dataset otomatis disimpan ke file `dataset_(device_id).csv`
- Hasil inferensi fuzzy ditampilkan di pop-up notifikasi device
- Dapat diperluas untuk visualisasi dashboard atau pelatihan model AI di masa depan

---

## 🚀 Tujuan Akhir
Membangun sistem **deteksi stres cerdas** berbasis **aktivitas digital dan lingkungan**, yang:
- Berjalan otomatis di background
- Menggabungkan sumber data lintas perangkat IoT & Android
- Memberikan umpan balik notifikasi kepada pengguna

---

## 👩‍💻 Pengembang
**Nama:** Zefa, Abyan, Nabil, Raihan  
**Program Studi:** Teknik Komputer, Universitas Jenderal Soedirman  
**Tahun:** 2025  

---

## 📁 Struktur Proyek (Contoh)

Projects/
│
├── Android/                         # Project Android
│   ├── app/src/main/java/...
│   └── build.gradle.kts
│
├── backend/                      
│   ├── app.py                    #app server
│   ├── logic
│         ├── fuzzy_logic.py     #AI Fuzzy Logic
│   └── room_generator
│
└── README.md                    # Dokumentasi proyek

---

## 📜 Lisensi
Proyek ini dikembangkan untuk tujuan akademik dan penelitian.

