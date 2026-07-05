import streamlit as st
from datetime import datetime
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Faza testów 🛠️", layout="centered")

# --- CSS - Wymuszenie stylu ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    h1, h2 { color: #FFD700 !important; }
    /* Ukrycie domyślnego menu Streamlit, żeby nie przeszkadzało */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- FUNKCJA DATY ---
def get_polish_date():
    dzis = datetime.now()
    dni = {"Monday": "Poniedziałek", "Tuesday": "Wtorek", "Wednesday": "Środa", "Thursday": "Czwartek", "Friday": "Piątek", "Saturday": "Sobota", "Sunday": "Niedziela"}
    miesiace = {"January": "stycznia", "February": "lutego", "March": "marca", "April": "kwietnia", "May": "maja", "June": "czerwca", "July": "lipca", "August": "sierpnia", "September": "września", "October": "października", "November": "listopada", "December": "grudnia"}
    return f"{dni[dzis.strftime('%A')]}, {dzis.day} {miesiace[dzis.strftime('%B')]} {dzis.year}"

# --- LOGIKA ---
if 'krok' not in st.session_state: st.session_state.krok = 1
if 'dane' not in st.session_state: st.session_state.dane = {"imie": "", "wiek": 18, "edukacja": "", "klasa": ""}

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
            st.session_state.dane["klasa"] = st.selectbox("Poziom:", zakres)
        if st.button("Zakończ"): st.session_state.krok = 4; st.rerun()

else:
    # NAWIGACJA NA GÓRZE (Najbezpieczniejsza dla telefonów)
    selected = option_menu(
        menu_title=None,
        options=["Plan", "Dom", "Testy"],
        icons=["calendar-date", "house", "pencil-square"],
        orientation="horizontal",
        styles={
            "container": {"background-color": "#1E1E1E"},
            "nav-link": {"color": "white", "--hover-color": "#333"},
            "nav-link-selected": {"background-color": "#FFD700", "color": "black"},
        }
    )

    if selected == "Dom":
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
        st.write("Wgraj plik PDF z notatkami, a AI stworzy dla Ciebie quiz.")
        
        uploaded_file = st.file_uploader("Wybierz plik PDF", type="pdf")
        
        if uploaded_file is not None:
            from pypdf import PdfReader
            
            with st.spinner("Analizuję Twój plik..."):
                reader = PdfReader(uploaded_file)
                tekst_z_pdf = ""
                for page in reader.pages:
                    tekst_z_pdf += page.extract_text() + "\n"
                
            st.success("Plik wczytany!")
            st.write(f"Wczytano {len(tekst_z_pdf)} znaków.")
            
            # Tu w przyszłości wyślemy 'tekst_z_pdf' do modelu AI
            if st.button("Wygeneruj test z tego materiału"):
                st.info("Logika AI zostanie podpięta w następnym kroku!")
                # st.write(tekst_z_pdf[:500] + "...") # Podgląd pierwszych 500 znaków

        
