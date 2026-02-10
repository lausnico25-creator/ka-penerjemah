import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Guru Bahasa AI", page_icon="🎓", layout="wide")

# --- KONFIGURASI API ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("API Key belum disetting di Secrets!")
    st.stop()

model = genai.GenerativeModel("gemini-2.5-flash")

# --- SISTEM PENYIMPANAN ---
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} # Format: { "Judul Chat": [pesan] }

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# --- FUNGSI BUAT JUDUL OTOMATIS ---
def generate_chat_title(user_input):
    prompt_judul = f"Buat satu judul sangat singkat (maksimal 3 kata) untuk topik ini: {user_input}"
    response = model.generate_content(prompt_judul)
    return response.text.strip()

# --- SIDEBAR ---
with st.sidebar:
    st.title("📚 Riwayat Guru")
    
    if st.button("+ Chat Baru"):
        st.session_state.current_chat_id = None
        st.rerun()

    st.write("---")
    # Menampilkan daftar chat yang sudah ada
    for chat_id in st.session_state.all_chats.keys():
        if st.button(f"💬 {chat_id}", key=chat_id, use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.rerun()

# --- TAMPILAN UTAMA ---
st.title("🎓 Guru Bahasa AI")

# Tampilkan chat yang sedang aktif
if st.session_state.current_chat_id:
    messages = st.session_state.all_chats[st.session_state.current_chat_id]
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
else:
    st.info("Apa yang bisa saya bantu?🧑‍🏫")

# --- INPUT USER ---
if prompt := st.chat_input("Tanya guru..."):
    
    # Jika ini chat baru (belum ada judul)
    if st.session_state.current_chat_id is None:
        with st.spinner("Menyiapkan percakapan..."):
            new_title = generate_chat_title(prompt)
            # Pastikan judul unik
            if new_title in st.session_state.all_chats:
                new_title = f"{new_title} ({len(st.session_state.all_chats)})"
            
            st.session_state.all_chats[new_title] = []
            st.session_state.current_chat_id = new_title

    # Simpan dan tampilkan pesan user
    st.session_state.all_chats[st.session_state.current_chat_id].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon AI
    with st.chat_message("assistant"):
        with st.spinner("Guru sedang mengetik..."):
            try:
                # Instruksi sistem
                instruction = (
                    "Kamu adalah Guru Bahasa ahli Indo, Inggris, Korea. "
                    "Jelaskan terjemahan secara kompleks dan edukatif."
                )
                
                # Mengambil history untuk konteks
                history_context = st.session_state.all_chats[st.session_state.current_chat_id]
                
                response = model.generate_content(f"{instruction}\n\nChat: {history_context}")
                answer = response.text
                
                st.markdown(answer)
                st.session_state.all_chats[st.session_state.current_chat_id].append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
    
    st.rerun() # Refresh agar judul di sidebar langsung muncul
