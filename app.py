import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Guru Bahasa AI", page_icon="🎓")

# --- KONFIGURASI API (Membaca dari Secrets) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("API Key tidak ditemukan di .streamlit/secrets.toml!")
    st.stop()

# --- SETUP MODEL ---
instruction = (
    "Kamu adalah 'Guru Bahasa AI' yang ahli dalam Bahasa Indonesia, Inggris, dan Korea. "
    "Tugasmu membantu terjemahan kompleks dan menjelaskan grammar. "
    "Bersikaplah ramah dan edukatif."
)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=instruction
)

# --- INISIALISASI RIWAYAT PESAN ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR (Untuk Fitur Simpan & Hapus) ---
with st.sidebar:
    st.header("Menu Riwayat")
    
    # Fitur Mengunduh Riwayat Chat
    if st.session_state.messages:
        # Menggabungkan semua chat menjadi satu teks panjang
        chat_text = ""
        for msg in st.session_state.messages:
            role = "Siswa" if msg["role"] == "user" else "Guru AI"
            chat_text += f"{role}: {msg['content']}\n\n"
        
        st.download_button(
            label="💾 Download Riwayat Chat (.txt)",
            data=chat_text,
            file_name="riwayat_belajar_bahasa.txt",
            mime="text/plain"
        )
    
    # Tombol Hapus Semua Chat
    if st.button("🗑️ Hapus Semua Percakapan"):
        st.session_state.messages = []
        st.rerun()

# --- TAMPILAN UTAMA ---
st.title("🎓 Guru Bahasa AI")
st.write("Riwayat pertanyaanmu akan tersimpan di bawah ini selama aplikasi berjalan.")

# Menampilkan riwayat chat dari session_state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- PROSES INPUT USER ---
if prompt := st.chat_input("Tanyakan sesuatu pada Guru..."):
    # 1. Tampilkan dan simpan pesan user ke riwayat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Ambil respon dari AI
    with st.chat_message("assistant"):
        with st.spinner("Guru sedang berpikir..."):
            try:
                # Mengirim pesan dengan menyertakan konteks sebelumnya
                chat = model.start_chat(history=[
                    {"role": "user", "parts": [m["content"]]} if m["role"] == "user" 
                    else {"role": "model", "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ])
                
                response = chat.send_message(prompt)
                full_response = response.text
                
                st.markdown(full_response)
                
                # 3. Simpan respon guru ke riwayat
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")