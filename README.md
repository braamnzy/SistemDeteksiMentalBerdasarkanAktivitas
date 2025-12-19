# 📱 Stress Detection System: Smartphone Activity & Room Quality Analysis

Proyek ini adalah sistem pemantauan kesehatan mental berbasis **Logika Fuzzy Mamdani**. Sistem ini mengintegrasikan durasi penggunaan layar smartphone (*screen time*) dan kualitas lingkungan fisik (suhu, kelembapan, udara) untuk mendeteksi tingkat stres pengguna secara real-time.

## 🛠️ Arsitektur & Alur Sistem

1. **Android Client:** Memantau penggunaan aplikasi melalui `UsageStatsManager` dan mengirimkan data secara periodik ke server di background menggunakan `WorkManager`.
2. **IoT Simulator:** Mengirimkan data simulasi kondisi ruangan (suhu, kelembapan, PM2.5) secara otomatis.
3. **Flask Server:** Bertindak sebagai hub pusat yang menerima data, menjalankan mesin inferensi fuzzy, dan menyimpan riwayat ke CSV.
4. **Fuzzy Logic Engine:** Mengolah 4 input sensor menggunakan 81 aturan fuzzy untuk menentukan skor stres (0-100).
5. **Dashboard Web:** Visualisasi real-time distribusi probabilitas fuzzy, status sensor, dan grafik fungsi keanggotaan.

---

## 📂 Struktur Proyek

```text
.
├── Android (Mobile App)
│   ├── MainActivity.kt       # UI Utama, perizinan, dan konfigurasi IP Server
│   └── UsageDataWorker.kt    # Background task pengumpul & pengirim data aplikasi
│
├── Backend (Flask Server)
│   ├── app.py                # REST API endpoints & manajemen data CSV
│   ├── logic/
│   │   └── fuzzy_logic.py    # Mesin Inferensi Fuzzy (Scikit-Fuzzy)
│   ├── room_generator.py     # Simulator IoT sensor ruangan
│   ├── templates/
│   │   └── dashboard.html    # UI Dashboard interaktif (Chart.js)
│   └── data/                 # Penyimpanan dataset otomatis (.csv)

```

---

## 🧠 Analisis Fuzzy Mamdani

Sistem ini menggunakan 4 variabel input untuk menentukan 1 variabel output (Stres):

| Input Sensor | Range | Kategori Lingkungan |
| --- | --- | --- |
| **Screen Time** | 0 - 24 Jam | Low, Medium, High |
| **Temperature** | 15 - 35 °C | Cold, Normal, Hot |
| **Humidity** | 30 - 90 % | Low, Medium, High |
| **Air Quality** | 0 - 5 PM2.5 | Good, Moderate, Poor |

**Output:** Nilai 0-100 yang dikategorikan menjadi: *Very Low, Low, Medium, High, & Very High Stress*.

---

## 🚀 Cara Menjalankan

### 1. Backend & Dashboard

Pastikan Python telah terinstal, lalu instal library:

```bash
pip install flask numpy scikit-fuzzy okhttp3 requests

```

Jalankan server:

```bash
python app.py

```

Akses dashboard di `http://localhost:5000`.

### 2. Simulator IoT

Jalankan simulator di terminal terpisah untuk mengisi data lingkungan:

```bash
python room_generator.py

```

### 3. Aplikasi Android

1. Buka project Android di Android Studio.
2. Pastikan smartphone dan laptop berada di jaringan Wi-Fi yang sama.
3. Jalankan aplikasi, tekan tombol **"Ubah IP"** dan masukkan alamat IP laptop Anda (contoh: `http://192.168.1.50:5000`).
4. Berikan izin **Usage Stats** agar aplikasi bisa membaca data durasi layar.

---

## 📊 Fitur Utama

* **Automatic Logging:** Data disimpan otomatis ke `data/dataset_(device_id).csv` untuk kebutuhan riset lebih lanjut.
* **Real-time Notification:** Jika hasil analisis menunjukkan *High* atau *Very High Stress*, smartphone akan menerima notifikasi peringatan secara instan.
* **Fuzzy Visualization:** Dashboard menampilkan grafik fungsi keanggotaan trapesium dan distribusi output secara dinamis.

---

## 👥 Tim Pengembang

* **Zefa, Abyan, Nabil, Raihan**
* *Teknik Komputer, Universitas Jenderal Soedirman (2025)*
