import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Guru Bahasa AI", page_icon="🎓", layout="wide")

# --- KONFIGURASI API ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("API Key tidak ditemukan di Secrets!")
    st.stop()

model = genai.GenerativeModel("gemini-2.5-flash")

# --- SISTEM PENYIMPANAN RIWAYAT ---
# Struktur: { "id_chat_1": [pesan1, pesan2], "id_chat_2": [pesan1] }
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {"Chat Utama": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat Utama"

# --- SIDEBAR: DAFTAR RIWAYAT ---
with st.sidebar:
    st.title("📚 Riwayat Guru")
    
    # Tombol Chat Baru
    if st.button("+ Buat Percakapan Baru"):
        new_id = f"Chat {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[new_id] = []
        st.session_state.current_chat = new_id
        st.rerun()

    st.write("---")
    st.write("Pilih Percakapan:")
    
    # Daftar Judul Chat yang pernah dibuat
    for chat_id in st.session_state.all_chats.keys():
        if st.button(chat_id, key=chat_id):
            st.session_state.current_chat = chat_id
            st.rerun()

# --- TAMPILAN UTAMA ---
st.title(f"🎓 {st.session_state.current_chat}")
st.info("Guru AI siap membantumu belajar Indo-Eng-Kor!")

# Ambil pesan dari chat yang sedang aktif dipilih
messages = st.session_state.all_chats[st.session_state.current_chat]

# Tampilkan pesan-pesan lama di chat yang dipilih
for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- PROSES INPUT ---
if prompt := st.chat_input("Tanya guru..."):
    # Simpan ke riwayat chat aktif
    st.session_state.all_chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Guru sedang berpikir..."):
            try:
                # Berikan instruksi agar AI menjadi guru
                full_prompt = f"Sebagai Guru Bahasa, jawablah ini: {prompt}"
                response = model.generate_content(full_prompt)
                answer = response.text
                
                st.markdown(answer)
                # Simpan jawaban ke riwayat chat aktif
                st.session_state.all_chats[st.session_state.current_chat].append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {e}")
