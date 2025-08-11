# Script Info HP

Ini adalah skrip Python sederhana yang dirancang untuk platform Termux di Android. Skrip ini berfungsi untuk menampilkan berbagai informasi penting mengenai perangkat, seperti detail CPU, penggunaan RAM, status baterai, dan informasi jaringan.

## Fitur Utama

- **Informasi Perangkat:** Menampilkan detail CPU, RAM, dan penyimpanan.
- **Status Baterai:** Menampilkan persentase, suhu, dan status pengisian.
- **Informasi Jaringan:** Menampilkan status koneksi, IP publik, dan detail Wi-Fi (jika tersedia).
- **Pengecekan Sensor:** Menampilkan daftar sensor yang terdeteksi di perangkat.
- **Monitoring Real-time:** Fitur untuk memantau penggunaan CPU, RAM, dan proses yang berjalan secara langsung.

## Persyaratan (Prasyarat)

Sebelum menjalankan skrip ini, pastikan Anda telah menginstal beberapa paket penting di Termux:

1.  **Git dan Python:**
    ```bash
    pkg install git python -y
    ```
2.  **Requests:**
    ```bash
    pip install requests
    ```
3.  **Termux API:** Fitur baterai, Wi-Fi, dan sensor memerlukan Termux API.
    ```bash
    pkg install termux-api -y
    ```

## Cara Instalasi dan Penggunaan

1.  **Klon (Clone) Repositori:**
    Buka Termux dan jalankan perintah berikut untuk mengunduh skrip:
    ```bash
    git clone [https://github.com/M4DK/infohp.git](https://github.com/M4DK/infohp.git)
    ```

2.  **Masuk ke Direktori Proyek:**
    ```bash
    cd infohp
    ```

3.  **Jalankan Skrip:**
    ```bash
    python infohp.py
    ```

## Catatan

-   Informasi Wi-Fi seperti SSID dan MAC Address mungkin tidak ditampilkan pada beberapa versi Android karena batasan privasi.
-   Fitur Termux API memerlukan izin yang bisa Anda berikan melalui pengaturan aplikasi Android.
