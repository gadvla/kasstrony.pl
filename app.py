import streamlit as st
from datetime import datetime
import locale

# Ustawienie polskiego formatu daty (jeśli system pozwala)
try:
    locale.setlocale(locale.LC_TIME, 'pl_PL.UTF-8')
except:
    pass

st.set_page_config(page_title="Faza testów 🛠️", layout="centered")

# --- STYLIZACJA (Przyklejony pasek i ciemny motyw) ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    h1, h2 { color: #FFD700 !important; }
    
    /* Pasek nawigacyjny */
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #1E1E1E;
        padding: 15px 0;
        display: flex;
        justify-content: space-around;
        border-top: 2px solid #FFD700;
        z-index: 1000;
    }
    .nav-btn {
        background: none; border: none; color: #FFD700; font-size: 24px; cursor: pointer;
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
        
        # Logika klas/semestrów
        if st.session_state.dane["edukacja"] == "Szkoła podstawowa":
            st.session_state.dane["klasa"] = st.selectbox("Klasa:", range(1, 9))
        elif st.session_state.dane["edukacja"] == "Szkoła średnia":
            st.session_state.dane["klasa"] = st.selectbox("Klasa:", range(1, 6))
        elif st.session_state.dane["edukacja"] == "Studia":
            st.session_state.dane["klasa"] = st.selectbox("Semestr:", range(1, 9))
        
        if st.button("Zakończ"): st.session_state.krok = 4; st.rerun()

# --- EKRAN GŁÓWNY (Po konfiguracji) ---
else:
    # Funkcje stron
    def render_dom():
        st.title("Faza testów 🛠️")
        st.subheader(f"Witaj, {st.session_state.dane['imie']}!")
        
        dzis = datetime.now()
        st.info(f"📅 **Dzisiaj:** {dzis.strftime('%A, %d %B %Y')}")
        
        st.write("### Twój Profil:")
        st.write(f"👤 Wiek: {st.session_state.dane['wiek']}")
        st.write(f"🏫 Szkoła: {st.session_state.dane['edukacja']}")
        if st.session_state.dane["klasa"]:
            st.write(f"🎓 Poziom: {st.session_state.dane['klasa']}")

    def render_plan():
        st.title("🗓️ Plan Nauki")
        st.write("Tutaj pojawi się Twój harmonogram.")

    def render_testy():
        st.title("📝 Testy i Egzaminy")
        st.write("Tu wygenerujesz testy z notatek.")

    # Wybór strony
    if st.session_state.active_page == "Dom": render_dom()
    elif st.session_state.active_page == "Plan": render_plan()
    elif st.session_state.active_page == "Testy": render_testy()

    # --- PASEK NAWIGACYJNY (Bottom Bar) ---
    st.markdown("""
        <div class="nav-bar">
            <button class="nav-btn" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'Plan'}, '*')">🗓️</button>
            <button class="nav-btn" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'Dom'}, '*')">🏠</button>
            <button class="nav-btn" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'Testy'}, '*')">📝</button>
        </div>
    """, unsafe_allow_html=True)

    # Hack do obsługi przycisków w Streamlit (używamy st.button jako zamiennik nawigacji, 
    # ponieważ prawdziwy JS w Streamlit wymaga komponentów, tutaj użyjemy przycisków w kolumnach na dole)
    
    st.write("<br><br><br>", unsafe_allow_html=True) # Odstęp, żeby treść nie wchodziła pod pasek
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🗓️ Plan"): st.session_state.active_page = "Plan"; st.rerun()
    with c2: 
        if st.button("🏠 Dom"): st.session_state.active_page = "Dom"; st.rerun()
    with c3: 
        if st.button("📝 Testy"): st.session_state.active_page = "Testy"; st.rerun()
            
