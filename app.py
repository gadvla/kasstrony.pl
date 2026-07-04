import streamlit as st
import time

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="Astra AI", layout="centered", initial_sidebar_state="collapsed")

# --- 2. STYLIZACJA (Ciemny motyw + Żółty) ---
st.markdown("""
    <style>
    /* Ciemne tło dla całej aplikacji */
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    
    /* Główny przycisk akcji (Żółty) */
    div.stButton > button:first-child {
        background-color: #FFD700; 
        color: #000000;
        font-weight: 800;
        border: none;
        border-radius: 8px;
        width: 100%;
        padding: 12px;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #FACC15;
        transform: scale(1.02);
    }

    /* Pola wprowadzania tekstu i liczb */
    .stTextInput input, .stNumberInput input {
        background-color: #1E1E1E;
        color: #FFD700;
        border: 2px solid #333;
        border-radius: 8px;
        font-size: 18px;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #FFD700;
        box-shadow: none;
    }

    /* Wygląd nagłówków */
    h1, h2, h3 {
        color: #FFD700 !important;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. INICJALIZACJA PAMIĘCI (SESSION STATE) ---
if 'krok' not in st.session_state:
    st.session_state.krok = 1
    st.session_state.dane = {"imie": "", "wiek": 18, "edukacja": ""}

def nastepny_krok():
    st.session_state.krok += 1

# --- 4. LOGIKA KROKÓW (WIZARD) ---

# Pasek postępu
if st.session_state.krok <= 3:
    st.progress(st.session_state.krok / 3)
st.write("---")

# KROK 1: Imię
if st.session_state.krok == 1:
    st.title("Witaj w Astra AI ⚡")
    st.markdown("<p style='text-align: center; color: #aaa;'>Twój osobisty asystent nauki. Zaczynamy?</p>", unsafe_allow_html=True)
    
    st.session_state.dane["imie"] = st.text_input("Jak masz na imię?", placeholder="Wpisz swoje imię...")
    
    st.write("") # Odstęp
    if st.button("Dalej"):
        if st.session_state.dane["imie"].strip() == "":
            st.warning("Podaj imię, żebyśmy mogli przejść dalej!")
        else:
            nastepny_krok()
            st.rerun()

# KROK 2: Wiek
elif st.session_state.krok == 2:
    st.title(f"Miło Cię poznać, {st.session_state.dane['imie']}!")
    st.markdown("<p style='text-align: center; color: #aaa;'>Muszę wiedzieć, jak dopasować poziom materiałów.</p>", unsafe_allow_html=True)
    
    st.session_state.dane["wiek"] = st.number_input("Ile masz lat?", min_value=7, max_value=100, value=18)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Wróć"):
            st.session_state.krok -= 1
            st.rerun()
    with col2:
        if st.button("Dalej "):
            nastepny_krok()
            st.rerun()

# KROK 3: Poziom edukacji
elif st.session_state.krok == 3:
    st.title("Ostatnie pytanie 🎯")
    st.markdown("<p style='text-align: center; color: #aaa;'>Na jakim etapie nauki obecnie jesteś?</p>", unsafe_allow_html=True)
    
    opcje_edukacji = ["Szkoła podstawowa", "Szkoła średnia", "Studia", "Inne / Samouctwo"]
    st.session_state.dane["edukacja"] = st.radio("Wybierz poziom:", opcje_edukacji)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Wróć"):
            st.session_state.krok -= 1
            st.rerun()
    with col2:
        if st.button("Zakończ konfigurację"):
            nastepny_krok()
            with st.spinner("Przygotowuję Twój panel..."):
                time.sleep(1) # Symulacja ładowania
            st.rerun()

# KROK 4: Ekran główny aplikacji (Po zalogowaniu)
elif st.session_state.krok == 4:
    st.title("Panel Główny 🚀")
    imie = st.session_state.dane["imie"]
    edukacja = st.session_state.dane["edukacja"]
    
    st.success(f"Profil utworzony! Zalogowano jako **{imie}** ({edukacja}).")
    st.write("Tu w przyszłości znajdzie się wgrywanie PDF-ów i generator planu nauki.")
    
    if st.button("Zacznij od nowa (Debug)"):
        st.session_state.krok = 1
        st.rerun()
              
