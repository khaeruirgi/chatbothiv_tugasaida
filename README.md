# Chatbot Informasi HIV Indonesia

## Deskripsi Proyek

Chatbot Informasi HIV Indonesia adalah program berbasis Python yang dirancang untuk memberikan informasi mengenai HIV serta menampilkan data kasus HIV di Indonesia berdasarkan dataset yang tersimpan dalam file Excel.

Chatbot ini mampu menjawab pertanyaan pengguna terkait pengetahuan umum HIV seperti definisi, gejala, penularan, pencegahan, dan pengobatan. Selain itu, chatbot juga dapat menampilkan data statistik HIV di Indonesia seperti jumlah kasus per provinsi, faktor risiko, jenis kelamin, regimen terapi, kepatuhan pengobatan, dan tipe HIV.

Program membaca data dari file Excel dan memprosesnya menggunakan pustaka Python sehingga pengguna dapat berinteraksi dengan sistem melalui input teks di terminal.

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

Library Python yang digunakan:

```
pandas
re
python-telegram-bot
```

---

## Cara Menjalankan Program

### 1. Install Python

Pastikan Python sudah terinstall di komputer Anda.

### 2. Install library yang dibutuhkan

```
pip install pandas python-telegram-bot
```

### 3. Pastikan file berikut berada dalam satu folder

```
chatbot.py
DASHBARD KEL 6B.xlsx
```

### 4. Jalankan program

```
python chatbot.py
```

### 5. Gunakan chatbot di terminal

Setelah program dijalankan, pengguna dapat langsung mengetik pertanyaan pada https://t.me/hiv_chatbot

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

## Contoh Interaksi Chatbot

```
Anda: Apa itu HIV?

Bot: HIV (Human Immunodeficiency Virus) adalah virus yang menyerang sistem kekebalan tubuh manusia. Jika tidak diobati, HIV dapat menyebabkan AIDS.

Anda: Berapa kasus HIV di Jawa Timur?

Bot: Jumlah kasus HIV di Jawa Timur (data 2025) adalah XXXX kasus.
```

---

## Anggota Kelompok

- Khaeru Irgi (2310631210034)
- Rahma Amalia (2310631210043)
- Yanti Windasari (231063121046)
- Yessica Natalia Lawrence (2310631210047)

---

## Tujuan Proyek

Tujuan dari proyek ini adalah mengembangkan chatbot sederhana yang dapat memberikan informasi mengenai HIV serta menampilkan data epidemiologi HIV di Indonesia secara interaktif menggunakan bahasa python.
