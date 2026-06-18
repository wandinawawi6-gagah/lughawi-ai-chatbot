"""
Nama Berkas: app.py
Deskripsi: Web App Chatbot Tutor Bahasa Arab (Mufradat Salafi) menggunakan Streamlit
Fokus Maharah: Mufradat (Kosakata) - Pemula
"""

import streamlit as st
import os
import time
from dotenv import load_dotenv
from groq import Groq

# ==============================================================================
# KONFIGURASI HALAMAN WEB STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Mufradat Salafi | Tutor AI",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Memuat variabel lingkungan
load_dotenv()

# ==============================================================================
# VALIDASI API KEY & INISIALISASI GROQ
# ==============================================================================
MODEL_NAME = "llama-3.3-70b-versatile"
api_key = os.getenv("GROQ_API_KEY")

if not api_key or "your_api_key" in api_key or api_key.strip() == "":
    st.error("🚨 Kritis: API Key Groq tidak ditemukan!")
    st.info("Silakan buat file `.env` di direktori proyek Anda dan tambahkan: `GROQ_API_KEY=kunci_api_anda`")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Gagal menghubungkan ke server AI: {e}")
    st.stop()

# ==============================================================================
# SYSTEM PROMPT
# ==============================================================================
SYSTEM_PROMPT = """
Kamu adalah Mufradat Salafi, tutor bahasa Arab spesialis mufradat tingkat pemula (mubtadi'). 
Gaya mengajarmu seperti seorang Ustaz yang ramah, sangat sabar, penuh perhatian, dan edukatif.

Tugas utama Anda:
1. Mengajarkan kosakata (mufradat) secara kontekstual.
2. Menjelaskan arti kata dengan jelas dalam Bahasa Indonesia.
3. Menjelaskan cara penggunaan kata tersebut dalam kalimat.
4. Memberikan transliterasi latin (Contoh: كِتَابٌ -> Kitaabun).
5. Memberikan contoh kalimat Arab beserta harakat lengkap dan artinya.
6. Menyesuaikan penjelasan dengan pemula.

Fokus selalu pada instruksi tersembunyi [SISTEM: Mode aktif = ...]. Tolak halus jika pengguna melenceng dari topik bahasa Arab.
"""

MODE_PROMPTS = {
    "1": "[SISTEM: Mode aktif = Mode 1 (Belajar Kosakata). Berikan 1 mufradat baru bertema dasar, arti, transliterasi, dan contoh kalimat.]",
    "2": "[SISTEM: Mode aktif = Mode 2 (Kuis Kosakata). Berikan 1 soal kuis tebak kata/pilihan ganda. Tunggu jawaban pengguna.]",
    "3": "[SISTEM: Mode aktif = Mode 3 (Percakapan Pendek Harian). Ajak pengguna berdialog interaktif dengan bahasa Arab sederhana.]"
}

# ==============================================================================
# MANAJEMEN SESSION STATE (MEMORI WEB)
# ==============================================================================
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "user_count" not in st.session_state:
    st.session_state.user_count = 0
if "ai_count" not in st.session_state:
    st.session_state.ai_count = 0
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "1"
if "messages" not in st.session_state:
    # Inisialisasi percakapan
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": MODE_PROMPTS["1"]}
    ]
    # Sapaan pertama
    with st.spinner("Ustaz sedang bersiap..."):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, 
                          {"role": "user", "content": "Halo Ustaz, sapa saya dan berikan materi pertama Mode 1."}],
                temperature=0.5,
                max_tokens=1024
            )
            bot_reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            st.session_state.ai_count += 1
        except:
            st.session_state.messages.append({"role": "assistant", "content": "Ahlan wa sahlan! Ada kendala jaringan awal, mari kita mulai belajar."})

# Fungsi Helper: Dapatkan durasi sesi
def get_uptime():
    elapsed = int(time.time() - st.session_state.start_time)
    return f"{elapsed // 60:02d} m {elapsed % 60:02d} s"

# Fungsi Helper: Reset Sesi
def reset_session():
    for key in ["user_count", "ai_count", "messages", "start_time", "current_mode"]:
        del st.session_state[key]
    st.rerun()

# ==============================================================================
# UI: SIDEBAR (NAVIGASI & METRIK)
# ==============================================================================
with st.sidebar:
    st.title("🕌 Mufradat Salafi")
    st.caption("UAS Pendidikan Bahasa Arab 2026")
    st.markdown("---")
    
    st.subheader("📚 Mode Pembelajaran")
    mode_options = {
        "1": "Mode 1: Belajar Kosakata Baru",
        "2": "Mode 2: Kuis Kosakata Interaktif",
        "3": "Mode 3: Percakapan Harian"
    }
    
    # Dropdown untuk memilih mode
    selected_mode = st.selectbox(
        "Pilih fokus belajar saat ini:", 
        options=list(mode_options.keys()), 
        format_func=lambda x: mode_options[x],
        index=list(mode_options.keys()).index(st.session_state.current_mode)
    )
    
    # Deteksi perubahan mode
    if selected_mode != st.session_state.current_mode:
        st.session_state.current_mode = selected_mode
        st.session_state.messages.append({"role": "system", "content": MODE_PROMPTS[selected_mode]})
        st.success(f"Beralih ke {mode_options[selected_mode]}")
        st.rerun()

    st.markdown("---")
    st.subheader("📊 Metrik Kelas")
    col1, col2 = st.columns(2)
    col1.metric("Pesan Santri", st.session_state.user_count)
    col2.metric("Respon Ustaz", st.session_state.ai_count)
    st.metric("Waktu Belajar (Uptime)", get_uptime())
    
    st.markdown("---")
    if st.button("🔄 Reset Papan Tulis", use_container_width=True):
        reset_session()
        
    st.markdown("""
    <div style="font-size: 0.8em; color: gray; margin-top: 20px;">
        <b>Engine:</b> Groq (Llama 3.3 70B)<br>
        <b>Maharah:</b> Mufradat (Pemula)
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# UI: AREA PERCAKAPAN UTAMA
# ==============================================================================
st.title("Tutor Bahasa Arab AI - Kelas Pemula")
st.markdown("Ahlan wa sahlan! Silakan berinteraksi dengan Ustaz Mufradat Salafi.")

# Render riwayat obrolan (sembunyikan pesan 'system')
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    
    avatar = "🕌" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Input obrolan pengguna
if prompt := st.chat_input("Tulis pesan atau jawaban Anda di sini..."):
    # Tampilkan pesan pengguna di UI
    st.chat_message("user", avatar="👤").markdown(prompt)
    
    # Simpan ke memori
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.user_count += 1
    
    # Dapatkan respon dari Groq
    with st.chat_message("assistant", avatar="🕌"):
        message_placeholder = st.empty()
        with st.spinner("Ustaz sedang merenungkan jawaban..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=st.session_state.messages,
                    temperature=0.5,
                    max_tokens=1024,
                )
                full_response = response.choices[0].message.content
                message_placeholder.markdown(full_response)
                
                # Simpan respon AI ke memori
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                st.session_state.ai_count += 1
            except Exception as e:
                error_msg = f"**Galat Terjadi:** {e}"
                message_placeholder.error(error_msg)
                
    st.rerun() # Refresh agar metrik di sidebar ikut ter-update
