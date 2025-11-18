# path: core/ui.py
from __future__ import annotations

import streamlit as st


def apply_base_config() -> None:
    """Configura la página y aplica todos los estilos globales (tema claro tipo Apple)."""
    st.set_page_config(
        page_title="Smart Form",
        page_icon="🧪",
        layout="wide",
    )
    _inject_global_css()


def _inject_global_css() -> None:
    """CSS global con estética tipo Apple / liquid glass en blanco."""
    st.markdown(
        """
        <style>
        :root {
            color-scheme: light;
        }

        /* --------- Fuente + layout base --------- */
        html, body, [class*="css"] {
            font-family: -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
        }

        body {
            background:
                radial-gradient(circle at 0 0, #ffffff 0, #f5f5f7 45%, #e5e7eb 100%);
        }

        .main .block-container {
            max-width: 1180px;
            padding-top: 2.4rem;
            padding-bottom: 3rem;
        }

        /* --------- Texto general --------- */
        .stMarkdown, .stText, .stSubheader, .stCaption {
            color: #111827;
        }

        /* --------- Sidebar (glass) --------- */
        section[data-testid="stSidebar"] {
            background: rgba(255,255,255,0.70);
            backdrop-filter: blur(26px);
            -webkit-backdrop-filter: blur(26px);
            border-right: 1px solid rgba(148,163,184,0.35);
            box-shadow: 0 0 30px rgba(15,23,42,0.08);
        }

        section[data-testid="stSidebar"] .stButton button {
            width: 100%;
        }

        /* --------- Hero principal (tarjeta grande) --------- */
        .sf-hero {
            padding: 1.8rem 2.0rem;
            border-radius: 26px;
            background: linear-gradient(135deg,#ffffff,#f5f5f7);
            border: 1px solid rgba(148,163,184,0.35);
            box-shadow:
                0 18px 40px rgba(15,23,42,0.16),
                0 0 0 0.5px rgba(148,163,184,0.4);
            margin-bottom: 1.8rem;
            position: relative;
            overflow: hidden;
        }

        .sf-hero::before {
            content: "";
            position: absolute;
            inset: -40%;
            background:
                radial-gradient(circle at 0 20%, rgba(59,130,246,0.18), transparent 60%),
                radial-gradient(circle at 90% 0, rgba(251,113,133,0.15), transparent 55%);
            opacity: 1;
            pointer-events: none;
        }

        .sf-hero-inner {
            position: relative;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .sf-hero-title {
            font-size: 2.1rem;
            font-weight: 700;
            letter-spacing: 0.01em;
            color: #111827;
        }

        .sf-hero-subtitle {
            font-size: 0.95rem;
            color: #4b5563;
            max-width: 40rem;
        }

        .sf-hero-badge {
            margin-top: 0.7rem;
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.28rem 0.95rem;
            border-radius: 999px;
            border: 1px solid rgba(59,130,246,0.4);
            background: rgba(255,255,255,0.8);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            color: #1d4ed8;
            font-size: 0.8rem;
        }

        .sf-hero-badge span:first-child {
            font-size: 1rem;
        }

        /* --------- Tabs tipo iOS segmentados --------- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.6rem;
            padding-bottom: 0.4rem;
            margin-bottom: 0.4rem;
            border-bottom: 1px solid rgba(209,213,219,0.9);
        }

        .stTabs [data-baseweb="tab"] {
            padding: 0.46rem 1.15rem;
            border-radius: 999px;
            border: 1px solid transparent;
            background: rgba(255,255,255,0.7);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            color: #374151;
            font-size: 0.88rem;
            line-height: 1.1;
            transition:
                background 0.18s ease-out,
                border-color 0.18s ease-out,
                box-shadow 0.18s ease-out,
                color 0.18s ease-out;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg,#ffffff,#e5f0ff);
            border-color: rgba(59,130,246,0.7);
            color: #111827;
            box-shadow: 0 10px 24px rgba(15,23,42,0.12);
        }

        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(249,250,251,0.9);
            border-color: rgba(209,213,219,0.9);
            box-shadow: 0 8px 18px rgba(15,23,42,0.10);
        }

        /* --------- Cards de inicio (glass) --------- */
        .sf-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-top: 0.8rem;
        }

        .sf-card {
            flex: 1 1 260px;
            background: rgba(255,255,255,0.78);
            border-radius: 22px;
            border: 1px solid rgba(209,213,219,0.9);
            box-shadow:
                0 16px 32px rgba(15,23,42,0.12),
                0 0 0 0.5px rgba(148,163,184,0.35);
            padding: 1.0rem 1.3rem 1.1rem;
            backdrop-filter: blur(26px);
            -webkit-backdrop-filter: blur(26px);
        }

        .sf-card-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: #111827;
            margin-bottom: 0.5rem;
        }

        .sf-card-row {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-top: 0.35rem;
        }

        .sf-card-label {
            font-size: 0.8rem;
            color: #6b7280;
        }

        .sf-card-value {
            font-size: 1.7rem;
            font-weight: 600;
            color: #111827;
        }

        .sf-card-ai {
            background: rgba(240,253,250,0.9);
            border-color: rgba(52,211,153,0.9);
        }

        .sf-card-ai-text {
            margin: 0.3rem 0 0;
            font-size: 0.88rem;
            color: #047857;
        }

        /* --------- Botones --------- */
        .stButton button {
            border-radius: 999px;
            border: 1px solid rgba(209,213,219,0.9);
            background: linear-gradient(135deg,#ffffff,#f9fafb);
            color: #111827;
            font-weight: 500;
            padding: 0.42rem 1.1rem;
            transition:
                background 0.16s ease-out,
                border-color 0.16s ease-out,
                box-shadow 0.16s ease-out,
                transform 0.1s ease-out;
        }

        .stButton button:hover {
            background: linear-gradient(135deg,#f9fafb,#edf2ff);
            border-color: rgba(59,130,246,0.7);
            box-shadow: 0 10px 22px rgba(15,23,42,0.18);
            transform: translateY(-0.5px);
        }

        .stButton button:active {
            box-shadow: 0 4px 10px rgba(15,23,42,0.18) inset;
            transform: translateY(0);
        }

        /* --------- Inputs / sliders --------- */
        .stNumberInput input {
            background: rgba(255,255,255,0.9);
            border-radius: 999px !important;
            border: 1px solid rgba(209,213,219,0.9);
            color: #111827;
        }

        .stNumberInput input:focus {
            outline: none !important;
            border-color: #007aff !important;
            box-shadow: 0 0 0 1px rgba(0,122,255,0.7);
        }

        .stSlider > div > div > div > div {
            background: linear-gradient(90deg,#3b82f6,#22c55e) !important;
        }

        /* --------- Expanders --------- */
        .streamlit-expander {
            border-radius: 20px !important;
            border: 1px solid rgba(209,213,219,0.9) !important;
            background: rgba(255,255,255,0.9) !important;
            box-shadow: 0 14px 30px rgba(15,23,42,0.10);
            margin-bottom: 0.9rem;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
        }

        .streamlit-expanderHeader {
            font-weight: 600 !important;
            color: #111827 !important;
        }

        /* --------- Alertas / métricas --------- */
        .stAlert, .stMetric {
            border-radius: 18px !important;
            background: rgba(255,255,255,0.95) !important;
            border: 1px solid rgba(209,213,219,0.9) !important;
            box-shadow: 0 12px 26px rgba(15,23,42,0.10);
        }

        /* --------- Dataframe (Historial) --------- */
        .stDataFrame {
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid rgba(209,213,219,0.9);
            box-shadow: 0 12px 26px rgba(15,23,42,0.10);
            background: rgba(255,255,255,0.9);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    """Hero de la parte superior (título + subtítulo + badge)."""
    st.markdown(
        """
        <div class="sf-hero">
          <div class="sf-hero-inner">
            <div class="sf-hero-title">Smart Form</div>
            <div class="sf-hero-subtitle">
              Practica Matemáticas, Física y Química con ejercicios interactivos,
              pistas y el modo PRUEBATE para mezclar todo.
            </div>
            <div class="sf-hero-badge">
              <span>🧪</span>
              <span>Modo estudio + examen con feedback inmediato</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home_cards(tol_pct: float, q: int, ai_text: str) -> None:
    """Cards del inicio con config actual y estado de IA."""
    st.markdown(
        f"""
        <div class="sf-grid">
          <div class="sf-card">
            <div class="sf-card-title">Configuración actual</div>
            <div class="sf-card-row">
              <span class="sf-card-label">Tolerancia</span>
              <span class="sf-card-value">{tol_pct:.1f}%</span>
            </div>
            <div class="sf-card-row">
              <span class="sf-card-label">Preguntas PRUEBATE</span>
              <span class="sf-card-value">{q}</span>
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


def render_sidebar(ai_on: bool, on_clear_history) -> None:
    """Sidebar con título, estado de IA y botón para borrar historial."""
    st.markdown("### 🧪 Smart Form")
    st.caption("Formulario interactivo para Matemáticas, Física y Química.")
    st.markdown("---")

    if ai_on:
        st.success("IA: activada (modo mixto local / modelos externos).")
    else:
        st.info("IA: solo modo local (sin modelos externos).")

    st.markdown("---")

    if st.button("🧹 Borrar historial"):
        on_clear_history()
        st.success("Historial borrado en esta sesión.")