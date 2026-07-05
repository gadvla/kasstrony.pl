import streamlit as st
from datetime import datetime
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Faza testów 🛠️", layout="centered")

# --- STYLIZACJA ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    h1, h2 { color: #FFD700 !important; }
    /* Ustawienie menu na dole */
    .st-emotion-cache-12fmueu { padding-bottom: 80px; } 
    </style>
""", unsafe_allow_html=True)

# --- FUNKCJA DATY ---
def get_polish_date():
    dzis = datetime.now()
    dni = {"Monday": "Poniedziałek", "Tuesday": "Wtorek", "Wednesday": "Środa", "Thursday": "Czwartek", "Friday": "Piątek", "Saturday": "Sobota", "Sunday": "Niedziela"}
    miesiace = {"January": "stycznia", "February": "lutego", "March": "marca", "April": "kwietnia", "May": "maja", "June": "czerwca", "July": "lipca", "August": "sierpnia", "September": "września", "October": "października", "November": "listopada", "December": "grudnia"}
    return f"{dni[dzis.strftime('%A')]}, {dzis.day} {miesiace[dzis.strftime('%B')]} {dzis.year}"

# --- INICJALIZACJA ---
if 'krok' not in st.session_state: st.session_state.krok = 1
if 'dane' not in st.session_state:
    st.session_state.dane = {"imie": "", "wiek": 18, "edukacja": "", "klasa": ""}

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

# --- EKRAN GŁÓWNY Z NAWIGACJĄ ---
else:
    # Wybór strony za pomocą streamlit-option-menu
    selected = option_menu(
        menu_title=None,
        options=["Plan", "Dom", "Testy"],
        icons=["calendar-date", "house", "pencil-square"],
        menu_icon="cast",
        default_index=1,
        orientation="horizontal",
        styles={
            "container": {"position": "fixed", "bottom": "0", "left": "0", "width": "100%", "background-color": "#1E1E1E"},
            "icon": {"color": "#FFD700", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#333"},
            "nav-link-selected": {"background-color": "#333", "color": "#FFD700"},
        }
    )

    if selected == "Dom":
        st.title("Faza testów 🛠️")
        st.subheader(f"Witaj, {st.session_state.dane['imie']}!")
        st.write(f"**Dzisiaj:** {get_polish_date()}")
        st.write("---")
        st.write(f"👤 Wiek: {st.session_state.dane['wiek']}")
        st.write(f"🏫 Szkoła: {st.session_state.dane['edukacja']}")
        if st.session_state.dane["klasa"]: st.write(f"🎓 Poziom: {st.session_state.dane['klasa']}")
        
    elif selected == "Plan":
        st.title("🗓️ Plan Nauki")
    elif selected == "Testy":
        st.title("📝 Testy i Egzaminy")
        
