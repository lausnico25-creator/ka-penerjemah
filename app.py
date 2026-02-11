import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Valentine's Day", page_icon="❤️")

# 2. Inisialisasi Database Sementara (Session State)
if 'no_count' not in st.session_state:
    st.session_state.no_count = 0
if 'say_yes' not in st.session_state:
    st.session_state.say_yes = False

# 3. Daftar Pesan Tombol No
no_messages = [
    "No", "Are you sure?", "Really sure??", "Are you positive?", 
    "Pookie please...", "Just think about it!", 
    "If you say no, I will be really sad...", "I will be very sad...", 
    "I will be very very very sad..."
]

# --- TAMPILAN UTAMA ---

if not st.session_state.say_yes:
    st.title("Will you be my Valentine? ❤️")
    
    # Gambar Kucing (Bisa diganti URL-nya jika punya sendiri)
    st.image("https://media.tenor.com/jck_6VvjY_0AAAAi/capoo-blue-cat.gif", width=250)

    # Logika ukuran tombol Yes (Makin banyak klik No, makin raksasa!)
    # Kita gunakan padding dan font-size untuk membesarkannya
    yes_size = 15 + (st.session_state.no_count * 15) 
    padding = 10 + (st.session_state.no_count * 5)

    # CSS Custom untuk tombol
    st.markdown(f"""
        <style>
        .stButton > button:first-child {{
            background-color: #28a745 !important;
            color: white !important;
            font-size: {yes_size}px !important;
            padding: {padding}px {padding*2}px !important;
            transition: 0.3s;
        }}
        div[data-testid="column"]:nth-child(2) button {{
            background-color: #dc3545 !important;
            color: white !important;
            font-size: 16px !important;
        }}
        </style>
    """, unsafe_content_allowed=True)

    # Membuat layout kolom
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Yes", key="yes_btn"):
            st.session_state.say_yes = True
            st.rerun() # Refresh halaman untuk pindah tampilan

    with col2:
        # Teks tombol No berubah sesuai hitungan
        msg_index = min(st.session_state.no_count, len(no_messages) - 1)
        if st.button(no_messages[msg_index], key="no_btn"):
            st.session_state.no_count += 1
            st.rerun() # Refresh untuk memperbesar tombol Yes

else:
    # --- TAMPILAN SETELAH KLIK YES ---
    st.title("Knew you would say yes! ❤️")
    st.image("https://media.tenor.com/gU_i95S8L7IAAAAi/bear-kiss-bear-cute.gif", width=350)
    st.balloons()
