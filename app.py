import streamlit as st

# Mengatur judul halaman dan ikon
st.set_page_config(page_title="Valentine's Day", page_icon="❤️")

# Inisialisasi 'session state' agar data tidak hilang saat halaman refresh
if 'no_count' not in st.session_state:
    st.session_state.no_count = 0
if 'say_yes' not in st.session_state:
    st.session_state.say_yes = False

# Daftar pesan yang muncul saat tombol "No" ditekan
no_messages = [
    "No",
    "Are you sure?",
    "Really sure??",
    "Are you positive?",
    "Pookie please...",
    "Just think about it!",
    "If you say no, I will be really sad...",
    "I will be very sad...",
    "I will be very very very sad..."
]

# Fungsi jika tombol "No" diklik
def press_no():
    st.session_state.no_count += 1

# Fungsi jika tombol "Yes" diklik
def press_yes():
    st.session_state.say_yes = True

# --- TAMPILAN ---

if not st.session_state.say_yes:
    st.title("Will you be my Valentine? ❤️")
    
    # Gambar GIF (Gunakan URL gambar kucing yang lucu)
    st.image("https://media.tenor.com/jck_6VvjY_0AAAAi/capoo-blue-cat.gif", width=200)

    # Hitung ukuran font tombol "Yes" (semakin sering klik No, semakin besar)
    yes_font_size = 16 + (st.session_state.no_count * 10)
    
    # Membuat kolom untuk tombol
    col1, col2 = st.columns([1, 1])

    with col1:
        # Tombol YES dengan ukuran dinamis menggunakan HTML
        if st.button("Yes", key="yes_btn", on_click=press_yes):
            pass
        # CSS sedikit untuk memperbesar tombol Yes secara visual
        st.markdown(f"""
            <style>
            div.stButton > button#yes_btn {{
                font-size: {yes_font_size}px !important;
                padding: {10 + st.session_state.no_count}px !important;
                background-color: #28a745;
                color: white;
            }}
            </style>
        """, unsafe_content_allowed=True)

    with col2:
        # Tombol NO yang teksnya berubah-ubah
        msg_index = min(st.session_state.no_count, len(no_messages) - 1)
        st.button(no_messages[msg_index], on_click=press_no)

else:
    # Tampilan jika sudah klik "YES"
    st.title("Knew you would say yes! ❤️")
    st.image("https://media.tenor.com/gU_i95S8L7IAAAAi/bear-kiss-bear-cute.gif", width=300)
    st.balloons() # Efek balon perayaan!
