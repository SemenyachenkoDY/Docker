import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import time

# ──────────────────────────────────────────────
# Конфигурация
# ──────────────────────────────────────────────
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-service:8000")

st.set_page_config(
    page_title="Learning Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Инициализация session_state
# ──────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "role" not in st.session_state:
    st.session_state.role = "admin"


# ──────────────────────────────────────────────
# CSS-стили (тёмная и светлая тема)
# ──────────────────────────────────────────────
def get_css(theme: str) -> str:
    if theme == "dark":
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

            /* ── Глобальные переменные ── */
            :root {
                --bg-primary: #0f0f1a;
                --bg-secondary: #1a1a2e;
                --bg-card: #16213e;
                --bg-card-hover: #1a2744;
                --accent-primary: #6c63ff;
                --accent-secondary: #e94560;
                --accent-gradient: linear-gradient(135deg, #6c63ff 0%, #e94560 100%);
                --text-primary: #e8e8f0;
                --text-secondary: #9898b0;
                --text-muted: #6b6b80;
                --border-color: rgba(108, 99, 255, 0.15);
                --shadow-color: rgba(0, 0, 0, 0.3);
                --success: #00d2a0;
                --warning: #ffb347;
                --star-color: #ffd700;
            }

            /* ── Основной фон ── */
            .stApp, [data-testid="stAppViewContainer"] {
                background: var(--bg-primary) !important;
                color: var(--text-primary) !important;
                font-family: 'Inter', sans-serif !important;
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
                border-right: 1px solid var(--border-color);
            }

            [data-testid="stSidebar"] * {
                color: var(--text-primary) !important;
            }

            /* ── Заголовки ── */
            h1, h2, h3, h4 {
                font-family: 'Inter', sans-serif !important;
                color: var(--text-primary) !important;
            }

            /* ── Tabs ── */
            .stTabs [data-baseweb="tab-list"] {
                gap: 4px;
                background: var(--bg-secondary);
                border-radius: 16px;
                padding: 6px;
                border: 1px solid var(--border-color);
            }
            .stTabs [data-baseweb="tab"] {
                border-radius: 12px;
                padding: 12px 28px;
                font-weight: 600;
                color: var(--text-secondary) !important;
                background: transparent;
                border: none;
                transition: all 0.3s ease;
            }
            .stTabs [aria-selected="true"] {
                background: var(--accent-gradient) !important;
                color: white !important;
                box-shadow: 0 4px 15px rgba(108, 99, 255, 0.4);
            }
            .stTabs [data-baseweb="tab"]:hover {
                color: var(--text-primary) !important;
            }
            .stTabs [data-baseweb="tab-highlight"] {
                display: none;
            }
            .stTabs [data-baseweb="tab-border"] {
                display: none;
            }

            /* ── Карточки ── */
            .course-card {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 16px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }
            .course-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 12px 40px rgba(108, 99, 255, 0.15);
                border-color: rgba(108, 99, 255, 0.3);
            }
            .course-card::before {
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 3px;
                background: var(--accent-gradient);
                border-radius: 16px 16px 0 0;
            }
            .course-card .card-title {
                font-size: 1.2em;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 8px;
            }
            .course-card .card-meta {
                color: var(--text-secondary);
                font-size: 0.9em;
                margin-bottom: 4px;
            }
            .course-card .card-badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.8em;
                font-weight: 600;
                margin-right: 8px;
                margin-top: 8px;
            }
            .badge-duration {
                background: rgba(108, 99, 255, 0.15);
                color: #8b83ff;
            }
            .badge-rating {
                background: rgba(255, 215, 0, 0.15);
                color: #ffd700;
            }
            .badge-author {
                background: rgba(0, 210, 160, 0.15);
                color: #00d2a0;
            }

            /* ── Метрики ── */
            .metric-card {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 16px;
                padding: 28px;
                text-align: center;
                transition: all 0.3s ease;
            }
            .metric-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 30px var(--shadow-color);
            }
            .metric-icon {
                font-size: 2.5em;
                margin-bottom: 8px;
            }
            .metric-value {
                font-size: 2.2em;
                font-weight: 800;
                background: var(--accent-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .metric-label {
                color: var(--text-secondary);
                font-size: 0.95em;
                font-weight: 500;
                margin-top: 4px;
            }

            /* ── Кнопки ── */
            .stButton > button {
                background: var(--accent-gradient) !important;
                color: white !important;
                border: none !important;
                border-radius: 12px !important;
                font-weight: 600 !important;
                padding: 12px 32px !important;
                font-size: 1em !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3) !important;
            }
            .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 25px rgba(108, 99, 255, 0.5) !important;
            }

            /* ── Формы / инпуты ── */
            .stTextInput > div > div > input,
            .stNumberInput > div > div > input,
            .stSelectbox > div > div {
                background: var(--bg-secondary) !important;
                border: 1px solid var(--border-color) !important;
                color: var(--text-primary) !important;
                border-radius: 12px !important;
                font-family: 'Inter', sans-serif !important;
            }
            .stTextInput > div > div > input:focus,
            .stNumberInput > div > div > input:focus {
                border-color: var(--accent-primary) !important;
                box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.2) !important;
            }

            /* ── Слайдер ── */
            .stSlider [data-baseweb="slider"] [role="slider"] {
                background: var(--accent-primary) !important;
            }

            /* ── Разделитель ── */
            hr {
                border-color: var(--border-color) !important;
            }

            /* ── DataFrames ── */
            .stDataFrame {
                border-radius: 12px;
                overflow: hidden;
            }

            /* ── Success / Error / Warning / Info ── */
            .stAlert {
                border-radius: 12px !important;
            }

            /* ── Header bar ── */
            .header-bar {
                background: linear-gradient(135deg, #6c63ff 0%, #e94560 50%, #6c63ff 100%);
                background-size: 200% 200%;
                animation: gradient-shift 6s ease infinite;
                padding: 32px 40px;
                border-radius: 20px;
                margin-bottom: 32px;
                position: relative;
                overflow: hidden;
            }
            .header-bar::after {
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0,0,0,0.15);
                border-radius: 20px;
            }
            .header-bar h1 {
                color: white !important;
                font-size: 2em;
                font-weight: 800;
                margin: 0;
                position: relative;
                z-index: 1;
            }
            .header-bar p {
                color: rgba(255,255,255,0.85);
                font-size: 1.1em;
                margin: 4px 0 0 0;
                position: relative;
                z-index: 1;
            }
            @keyframes gradient-shift {
                0%   { background-position: 0% 50%; }
                50%  { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            /* ── Star rating ── */
            .stars {
                color: var(--star-color);
                font-size: 1.1em;
                letter-spacing: 2px;
            }

            /* ── Scrollbar ── */
            ::-webkit-scrollbar { width: 8px; }
            ::-webkit-scrollbar-track { background: var(--bg-primary); }
            ::-webkit-scrollbar-thumb { background: var(--accent-primary); border-radius: 4px; }

            /* ── Empty state ── */
            .empty-state {
                text-align: center;
                padding: 60px 20px;
                color: var(--text-muted);
            }
            .empty-state .icon {
                font-size: 4em;
                margin-bottom: 16px;
            }
            .empty-state .title {
                font-size: 1.4em;
                font-weight: 600;
                color: var(--text-secondary);
                margin-bottom: 8px;
            }

            /* ── Form card ── */
            .form-card {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 20px;
                padding: 32px;
            }

            /* ── Sidebar styles ── */
            .sidebar-section {
                background: rgba(108, 99, 255, 0.08);
                border: 1px solid rgba(108, 99, 255, 0.15);
                border-radius: 12px;
                padding: 16px;
                margin-bottom: 16px;
            }
            .sidebar-title {
                font-weight: 700;
                font-size: 0.85em;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                color: var(--text-secondary);
                margin-bottom: 12px;
            }

            /* Hide Streamlit branding */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """
    else:
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

            :root {
                --bg-primary: #f5f7fb;
                --bg-secondary: #ffffff;
                --bg-card: #ffffff;
                --bg-card-hover: #f8f9fc;
                --accent-primary: #6c63ff;
                --accent-secondary: #e94560;
                --accent-gradient: linear-gradient(135deg, #6c63ff 0%, #e94560 100%);
                --text-primary: #1a1a2e;
                --text-secondary: #5a5a7a;
                --text-muted: #9898b0;
                --border-color: rgba(0, 0, 0, 0.08);
                --shadow-color: rgba(0, 0, 0, 0.06);
                --success: #00b894;
                --warning: #fdcb6e;
                --star-color: #f39c12;
            }

            .stApp, [data-testid="stAppViewContainer"] {
                background: var(--bg-primary) !important;
                color: var(--text-primary) !important;
                font-family: 'Inter', sans-serif !important;
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #ffffff 0%, #f5f7fb 100%) !important;
                border-right: 1px solid var(--border-color);
            }

            [data-testid="stSidebar"] * {
                color: var(--text-primary) !important;
            }

            h1, h2, h3, h4 {
                font-family: 'Inter', sans-serif !important;
                color: var(--text-primary) !important;
            }

            .stTabs [data-baseweb="tab-list"] {
                gap: 4px;
                background: var(--bg-secondary);
                border-radius: 16px;
                padding: 6px;
                border: 1px solid var(--border-color);
                box-shadow: 0 2px 8px var(--shadow-color);
            }
            .stTabs [data-baseweb="tab"] {
                border-radius: 12px;
                padding: 12px 28px;
                font-weight: 600;
                color: var(--text-secondary) !important;
                background: transparent;
                border: none;
                transition: all 0.3s ease;
            }
            .stTabs [aria-selected="true"] {
                background: var(--accent-gradient) !important;
                color: white !important;
                box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3);
            }
            .stTabs [data-baseweb="tab"]:hover {
                color: var(--text-primary) !important;
            }
            .stTabs [data-baseweb="tab-highlight"] { display: none; }
            .stTabs [data-baseweb="tab-border"] { display: none; }

            .course-card {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 16px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
                box-shadow: 0 2px 12px var(--shadow-color);
            }
            .course-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 12px 40px rgba(108, 99, 255, 0.12);
                border-color: rgba(108, 99, 255, 0.2);
            }
            .course-card::before {
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 3px;
                background: var(--accent-gradient);
                border-radius: 16px 16px 0 0;
            }
            .course-card .card-title {
                font-size: 1.2em;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 8px;
            }
            .course-card .card-meta {
                color: var(--text-secondary);
                font-size: 0.9em;
                margin-bottom: 4px;
            }
            .course-card .card-badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.8em;
                font-weight: 600;
                margin-right: 8px;
                margin-top: 8px;
            }
            .badge-duration { background: rgba(108, 99, 255, 0.1); color: #6c63ff; }
            .badge-rating { background: rgba(243, 156, 18, 0.1); color: #f39c12; }
            .badge-author { background: rgba(0, 184, 148, 0.1); color: #00b894; }

            .metric-card {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 16px;
                padding: 28px;
                text-align: center;
                box-shadow: 0 2px 12px var(--shadow-color);
                transition: all 0.3s ease;
            }
            .metric-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 30px var(--shadow-color);
            }
            .metric-icon { font-size: 2.5em; margin-bottom: 8px; }
            .metric-value {
                font-size: 2.2em;
                font-weight: 800;
                background: var(--accent-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .metric-label {
                color: var(--text-secondary);
                font-size: 0.95em;
                font-weight: 500;
                margin-top: 4px;
            }

            .stButton > button {
                background: var(--accent-gradient) !important;
                color: white !important;
                border: none !important;
                border-radius: 12px !important;
                font-weight: 600 !important;
                padding: 12px 32px !important;
                font-size: 1em !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 15px rgba(108, 99, 255, 0.2) !important;
            }
            .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 25px rgba(108, 99, 255, 0.35) !important;
            }

            .stTextInput > div > div > input,
            .stNumberInput > div > div > input,
            .stSelectbox > div > div {
                background: var(--bg-primary) !important;
                border: 1px solid var(--border-color) !important;
                color: var(--text-primary) !important;
                border-radius: 12px !important;
                font-family: 'Inter', sans-serif !important;
            }
            .stTextInput > div > div > input:focus,
            .stNumberInput > div > div > input:focus {
                border-color: var(--accent-primary) !important;
                box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.15) !important;
            }

            hr { border-color: var(--border-color) !important; }
            .stDataFrame { border-radius: 12px; overflow: hidden; }
            .stAlert { border-radius: 12px !important; }

            .header-bar {
                background: linear-gradient(135deg, #6c63ff 0%, #e94560 50%, #6c63ff 100%);
                background-size: 200% 200%;
                animation: gradient-shift 6s ease infinite;
                padding: 32px 40px;
                border-radius: 20px;
                margin-bottom: 32px;
                position: relative;
                overflow: hidden;
                box-shadow: 0 8px 32px rgba(108, 99, 255, 0.25);
            }
            .header-bar::after {
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0,0,0,0.1);
                border-radius: 20px;
            }
            .header-bar h1 {
                color: white !important;
                font-size: 2em;
                font-weight: 800;
                margin: 0;
                position: relative; z-index: 1;
            }
            .header-bar p {
                color: rgba(255,255,255,0.9);
                font-size: 1.1em;
                margin: 4px 0 0 0;
                position: relative; z-index: 1;
            }
            @keyframes gradient-shift {
                0%   { background-position: 0% 50%; }
                50%  { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            .stars { color: var(--star-color); font-size: 1.1em; letter-spacing: 2px; }

            .empty-state {
                text-align: center; padding: 60px 20px; color: var(--text-muted);
            }
            .empty-state .icon { font-size: 4em; margin-bottom: 16px; }
            .empty-state .title {
                font-size: 1.4em; font-weight: 600; color: var(--text-secondary); margin-bottom: 8px;
            }

            .form-card {
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 20px;
                padding: 32px;
                box-shadow: 0 2px 12px var(--shadow-color);
            }

            .sidebar-section {
                background: rgba(108, 99, 255, 0.05);
                border: 1px solid rgba(108, 99, 255, 0.1);
                border-radius: 12px;
                padding: 16px;
                margin-bottom: 16px;
            }
            .sidebar-title {
                font-weight: 700; font-size: 0.85em;
                text-transform: uppercase; letter-spacing: 1.5px;
                color: var(--text-secondary); margin-bottom: 12px;
            }

            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """


# ──────────────────────────────────────────────
# Хелперы
# ──────────────────────────────────────────────
def render_stars(rating: float) -> str:
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + ("½" if half else "") + "☆" * empty


def render_course_card(course: dict, show_id: bool = False) -> str:
    stars = render_stars(course.get("rating", 0))
    id_badge = f'<span class="card-badge" style="background:rgba(233,69,96,0.12);color:#e94560;">ID: {course["id"]}</span>' if show_id else ""
    return f"""<div class="course-card">
<div class="card-title">{course["name"]}</div>
<div class="card-meta">👤 {course["author"]}</div>
<div class="stars">{stars}</div>
<div>
{id_badge}
<span class="card-badge badge-duration">⏱ {course["duration"]} ч</span>
<span class="card-badge badge-rating">⭐ {course["rating"]}</span>
<span class="card-badge badge-author">✍ {course["author"]}</span>
</div>
</div>"""


def render_metric_card(icon: str, value: str, label: str) -> str:
    return f"""<div class="metric-card">
<div class="metric-icon">{icon}</div>
<div class="metric-value">{value}</div>
<div class="metric-label">{label}</div>
</div>"""


def fetch_courses() -> list:
    try:
        res = requests.get(f"{BACKEND_URL}/courses", timeout=10)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None


# ──────────────────────────────────────────────
# Inject CSS
# ──────────────────────────────────────────────
st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 Learning Platform")
    st.markdown("---")

    # ── Тема ──
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">🎨 Оформление</div>', unsafe_allow_html=True)
    theme_label = "🌙 Тёмная тема" if st.session_state.theme == "dark" else "☀️ Светлая тема"
    if st.button(theme_label, key="theme_toggle", use_container_width=True):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Роль ──
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">👤 Режим просмотра</div>', unsafe_allow_html=True)
    role = st.radio(
        "Роль",
        options=["admin", "user"],
        format_func=lambda x: "🛡️ Администратор" if x == "admin" else "👁️ Пользователь",
        index=0 if st.session_state.role == "admin" else 1,
        key="role_radio",
        label_visibility="collapsed",
    )
    if role != st.session_state.role:
        st.session_state.role = role
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Статус Backend ──
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">⚡ Статус системы</div>', unsafe_allow_html=True)
    try:
        r = requests.get(f"{BACKEND_URL}/", timeout=5)
        if r.status_code == 200:
            st.success("Backend: онлайн ✅")
        else:
            st.warning(f"Backend: {r.status_code}")
    except Exception:
        st.error("Backend: оффлайн ❌")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("v2.0 • Built with Streamlit")


# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
role_text = "Администратор" if st.session_state.role == "admin" else "Пользователь"
st.markdown(
    f"""
    <div class="header-bar">
        <h1>🎓 Learning Platform</h1>
        <p>Каталог онлайн-курсов • Режим: {role_text}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# Tabs
# ──────────────────────────────────────────────
if st.session_state.role == "admin":
    tab_courses, tab_add, tab_analytics = st.tabs([
        "📋 Список курсов",
        "➕ Добавить курс",
        "📊 Аналитика",
    ])
else:
    tab_courses, tab_analytics = st.tabs([
        "📋 Каталог курсов",
        "📊 Статистика",
    ])
    tab_add = None

# ──────────────────────────────────────────────
# TAB 1 — Список курсов
# ──────────────────────────────────────────────
with tab_courses:
    data = fetch_courses()

    if data is None:
        st.error(f"❌ Не удалось подключиться к Backend ({BACKEND_URL})")
    elif len(data) == 0:
        st.markdown(
            """
            <div class="empty-state">
                <div class="icon">📭</div>
                <div class="title">Курсов пока нет</div>
                <div>Добавьте первый курс, чтобы начать!</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # ── Поиск и фильтры ──
        col_search, col_sort = st.columns([3, 1])
        with col_search:
            search = st.text_input("🔍 Поиск по названию или автору", key="search", label_visibility="collapsed",
                                   placeholder="🔍 Поиск по названию или автору...")
        with col_sort:
            sort_by = st.selectbox(
                "Сортировка",
                options=["По умолчанию", "По рейтингу ↓", "По рейтингу ↑", "По длительности ↓", "По длительности ↑", "По имени А-Я"],
                label_visibility="collapsed",
            )

        # Применяем фильтрацию
        filtered = data
        if search:
            search_lower = search.lower()
            filtered = [c for c in filtered if search_lower in c["name"].lower() or search_lower in c["author"].lower()]

        # Применяем сортировку
        if sort_by == "По рейтингу ↓":
            filtered = sorted(filtered, key=lambda x: x["rating"], reverse=True)
        elif sort_by == "По рейтингу ↑":
            filtered = sorted(filtered, key=lambda x: x["rating"])
        elif sort_by == "По длительности ↓":
            filtered = sorted(filtered, key=lambda x: x["duration"], reverse=True)
        elif sort_by == "По длительности ↑":
            filtered = sorted(filtered, key=lambda x: x["duration"])
        elif sort_by == "По имени А-Я":
            filtered = sorted(filtered, key=lambda x: x["name"])

        st.markdown(f"**Найдено курсов: {len(filtered)}**")
        st.markdown("")

        # ── Отрисовка карточек ──
        cols = st.columns(2)
        for i, course in enumerate(filtered):
            with cols[i % 2]:
                st.markdown(
                    render_course_card(course, show_id=(st.session_state.role == "admin")),
                    unsafe_allow_html=True,
                )

        # ── Удаление курса (только для админа) ──
        if st.session_state.role == "admin":
            st.markdown("---")
            st.subheader("🗑️ Удалить курс")
            col_del1, col_del2 = st.columns([3, 1])
            with col_del1:
                course_options = {f"ID {c['id']} — {c['name']}": c["id"] for c in data}
                selected_course = st.selectbox("Выберите курс для удаления", options=list(course_options.keys()), label_visibility="collapsed")
            with col_del2:
                if st.button("🗑️ Удалить", key="delete_btn", use_container_width=True):
                    course_id = course_options[selected_course]
                    try:
                        del_res = requests.delete(f"{BACKEND_URL}/courses/{course_id}", timeout=10)
                        if del_res.status_code == 200:
                            st.success(f"✅ Курс «{selected_course}» удалён!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(f"Ошибка: {del_res.json().get('detail', 'Unknown')}")
                    except Exception as e:
                        st.error(f"Ошибка: {e}")


# ──────────────────────────────────────────────
# TAB 2 — Добавить курс (только админ)
# ──────────────────────────────────────────────
if tab_add is not None:
    with tab_add:
        st.markdown("")

        col_form, col_preview = st.columns([1, 1])

        with col_form:
            st.markdown("### ✏️ Заполните информацию о курсе")
            st.markdown("")

            with st.form("course_form", clear_on_submit=True):
                name = st.text_input("📝 Название курса", placeholder="Введите название курса...")
                author = st.text_input("👤 Автор", placeholder="Имя автора...")
                duration = st.number_input("⏱ Длительность (часы)", min_value=0.5, max_value=1000.0, step=0.5, value=2.0)
                rating = st.slider("⭐ Рейтинг", min_value=1.0, max_value=5.0, step=0.5, value=4.0)

                st.markdown("")
                submitted = st.form_submit_button("🚀 Добавить курс", use_container_width=True)

                if submitted:
                    if not name or not author:
                        st.warning("⚠️ Заполните все поля!")
                    else:
                        try:
                            res = requests.post(
                                f"{BACKEND_URL}/courses",
                                json={"name": name, "duration": duration, "author": author, "rating": rating},
                                timeout=10,
                            )
                            if res.status_code == 200:
                                st.success(f"✅ Курс «{name}» успешно добавлен!")
                                st.balloons()
                            else:
                                st.error(f"Ошибка API: {res.status_code} — {res.text}")
                        except Exception as e:
                            st.error(f"❌ Не удалось подключиться к Backend: {e}")

        with col_preview:
            st.markdown("### 👁️ Предпросмотр карточки")
            st.markdown("")
            preview = {
                "id": "—",
                "name": name if 'name' in dir() and name else "Название курса",
                "author": author if 'author' in dir() and author else "Автор",
                "duration": duration if 'duration' in dir() else 2.0,
                "rating": rating if 'rating' in dir() else 4.0,
            }
            st.markdown(render_course_card(preview, show_id=False), unsafe_allow_html=True)
            st.caption("Так будет выглядеть карточка курса в каталоге")


# ──────────────────────────────────────────────
# TAB 3 — Аналитика
# ──────────────────────────────────────────────
with tab_analytics:
    data = fetch_courses()

    if data is None:
        st.error(f"❌ Не удалось подключиться к Backend")
    elif len(data) == 0:
        st.markdown(
            """
            <div class="empty-state">
                <div class="icon">📊</div>
                <div class="title">Нет данных для аналитики</div>
                <div>Добавьте курсы, чтобы видеть статистику</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        df = pd.DataFrame(data)
        df = df[["id", "name", "duration", "author", "rating"]]
        df.columns = ["ID", "Название", "Длительность (ч)", "Автор", "Рейтинг"]
        df["Длительность (ч)"] = pd.to_numeric(df["Длительность (ч)"], errors="coerce")
        df["Рейтинг"] = pd.to_numeric(df["Рейтинг"], errors="coerce")

        total_courses = len(df)
        avg_rating = df["Рейтинг"].mean()
        avg_duration = df["Длительность (ч)"].mean()
        total_hours = df["Длительность (ч)"].sum()

        # ── Метрики ──
        st.markdown("")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(render_metric_card("📚", str(total_courses), "Всего курсов"), unsafe_allow_html=True)
        with col2:
            st.markdown(render_metric_card("⭐", f"{avg_rating:.1f}", "Средний рейтинг"), unsafe_allow_html=True)
        with col3:
            st.markdown(render_metric_card("⏱", f"{avg_duration:.1f} ч", "Средняя длительность"), unsafe_allow_html=True)
        with col4:
            st.markdown(render_metric_card("🎯", f"{total_hours:.0f} ч", "Всего часов контента"), unsafe_allow_html=True)

        st.markdown("")
        st.markdown("---")

        # ── Графики ──
        is_dark = st.session_state.theme == "dark"
        plot_bg = "rgba(0,0,0,0)" if is_dark else "rgba(0,0,0,0)"
        paper_bg = "rgba(22,33,62,0.5)" if is_dark else "rgba(255,255,255,0.8)"
        text_color = "#e8e8f0" if is_dark else "#1a1a2e"
        grid_color = "rgba(108,99,255,0.1)" if is_dark else "rgba(0,0,0,0.05)"

        chart_layout = dict(
            plot_bgcolor=plot_bg,
            paper_bgcolor=paper_bg,
            font=dict(family="Inter", color=text_color),
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(gridcolor=grid_color),
            yaxis=dict(gridcolor=grid_color),
        )

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.markdown("#### 📊 Рейтинг курсов")
            fig_rating = px.bar(
                df.sort_values("Рейтинг", ascending=True),
                x="Рейтинг",
                y="Название",
                orientation="h",
                color="Рейтинг",
                color_continuous_scale=["#e94560", "#ffb347", "#6c63ff", "#00d2a0"],
            )
            fig_rating.update_layout(**chart_layout, showlegend=False, coloraxis_showscale=False, height=max(300, len(df) * 50))
            fig_rating.update_traces(marker_line_width=0, marker_cornerradius=6)
            st.plotly_chart(fig_rating, use_container_width=True)

        with col_chart2:
            st.markdown("#### ⏱ Длительность курсов")
            fig_duration = px.bar(
                df.sort_values("Длительность (ч)", ascending=True),
                x="Длительность (ч)",
                y="Название",
                orientation="h",
                color="Длительность (ч)",
                color_continuous_scale=["#6c63ff", "#e94560"],
            )
            fig_duration.update_layout(**chart_layout, showlegend=False, coloraxis_showscale=False, height=max(300, len(df) * 50))
            fig_duration.update_traces(marker_line_width=0, marker_cornerradius=6)
            st.plotly_chart(fig_duration, use_container_width=True)

        col_chart3, col_chart4 = st.columns(2)

        with col_chart3:
            st.markdown("#### 👤 Курсы по авторам")
            author_counts = df["Автор"].value_counts().reset_index()
            author_counts.columns = ["Автор", "Количество"]
            fig_authors = px.pie(
                author_counts,
                values="Количество",
                names="Автор",
                color_discrete_sequence=["#6c63ff", "#e94560", "#00d2a0", "#ffb347", "#3ec6e0", "#ff6b9d"],
                hole=0.45,
            )
            fig_authors.update_layout(**chart_layout, height=400)
            fig_authors.update_traces(
                textposition="inside",
                textinfo="label+percent",
                marker=dict(line=dict(color=paper_bg, width=2)),
            )
            st.plotly_chart(fig_authors, use_container_width=True)

        with col_chart4:
            st.markdown("#### 📈 Распределение рейтингов")
            fig_hist = px.histogram(
                df,
                x="Рейтинг",
                nbins=10,
                color_discrete_sequence=["#6c63ff"],
            )
            fig_hist.update_layout(**chart_layout, height=400, bargap=0.1)
            fig_hist.update_traces(marker_line_width=0, marker_cornerradius=6)
            st.plotly_chart(fig_hist, use_container_width=True)

        # ── Таблица данных (для админа) ──
        if st.session_state.role == "admin":
            st.markdown("---")
            st.markdown("#### 📋 Полная таблица данных")
            st.dataframe(
                df.style.format({"Рейтинг": "{:.1f}", "Длительность (ч)": "{:.1f}"}),
                use_container_width=True,
                hide_index=True,
            )
