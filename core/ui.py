# path: core/ui.py
from __future__ import annotations

import streamlit as st


def apply_base_config() -> None:
    """Configura la página y aplica todos los estilos globales."""
    st.set_page_config(
        page_title="Smart Form",
        page_icon="🧪",
        layout="wide",
    )
    _inject_global_css()


def _inject_global_css() -> None:
    """CSS global con estética tipo Apple: limpio, sutil y sin animaciones estridentes."""
    st.markdown(
        """
        <style>
        :root {
            color-scheme: dark;
        }

        /* --------- Fuente + layout base --------- */
        html, body, [class*="css"] {
            font-family: -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
        }

        body {
            background: radial-gradient(circle at 0 0, #020617 0, #020617 45%, #000000 100%);
        }

        .main .block-container {
            max-width: 1180px;
            padding-top: 2.4rem;
            padding-bottom: 3rem;
        }

        /* --------- Sidebar --------- */
        section[data-testid="stSidebar"] {
            background: #020617;
            border-right: 1px solid rgba(148,163,184,0.35);
        }

        section[data-testid="stSidebar"] .stButton button {
            width: 100%;
        }

        /* --------- Hero principal --------- */
        .sf-hero {
            padding: 1.8rem 2.0rem;
            border-radius: 24px;
            background: linear-gradient(120deg, #0f172a, #020617);
            border: 1px solid rgba(148,163,184,0.55);
            box-shadow: 0 18px 40px rgba(15,23,42,0.9);
            margin-bottom: 1.8rem;
            position: relative;
            overflow: hidden;
        }

        .sf-hero::before {
            content: "";
            position: absolute;
            inset: -40%;
            background:
                radial-gradient(circle at 0 20%, rgba(96,165,250,0.25), transparent 60%),
                radial-gradient(circle at 90% 0, rgba(251,113,133,0.22), transparent 55%);
            opacity: 0.9;
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
            color: #f9fafb;
        }

        .sf-hero-subtitle {
            font-size: 0.95rem;
            color: #cbd5f5;
            max-width: 38rem;
        }

        .sf-hero-badge {
            margin-top: 0.6rem;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.26rem 0.9rem;
            border-radius: 999px;
            border: 1px solid rgba(96,165,250,0.9);
            background: rgba(15,23,42,0.92);
            color: #e5f0ff;
            font-size: 0.8rem;
        }

        .sf-hero-badge span {
            font-size: 1rem;
        }

        /* --------- Tabs (segmentados estilo iPad) --------- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.7rem;
            padding-bottom: 0.4rem;
            border-bottom: 1px solid rgba(55,65,81,0.7);
            margin-bottom: 0.4rem;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 0.46rem 1.15rem;
            border-radius: 999px;
            border: 1px solid transparent;
            background: rgba(15,23,42,0.8);
            color: #e5e7eb;
            font-size: 0.88rem;
            line-height: 1.1;
            transition:
                background 0.18s ease-out,
                border-color 0.18s ease-out,
                box-shadow 0.18s ease-out;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg,#2563eb,#1d4ed8);
            border-color: rgba(129,140,248,0.9);
            color: #f9fafb;
            box-shadow: 0 10px 24px rgba(15,23,42,0.9);
        }

        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(31,41,55,0.9);
            border-color: rgba(148,163,184,0.7);
            box-shadow: 0 8px 18px rgba(15,23,42,0.9);
        }

        /* --------- Texto general --------- */
        .stMarkdown, .stText, .stSubheader, .stCaption {
            color: #e5e7eb;
        }

        /* --------- Cards de inicio --------- */
        .sf-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-top: 0.8rem;
        }

        .sf-card {
            flex: 1 1 260px;
            background: radial-gradient(circle at 0 0,#020617,#020617);
            border-radius: 20px;
            border: 1px solid rgba(55,65,81,0.9);
            padding: 1.0rem 1.3rem 1.1rem;
            box-shadow: 0 14px 30px rgba(15,23,42,0.95);
        }

        .sf-card-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: #e5e7eb;
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
            color: #9ca3af;
        }

        .sf-card-value {
            font-size: 1.7rem;
            font-weight: 600;
            color: #f9fafb;
        }

        .sf-card-ai {
            background: radial-gradient(circle at 0 0,#022c22,#052e16);
            border-color: rgba(22,163,74,0.9);
        }

        .sf-card-ai-text {
            margin: 0.3rem 0 0;
            font-size: 0.88rem;
            color: #bbf7d0;
        }

        /* --------- Botones --------- */
        .stButton button {
            border-radius: 999px;
            border: 1px solid rgba(148,163,184,0.7);
            background: linear-gradient(135deg,#111827,#020617);
            color: #e5e7eb;
            font-weight: 500;
            padding: 0.42rem 1.1rem;
            transition:
                background 0.16s ease-out,
                border-color 0.16s ease-out,
                box-shadow 0.16s ease-out;
        }

        .stButton button:hover {
            background: linear-gradient(135deg,#1f2937,#020617);
            border-color: rgba(129,140,248,0.9);
            box-shadow: 0 10px 22px rgba(15,23,42,1);
        }

        .stButton button:active {
            box-shadow: 0 4px 12px rgba(15,23,42,1) inset;
        }

        /* --------- Inputs / sliders --------- */
        .stNumberInput input {
            background: rgba(15,23,42,0.95);
            border-radius: 999px !important;
            border: 1px solid rgba(55,65,81,0.9);
            color: #e5e7eb;
        }

        .stNumberInput input:focus {
            outline: none !important;
            border-color: rgba(129,140,248,0.95) !important;
            box-shadow: 0 0 0 1px rgba(129,140,248,0.9);
        }

        .stSlider > div > div > div > div {
            background: linear-gradient(90deg,#2563eb,#22c55e) !important;
        }

        /* --------- Expanders --------- */
        .streamlit-expander {
            border-radius: 18px !important;
            border: 1px solid rgba(55,65,81,0.9) !important;
            background: rgba(15,23,42,0.97) !important;
            box-shadow: 0 14px 30px rgba(15,23,42,0.95);
            margin-bottom: 0.9rem;
        }

        .streamlit-expanderHeader {
            font-weight: 600 !important;
        }

        /* --------- Alertas / métricas --------- */
        .stAlert, .stMetric {
            border-radius: 16px !important;
            background: rgba(15,23,42,0.97) !important;
            border: 1px solid rgba(55,65,81,0.9) !important;
        }

        /* --------- Dataframe (Historial) --------- */
        .stDataFrame {
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid rgba(55,65,81,0.9);
            box-shadow: 0 12px 26px rgba(15,23,42,0.95);
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