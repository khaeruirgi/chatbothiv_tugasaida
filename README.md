# Chatbot Informasi HIV Indonesia

## Deskripsi Proyek

Chatbot Informasi HIV Indonesia adalah program berbasis Python yang dirancang untuk memberikan informasi mengenai HIV serta menampilkan data kasus HIV di Indonesia berdasarkan dataset yang tersimpan dalam file Excel.

Chatbot ini mampu menjawab pertanyaan pengguna terkait pengetahuan umum HIV seperti definisi, gejala, penularan, pencegahan, dan pengobatan. Selain itu, chatbot juga dapat menampilkan data statistik HIV di Indonesia seperti jumlah kasus per provinsi, faktor risiko, jenis kelamin, regimen terapi, kepatuhan pengobatan, dan tipe HIV.

Program membaca data dari file Excel dan memprosesnya menggunakan pustaka Python. Untuk pertanyaan yang lebih kompleks atau di luar data statistik, chatbot memanfaatkan **Google Gemini AI** sebagai kecerdasan buatan untuk memberikan jawaban yang informatif.

Proyek ini dibuat sebagai bagian dari tugas kelompok.

---

## Fitur Chatbot

Chatbot ini memiliki beberapa fitur utama:

### 1. Informasi Umum tentang HIV
- Pengertian HIV  
- Gejala HIV  
- Cara penularan HIV  
- Pencegahan HIV  
- Pengobatan HIV  

### 2. Informasi Terapi HIV
- Penjelasan ARV (Antiretroviral)  
- Penjelasan regimen terapi HIV  

### 3. Data Epidemiologi HIV di Indonesia
- Jumlah kasus HIV per provinsi  
- Peringkat provinsi dengan kasus HIV tertinggi  
- Peringkat provinsi dengan kasus HIV terendah  
- Total kasus HIV di Indonesia  

### 4. Data Tambahan dari Dataset
- Distribusi kasus berdasarkan jenis kelamin  
- Faktor risiko penularan HIV  
- Data regimen terapi berdasarkan umur  
- Data kepatuhan pengobatan dan kematian  
- Data tipe HIV (HIV-1 dan HIV-2)

### 5. Integrasi dengan Google Gemini AI
- Menjawab pertanyaan terbuka seputar HIV yang tidak tersedia dalam dataset  
- Memberikan penjelasan tambahan secara naratif dan mudah dipahami  
- Membatasi topik hanya pada HIV/AIDS

---

## Sumber Data

Data yang digunakan dalam chatbot berasal dari dataset Excel yang berisi informasi mengenai kasus HIV di Indonesia.

File dataset yang digunakan:

```
DASHBARD KEL 6B.xlsx
```

Dataset ini digunakan sebagai sumber data utama yang dibaca menggunakan Python dan pustaka **Pandas**.

---

## Teknologi yang Digunakan

Program ini dikembangkan menggunakan:

- Python
- Pandas
- Regular Expression (re)
- python-telegram-bot
- Google Gemini API (google-generativeai)

Library Python yang digunakan:

```
pandas
python-telegram-bot
google-generativeai
```

---

## Cara Menjalankan Program

### 1. Install Python

Pastikan Python sudah terinstall di komputer Anda.

### 2. Install library yang dibutuhkan

```
pip install pandas python-telegram-bot google-generativeai
```

### 3. Siapkan Token API

Program ini membutuhkan dua token:
- **Telegram Bot Token**: Dapatkan dari [@BotFather](https://t.me/botfather) di Telegram.
- **Google Gemini API Key**: Dapatkan dari [Google AI Studio](https://makersuite.google.com/app/apikey).

Setelah mendapatkan token, Anda dapat menyimpannya sebagai environment variable:
- `TELEGRAM_BOT_TOKEN`
- `GEMINI_API_KEY`

Atau, Anda bisa mengganti nilai default di dalam kode (tidak disarankan untuk produksi).

### 4. Pastikan file berikut berada dalam satu folder

```
chatbot.py
DASHBARD KEL 6B.xlsx
```

### 5. Jalankan program

```
python chatbot.py
```

### 6. Gunakan chatbot di Telegram

Cari bot Anda di Telegram dengan username yang sudah dibuat, lalu kirim pesan.  
Contoh pertanyaan yang dapat diajukan:

```
Apa itu HIV
Apa gejala HIV
Bagaimana penularan HIV
Berapa kasus HIV di Jawa Timur
Provinsi dengan kasus HIV tertinggi
Data jenis kelamin penderita HIV
```

---

## Cara Kerja Sistem

1. **Pembacaan Data**: Program membaca file `DASHBARD KEL 6B.xlsx` menggunakan Pandas dan mengekstrak informasi ke dalam struktur data Python.
2. **Pencocokan Pertanyaan**: Pertanyaan pengguna diproses menggunakan Regular Expression untuk mendeteksi apakah pertanyaan terkait data statistik atau pengetahuan umum.
3. **Pencarian Provinsi**: Jika pertanyaan menyebutkan provinsi, sistem akan mencari kecocokan berdasarkan nama provinsi dan alias yang telah didefinisikan.
4. **Respon Data Statistik**: Jika pola pertanyaan cocok dengan data yang tersedia, chatbot akan merespon dengan data dari dataset.
5. **Integrasi Gemini AI**: Jika pertanyaan bersifat umum dan terkait HIV, tetapi tidak terdeteksi oleh pola yang ada, chatbot akan meneruskannya ke Google Gemini AI untuk dijawab.
6. **Pembatasan Topik**: Gemini AI diinstruksikan untuk hanya menjawab pertanyaan seputar HIV/AIDS. Jika pertanyaan di luar topik, akan ditolak dengan sopan.

---

## Contoh Interaksi Chatbot

**Telegram:**
```
Pengguna: Apa itu HIV?
Bot: HIV (Human Immunodeficiency Virus) adalah virus yang menyerang sistem kekebalan tubuh manusia. Jika tidak diobati, HIV dapat menyebabkan AIDS (Acquired Immunodeficiency Syndrome). HIV menular melalui cairan tubuh seperti darah, air mani, cairan vagina, dan ASI.
```

```
Pengguna: Berapa kasus HIV di Jawa Timur?
Bot: Jumlah kasus HIV di Jawa Timur (data 2025) adalah 12.345 kasus.
```

```
Pengguna: Apa saja faktor risiko HIV?
Bot: Faktor risiko HIV (data 2025):
- Hubungan seksual berisiko: 45.678
- NAPZA suntik: 12.345
- Turunan orang tua: 5.678
- Transfusi/prosedur medis: 3.456
- Tidak diketahui/lainnya: 1.234
```

```
Pengguna: Bagaimana cara mencegah HIV?
Bot: [Jawaban dari Gemini AI berupa penjelasan naratif tentang pencegahan HIV]
```

---

## Struktur Kode

- `chatbot.py`: File utama yang berisi semua logika program.
- Konfigurasi token menggunakan environment variable.
- Fungsi `jawab_pertanyaan()`: Mengatur alur pencocokan pertanyaan dan memanggil fungsi yang sesuai.
- Fungsi `tanya_gemini()`: Menghubungkan ke Google Gemini AI untuk menjawab pertanyaan umum.
- Fungsi-fungsi data: `data_provinsi()`, `peringkat_provinsi()`, `data_jenis_kelamin()`, dll.

---

## Anggota Kelompok

- Khaeru Irgi (2310631210034)
- Rahma Amalia (2310631210043)
- Yanti Windasari (231063121046)
- Yessica Natalia Lawrence (2310631210047)

---

## Tujuan Proyek

Tujuan dari proyek ini adalah mengembangkan chatbot sederhana yang dapat memberikan informasi mengenai HIV serta menampilkan data epidemiologi HIV di Indonesia secara interaktif melalui platform Telegram dengan memanfaatkan kecerdasan buatan Google Gemini AI.
```
