import os
import re
import pandas as pd
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# KONFIGURASI
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8469714703:AAHmzUxeW0HWT6oOGbRbH1TeQFKfLTQnXtg")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")

openai.api_key = OPENAI_API_KEY

# DEFINE DATA DARI EXCEL
FILE_PATH = 'DASHBARD KEL 6B.xlsx'

try:
    df = pd.read_excel(FILE_PATH, sheet_name='Data', header=None)
except FileNotFoundError:
    print(f"File '{FILE_PATH}' tidak ditemukan. Pastikan file berada di direktori yang sama.")
    exit()
except Exception as e:
    print(f"Gagal membaca file Excel: {e}")
    exit()

# Inisialisasi struktur data
provinsi = []
jenis_kelamin = {}
faktor_risiko = {}
regimen = []
kepatuhan = {}
tipe_hiv = {}

# Loop setiap baris untuk mengekstrak informasi
for idx, row in df.iterrows():
    # Data Provinsi (kolom A, B, C)
    no = row[0]
    nama_prov = row[1]
    kasus = row[2]
    if pd.notna(no) and pd.notna(nama_prov) and isinstance(nama_prov, str):
        try:
            no_int = int(no)
            kasus_int = int(kasus) if pd.notna(kasus) else 0
            provinsi.append({'no': no_int, 'provinsi': nama_prov.strip(), 'kasus': kasus_int})
        except:
            pass

    # Data Jenis Kelamin
    if pd.notna(row[4]) and row[4] == 'Laki-Laki':
        jenis_kelamin['Laki-Laki'] = int(row[5]) if pd.notna(row[5]) else 0
    if pd.notna(row[4]) and row[4] == 'Perempuan':
        jenis_kelamin['Perempuan'] = int(row[5]) if pd.notna(row[5]) else 0

    # Data Faktor Risiko
    if pd.notna(row[4]) and row[4] == 'Hubungan seksual berisiko':
        faktor_risiko['Hubungan seksual berisiko'] = int(row[5]) if pd.notna(row[5]) else 0
    if pd.notna(row[4]) and row[4] == 'NAPZA suntik':
        faktor_risiko['NAPZA suntik'] = int(row[5]) if pd.notna(row[5]) else 0
    if pd.notna(row[4]) and row[4] == 'Turunan orang tua':
        faktor_risiko['Turunan orang tua'] = int(row[5]) if pd.notna(row[5]) else 0
    if pd.notna(row[4]) and row[4] == 'Transfusi/prosedur medis':
        faktor_risiko['Transfusi/prosedur medis'] = int(row[5]) if pd.notna(row[5]) else 0
    if pd.notna(row[4]) and row[4] == 'Tidak diketahui/lainnya':
        faktor_risiko['Tidak diketahui/lainnya'] = int(row[5]) if pd.notna(row[5]) else 0

    # Data Regimen per Umur (kolom H-L)
    if pd.notna(row[7]) and 'Tahun' in str(row[7]):
        umur = row[7].strip()
        regimen.append({
            'umur': umur,
            'TDF+3TC/FTC+LPV/r': int(row[8]) if pd.notna(row[8]) and row[8] != '-' else 0,
            'AZT+3TC+EFV': int(row[9]) if pd.notna(row[9]) and row[9] != '-' else 0,
            'TDF+3TC+LPV/r': int(row[10]) if pd.notna(row[10]) and row[10] != '-' else 0,
            'AZT+3TC+EFV2': int(row[11]) if pd.notna(row[11]) and row[11] != '-' else 0
        })

    # Data Kepatuhan dan Kematian (kolom G-H)
    if pd.notna(row[6]) and row[6] == 'Mengkonsumsi Obat':
        kepatuhan['Mengkonsumsi Obat'] = int(row[7]) if pd.notna(row[7]) else 0
    if pd.notna(row[6]) and row[6] == 'Tidak Mengkonsumsi Obat':
        kepatuhan['Tidak Mengkonsumsi Obat'] = int(row[7]) if pd.notna(row[7]) else 0

    # Data Tipe HIV (kolom E-F)
    if pd.notna(row[4]) and row[4] == 'HIV 1':
        tipe_hiv['HIV 1'] = int(row[5]) if pd.notna(row[5]) else 0
    if pd.notna(row[4]) and row[4] == 'HIV 2':
        tipe_hiv['HIV 2'] = int(row[5]) if pd.notna(row[5]) else 0
    if pd.notna(row[4]) and row[4] == 'TOTAL':
        tipe_hiv['TOTAL'] = int(row[5]) if pd.notna(row[5]) else 0

# Urutkan provinsi berdasarkan nomor
provinsi.sort(key=lambda x: x['no'])

# Buat daftar nama provinsi (lowercase) untuk pencarian
nama_provinsi_lower = [p['provinsi'].lower() for p in provinsi]

# Buat kamus singkatan/nama alternatif
alias_provinsi = {
    'jatim': 'Jawa Timur',
    'jabar': 'Jawa Barat',
    'jateng': 'Jawa Tengah',
    'jakarta': 'DKI Jakarta',
    'dki': 'DKI Jakarta',
    'dki jakarta': 'DKI Jakarta',
    'yogya': 'DI Yogyakarta',
    'jogja': 'DI Yogyakarta',
    'kaltim': 'Kalimantan Timur',
    'kalsel': 'Kalimantan Selatan',
    'kalbar': 'Kalimantan Barat',
    'kalteng': 'Kalimantan Tengah',
    'kalut': 'Kalimantan Utara',
    'sulsel': 'Sulawesi Selatan',
    'sulut': 'Sulawesi Utara',
    'sulteng': 'Sulawesi Tengah',
    'sultra': 'Sulawesi Tenggara',
    'sulbar': 'Sulawesi Barat',
    'sumut': 'Sumatera Utara',
    'sumbar': 'Sumatera Barat',
    'sumsel': 'Sumatera Selatan',
    'lampung': 'Lampung',
    'banten': 'Banten',
    'bali': 'Bali',
    'ntb': 'Nusa Tenggara Barat',
    'ntt': 'Nusa Tenggara Timur',
    'papua': 'Papua',
    'pabar': 'Papua Barat',
    'pbd': 'Papua Barat Daya',
    'ptg': 'Papua Tengah',
    'psl': 'Papua Selatan',
    'ppeg': 'Papua Pegunungan',
    'maluku': 'Maluku',
    'malut': 'Maluku Utara',
    'gorontalo': 'Gorontalo',
    'aceh': 'Aceh',
    'riau': 'Riau',
    'kepri': 'Kepulauan Riau',
    'jambi': 'Jambi',
    'babel': 'Bangka Belitung',
    'bengkulu': 'Bengkulu',
}

# Balikkan alias: tambahkan ke dict dengan nilai objek provinsi
provinsi_by_alias = {}
for alias, nama_lengkap in alias_provinsi.items():
    for p in provinsi:
        if p['provinsi'].lower() == nama_lengkap.lower():
            provinsi_by_alias[alias] = p
            break

# FUNGSI BANTU
def format_angka(angka):
    """Format angka dengan pemisah ribuan titik."""
    return f"{angka:,}".replace(',', '.')

def cari_provinsi_dari_teks(teks):
    """Mengembalikan daftar objek provinsi yang cocok dengan teks."""
    teks_lower = teks.lower()
    hasil = []

    # 1. Cek apakah teks mengandung alias
    for alias, prov in provinsi_by_alias.items():
        if alias in teks_lower:
            hasil.append(prov)
    if hasil:
        return hasil

    # 2. Cek apakah teks mengandung nama provinsi secara tepat (sebagai kata utuh)
    sorted_prov = sorted(provinsi, key=lambda x: len(x['provinsi']), reverse=True)
    for p in sorted_prov:
        nama_lower = p['provinsi'].lower()
        if re.search(r'\b' + re.escape(nama_lower) + r'\b', teks_lower):
            hasil.append(p)
    if hasil:
        return hasil

    # 3. Jika tidak ada yang cocok persis, coba cocokkan sebagian (substring)
    substring_matches = []
    for p in provinsi:
        if p['provinsi'].lower() in teks_lower or teks_lower in p['provinsi'].lower():
            substring_matches.append(p)
    if substring_matches:
        return substring_matches

    return []

# FUNGSI PENGETAHUAN UMUM
def tentang_hiv():
    return """
HIV (Human Immunodeficiency Virus) adalah virus yang menyerang sistem kekebalan tubuh manusia. Jika tidak diobati, HIV dapat menyebabkan AIDS (Acquired Immunodeficiency Syndrome). HIV menular melalui cairan tubuh seperti darah, air mani, cairan vagina, dan ASI.
"""

def gejala_hiv():
    return """
Gejala HIV bervariasi tergantung tahap infeksi:
- Tahap akut (2-4 minggu setelah infeksi): demam, sakit kepala, ruam, sakit tenggorokan, pembengkakan kelenjar getah bening.
- Tahap laten (bisa bertahun-tahun): tidak ada gejala spesifik, virus tetap aktif tetapi berkembang lambat.
- Tahap AIDS: penurunan berat badan drastis, diare kronis, berkeringat malam, demam berulang, infeksi oportunistik (misal TBC, pneumonia), dan kanker.
"""

def penularan_hiv():
    return """
HIV menular melalui:
- Hubungan seksual vaginal, anal, atau oral tanpa kondom dengan orang yang terinfeksi.
- Berbagi jarum suntik atau alat suntik lainnya.
- Transfusi darah atau produk darah yang terkontaminasi.
- Dari ibu ke anak selama kehamilan, persalinan, atau menyusui.
HIV TIDAK menular melalui sentuhan biasa, keringat, air liur, air mata, atau berbagi peralatan makan.
"""

def pencegahan_hiv():
    return """
Pencegahan HIV:
- Gunakan kondom setiap berhubungan seksual.
- Jangan berbagi jarum suntik.
- Lakukan sunat medis (dapat mengurangi risiko).
- Gunakan obat PrEP (pre-exposure prophylaxis) jika berisiko tinggi.
- Ibu hamil dengan HIV harus mendapatkan pengobatan ARV untuk mencegah penularan ke bayi.
- Hindari kontak langsung dengan darah orang lain.
"""

def pengobatan_hiv():
    return """
HIV tidak dapat disembuhkan, tetapi dapat dikendalikan dengan terapi antiretroviral (ARV). ARV bekerja dengan menekan jumlah virus dalam tubuh sehingga sistem kekebalan dapat pulih dan penderita dapat hidup sehat. Kepatuhan minum obat sangat penting untuk mencegah resistensi dan perkembangan ke AIDS.
"""

def apa_itu_arv():
    return """
ARV (Antiretroviral) adalah obat-obatan yang digunakan untuk mengobati HIV. ARV bekerja dengan menghambat perkembangan virus HIV dalam tubuh, sehingga sistem kekebalan dapat membaik dan penderita dapat hidup lebih lama dan sehat. Ada berbagai jenis ARV yang biasanya dikombinasikan dalam regimen tertentu.
"""

def apa_itu_regimen():
    return """
Regimen HIV adalah kombinasi dari beberapa obat ARV yang diminum secara teratur. Tujuannya adalah untuk menekan virus HIV seminimal mungkin dan mencegah resistensi. Regimen biasanya terdiri dari 2-3 jenis obat dari kelas yang berbeda. Contoh regimen yang ada dalam data kami: TDF+3TC/FTC+LPV/r, AZT+3TC+EFV, dll.
"""

# FUNGSI DATA
def peringkat_provinsi(limit=None):
    sorted_prov = sorted(provinsi, key=lambda x: x['kasus'], reverse=True)
    if limit:
        sorted_prov = sorted_prov[:limit]
    resp = "Peringkat provinsi berdasarkan jumlah kasus HIV (data 2025):\n"
    for i, p in enumerate(sorted_prov, 1):
        resp += f"{i}. {p['provinsi']}: {format_angka(p['kasus'])} kasus\n"
    return resp

def data_jenis_kelamin():
    if jenis_kelamin:
        lk = jenis_kelamin.get('Laki-Laki', 0)
        pr = jenis_kelamin.get('Perempuan', 0)
        return f"Jumlah pengidap HIV berdasarkan jenis kelamin (data 2025):\nLaki-laki: {format_angka(lk)}\nPerempuan: {format_angka(pr)}"
    else:
        return "Data jenis kelamin tidak tersedia."

def data_faktor_risiko():
    if faktor_risiko:
        resp = "Faktor risiko HIV (data 2025):\n"
        for k, v in faktor_risiko.items():
            resp += f"- {k}: {format_angka(v)}\n"
        return resp
    else:
        return "Data faktor risiko tidak tersedia."

def data_regimen():
    if regimen:
        resp = "Data regimen HIV berdasarkan umur (data 2025):\n"
        for r in regimen:
            resp += f"Umur {r['umur']}: TDF+3TC/FTC+LPV/r = {format_angka(r['TDF+3TC/FTC+LPV/r'])}, AZT+3TC+EFV = {format_angka(r['AZT+3TC+EFV'])}, TDF+3TC+LPV/r = {format_angka(r['TDF+3TC+LPV/r'])}, AZT+3TC+EFV2 = {format_angka(r['AZT+3TC+EFV2'])}\n"
        return resp
    else:
        return "Data regimen tidak tersedia."

def data_kepatuhan():
    if kepatuhan:
        patuh = kepatuhan.get('Mengkonsumsi Obat', 0)
        tidak = kepatuhan.get('Tidak Mengkonsumsi Obat', 0)
        return f"Jumlah kematian akibat HIV berdasarkan kepatuhan minum obat (data 2025):\n- Mengkonsumsi obat: {format_angka(patuh)}\n- Tidak mengkonsumsi obat: {format_angka(tidak)}"
    else:
        return "Data kepatuhan tidak tersedia."

def data_tipe_hiv():
    if tipe_hiv:
        return f"Tipe HIV (data 2025):\nHIV 1 = {format_angka(tipe_hiv.get('HIV 1', 0))}\nHIV 2 = {format_angka(tipe_hiv.get('HIV 2', 0))}\nTotal = {format_angka(tipe_hiv.get('TOTAL', 0))}"
    else:
        return "Data tipe HIV tidak tersedia."

def data_provinsi(prov):
    return f"Jumlah kasus HIV di {prov['provinsi']} (data 2025) adalah {format_angka(prov['kasus'])}."

def daftar_provinsi():
    daftar = ', '.join([p['provinsi'] for p in provinsi])
    return f"Daftar 38 provinsi di Indonesia: {daftar}"

# FUNGSI CHATGPT
def tanya_chatgpt(pertanyaan):
    """
    Kirim pertanyaan ke ChatGPT dengan batasan topik HIV.
    """
    if not OPENAI_API_KEY:
        return "Maaf, layanan AI tidak dikonfigurasi. Hubungi administrator."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Anda adalah asisten ahli HIV/AIDS. "
                        "Anda hanya boleh menjawab pertanyaan yang berkaitan dengan HIV/AIDS. "
                        "Jika pertanyaan tidak berkaitan, tolak dengan sopan dan arahkan kembali ke topik HIV. "
                        "Berikan jawaban yang informatif, akurat, dan mudah dipahami."
                    )
                },
                {"role": "user", "content": pertanyaan}
            ],
            max_tokens=400,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Maaf, terjadi kesalahan saat menghubungi layanan AI: {e}"

# FUNGSI UTAMA
def jawab_pertanyaan(pertanyaan):
    q = pertanyaan.lower().strip()

    # Salam
    if re.search(r'\b(halo|hai|hi|hello|selamat pagi|selamat siang|selamat sore|selamat malam|pagi|siang|sore|malam)\b', q):
        return "Halo! Ada yang bisa saya bantu tentang HIV? (Ketik 'bantuan' untuk melihat fitur, 'keluar' untuk berhenti)"

    # Bantuan
    if re.search(r'\b(bantuan|help|fitur|apa saja yang bisa|yang bisa ditanyakan)\b', q):
        return """
Saya dapat membantu Anda dengan:
- Pengetahuan umum tentang HIV (apa itu HIV, gejala, penularan, pencegahan, pengobatan, ARV, regimen)
- Data kasus HIV per provinsi (contoh: "berapa kasus di Jawa Timur?", "data HIV di Jabar")
- Peringkat provinsi (contoh: "provinsi dengan kasus tertinggi", "10 besar", "urutan pertama")
- Data berdasarkan jenis kelamin, faktor risiko, regimen obat, kepatuhan, dan tipe HIV
- Semua data adalah perkiraan tahun 2025.
Cukup tanyakan dengan bahasa sehari-hari.
"""

    # Pengetahuan umum tentang ARV/Regimen
    if re.search(r'\b(apa itu arv|arv itu apa|pengertian arv)\b', q):
        return apa_itu_arv()
    if re.search(r'\b(apa itu regimen|regimen itu apa|pengertian regimen|regimen arv)\b', q):
        return apa_itu_regimen()

    # Pengetahuan umum lainnya
    if re.search(r'\b(apa itu hiv|definisi hiv|hiv itu apa|pengertian hiv)\b', q):
        return tentang_hiv() + "\n\n(Data yang saya miliki adalah perkiraan tahun 2025.)"
    if re.search(r'\b(gejala|tanda-tanda|ciri-ciri)\b', q) and not re.search(r'\b(provinsi|kasus|data)\b', q):
        return gejala_hiv()
    if re.search(r'\b(cara penularan|penularan|menular|penyebaran|menginfeksi|tertular|transmisi)\b', q) and not re.search(r'\b(faktor risiko|risiko)\b', q):
        return penularan_hiv()
    if re.search(r'\b(pencegahan|mencegah|cara agar tidak)\b', q):
        return pencegahan_hiv()
    if re.search(r'\b(pengobatan|obat|terapi|arv|pengobatan hiv)\b', q):
        return pengobatan_hiv()

    # Data umum (tanpa provinsi spesifik)
    if re.search(r'\b(jumlah kasus total|total kasus|kasus seluruh indonesia)\b', q):
        total = sum(p['kasus'] for p in provinsi)
        return f"Total kasus HIV di Indonesia (data 2025) adalah {format_angka(total)}."

    # Data jenis kelamin
    if re.search(r'\b(jenis kelamin|laki-laki|perempuan|gender)\b', q) and not re.search(r'\b(provinsi)\b', q):
        return data_jenis_kelamin()

    # Data faktor risiko
    if re.search(r'\b(faktor risiko|penyebab|risiko penularan|faktor penyebab)\b', q):
        return data_faktor_risiko()

    # Data regimen
    if re.search(r'\b(regimen|obat hiv|terapi hiv|jenis obat|obat berdasarkan umur|data regimen)\b', q):
        return "Regimen HIV adalah kombinasi obat ARV yang digunakan. Berikut data regimen berdasarkan umur:\n\n" + data_regimen()

    # Data kepatuhan dan kematian
    if re.search(r'\b(kepatuhan|kematian|meninggal|patuh minum obat|kematian akibat hiv)\b', q):
        return data_kepatuhan()

    # Data tipe HIV
    if re.search(r'\b(tipe hiv|jenis hiv|hiv 1|hiv 2)\b', q):
        return data_tipe_hiv()

    # Daftar provinsi
    if re.search(r'\b(daftar provinsi|provinsi apa saja|nama provinsi)\b', q):
        return daftar_provinsi()

    # Peringkat/urutan (tanpa provinsi spesifik)
    if re.search(r'\b(peringkat|urutan|tertinggi|terbanyak|terendah|terkecil|10 besar|top)\b', q):
        if 'tertinggi' in q or 'terbanyak' in q:
            tertinggi = max(provinsi, key=lambda x: x['kasus'])
            return f"Provinsi dengan kasus HIV tertinggi (data 2025) adalah {tertinggi['provinsi']} dengan {format_angka(tertinggi['kasus'])} kasus."
        elif 'terendah' in q or 'terkecil' in q:
            terendah = min(provinsi, key=lambda x: x['kasus'])
            return f"Provinsi dengan kasus HIV terendah (data 2025) adalah {terendah['provinsi']} dengan {format_angka(terendah['kasus'])} kasus."
        elif '10 besar' in q or 'top 10' in q:
            return peringkat_provinsi(10)
        else:
            return peringkat_provinsi()

    # Data provinsi spesifik
    prov_terdeteksi = cari_provinsi_dari_teks(q)
    if prov_terdeteksi:
        if len(prov_terdeteksi) == 1:
            prov = prov_terdeteksi[0]
            if re.search(r'\b(jumlah kasus|kasus hiv|berapa kasus|data kasus|penderita hiv|pengidap hiv)\b', q):
                return data_provinsi(prov)
            else:
                # Jika hanya menyebut nama provinsi, berikan jumlah kasus
                return data_provinsi(prov)
        else:
            nama_prov = [p['provinsi'] for p in prov_terdeteksi]
            return f"Maaf, saya menemukan beberapa provinsi dengan nama mirip: {', '.join(nama_prov)}. Bisa lebih spesifik?"
    else:
        if re.search(r'\b(provinsi|kasus|data)\b', q):
            return "Maaf, saya tidak menemukan provinsi yang dimaksud. Ketik 'daftar provinsi' untuk melihat semua provinsi."

    # Jika tidak ada pola yang cocok, cek apakah pertanyaan terkait HIV
    kata_kunci_hiv = ['hiv', 'aids', 'virus', 'obat', 'arv', 'regimen', 'gejala', 
                      'penularan', 'pencegahan', 'pengobatan', 'kondom', 'seks', 
                      'darah', 'jarum', 'infeksi', 'imun', 'cd4', 'viral load', 
                      'resistensi', 'efek samping', 'terapi', 'antiretroviral']

    if any(kata in q for kata in kata_kunci_hiv):
        return tanya_chatgpt(pertanyaan)
    else:
        return "Maaf, saya hanya dapat menjawab pertanyaan seputar HIV. Silakan tanyakan hal lain tentang HIV."

# TELEGRAM BOT HANDLER
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Selamat datang di Chatbot HIV Indonesia (Kelompok 6B)!\n"
        "Data yang digunakan adalah perkiraan tahun 2025.\n"
        "Ketik apa saja atau 'bantuan' untuk melihat fitur."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    bot_response = jawab_pertanyaan(user_message)
    await update.message.reply_text(bot_response)

# MAIN
if __name__ == '__main__':
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot sedang berjalan... Tekan Ctrl+C untuk berhenti.")
    application.run_polling()
