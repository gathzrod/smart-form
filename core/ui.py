# path: core/ui.py
from __future__ import annotations

import streamlit as st


def apply_base_config() -> None:
    """Configura la página y aplica estilos globales."""
    st.set_page_config(page_title="Smart Form", page_icon="🧪", layout="wide")
    _inject_global_css()


def _inject_global_css() -> None:
    st.markdown(
        """
        <style>
        /* --------- Variables "Apple-ish" --------- */
        :root {
            --sf-bg: #020617;
            --sf-bg-elevated: rgba(15,23,42,0.96);
            --sf-border-subtle: rgba(148,163,184,0.35);
            --sf-border-strong: rgba(148,163,184,0.55);
            --sf-accent: #38bdf8;
            --sf-accent-soft: rgba(56,189,248,0.12);
            --sf-success: #22c55e;
            --sf-success-soft: rgba(34,197,94,0.13);
            --sf-text-main: #e5e7eb;
            --sf-text-dim: #9ca3af;
        }

        /* --------- Fuente + layout base --------- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            background:
                radial-gradient(circle at 0% 0%, #020617 0, #000000 45%, #020617 100%);
        }

        .main .block-container {
            max-width: 1200px;
            padding-top: 2.4rem;
            padding-bottom: 3rem;
        }

        /* --------- Hero principal tipo tarjeta de sistema --------- */
        .sf-hero {
            padding: 1.9rem 2rem;
            border-radius: 26px;
            background: linear-gradient(135deg,
                        rgba(15,23,42,0.96),
                        rgba(15,23,42,0.94));
            border: 1px solid var(--sf-border-subtle);
            box-shadow:
                0 24px 60px rgba(15,23,42,0.95),
                0 0 0 1px rgba(15,23,42,0.9);
            margin-bottom: 2.0rem;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(22px);
        }

        .sf-hero::before {
            content: "";
            position: absolute;
            inset: -40%;
            background:
                radial-gradient(circle at 0 0, rgba(56,189,248,0.26), transparent 60%),
                radial-gradient(circle at 80% 0, rgba(129,140,248,0.24), transparent 55%);
            opacity: 0.75;
            pointer-events: none;
            mix-blend-mode: screen;
        }

        .sf-hero-inner {
            position: relative;
            z-index: 2;
        }

        .sf-hero-title {
            font-size: 2.15rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            background: linear-gradient(90deg,#f9fafb,#e5e7eb,#c7d2fe);
            -webkit-background-clip: text;
            color: transparent;
        }

        .sf-hero-subtitle {
            margin-top: 0.45rem;
            font-size: 0.98rem;
            color: var(--sf-text-main);
            opacity: 0.95;
            max-width: 620px;
        }

        .sf-hero-row {
            margin-top: 1.2rem;
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            align-items: center;
        }

        .sf-hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.26rem 0.9rem;
            border-radius: 999px;
            border: 1px solid rgba(148,163,184,0.7);
            background: linear-gradient(120deg,
                        rgba(15,23,42,0.85),
                        rgba(15,23,42,0.9));
            color: var(--sf-text-main);
            font-size: 0.8rem;
        }

        .sf-hero-dot {
            width: 8px;
            height: 8px;
            border-radius: 999px;
            background: var(--sf-success);
            box-shadow: 0 0 0 4px var(--sf-success-soft);
        }

        .sf-hero-pill {
            display:inline-flex;
            align-items:center;
            gap:0.35rem;
            padding:0.24rem 0.8rem;
            border-radius:999px;
            border:1px solid var(--sf-border-subtle);
            background:rgba(15,23,42,0.9);
            color:var(--sf-text-dim);
            font-size:0.78rem;
        }

        /* --------- Sidebar --------- */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg,#020617,#020617);
            border-right: 1px solid var(--sf-border-subtle);
        }

        section[data-testid="stSidebar"] .stMarkdown p {
            font-size: 0.9rem;
        }

        section[data-testid="stSidebar"] .stButton button {
            width: 100%;
        }

        /* --------- Tabs (tipo segmented control) --------- */
        .stTabs {
            margin-top: 0.2rem !important;  /* separamos del hero */
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.55rem;
            padding: 0.35rem;
            margin-bottom: 0.4rem;
            border-radius: 999px;
            background: rgba(15,23,42,0.9);
            border: 1px solid rgba(31,41,55,0.95);
            position: relative;
            z-index: 3;  /* por encima del hero */
        }

        .stTabs [data-baseweb="tab"] {
            padding: 0.3rem 1.25rem;
            border-radius: 999px;
            border: none;
            background: transparent;
            color: var(--sf-text-dim);
            font-size: 0.88rem;
            font-weight: 500;
            transition:
                background 0.14s ease-out,
                color 0.14s ease-out,
                transform 0.12s ease-out,
                box-shadow 0.12s ease-out;
            position: relative;
        }

        .stTabs [data-baseweb="tab"]::after {
            content: "";
            position: absolute;
            inset: 0;
            border-radius: 999px;
            border: 1px solid transparent;
            transition: border-color 0.16s ease-out;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg,#0f172a,#020617);
            color: #f9fafb;
            box-shadow: 0 10px 26px rgba(15,23,42,0.9);
            transform: translateY(-1px);
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"]::after {
            border-color: rgba(148,163,184,0.65);
        }

        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(15,23,42,0.9);
            color: #e5e7eb;
        }

        /* --------- Botones --------- */
        .stButton button {
            border-radius: 999px;
            border: 1px solid var(--sf-border-strong);
            background: linear-gradient(135deg,#0ea5e9,#38bdf8);
            color: #f9fafb;
            font-weight: 500;
            padding: 0.42rem 1.35rem;
            transition:
                transform 0.11s ease-out,
                box-shadow 0.11s ease-out,
                background 0.18s ease-out,
                border-color 0.18s ease-out;
            cursor: pointer;
        }

        .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 24px rgba(15,23,42,0.95);
            background: linear-gradient(135deg,#38bdf8,#0ea5e9);
            border-color: rgba(191,219,254,0.85);
        }

        .stButton button:active {
            transform: translateY(0);
            box-shadow: 0 4px 14px rgba(15,23,42,1);
        }

        /* --------- Inputs / sliders --------- */
        input, textarea {
            border-radius: 999px !important;
        }

        .stNumberInput input {
            background: rgba(15,23,42,0.96);
            border-radius: 999px !important;
            border: 1px solid var(--sf-border-strong);
            color: var(--sf-text-main);
        }

        .stNumberInput input:focus {
            outline: none !important;
            border-color: var(--sf-accent) !important;
            box-shadow: 0 0 0 1px rgba(56,189,248,0.8);
        }

        .stSlider > div > div > div > div {
            background: linear-gradient(90deg,#0ea5e9,#22c55e) !important;
        }

        /* --------- Expanders --------- */
        .streamlit-expander {
            border-radius: 18px !important;
            border: 1px solid var(--sf-border-subtle) !important;
            background: rgba(15,23,42,0.98) !important;
            box-shadow: 0 18px 40px rgba(15,23,42,0.95);
            margin-bottom: 0.9rem;
        }

        .streamlit-expanderHeader {
            font-weight: 600 !important;
        }

        /* --------- Métricas / alerts --------- */
        .stMetric, .stAlert {
            border-radius: 16px !important;
            background: rgba(15,23,42,0.98) !important;
            border: 1px solid var(--sf-border-strong) !important;
        }

        /* --------- Cards personalizadas (Inicio) --------- */
        .sf-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-top: 0.9rem;
        }

        .sf-card {
            flex: 1 1 260px;
            background: var(--sf-bg-elevated);
            border-radius: 20px;
            border: 1px solid var(--sf-border-strong);
            padding: 1rem 1.2rem 0.9rem;
            box-shadow: 0 16px 40px rgba(15,23,42,0.95);
        }

        .sf-card-title {
            font-size: 0.98rem;
            font-weight: 600;
            margin-bottom: 0.3rem;
            color: var(--sf-text-main);
        }

        .sf-card-row {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-top: 0.45rem;
        }

        .sf-card-label {
            font-size: 0.8rem;
            color: var(--sf-text-dim);
        }

        .sf-card-value {
            font-size: 1.6rem;
            font-weight: 600;
            color: #f9fafb;
        }

        .sf-card-ai {
            background: linear-gradient(135deg,
                        rgba(22,163,74,0.23),
                        rgba(5,46,22,0.95));
            border-color: rgba(74,222,128,0.9);
        }

        .sf-card-ai-text {
            margin: 0.45rem 0 0;
            font-size: 0.9rem;
            color: #dcfce7;
        }

        /* --------- Historial tabla --------- */
        [data-testid="stDataFrame"] {
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid var(--sf-border-subtle);
            box-shadow: 0 16px 40px rgba(15,23,42,0.95);
        }

        /* --------- Responsivo --------- */
        @media (max-width: 768px) {
            .main .block-container {
                padding-top: 1.4rem;
            }
            .sf-hero {
                padding: 1.4rem 1.3rem;
                margin-bottom: 1.6rem;
            }
            .sf-hero-title {
                font-size: 1.7rem;
            }
            .sf-grid {
                flex-direction: column;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    """Hero principal de la app."""
    st.markdown(
        """
        <div class="sf-hero">
          <div class="sf-hero-inner">
            <div class="sf-hero-title">Smart Form</div>
            <div class="sf-hero-subtitle">
              Practica Matemáticas, Física y Química con ejercicios interactivos,
              pistas puntuales y el modo PRUEBATE para simular un examen mixto.
            </div>
            <div class="sf-hero-row">
              <div class="sf-hero-badge">
                <span class="sf-hero-dot"></span>
                Sesión activa · Progreso en tiempo real
              </div>
              <div class="sf-hero-pill">
                🧪 Diseñado para Ingeniería Física
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home_cards(tol_pct: float, q: int, ai_text: str) -> None:
    """Tarjetas de la pestaña Inicio con config y estado de IA."""
    st.markdown(
        f"""
        <div class="sf-grid">
          <div class="sf-card">
            <div class="sf-card-title">Configuración actual</div>
            <div class="sf-card-body">
              <div class="sf-card-row">
                <span class="sf-card-label">Tolerancia</span>
                <span class="sf-card-value">{tol_pct:.1f}%</span>
              </div>
              <div class="sf-card-row">
                <span class="sf-card-label">Preguntas PRUEBATE</span>
                <span class="sf-card-value">{q}</span>
              </div>
            </div>
          </div>
          <div class="sf-card sf-card-ai">
            <div class="sf-card-title">Estado de IA</div>
            <p class="sf-card-ai-text">{ai_text}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )