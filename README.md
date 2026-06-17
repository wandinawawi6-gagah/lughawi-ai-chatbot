# lughawi-ai-chatbot
Chatbot Pembelajaran Bahasa Arab Berbasis AI (Lughawi AI)
# Lughawi AI

## Chatbot Pembelajaran Bahasa Arab Berbasis Artificial Intelligence

Lughawi AI merupakan chatbot pembelajaran bahasa Arab berbasis kecerdasan buatan (Artificial Intelligence) yang dirancang untuk membantu pembelajar bahasa Arab tingkat pemula dalam menguasai kosakata (mufradat) secara interaktif. Chatbot ini menggunakan teknologi Large Language Model (LLM) melalui Groq API dan dibangun menggunakan bahasa pemrograman Python.

---

## Identitas Mahasiswa

**Nama:** Wandi Nawawi  
**NIM:** 1232030105  
**Program Studi:** Pendidikan Bahasa Arab  
**Mata Kuliah:** Artificial Intelligence  
**Semester:** 6

---

## Maharah yang Dipilih

**Maharah Mufradat (Kosakata Bahasa Arab)**

### Alasan Memilih Maharah Mufradat

Maharah mufradat dipilih karena penguasaan kosakata merupakan fondasi utama dalam pembelajaran bahasa Arab. Dengan menguasai kosakata yang cukup, peserta didik akan lebih mudah mengembangkan keterampilan berbahasa lainnya seperti istima', kalam, qira'ah, dan kitabah. Oleh karena itu, chatbot ini difokuskan untuk membantu pengguna mempelajari kosakata Arab secara kontekstual dan interaktif.

---

## API yang Digunakan

**Groq API**

Model AI yang digunakan:

- Llama 3.3 70B Versatile

Groq API digunakan untuk menghubungkan aplikasi Python dengan model kecerdasan buatan sehingga chatbot dapat memberikan respons yang cepat, relevan, dan edukatif.

---

## Cara Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/wandinawawi6-gagah/lughawi-ai-chatbot.git
```

### 2. Masuk ke Folder Proyek

```bash
cd lughawi-ai-chatbot
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Buat File .env

Buat file bernama `.env` kemudian isi dengan API Key Groq:

```env
GROQ_API_KEY=your_api_key_here
```

---

## Cara Menjalankan Aplikasi

Jalankan perintah berikut:

```bash
python chatbot.py
```

atau jika file masih bernama:

```bash
python nawawi.py
```

---

## Fitur Utama

### 1. Belajar Kosakata (Mode 1)
- Mempelajari mufradat baru
- Menampilkan arti kosakata
- Menampilkan transliterasi
- Memberikan contoh kalimat

### 2. Kuis Kosakata (Mode 2)
- Soal latihan interaktif
- Evaluasi jawaban pengguna
- Pembelajaran berbasis latihan

### 3. Percakapan Sederhana (Mode 3)
- Simulasi dialog bahasa Arab
- Latihan penggunaan kosakata dalam konteks nyata

### 4. Conversation History
- Menyimpan riwayat percakapan dalam satu sesi

### 5. Help Menu
- Menampilkan daftar perintah yang tersedia

### 6. Info Sistem
- Menampilkan informasi mode aktif
- Menampilkan model AI yang digunakan
- Menampilkan durasi sesi

### 7. Riwayat Sesi
- Menampilkan jumlah pesan pengguna
- Menampilkan jumlah respons AI
- Menampilkan statistik penggunaan

### 8. Reset Session
- Menghapus riwayat percakapan
- Memulai sesi pembelajaran baru

### 9. Exit & Summary
- Mengakhiri sesi pembelajaran
- Menampilkan ringkasan aktivitas pengguna

---

## Teknologi yang Digunakan

- Python 3.10+
- Groq API
- Rich
- Python Dotenv

---

## Penutup

Lughawi AI diharapkan dapat menjadi media pembelajaran bahasa Arab yang interaktif, inovatif, dan mudah digunakan, khususnya dalam meningkatkan penguasaan kosakata (mufradat) bagi pembelajar tingkat pemula.

---

**© 2026 – Wandi Nawawi | Pendidikan Bahasa Arab**
