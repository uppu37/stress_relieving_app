import streamlit as st
import time
import random
from music import music_player
from database import create_table, add_entry, get_entries, register_user, login_user

# ── PAGE CONFIG ──
st.set_page_config(page_title="MindEase | Stress Relief", page_icon="logo.png", layout="wide")

# ── CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700&family=Cormorant+Garamond:ital,wght@0,300;1,300&display=swap');

html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

.stApp {
    background: linear-gradient(160deg, #f5f1e8 80%, #f5f1e8 100%);
    background-attachment: fixed;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2d4a2d 0%, #3d6b5e 100%);
    border-right: none;
    box-shadow: 4px 0 20px rgba(0,0,0,0.08);
}
[data-testid="stSidebar"] * { color: #e8f0e8 !important; }
[data-testid="stSidebar"] h1 { font-size: 24px !important; letter-spacing: 1px; }
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 8px 14px;
    margin: 3px 0;
    display: block;
    transition: background 0.2s;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,0.18);
}

h1 { color: #2d4a2d !important; font-weight: 700; letter-spacing: -0.5px; }
h2, h3 { color: #2d4a2d !important; font-weight: 600; }
p, li { color: #4a5a4a; font-size: 16px; line-height: 1.7; }

/* Cards */
.calm-card {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(12px);
    padding: 28px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.9);
    box-shadow: 0 8px 32px rgba(45,74,45,0.08);
    text-align: center;
    transition: transform 0.25s, box-shadow 0.25s;
    margin-bottom: 8px;
}
.calm-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 14px 40px rgba(45,74,45,0.13);
}
.calm-card .icon { font-size: 36px; display: block; margin-bottom: 10px; }
.calm-card h3 { color: #3d6b5e !important; margin: 0; font-size: 15px; }

/* Journal entry card */
.entry-card {
    background: rgba(255,255,255,0.8);
    border-radius: 18px;
    padding: 20px 24px;
    margin-bottom: 14px;
    border-left: 4px solid #7aab82;
    box-shadow: 0 4px 16px rgba(45,74,45,0.07);
    font-size: 15px;
    color: #3a4a3a;
    line-height: 1.7;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #5a8a62 0%, #3d6b5e 100%);
    color: white !important;
    border: none;
    border-radius: 50px;
    padding: 12px 32px;
    font-size: 15px;
    font-weight: 600;
    box-shadow: 0 4px 16px rgba(61,107,94,0.35);
    transition: all 0.25s;
    width: 100%;
    letter-spacing: 0.3px;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(61,107,94,0.4);
}

/* Inputs */
.stTextArea textarea, .stTextInput input {
    background: rgba(255,255,255,0.85) !important;
    border: 1.5px solid rgba(122,171,130,0.4) !important;
    border-radius: 16px !important;
    font-size: 15px !important;
    color: #3a4a3a !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #5a8a62 !important;
    box-shadow: 0 0 0 3px rgba(90,138,98,0.12) !important;
}
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.85) !important;
    border-radius: 14px !important;
    border: 1.5px solid rgba(122,171,130,0.4) !important;
}

/* Progress */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #7aab82, #3d6b5e) !important;
    border-radius: 99px;
}

/* Alerts */
.stAlert { background: rgba(255,255,255,0.8) !important; border-radius: 16px !important; }
div[data-baseweb="notification"] { border-radius: 16px !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 8px; background: transparent; }
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.6);
    border-radius: 14px !important;
    padding: 10px 22px;
    font-weight: 600;
    border: none !important;
    color: #4a5a4a !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #5a8a62, #3d6b5e) !important;
    color: white !important;
}

/* Number input */
.stNumberInput input {
    background: rgba(255,255,255,0.85) !important;
    border-radius: 12px !important;
    border: 1.5px solid rgba(122,171,130,0.4) !important;
}

/* Breathing timer */
.breath-display {
    background: linear-gradient(135deg, rgba(122,171,130,0.15), rgba(61,107,94,0.1));
    border-radius: 24px;
    padding: 40px;
    text-align: center;
    border: 1px solid rgba(122,171,130,0.25);
    font-size: 42px;
    font-family: 'Cormorant Garamond', serif;
    color: #2d4a2d;
    letter-spacing: 2px;
    box-shadow: 0 8px 32px rgba(45,74,45,0.08);
}

footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── DATABASE INIT ──
create_table()
# SESSION STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
def get_emoji(mood):
    return {"Happy": "😊", "Calm": "😌", "Neutral": "😐", "Stressed": "😰", "Sad": "😢", "Excited": "🤩"}.get(mood, "😐")
# LOGIN PAGE
# LOGIN PAGE
if not st.session_state.logged_in:

    st.markdown("<br><br>", unsafe_allow_html=True)

    # CENTERED CONTAINER
    left, center, right = st.columns([1,2,1])

    with center:

        # CENTERED LOGO
        logo_left, logo_center, logo_right = st.columns([2,2,2])
        with logo_center:
            st.image("logo.png", width=200)

        st.markdown(
        """
        <div style="
            background: rgba(255,255,255,0.85);
            padding:35px;
            border-radius:24px;
            box-shadow:0 10px 35px rgba(45,74,45,0.12);
            text-align:center;
            margin-top:20px;
        ">
        <h2 style="color:#2d4a2d;">Welcome</h2>
        <p style="color:#4a5a4a;">
        Sign in to continue your wellness journey 🌿
        </p>
        </div>
        """,
        unsafe_allow_html=True
        )

        tab1, tab2 = st.tabs(["Login", "Register"])

        # LOGIN TAB
        with tab1:

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            btn_left, btn_center, btn_right = st.columns([2,2,1])

            with btn_center:
                login_clicked = st.button("Login")

            if login_clicked:
                user = login_user(username, password)

                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        # REGISTER TAB
        with tab2:

            new_user = st.text_input("Create Username")
            new_pass = st.text_input("Create Password", type="password")

            btn_left, btn_center, btn_right = st.columns([1,1,1])

            with btn_center:
                register_clicked = st.button("Register")

            if register_clicked:
                if register_user(new_user, new_pass):
                    st.success("Account created! Please login.")
                else:
                    st.error("Username already exists")

        

    st.stop()
# ── SIDEBAR ──
with st.sidebar: 
    st.image("logo.png", width=150) 
    st.write(f"Welcome, {st.session_state.username}") 
    if st.button("Logout"): 
        st.session_state.logged_in = False 
        st.rerun() 
    menu = st.radio("Navigate", [ "🏠 Home", "💙 Mood Detection", "🧘 Breathing Exercise", "🎵 Calm Music Player", "📔 Personal Journal", "📚 Exam Stress Zone" ]) 
    st.markdown("---") 
    st.markdown("*🌿 Take a breath. You're doing great.*")
# ── HOME ──
if menu == "🏠 Home":
    col1, col2, col3 = st.columns([3,1,3])
    with col2:
        st.image("logo.png", width=200)
    
    st.markdown("""
        <div style="text-align:center;">
            <h2 style="color:black;">
                MindEase — Your Wellness Companion 💙
            </h2>
        </div>
        """, unsafe_allow_html=True)    
    st.markdown("")

    st.markdown("""
        <div style="text-align:center;">
            <h3 style="color:black;">
                Your gentle space to pause, breathe, and restore.
            </h3>
        </div>
        """, unsafe_allow_html=True)    
    st.markdown("")

    features = [
        ("😊", "AI Mood Detection"), ("🧘", "Breathing Exercise"), ("🎵", "Calm Music"),
        ("📔", "Personal Journal"), ("📚", "Exam Zone"), ("💡", "Daily Motivation")
    ]
    cols = st.columns(3)
    for i, (icon, name) in enumerate(features):
        cols[i % 3].markdown(f'<div class="calm-card"><span class="icon">{icon}</span><h3>{name}</h3></div>', unsafe_allow_html=True)

    st.markdown("")
    st.success("🌸 Your mental wellness journey starts today — one breath at a time.")

# ── MOOD DETECTION ──
elif menu == "💙 Mood Detection":
    st.title("💙 Mood Detection")
    st.markdown("Share how you're feeling. There's no right or wrong answer.")

    user_input = st.text_area("How are you feeling today?", height=130)

    if st.button("✨ Analyze Mood"):
        if user_input.strip():
            txt = user_input.lower()
            if any(w in txt for w in ["happy", "great", "joy", "love", "wonderful"]): mood, score = "Happy", 0.92
            elif any(w in txt for w in ["calm", "peace", "relax", "serene"]): mood, score = "Calm", 0.88
            elif any(w in txt for w in ["sad", "down", "depressed", "cry", "upset"]): mood, score = "Sad", 0.85
            elif any(w in txt for w in ["stress", "overwhelm", "anxious", "worry"]): mood, score = "Stressed", 0.90
            elif any(w in txt for w in ["excited", "thrilled", "energetic"]): mood, score = "Excited", 0.93
            else: mood, score = "Neutral", 0.78

            st.subheader(f"Detected Mood: {mood} {get_emoji(mood)}")
            st.progress(score)
            st.caption(f"Confidence: {int(score * 100)}%")

            if st.button("📔 Save to Journal"):
                add_entry(st.session_state.username, mood, score, user_input)
                st.success("Saved to your journal!")
        else:
            st.warning("Please write how you're feeling first.")

# ── BREATHING ──
elif menu == "🧘 Breathing Exercise":
    st.title("🧘 4-7-8 Breathing Technique")
    st.markdown("A natural way to calm your nervous system. Follow the rhythm.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Inhale", "4 sec")
    col2.metric("Hold", "7 sec")
    col3.metric("Exhale", "8 sec")
    st.markdown("")

    if st.button("🌬️ Begin Session"):
        phases = [("🌬 Breathe In", 4), ("🤲 Hold", 7), ("💨 Breathe Out", 8)]
        placeholder = st.empty()

        for cycle in range(2):
            for text, seconds in phases:
                for sec in range(seconds, 0, -1):
                    placeholder.markdown(f'<div class="breath-display">{text}<br>{sec}</div>', unsafe_allow_html=True)
                    time.sleep(1)

        placeholder.empty()
        st.success("🎉 Well done! Session complete. Notice how you feel.")

# ── MUSIC ──
elif menu == "🎵 Calm Music Player":
    st.title("🎵 Calm Music")
    st.markdown("Let the sounds carry your stress away.")
    music_player()

# ── JOURNAL ──
elif menu == "📔 Personal Journal":
    st.title("📔 Personal Journal")

    st.subheader("✍ Write New Entry")
    journal_text = st.text_area("What's on your mind today?", height=150)
    mood_option = st.selectbox("How are you feeling?", ["Happy", "Calm", "Neutral", "Stressed", "Sad", "Excited"])

    if st.button("💾 Save Entry"):
        if journal_text.strip():
            add_entry(st.session_state.username, mood_option, 1.0, journal_text)
            st.success("Entry saved! 🌿")
            st.rerun()
        else:
            st.warning("Write something first.")

    st.markdown("---")
    st.subheader("📜 Your Entries")
    entries = get_entries(st.session_state.username)

    if entries:
        for entry in entries:
            st.markdown(f"""
            <div class="entry-card">
            📅 <b>{entry[2]}</b> &nbsp;|&nbsp; {entry[3]} {get_emoji(entry[3])}<br>
            <span style="color:#4a5a4a">{entry[5]}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Your journal is empty. Write your first entry above!")

# ── EXAM STRESS ZONE ──
elif menu == "📚 Exam Stress Zone":
    st.title("📚 Exam Stress Zone")
    st.markdown("Study smarter, rest better. You've got this. 💪")

    tab1, tab2 = st.tabs(["⏳ Pomodoro Timer", "💡 Motivation"])

    # ---------------- POMODORO TIMER ----------------
    with tab1:

        st.markdown("""
        ### What is the Pomodoro Technique? 🍅

        The **Pomodoro Technique** is a time-management method where you study in 
        **focused sessions followed by short breaks**.

        Typical cycle:
        - 📖 Study for **25 minutes**
        - 🌿 Take a **5 minute break**
        - 🔁 Repeat the cycle

        This helps improve **focus, memory retention, and reduces burnout during exams.**
        """)

        st.divider()

        col1, col2 = st.columns(2)
        study = col1.number_input("Study (minutes)", 1, 60, 25)
        brk = col2.number_input("Break (minutes)", 1, 30, 5)

        if st.button("▶ Start Timer"):
            timer = st.empty()

            for sec in range(study * 60, 0, -1):
                m, s = divmod(sec, 60)
                timer.markdown(
                    f'<div class="breath-display">📖 Study Time<br>{m:02d}:{s:02d}</div>',
                    unsafe_allow_html=True
                )
                time.sleep(1)

            st.success("✅ Study session done! Take your break.")

            for sec in range(brk * 60, 0, -1):
                m, s = divmod(sec, 60)
                timer.markdown(
                    f'<div class="breath-display">🌿 Break Time<br>{m:02d}:{s:02d}</div>',
                    unsafe_allow_html=True
                )
                time.sleep(1)

            timer.empty()
            st.success("🎉 Break complete! Great session.")

    # ---------------- MOTIVATION ----------------
    with tab2:

        st.markdown("### 🌟 Study Motivation")

        st.markdown("""
        Feeling overwhelmed before exams is normal.  
        Take a breath, reset your focus, and remind yourself why you started.  
        Click below whenever you need a **quick boost of motivation.**
        """)

        st.markdown("<br>", unsafe_allow_html=True)

        quotes = [
            "Success is built on small daily efforts.",
            "Exams test knowledge, not your worth as a person.",
            "You are more capable than you think.",
            "Progress over perfection. Always.",
            "Stay consistent. Rest is part of the process.",
            "Every expert was once a beginner who kept going."
        ]

        col1, col2, col3 = st.columns([1,2,1])

        with col2:
            if st.button("✨ Get Motivation"):

                quote = random.choice(quotes)

                st.markdown(
                f"""
                <div style="
                background:#ffffff;
                padding:30px;
                border-radius:18px;
                text-align:center;
                box-shadow:0 8px 20px rgba(0,0,0,0.1);
                font-size:20px;
                color:#2d4a2d;
                ">
                💬 <i>{quote}</i>
                </div>
                """,
                unsafe_allow_html=True
                )