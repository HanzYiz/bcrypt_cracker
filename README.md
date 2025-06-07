# Bcrypt Cracker Kinerja Tinggi (Multiprocessing)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Sebuah tool command-line berbasis Python yang dirancang untuk melakukan serangan *brute-force* terhadap hash bcrypt secara efisien. Dibuat dengan modul `multiprocessing` untuk memanfaatkan semua core CPU yang tersedia, sehingga memberikan kecepatan cracking yang jauh lebih tinggi dibandingkan pendekatan single-thread atau multi-thread biasa.

Proyek ini dibuat untuk tujuan edukasi, yaitu untuk mendemonstrasikan kekuatan (dan kelemahan) dari algoritma hashing modern dan pentingnya *cost factor* pada bcrypt.

## ✨ Fitur Utama

-   **Performa Tinggi:** Menggunakan `multiprocessing.Pool` untuk mendistribusikan beban kerja ke semua core CPU, melewati batasan Global Interpreter Lock (GIL) Python.
-   **Penggunaan CPU Efisien:** Secara otomatis menggunakan jumlah proses yang setara dengan jumlah core CPU untuk performa optimal.
-   **Antarmuka CLI Modern:** Dibuat dengan `argparse` untuk penggunaan yang mudah dan intuitif dari terminal.
-   **Laporan Progres Real-Time:** Menampilkan status serangan secara langsung, termasuk jumlah percobaan, persentase kemajuan, dan kecepatan (hash/detik).
-   **Penanganan Sinyal:** Dapat dihentikan dengan aman kapan saja menggunakan `Ctrl+C` tanpa menimbulkan error.
-   **Validasi Input:** Secara otomatis memeriksa format hash bcrypt untuk memastikan input yang valid.

## 📸 Tangkapan Layar

*(Sangat disarankan untuk menambahkan tangkapan layar dari tool Anda saat berjalan di sini)*
![Tangkapan Layar](httpsd-Aset/bcrypt_cracker_mp_demo.png)

## ⚙️ Instalasi

Untuk menjalankan tool ini, Anda memerlukan Python 3.9 atau yang lebih baru.

1.  **Clone repository ini:**
    ```bash
    git clone [https://github.com/NAMA_USER_ANDA/NAMA_REPO_ANDA.git](https://github.com/NAMA_USER_ANDA/NAMA_REPO_ANDA.git)
    cd NAMA_REPO_ANDA
    ```

2.  **Buat dan aktifkan virtual environment (sangat disarankan):**
    ```bash
    # Membuat environment
    python -m venv venv

    # Mengaktifkan di Windows
    .\venv\Scripts\activate

    # Mengaktifkan di Linux/macOS
    source venv/bin/activate
    ```

3.  **Buat file `requirements.txt`:**
    Buat sebuah file baru bernama `requirements.txt` di direktori proyek dan isikan dengan:
    ```
    bcrypt
    ```

4.  **Install dependensi yang diperlukan:**
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Penggunaan

Jalankan skrip dari terminal dengan format perintah berikut:

```bash
python bcrypt_cracker_mp.py <HASH> <PATH_WORDLIST> [OPTIONS]