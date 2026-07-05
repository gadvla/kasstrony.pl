import streamlit as st
from datetime import datetime
import locale

# Ustawienie języka polskiego dla daty
try:
    locale.setlocale(locale.LC_TIME, 'pl_PL.UTF-8')
except:
    locale.setlocale(locale.LC_TIME, 'pl_PL') # Zapasowe ustawienie

st.set_page_config(page_title="Faza testów 🛠️", layout="centered")



# --- STYLIZACJA ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    h1, h2 { color: #FFD700 !important; }
    
    /* Pasek nawigacyjny - przyklejony do dołu */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #1E1E1E;
        color: white;
        text-align: center;
        padding: 10px 0;
        border-top: 2px solid #FFD700;
        z-index: 999;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICJALIZACJA ---
if 'krok' not in st.session_state: st.session_state.krok = 1
if 'dane' not in st.session_state:
    st.session_state.dane = {"imie": "", "wiek": 18, "edukacja": "", "klasa": ""}
if 'active_page' not in st.session_state: st.session_state.active_page = "Dom"

# --- LOGIKA KONFIGURACJI ---
if st.session_state.krok <= 3:
    if st.session_state.krok == 1:
        st.title("Faza testów 🛠️")
        st.session_state.dane["imie"] = st.text_input("Imię:")
        if st.button("Dalej"): st.session_state.krok = 2; st.rerun()
    elif st.session_state.krok == 2:
        st.session_state.dane["wiek"] = st.number_input("Wiek:", 5, 100, 18)
        if st.button("Dalej"): st.session_state.krok = 3; st.rerun()
    elif st.session_state.krok == 3:
        st.session_state.dane["edukacja"] = st.selectbox("Szkoła:", ["Szkoła podstawowa", "Szkoła średnia", "Studia", "Inne"])
        if st.session_state.dane["edukacja"] in ["Szkoła podstawowa", "Szkoła średnia", "Studia"]:
            zakres = range(1, 9) if st.session_state.dane["edukacja"] != "Szkoła średnia" else range(1, 6)
            st.session_state.dane["klasa"] = st.selectbox("Poziom (klasa/semestr):", zakres)
        if st.button("Zakończ"): st.session_state.krok = 4; st.rerun()

# --- EKRAN GŁÓWNY (Po konfiguracji) ---
else:
    # Zawartość stron
    if st.session_state.active_page == "Dom":
        st.title("Faza testów 🛠️")
        st.subheader(f"Witaj, {st.session_state.dane['imie']}!")
        # Data po polsku
        dzis = datetime.now()
        st.write(f"**Dzisiaj:** {dzis.strftime('%A, %d %B %Y').capitalize()}")
        st.write("---")
        st.write(f"👤 Wiek: {st.session_state.dane['wiek']}")
        st.write(f"🏫 Szkoła: {st.session_state.dane['edukacja']}")
        if st.session_state.dane["klasa"]: st.write(f"🎓 Poziom: {st.session_state.dane['klasa']}")
        
    elif st.session_state.active_page == "Plan":
        st.title("🗓️ Plan Nauki")
    elif st.session_state.active_page == "Testy":
        st.title("📝 Testy i Egzaminy")

    # --- PASEK NAWIGACYJNY (Naprawiony) ---
    # Używamy kontenera z przyciskami, który jest zawsze widoczny
    footer = st.container()
    with footer:
        st.markdown('<div class="footer">', unsafe_allow_html=True)
        cols = st.columns(3)
        with cols[0]:
            if st.button("🗓️ Plan"): st.session_state.active_page = "Plan"; st.rerun()
        with cols[1]:
            if st.button("🏠 Dom"): st.session_state.active_page = "Dom"; st.rerun()
        with cols[2]:
            if st.button("📝 Testy"): st.session_state.active_page = "Testy"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
