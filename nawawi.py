"""
Nama Berkas: chatbot.py
Deskripsi: Proyek UAS Mata Kuliah Artificial Intelligence - Chatbot Tutor Bahasa Arab (Lughawi AI)
Fokus Maharah: Mufradat (Kosakata) untuk Tingkat Pemula (Beginner)
Kompatibilitas: Python 3.10+, Groq SDK v1.x, Rich v13.x
"""

import os
import sys
import time
from dotenv import load_dotenv
from groq import Groq
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.table import Table
from rich.markup import escape

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Inisialisasi Rich Console untuk representasi antarmuka CLI yang profesional
console = Console()

# ==============================================================================
# CONFIGURATION & API VALIDATION (ERROR HANDLING)
# ==============================================================================
# Menggunakan model Llama 3.3 70B Versatile yang stabil dan optimal untuk pemrosesan teks multibahasa
MODEL_NAME = "llama-3.3-70b-versatile"

api_key = os.getenv("GROQ_API_KEY")
if not api_key or "your_groq" in api_key or api_key.strip() == "":
    console.print(Panel(
        "[bold red]CRITICAL ERROR:[/] API Key Groq tidak ditemukan di file .env!\n\n"
        "[yellow]Langkah Perbaikan:[/]\n"
        "1. Buat berkas bernama [bold].env[/] di root direktori proyek.\n"
        "2. Tuliskan kode: [bold cyan]GROQ_API_KEY=gsk_your_actual_api_key_here[/]",
        title="[bold red]Sistem Inisialisasi Gagal[/]",
        border_style="red"
    ))
    sys.exit(1)

try:
    # Menginisialisasi SDK Groq Client secara resmi
    client = Groq(api_key=api_key)
except Exception as e:
    console.print(f"[bold red]Gagal menghubungkan pustaka Groq Client:[/] {e}")
    sys.exit(1)


# ==============================================================================
# SYSTEM PROMPT (CORE PERSONA ARSITEKTUR)
# ==============================================================================
# Definisi persona instruksional yang ketat dan konsisten (Ustaz/Tutor Sabar)
SYSTEM_PROMPT = """
Kamu adalah Lughawi AI, tutor bahasa Arab spesialis mufradat tingkat pemula. 
Gaya mengajarmu seperti seorang Ustaz yang ramah, sangat sabar, komunikatif, suportif, edukatif, dan profesional. 

Tugas utama Anda:
1. Mengajarkan kosakata bahasa Arab secara kontekstual.
2. Menjelaskan arti kata dengan jelas.
3. Menjelaskan cara penggunaan kata tersebut dalam struktur kalimat sederhana.
4. Memberikan transliterasi latin untuk setiap kata/kalimat Arab (Contoh: كِتَابٌ -> Kitaabun).
5. Memberikan contoh kalimat Arab beserta artinya dalam bahasa Indonesia.
6. Memberikan latihan singkat atau kuis yang bertahap dan suportif.
7. Menyesuaikan seluruh penjelasan dengan kemampuan tingkat pemula (Beginner).
8. Menggunakan bahasa Indonesia yang sederhana, santun, dan mudah dipahami.

Aturan Ketat Keamanan Konten (Guardrails):
- Fokus utama saat ini ditentukan oleh perintah sistem tersembunyi '[SISTEM: Mode aktif = ...]'.
- Jika pengguna bertanya, mengobrol, atau mengalihkan topik di luar koridor pembelajaran bahasa Arab atau kosakata, tolak dengan halus dan arahkan kembali mereka ke materi mufradat dengan cara yang edukatif.
"""


# ==============================================================================
# CORE LOGIC CHATBOT ENGINE
# ==============================================================================
class LughawiChatbot:
    def __init__(self):
        """
        Tujuan: Konstruktor untuk mempersiapkan statistik sesi, pencatatan uptime, dan penanganan memori.
        Input: None
        Output: Instance Objek LughawiChatbot
        """
        self.start_time = time.time()
        self.user_message_count = 0  # Melacak khusus pesan riil dari pengguna
        self.ai_response_count = 0   # Melacak jumlah respons balik dari kecerdasan buatan
        self.current_mode = "1"
        self.mode_names = {
            "1": "Belajar Kosakata Baru",
            "2": "Kuis Kosakata",
            "3": "Percakapan Sederhana"
        }
        self.conversation_history = []
        self.initialize_session()

    def initialize_session(self):
        """
        Tujuan: Menyusun struktur awal memori percakapan (Conversation History) dengan menyuntikkan prompt sistem.
        Input: None
        Output: None
        """
        self.conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.inject_mode_context(self.current_mode)

    def inject_mode_context(self, mode_code):
        """
        Tujuan: Memberikan konteks pengondisian perilaku LLM sesuai dengan Mode Pembelajaran yang dipilih.
        Input: mode_code (str) -> Representasi string angka "1", "2", atau "3"
        Output: None
        """
        context_prompts = {
            "1": "[SISTEM: Mode aktif = Mode 1 (Belajar Kosakata). Berikan 1 mufradat baru, transliterasi, arti, dan contoh kalimat sederhana.]",
            "2": "[SISTEM: Mode aktif = Mode 2 (Kuis Kosakata). Buatkan SATU soal kuis mufradat pilihan ganda/isian pendek. Tunggu jawaban pengguna sebelum memberi evaluasi.]",
            "3": "[SISTEM: Mode aktif = Mode 3 (Percakapan Sederhana). Ajak pengguna melakukan hiwar/dialog pendek interaktif bertema harian.]"
        }
        self.conversation_history.append({"role": "system", "content": context_prompts.get(mode_code, "")})

    def switch_mode(self, mode_code):
        """
        Tujuan: Mengubah alur pembelajaran secara dinamis tanpa merusak konsistensi memori percakapan sebelumnya.
        Input: mode_code (str) -> "1", "2", atau "3"
        Output: None
        """
        self.current_mode = mode_code
        self.inject_mode_context(mode_code)
        console.print(f"\n[bold green]Sistem:[/] Berhasil beralih ke [bold yellow]Mode {mode_code}: {self.mode_names[mode_code]}[/].")

    def reset_chatbot(self):
        """
        Tujuan: Implementasi fitur RESET. Menghapus total riwayat, mengembalikan mode ke asal, dan memicu greeting baru.
        Input: None
        Output: Teks salam pembuka pasca-reset (str)
        """
        self.current_mode = "1"
        self.initialize_session()
        # Mengirimkan instruksi pemantik secara terisolasi tanpa mengotori history utama
        return self.get_response("Sistem mendeteksi reset sukses. Sapa kembali pengguna dengan ramah untuk memulai dari awal di Mode 1.", is_user_chat=False)

    def get_uptime_string(self):
        """
        Tujuan: Menghitung durasi waktu berjalannya sesi aplikasi sejak dijalankan pertama kali.
        Input: None
        Output: String representasi durasi (str) -> e.g., "01 menit 45 detik"
        """
        elapsed = int(time.time() - self.start_time)
        return f"{elapsed // 60:02d} menit {elapsed % 60:02d} detik"

    def get_response(self, user_input, is_user_chat=True):
        """
        Tujuan: Menangani manajemen I/O pesan ke Groq API, mengelola statistik riil, serta isolasi galat jaringan.
        Input: user_input (str), is_user_chat (bool)
        Output: Teks jawaban akhir dari model kecerdasan buatan (str)
        """
        # Menambahkan pesan ke riwayat percakapan
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Validasi apakah pesan berasal dari user riil atau trigger sistem
        if is_user_chat:
            self.user_message_count += 1
        
        try:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=self.conversation_history,
                temperature=0.5,  # Diturunkan ke 0.5 untuk membatasi halusinasi tata bahasa Arab
                max_tokens=1024,
                top_p=1,
                stream=False,
            )
            
            bot_response = completion.choices[0].message.content
            if not bot_response or bot_response.strip() == "":
                return "[bold red]Ustaz Lughawi AI terdiam sejenak. Silakan coba kirim kembali pesan Anda.[/]"
            
            # Menyimpan respons asisten ke dalam riwayat obrolan
            self.conversation_history.append({"role": "assistant", "content": bot_response})
            self.ai_response_count += 1
            
            return bot_response
            
        except Exception as e:
            # Penanganan Error Terperinci untuk Keperluan Akademis
            err_str = str(e).lower()
            if "api_key" in err_str or "authentication" in err_str:
                return "[bold red]Kesalahan Otentikasi:[/] Kunci API Groq pada .env tidak valid atau kedaluwarsa."
            elif "rate_limit" in err_str:
                return "[bold yellow]Sistem Sibuk (Rate Limit):[/] Ustaz sedang menjawab santri lain. Mohon jeda beberapa detik."
            else:
                return f"[bold red]Masalah Jaringan/Koneksi:[/] Gagal menghubungi server Groq AI. Detail: {e}"

    # ==============================================================================
    # SUB-SISTEM REPRESENTASI VISUAL (RICH UTILITIES)
    # ==============================================================================
    def display_help(self):
        """Menampilkan menu panduan seluruh perintah sistem navigasi yang valid."""
        table = Table(title="[bold magenta]PANDUAN NAVIGASI PERINTAH SISTEM[/]", show_header=True, header_style="bold cyan")
        table.add_column("Perintah", style="bold yellow")
        table.add_column("Fungsi Operasional")
        table.add_row("1, 2, 3", "Pindah secara instan ke Mode Pembelajaran 1, 2, atau 3")
        table.add_row("contoh", "Menampilkan visualisasi skenario simulasi tiap mode")
        table.add_row("riwayat", "Melihat statistik interaksi dan volume pesan dalam sesi aktif")
        table.add_row("tentang", "Menampilkan informasi akademis, tujuan, dan modul teknologi")
        table.add_row("info", "Memantau waktu aktif aplikasi (uptime) dan model AI aktif")
        table.add_row("reset", "Menghapus seluruh memori percakapan dan kembali ke kondisi awal")
        table.add_row("exit / quit", "Mengakhiri sesi belajar dan memunculkan ringkasan nilai akademik")
        console.print(table)

    def display_info(self):
        """Menampilkan metrik performa uptime aplikasi."""
        table = Table(show_header=False, box=None)
        table.add_row("[bold cyan]Durasi Sesi Aktif (Uptime):[/]", self.get_uptime_string())
        table.add_row("[bold cyan]Total Interaksi Pengguna:[/]", f"{self.user_message_count} pesan terkirim")
        table.add_row("[bold cyan]Mode Belajar Saat Ini:[/]", f"Mode {self.current_mode} - {self.mode_names[self.current_mode]}")
        table.add_row("[bold cyan]Arsitektur Model AI Engine:[/]", f"{MODEL_NAME}")
        console.print(Panel(table, title="[bold gold1]ℹ️ METRIK MONITORING SISTEM[/]", border_style="gold1", expand=False))

    def display_examples(self):
        """Menampilkan orientasi simulasi penggunaan ragam mode pembelajaran."""
        ex_text = Text()
        ex_text.append("💡 [CONTOH MODE 1: Belajar Kosakata]\n", style="bold yellow")
        ex_text.append("   User : Ustaz, berikan satu mufradat tentang kata kerja di dapur.\n")
        ex_text.append("   Bot  : Kata: طَبَخَ (Thobokha) | Arti: Memasak. Transliterasi: Tho-bo-kha.\n")
        ex_text.append("          Contoh Kalimat: طَبَخَ أُمِّي فِي المَطْبَخِ - Ibuku memasak di dapur.\n\n")
        ex_text.append("💡 [CONTOH MODE 2: Kuis Kosakata]\n", style="bold cyan")
        ex_text.append("   Bot  : Apa arti dari mufradat مَكْتَبٌ (Maktabun)? [A] Sekolah [B] Meja\n")
        ex_text.append("   User : Jawabannya B\n")
        ex_text.append("   Bot  : Mumtaz! Jawabanmu benar. Maktabun artinya Meja.\n\n")
        ex_text.append("💡 [CONTOH MODE 3: Percakapan Sederhana]\n", style="bold green")
        ex_text.append("   Bot  : Kaifa Haluka? (Bagaimana kabarmu?)\n")
        ex_text.append("   User : Biikhairin, Alhamdulillah! (Baik, Alhamdulillah!)")
        console.print(Panel(ex_text, title="[bold gold1]📖 SIMULASI MODUL PEMBELAJARAN[/]", border_style="gold1"))

    def display_about(self):
        """Menampilkan deskripsi akademis tujuan perancangan aplikasi proyek AI."""
        table = Table(show_header=False, box=None)
        table.add_row("[bold cyan]Nama Chatbot  :[/]", "Lughawi AI (Version Final Production)")
        table.add_row("[bold cyan]Persona Core  :[/]", "Ustaz / Tutor Bahasa Arab yang Ramah, Sabar, dan Edukatif")
        table.add_row("[bold cyan]Spesialisasi  :[/]", "Maharah Mufradat (Penguasaan Kosakata Dasar)")
        table.add_row("[bold cyan]Target Level  :[/]", "Pemula / Beginner (Mubtadi')")
        table.add_row("[bold cyan]Teknology Stack :[/]", "Python 3.10+, Groq Cloud API Engine, Rich Text Formatting, Python-Dotenv")
        table.add_row("[bold cyan]Tujuan Utama  :[/]", "Menyediakan media instruksional interaktif berbasis generative AI\n"
                                                  "untuk membantu pembelajar mandiri menguasai kosakata Arab secara kontekstual.")
        console.print(Panel(table, title="[bold gold1]🎓 TENTANG PROYEK UAS[/]", border_style="gold1", expand=False))

    def display_history_metrics(self):
        """Menampilkan kuantitas volume log pesan saat ini."""
        table = Table(show_header=False, box=None)
        table.add_row("[bold yellow]Jumlah Pesan Pengguna (User)  :[/]", f"{self.user_message_count} pesan")
        table.add_row("[bold green]Jumlah Respons Kecerdasan (AI) :[/]", f"{self.ai_response_count} pesan")
        table.add_row("[bold cyan]Mode Konteks yang Aktif        :[/]", f"Mode {self.current_mode} ({self.mode_names[self.current_mode]})")
        table.add_row("[bold magenta]Durasi Sesi Berjalan (Uptime)  :[/]", self.get_uptime_string())
        console.print(Panel(table, title="[bold magenta]📊 LOG STATISTIK RIWAYAT PERCAKAPAN[/]", border_style="magenta", expand=False))

    def print_footer_hint(self):
        """Merender panduan jalan pintas navigasi di bagian bawah chat."""
        console.print("[dim white]Panduan Akses: Ketik [bold yellow]help[/] (bantuan) | [bold cyan]info[/] (uptime) | [bold green]contoh[/] | [bold magenta]riwayat[/] | [bold white]tentang[/] | [bold red]exit[/][/]")


# ==============================================================================
# MAIN FUNCTION PROGRAM LOOP
# ==============================================================================
def main():
    console.clear()
    
    # Render Komponen Banner Utama yang Simetris dan Estetik untuk Presentasi
    banner = Text()
    banner.append("┌────────────────────────────────────────────────────────────────┐\n", style="bold green")
    banner.append("│                         LUGHAWI AI                             │\n", style="bold gold1")
    banner.append("│           Tutor AI Pembelajaran Maharah Mufradat Dasar         │\n", style="italic white")
    banner.append("│     UAS - Program Studi Pendidikan Bahasa Arab (PBA) 2026      │\n", style="bold green")
    banner.append("└────────────────────────────────────────────────────────────────┘\n", style="bold green")
    console.print(banner)
    
    bot = LughawiChatbot()
    
    # Meminta sapaan awal dari AI secara aman
    with console.status("[bold green]Ustaz Lughawi AI sedang memasuki ruang kelas...[/]"):
        initial_greeting = bot.get_response("Halo Ustaz Lughawi AI, saya baru masuk kelas. Sapa saya dengan ramah dan berikan materi pertama Mode 1.", is_user_chat=False)
    
    console.print(Panel(escape(initial_greeting), title=f"[bold green]Ustaz Lughawi AI ({bot.mode_names[bot.current_mode]})[/]", border_style="green"))
    bot.print_footer_hint()

    # Loop Interaksi CLI Utama
    while True:
        console.print("")
        user_input = Prompt.ask("[bold magenta]User[/]").strip()
        
        if not user_input:
            continue
            
        # Penanganan Operasional Perintah 'EXIT / QUIT' + Rekapitulasi Akhir Akademis
        if user_input.lower() in ['exit', 'quit']:
            summary_table = Table(show_header=False, box=None)
            summary_table.add_row("[bold cyan]Nama Chatbot      :[/]", "Lughawi AI")
            summary_table.add_row("[bold cyan]Persona Core      :[/]", "Ustaz Pembimbing Spesialis Mufradat")
            summary_table.add_row("[bold cyan]Bidang Maharah    :[/]", "Mufradat (Kosakata Bahasa Arab)")
            summary_table.add_row("[bold cyan]Target Level      :[/]", "Pemula / Beginner (Mubtadi')")
            summary_table.add_row("[bold cyan]Total Interaksi   :[/]", f"{bot.user_message_count} pesan dari pengguna")
            summary_table.add_row("[bold cyan]Durasi Belajar    :[/]", bot.get_uptime_string())
            summary_table.add_row("[bold cyan]Status Akhir Sesi :[/]", "[bold green]Sukses Diujikan (Sesi Selesai)[/]")
            
            console.print("\n")
            console.print(Panel(
                summary_table, 
                title="[bold gold1]🎓 LAPORAN SUMMARY PRESENTASI UAS - EVALUASI AKHIR[/]", 
                border_style="gold1", 
                expand=False
            ))
            console.print("[bold gold1]Syukran jazilan! Demonstrasi program selesai. Semoga proyek Anda meraih nilai maksimal! 👋[/]\n")
            break
            
        elif user_input.lower() == 'help':
            bot.display_help()
            continue
            
        elif user_input.lower() == 'info':
            bot.display_info()
            continue
            
        elif user_input.lower() == 'contoh':
            bot.display_examples()
            continue
            
        elif user_input.lower() == 'tentang':
            bot.display_about()
            continue
            
        elif user_input.lower() == 'riwayat':
            bot.display_history_metrics()
            continue
            
        elif user_input.lower() == 'reset':
            with console.status("[bold red]Membersihkan seluruh papan tulis dan memori kelas...[/]"):
                new_greeting = bot.reset_chatbot()
            console.print("\n[bold red]🔄 Sistem:[/] Riwayat obrolan dihapus bersih. Aplikasi kembali ke Mode 1.")
            console.print(Panel(escape(new_greeting), title=f"[bold green]Ustaz Lughawi AI ({bot.mode_names[bot.current_mode]})[/]", border_style="green"))
            bot.print_footer_hint()
            continue
            
        # Penanganan Sistem Alih Mode via Shortcut Angka
        elif user_input in ["1", "2", "3"]:
            bot.switch_mode(user_input)
            prompt_pindah = f"Sistem memberi tahu Anda bahwa saya berganti ke {bot.mode_names[user_input]}. Harap berikan materi awal sesuai mode ini."
            
            with console.status("[bold green]Ustaz sedang mempersiapkan modul pembelajaran baru...[/]"):
                response = bot.get_response(prompt_pindah, is_user_chat=False)
            console.print(Panel(escape(response), title=f"[bold green]Ustaz Lughawi AI ({bot.mode_names[user_input]})[/]", border_style="green"))
            bot.print_footer_hint()
            continue
            
        # Pemrosesan Teks Chat Normal Pengguna ke Groq API Engine
        else:
            with console.status("[bold green]Ustaz sedang mengetik...[/]"):
                response = bot.get_response(user_input, is_user_chat=True)
            console.print(Panel(escape(response), title=f"[bold green]Ustaz Lughawi AI ({bot.mode_names[bot.current_mode]})[/]", border_style="green"))
            bot.print_footer_hint()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold red]Aplikasi dihentikan paksa.[/] [bold gold1]Ma'as salamah! 👋[/]\n")