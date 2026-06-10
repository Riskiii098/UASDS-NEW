---
title: Smart City AQI
emoji: 🏙️
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---

# Laporan Proyek: Prediksi Kualitas Udara (PM2.5) Bandar Lampung

## 1. Pendahuluan

### 1.1. Latar Belakang Masalah
Kualitas udara yang buruk, terutama tingginya kadar partikulat halus (PM2.5), merupakan ancaman serius bagi kesehatan masyarakat di kawasan perkotaan. Peningkatan aktivitas industri, volume kendaraan bermotor, dan perubahan cuaca dapat memengaruhi fluktuasi polusi udara secara signifikan. Oleh karena itu, diperlukan sebuah sistem cerdas yang mampu memprediksi kualitas udara di masa depan agar masyarakat dan pemangku kebijakan dapat mengambil tindakan preventif yang tepat.

### 1.2. Business Understanding
Dalam konteks *Smart City*, pemantauan lingkungan merupakan salah satu pilar utama. Proyek ini bertujuan untuk memberikan solusi berbasis data dengan membangun sistem prediksi polusi udara (PM2.5). Sistem ini akan memberikan wawasan (insight) prediktif kepada masyarakat terkait tingkat bahaya polusi di lokasi dan waktu tertentu, sehingga dapat membantu meminimalisir risiko paparan polusi terhadap warga kota.

### 1.3. Tujuan Proyek
- Membangun model *Machine Learning* yang dapat memprediksi tingkat konsentrasi PM2.5 berdasarkan parameter cuaca dan waktu.
- Melakukan evaluasi dan eksperimentasi model menggunakan *tools tracking* seperti MLflow.
- Mengembangkan dan men-deploy *dashboard* interaktif berbasis web (Flask) agar prediksi model dapat diakses dengan mudah oleh pengguna akhir.

## 2. Deskripsi Dataset
Dataset yang digunakan berisi rekam data polusi dan cuaca lokal yang disimpan dalam file `data_polusi_lokal.csv`. Data ini bersumber dari API publik seperti OpenAQ / Open-Meteo. 
**Fitur (Features) yang digunakan meliputi:**
- `hour`: Jam pengukuran (0-23).
- `day_of_week`: Hari dalam seminggu.
- `latitude` & `longitude`: Koordinat geografis lokasi pemantauan.
- `temperature`: Suhu udara.
- `humidity`: Kelembapan udara.
- `wind_speed`: Kecepatan angin.

**Target:**
- `pm25`: Tingkat konsentrasi partikulat PM2.5 (mikrogram per meter kubik).

> 💡 **GAMBAR YANG PERLU DITAMBAHKAN DI SINI:**
> Tambahkan gambar cuplikan tabel dataset (misalnya hasil dari fungsi `df.head()` di Jupyter Notebook) atau grafik distribusi awal (histogram) dari target PM2.5. Tujuannya untuk menunjukkan struktur baris data dan sebaran rentang nilai polusi kepada pembaca laporan.
> 
> *Contoh penulisan markdown jika gambar diletakkan di folder assets:*
> `![Cuplikan Dataset](assets/dataset_head.png)`

## 3. Metodologi (Data Science Process)

### 3.1. Data Preparation dan Cleaning
Proses ini mencakup pengumpulan data mentah, pembersihan nilai yang kosong (*missing values*), penyesuaian format tipe data, serta ekstraksi fitur waktu seperti `hour` dan `day_of_week` dari data *timestamp*. Hal ini bertujuan agar data bebas dari anomali dan formatnya kompatibel saat diproses oleh algoritma *Machine Learning*.

### 3.2. Exploratory Data Analysis (EDA)
Tahap EDA dilakukan untuk mengeksplorasi karakteristik data. Pada tahap ini, dianalisis distribusi fitur serta korelasi antara variabel cuaca (suhu, kelembapan, kecepatan angin) terhadap tingkat PM2.5. Selain itu, divisualisasikan pula pola fluktuasi polusi berdasarkan parameter waktu.

> 💡 **GAMBAR YANG PERLU DITAMBAHKAN DI SINI:**
> Tambahkan **Heatmap Correlation Matrix** (matriks korelasi) untuk memperlihatkan fitur apa yang paling berpengaruh terhadap polusi PM2.5. Anda juga bisa menambahkan grafik tren garis (*Time Series Plot*) atau diagram batang rata-rata PM2.5 berdasarkan jam (`hour`) untuk melihat di jam berapa polusi paling tinggi.
> 
> *Contoh penulisan markdown:*
> `![Heatmap Korelasi](assets/heatmap_korelasi.png)`

### 3.3. Modeling
Proses pemodelan menggunakan algoritma **HistGradientBoostingRegressor** dari library *Scikit-Learn*, yang cepat dan efisien dalam menangani data tabular dengan banyak observasi.
- **Hyperparameter Tuning:** Menggunakan `RandomizedSearchCV` yang digabungkan dengan validasi silang (*Cross-Validation*) untuk menemukan konfigurasi parameter terbaik (seperti `learning_rate`, `max_iter`, `max_depth`).
- **Experiment Tracking:** Menggunakan **MLflow** (yang terhubung dengan DagsHub) untuk mencatat (*log*) secara sistematis parameter, metrik evaluasi, dan model dari setiap perulangan eksperimen.

> 💡 **GAMBAR YANG PERLU DITAMBAHKAN DI SINI:**
> Ambil tangkapan layar (*screenshot*) dari antarmuka Web (UI) **MLflow / DagsHub**. Perlihatkan tabel atau grafik dari riwayat *runs* eksprimen Anda. Ini penting untuk menunjukkan proses *hyperparameter tuning* secara profesional.
> 
> *Contoh penulisan markdown:*
> `![Screenshot MLflow UI](assets/mlflow_ui.png)`

### 3.4. Evaluasi
Model terbaik hasil *tuning* dievaluasi pada data pengujian (*Test Set*) untuk melihat kinerjanya menggunakan beberapa metrik regresi, yaitu:
- **Mean Absolute Error (MAE):** Rata-rata selisih absolut antara nilai prediksi dan nilai sebenarnya.
- **Mean Squared Error (MSE):** Rata-rata dari kuadrat selisih nilai prediksi dan aktual.
- **R-Squared ($R^2$):** Proporsi varians dari variabel target yang dapat dijelaskan oleh fitur-fitur independen yang digunakan.

> 💡 **GAMBAR YANG PERLU DITAMBAHKAN DI SINI (Opsional namun disarankan):**
> Tambahkan **Scatter Plot (Actual vs Predicted)**. Sumbu X adalah nilai asli PM2.5, sumbu Y adalah nilai Prediksi PM2.5. Gambar ini sangat disukai dosen atau *reviewer* karena secara visual langsung memperlihatkan seberapa baik prediksi model mendekati garis miring ideal (diagonal).
> 
> *Contoh penulisan markdown:*
> `![Grafik Actual vs Predicted](assets/actual_vs_predicted.png)`

## 4. Dashboard dan Form Prediksi
Model *Machine Learning* yang siap digunakan telah disimpan dalam format file `.joblib` dan diintegrasikan ke dalam backend menggunakan *framework* **Flask**. Aplikasi web ini menyediakan *endpoint* API dan halaman antarmuka HTML. Melalui sebuah *form* interaktif di halaman utama (*Dashboard*), pengguna dapat memasukkan variabel kondisi lingkungan (suhu, kelembapan, jam, dll.), dan sistem secara *real-time* akan memberikan skor prediksi PM2.5 beserta keterangan tingkat berbahayanya.

> 💡 **GAMBAR YANG PERLU DITAMBAHKAN DI SINI:**
> Ambil hasil *screenshot* halaman web aplikasi **Flask** Anda ketika sedang dijalankan. Jika memungkinkan, screenshot aplikasi setelah pengguna menekan tombol "Prediksi", agar hasil prediksinya juga terlihat.
> 
> *Contoh penulisan markdown:*
> `![Screenshot Dashboard App](assets/dashboard_flask.png)`

## 5. Kesimpulan dan Saran

### 5.1. Kesimpulan
- Model berbasis *HistGradientBoostingRegressor* dengan *Hyperparameter Tuning* mampu memberikan hasil prediksi kadar PM2.5 yang memadai berdasarkan parameter lokasi, waktu, dan elemen cuaca.
- Penggunaan alat pelacakan seperti MLflow terbukti esensial dalam menjaga proses pelatihan model terstruktur dan metrik pengujian mudah untuk dikomparasi.
- *Dashboard* berbasis web mempermudah akses fungsionalitas model oleh pengguna akhir, sehingga penerapan *Smart City* dalam pemantauan lingkungan udara dapat disimulasikan secara komprehensif.

### 5.2. Saran
- **Kuantitas dan Kualitas Data:** Untuk pengembangan selanjutnya, disarankan memperkaya dataset dari rentang waktu multi-tahun serta mengakomodasi data polusi jenis lain seperti SO2, NO2, atau CO.
- **Penggunaan Model Lanjutan:** Mengingat polusi erat kaitannya dengan deret waktu (*time-series*), pendekatan model prediktif berbasis *Deep Learning* seperti Long Short-Term Memory (LSTM) patut dieksplorasi di masa depan.
- **Pengembangan UI/UX:** Dashboard dapat dikembangkan lebih lanjut dengan pemetaan spasial (peta interaktif) untuk melihat perbedaan kondisi kualitas udara antar wilayah secara langsung.
