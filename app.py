import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Guru Bahasa AI", page_icon="🎓")

# --- AMBIL API KEY DARI SECRETS ---
# Streamlit otomatis membaca dari .streamlit/secrets.toml
try:
    genai.configure(api_key=st.secrets["AIzaSyBbueIhOhFNZDNSVYiXk0C6MJGhrKzA15w"])
except KeyError:
    st.error("API Key tidak ditemukan! Pastikan sudah ada di .streamlit/secrets.toml")
    st.stop()

# --- SETUP MODEL ---
instruction = (
    "Kamu adalah 'Guru Bahasa AI' yang sangat ahli dalam Bahasa Indonesia, Inggris, dan Korea. "
    "Berikan terjemahan yang natural, jelaskan tata bahasa, dan berikan tips budaya. "
    "Gunakan bahasa yang ramah dan suportif seperti guru sungguhan."
)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=instruction
)

# --- ANTARMUKA PENGGUNA (UI) ---
st.title("🎓 Guru Bahasa AI: Indo-Eng-Kor")
st.markdown("Halo! Aku gurumu. Masukkan teks yang ingin kamu terjemahkan atau tanyakan soal grammar.")

# Inisialisasi chat history jika belum ada
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan riwayat pesan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dari User
if prompt := st.chat_input("Tanya guru di sini..."):
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon AI
    with st.chat_message("assistant"):
        with st.spinner("Guru sedang berpikir..."):
            try:
                # Memulai chat dengan history agar AI ingat konteks sebelumnya
                chat = model.start_chat(history=[
                    {"role": "user", "parts": [m["content"]]} if m["role"] == "user" 
                    else {"role": "model", "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ])
                
                response = chat.send_message(prompt)
                full_response = response.text
                st.markdown(full_response)
                
                # Simpan respon ke history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Terjadi kesalahan: {str(e)}")

# --- SIDEBAR INFO ---
with st.sidebar:
    st.header("Tentang Aplikasi")
    st.info("Aplikasi ini menggunakan Gemini API dan Streamlit untuk membantumu belajar bahasa secara kompleks.")
    if st.button("Hapus Percakapan"):
        st.session_state.messages = []
        st.rerun()
