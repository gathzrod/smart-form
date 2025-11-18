# path: app.py
from __future__ import annotations

import math
import random

import streamlit as st

from core.utils import (
    within_tol,
    add_history,
    get_history_df,
    history_to_csv,
    clear_history,
    Topic,
)
from core.topics_phys import PHYS_TOPICS
from core.topics_chem import CHM_TOPICS
from core.ai import ask_ai, has_ai

# =========================================================
#  FALLBACK DE MATEMÁTICAS (por si el módulo importado está incompleto)
# =========================================================

try:
    from core.topics_math import MATH_TOPICS as IMPORTED_MATH_TOPICS
except Exception:
    IMPORTED_MATH_TOPICS = []


def default_math_topics() -> list[Topic]:
    """Fallback con 4 temas de Matemáticas (lineal, cuadrática, Pitágoras, pendiente)."""

    # ---- Lineal ----
    def m_lineal_explain() -> str:
        return (
            "Ecuación lineal en una variable:\n"
            "  a·x + b = 0 con a ≠ 0.\n\n"
            "La idea es dejar a x sola:\n"
            "  a·x + b = 0 → a·x = -b → x = -b / a.\n"
            "Ojo con los signos y con no dividir entre cero."
        )

    def m_lineal_example() -> tuple[str, str]:
        a, b = 2, -6
        x = -(b) / a
        enun = "Ejemplo: resuelve 2x - 6 = 0."
        sol = (
            "2x - 6 = 0 → 2x = 6 → x = 6/2 = 3.\n\n"
            f"Resultado numérico: x = {x:.3f}."
        )
        return enun, sol

    def m_lineal_exercise() -> tuple[str, float, str, str]:
        variants = [(3, 9), (-4, 8), (7, -21), (5, -10), (-6, 18), (9, -27)]
        a, b = random.choice(variants)
        expected = -(b) / a
        enun = f"Resuelve la ecuación {a}x {b:+d} = 0. Ingresa el valor de x."
        unit = ""
        hint = "Pasa el término independiente al otro lado y divide entre a."
        return enun, expected, unit, hint

    # ---- Cuadrática ----
    def m_quad_explain() -> str:
        return (
            "Ecuación cuadrática:\n"
            "  a·x² + b·x + c = 0 (a ≠ 0).\n\n"
            "Se resuelve con la fórmula general:\n"
            "  x = [-b ± √(b² - 4ac)] / (2a).\n"
            "Al término b² - 4ac se le llama discriminante D."
        )

    def m_quad_example() -> tuple[str, str]:
        a, b, c = 1, -3, 2
        D = b * b - 4 * a * c
        x1 = (-b - math.sqrt(D)) / (2 * a)
        x2 = (-b + math.sqrt(D)) / (2 * a)
        enun = "Ejemplo: resuelve x² - 3x + 2 = 0."
        sol = (
            "a = 1, b = -3, c = 2.\n"
            "D = b² - 4ac = 9 - 8 = 1.\n"
            "x = [3 ± √1]/2 → x1 = 1, x2 = 2.\n\n"
            f"x1 = {x1:.3f}, x2 = {x2:.3f}."
        )
        return enun, sol

    def m_quad_exercise() -> tuple[str, float, str, str]:
        presets = [(1, -5, 6), (2, 5, -3), (1, -4, 3), (1, -2, -8)]
        a, b, c = random.choice(presets)
        D = float(b * b - 4 * a * c)
        if D < 0:
            D = 0.0
        xs = (-b - math.sqrt(D)) / (2.0 * a)
        enun = (
            f"Resuelve {a}x² {b:+d}x {c:+d} = 0 y escribe la raíz más pequeña (xₘᵢₙ)."
        )
        unit = ""
        hint = "Usa la fórmula general y quédate con la raíz del signo menos."
        return enun, xs, unit, hint

    # ---- Pitágoras ----
    def m_pitagoras_explain() -> str:
        return (
            "En un triángulo rectángulo se cumple:\n"
            "  c² = a² + b².\n\n"
            "Si conoces los catetos a y b, la hipotenusa es:\n"
            "  c = √(a² + b²)."
        )

    def m_pitagoras_example() -> tuple[str, str]:
        a, b = 6, 8
        c = math.sqrt(a * a + b * b)
        enun = "Ejemplo: catetos 6 y 8. Calcula la hipotenusa."
        sol = (
            "c = √(6² + 8²) = √(36 + 64) = √100 = 10.\n\n"
            f"Resultado numérico: c = {c:.3f}."
        )
        return enun, sol

    def m_pitagoras_exercise() -> tuple[str, float, str, str]:
        variants = [(3, 4), (5, 12), (7, 24), (9, 40), (8, 15), (12, 16)]
        a, b = random.choice(variants)
        c = math.sqrt(a * a + b * b)
        enun = (
            f"En un triángulo rectángulo, a = {a} y b = {b}. "
            "Calcula la hipotenusa c."
        )
        unit = ""
        hint = "Eleva cada cateto al cuadrado, suma y saca la raíz cuadrada."
        return enun, c, unit, hint

    # ---- Pendiente ----
    def m_slope_explain() -> str:
        return (
            "Pendiente de una recta que pasa por (x₁, y₁) y (x₂, y₂):\n"
            "  m = (y₂ - y₁) / (x₂ - x₁), con x₂ ≠ x₁."
        )

    def m_slope_example() -> tuple[str, str]:
        x1, y1, x2, y2 = 1, 2, 5, 10
        m = (y2 - y1) / (x2 - x1)
        enun = "Ejemplo: pendiente de la recta que pasa por (1, 2) y (5, 10)."
        sol = (
            "Δy = 10 - 2 = 8, Δx = 5 - 1 = 4.\n"
            "m = Δy / Δx = 8 / 4 = 2.\n\n"
            f"Resultado numérico: m = {m:.3f}."
        )
        return enun, sol

    def m_slope_exercise() -> tuple[str, float, str, str]:
        sets = [
            (0, 0, 4, 6),
            (-2, 3, 1, 12),
            (2, -1, 8, 5),
            (-3, -2, 4, 7),
            (1, 5, 7, 17),
        ]
        x1, y1, x2, y2 = random.choice(sets)
        m = (y2 - y1) / (x2 - x1)
        enun = (
            f"Calcula la pendiente m de la recta que pasa por "
            f"({x1}, {y1}) y ({x2}, {y2})."
        )
        unit = ""
        hint = "Resta primero las y, luego las x y divide: m = Δy / Δx."
        return enun, m, unit, hint

    return [
        Topic(
            area="Matemáticas",
            name="Ecuación lineal (ax + b = 0)",
            explain=m_lineal_explain,
            example=m_lineal_example,
            exercise=m_lineal_exercise,
        ),
        Topic(
            area="Matemáticas",
            name="Ecuación cuadrática",
            explain=m_quad_explain,
            example=m_quad_example,
            exercise=m_quad_exercise,
        ),
        Topic(
            area="Matemáticas",
            name="Pitágoras (c² = a² + b²)",
            explain=m_pitagoras_explain,
            example=m_pitagoras_example,
            exercise=m_pitagoras_exercise,
        ),
        Topic(
            area="Matemáticas",
            name="Pendiente entre puntos",
            explain=m_slope_explain,
            example=m_slope_example,
            exercise=m_slope_exercise,
        ),
    ]


if IMPORTED_MATH_TOPICS and len(IMPORTED_MATH_TOPICS) > 1:
    MATH_TOPICS = list(IMPORTED_MATH_TOPICS)
else:
    MATH_TOPICS = default_math_topics()


# =========================================================
#  ESTADO GLOBAL
# =========================================================

def init_state() -> None:
    if "tol_pct" not in st.session_state:
        st.session_state.tol_pct = 0.05  # 5 %
    if "pruebate_q" not in st.session_state:
        st.session_state.pruebate_q = 8

    if "pruebate_active" not in st.session_state:
        st.session_state.pruebate_active = False
    if "pruebate_questions" not in st.session_state:
        st.session_state.pruebate_questions = []
    if "pruebate_idx" not in st.session_state:
        st.session_state.pruebate_idx = 0
    if "pruebate_correct" not in st.session_state:
        st.session_state.pruebate_correct = 0
    if "pruebate_misses" not in st.session_state:
        st.session_state.pruebate_misses = []


def get_or_init_exercise(topic: Topic) -> dict:
    """
    Devuelve un ejercicio fijo por tema (no cambia en cada rerun).
    Solo se regenera cuando el usuario pide "Nuevo ejercicio".
    """
    key = f"ex_{topic.area}_{topic.name}"
    if key not in st.session_state:
        enun, expected, unit, hint = topic.exercise()
        st.session_state[key] = {
            "enunciado": enun,
            "correcto": float(expected),
            "unit": unit,
            "hint": hint,
        }
    return st.session_state[key]


def reset_exercise(topic: Topic) -> None:
    key = f"ex_{topic.area}_{topic.name}"
    if key in st.session_state:
        del st.session_state[key]


# =========================================================
#  ESTILOS GLOBALES
# =========================================================

def inject_global_css() -> None:
    st.markdown(
        """
        <style>
        /* --------- Fuente + layout base --------- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            background:
                radial-gradient(circle at 0% 0%, #020617 0, #020617 40%, #020617 100%);
        }

        .main .block-container {
            max-width: 1200px;
            padding-top: 2.5rem;
            padding-bottom: 3rem;
        }

        /* --------- Animaciones suaves --------- */
        @keyframes sfGradientMove {
            0%   { background-position: 0%   50%; }
            50%  { background-position: 100% 50%; }
            100% { background-position: 0%   50%; }
        }

        @keyframes sfFadeInUp {
            0% {
                opacity: 0;
                transform: translateY(8px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .sf-fade {
            animation: sfFadeInUp 0.45s ease-out both;
        }

        /* --------- Hero principal con degradado animado --------- */
        .sf-hero {
            padding: 1.8rem 1.9rem;
            border-radius: 22px;
            background: linear-gradient(135deg,
                        rgba(15,23,42,0.98),
                        rgba(15,23,42,0.98));
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(148,163,184,0.55);
            box-shadow:
                0 22px 60px rgba(15,23,42,0.95),
                0 0 0 1px rgba(15,23,42,0.9);
        }

        .sf-hero::before {
            content: "";
            position: absolute;
            inset: -40%;
            background: radial-gradient(circle at 0% 0%,
                        rgba(56,189,248,0.28),
                        transparent 55%);
            opacity: 0.8;
            mix-blend-mode: screen;
            pointer-events: none;
            animation: sfGradientMove 18s ease-in-out infinite;
        }

        .sf-hero::after {
            content: "";
            position: absolute;
            inset: -40%;
            background: radial-gradient(circle at 100% 100%,
                        rgba(244,114,182,0.24),
                        transparent 55%);
            opacity: 0.8;
            mix-blend-mode: screen;
            pointer-events: none;
            animation: sfGradientMove 22s ease-in-out infinite;
        }

        .sf-hero-inner {
            position: relative;
            z-index: 1;
        }

        .sf-hero-title {
            font-size: 2.15rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            background: linear-gradient(90deg,#f9fafb,#e5e7eb,#a5b4fc,#f472b6,#facc15);
            -webkit-background-clip: text;
            color: transparent;
        }

        .sf-hero-subtitle {
            margin-top: 0.35rem;
            font-size: 0.98rem;
            color: #e5e7eb;
            opacity: 0.92;
        }

        .sf-hero-badge {
            margin-top: 0.95rem;
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.26rem 0.8rem;
            border-radius: 999px;
            border: 1px solid rgba(94,234,212,0.9);
            background: rgba(15,118,110,0.5);
            color: #ccfbf1;
            font-size: 0.78rem;
            box-shadow:
                0 0 0 1px rgba(15,23,42,0.85),
                0 10px 30px rgba(15,23,42,0.95);
        }

        /* --------- Sidebar --------- */
        section[data-testid="stSidebar"] {
            background: radial-gradient(circle at 0 0,#020617 0,#020617 70%,#020617 100%);
            border-right: 1px solid rgba(30,64,175,0.65);
        }

        section[data-testid="stSidebar"] .stButton button {
            width: 100%;
        }

        /* --------- Tabs --------- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.75rem;
            padding-bottom: 0.3rem;
            margin-top: 0.35rem;
            position: relative;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 0.45rem 1.25rem;
            border-radius: 999px;
            border: 1px solid rgba(148,163,184,0.35);
            background: radial-gradient(circle at 0 0, #020617, #020617);
            color: #e5e7eb;
            transition:
                transform 0.16s ease-out,
                box-shadow 0.16s ease-out,
                border-color 0.18s ease-out,
                background 0.18s ease-out;
            position: relative;
            overflow: visible;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            border-color: rgba(129,140,248,0.95);
            background: radial-gradient(circle at 0 0,#4338ca,#1d4ed8);
            box-shadow: 0 14px 34px rgba(15,23,42,0.95);
        }

        .stTabs [data-baseweb="tab"]:hover {
            transform: translateY(-1px);
            box-shadow: 0 12px 30px rgba(15,23,42,0.95);
            border-color: rgba(191,219,254,0.85);
        }

        .stTabs [data-baseweb="tab-list"]::after {
            content: "";
            position: absolute;
            left: 0;
            right: 0;
            bottom: -0.28rem;
            height: 2px;
            background: linear-gradient(90deg,#22c55e,#6366f1,#f97316);
            opacity: 0.55;
        }

        /* --------- Botones --------- */
        .stButton button {
            border-radius: 999px;
            border: 1px solid rgba(148,163,184,0.55);
            background: radial-gradient(circle at 0 0,#4f46e5,#1d4ed8);
            color: #f9fafb;
            font-weight: 500;
            padding: 0.42rem 1.3rem;
            transition:
                transform 0.11s ease-out,
                box-shadow 0.11s ease-out,
                background 0.20s ease-out,
                border-color 0.2s ease-out;
            cursor: pointer;
        }

        .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 12px 30px rgba(30,64,175,0.9);
            background: radial-gradient(circle at 0 0,#6366f1,#2563eb);
            border-color: rgba(191,219,254,0.85);
        }

        .stButton button:active {
            transform: translateY(0);
            box-shadow: 0 4px 12px rgba(15,23,42,1);
        }

        /* --------- Inputs / sliders --------- */
        input, textarea {
            border-radius: 999px !important;
        }

        .stNumberInput input {
            background: rgba(15,23,42,0.96);
            border-radius: 999px !important;
            border: 1px solid rgba(148,163,184,0.6);
        }

        .stNumberInput input:focus {
            outline: none !important;
            border-color: rgba(129,140,248,0.95) !important;
            box-shadow: 0 0 0 1px rgba(129,140,248,0.9);
        }

        .stSlider > div > div > div > div {
            background: linear-gradient(90deg,#4f46e5,#22c55e) !important;
        }

        /* --------- Expanders --------- */
        .streamlit-expander {
            border-radius: 18px !important;
            border: 1px solid rgba(148,163,184,0.45) !important;
            background: radial-gradient(circle at 0 0,
                        rgba(15,23,42,0.98),
                        rgba(15,23,42,0.96)) !important;
            box-shadow: 0 18px 45px rgba(15,23,42,0.9);
            margin-bottom: 1.0rem;
        }

        .streamlit-expanderHeader {
            font-weight: 600 !important;
        }

        /* --------- Métricas / alerts --------- */
        .stMetric, .stAlert {
            border-radius: 16px !important;
            background: rgba(15,23,42,0.97) !important;
            border: 1px solid rgba(148,163,184,0.55) !important;
        }

        /* --------- Cards (Inicio) --------- */
        .sf-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-top: 0.75rem;
        }

        .sf-card {
            flex: 1 1 260px;
            background: radial-gradient(circle at 0 0,
                        rgba(15,23,42,0.98),
                        rgba(15,23,42,0.97));
            border-radius: 18px;
            border: 1px solid rgba(148,163,184,0.55);
            padding: 1rem 1.2rem;
            box-shadow: 0 14px 36px rgba(15,23,42,0.9);
        }

        .sf-card-title {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 0.35rem;
            color: #e5e7eb;
        }

        .sf-card-row {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-top: 0.4rem;
        }

        .sf-card-label {
            font-size: 0.82rem;
            color: #9ca3af;
        }

        .sf-card-value {
            font-size: 1.7rem;
            font-weight: 600;
            color: #f9fafb;
        }

        .sf-card-ai {
            background: linear-gradient(135deg,
                        rgba(22,163,74,0.85),
                        rgba(5,46,22,0.96));
            border-color: rgba(74,222,128,0.85);
        }

        .sf-card-ai-text {
            margin: 0.4rem 0 0;
            font-size: 0.9rem;
            color: #dcfce7;
        }

        .sf-chip {
            display:inline-flex;
            align-items:center;
            gap:0.35rem;
            padding:0.22rem 0.7rem;
            border-radius:999px;
            border:1px solid rgba(52,211,153,0.95);
            background:rgba(22,101,52,0.4);
            font-size:0.8rem;
            color:#bbf7d0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
#  COMPONENTES DE UI
# =========================================================

def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("## 🧪 Smart Form")
        st.caption("Formulario interactivo para Matemáticas, Física y Química.")
        st.markdown("---")
        if has_ai():
            st.success("IA: activada (modo mixto local / modelos externos).")
        else:
            st.info("IA: solo modo local (sin modelos externos).")
        st.markdown("---")
        if st.button("🧹 Borrar historial"):
            clear_history()
            st.success("Historial borrado en esta sesión.")


def render_hero() -> None:
    st.markdown(
        """
        <div class="sf-hero sf-fade">
          <div class="sf-hero-inner">
            <div class="sf-hero-title">Smart Form</div>
            <div class="sf-hero-subtitle">
              Practica Matemáticas, Física y Química con ejercicios interactivos,
              pistas y modo PRUEBATE.
            </div>
            <div class="sf-hero-badge">
              🚀 Modo estudio + examen mixto · feedback inmediato
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home_tab() -> None:
    st.subheader("Bienvenido 👋")
    st.write(
        "Esta es la vista general de **Smart Form**. "
        "Aquí ves tu configuración y el estado de la IA antes de entrar a cada materia."
    )

    tol_pct = st.session_state.tol_pct * 100.0
    q = st.session_state.pruebate_q

    if has_ai():
        ai_text = "IA activada. Si un modelo externo falla, se usa explicación local."
    else:
        ai_text = "IA local: por ahora solo se usan explicaciones sin modelo externo."

    st.markdown(
        f"""
        <div class="sf-grid sf-fade">
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

    st.markdown("---")
    st.write(
        "Usa las pestañas de arriba para entrar a **Matemáticas, Física y Química**, "
        "y el modo **PRUEBATE** para un examen mixto. "
        "Cada intento se guarda en el historial para que puedas ver tu progreso."
    )


def render_topic_tab(area_code: str, area_name: str, icon: str, topics: list[Topic]) -> None:
    st.markdown(f"## {icon} {area_name}")

    topic_names = [t.name for t in topics]
    sel_topic_name = st.selectbox(
        f"Selecciona un tema de {area_name}",
        topic_names,
        key=f"select_{area_code}",
    )
    topic = topics[topic_names.index(sel_topic_name)]

    # Si cambias de tema, reiniciamos el ejercicio guardado para ese tema
    last_topic_key = f"last_topic_{area_code}"
    if st.session_state.get(last_topic_key) != sel_topic_name:
        st.session_state[last_topic_key] = sel_topic_name
        reset_exercise(topic)

    # ---------- Explicación ----------
    with st.expander("📘 Explicación del tema", expanded=True):
        st.write(topic.explain())
        if st.button("Pedir explicación IA del tema", key=f"{area_code}_ai_topic"):
            txt = ask_ai(
                topic=f"{area_name}: {topic.name}",
                prompt=topic.explain(),
                expected=None,
                unit="",
            )
            st.info(txt)

    # ---------- Ejemplo ----------
    with st.expander("🧪 Ejemplo resuelto", expanded=False):
        enun_ex, sol_ex = topic.example()
        st.write(enun_ex)
        if st.button("Mostrar solución del ejemplo", key=f"{area_code}_show_example"):
            st.success(sol_ex)

    # ---------- Ejercicio interactivo ----------
    with st.expander("📝 Ejercicio interactivo", expanded=False):
        ex_data = get_or_init_exercise(topic)
        enun_exe = ex_data["enunciado"]
        expected = float(ex_data["correcto"])
        unit = ex_data["unit"]
        hint = ex_data["hint"]

        st.write(enun_exe)
        user = st.number_input(
            f"Tu respuesta ({area_name})",
            value=0.0,
            step=0.1,
            format="%.6f",
            key=f"{area_code}_answer",
        )

        b1, b2, b3 = st.columns(3)

        with b1:
            if st.button(f"Corregir ({area_name})", key=f"{area_code}_check"):
                ok = within_tol(expected, float(user), st.session_state.tol_pct)
                add_history(
                    area=area_name,
                    tema=topic.name,
                    tipo="Ejercicio",
                    correcto=expected,
                    usuario=float(user),
                    acierto=ok,
                )
                if ok:
                    st.success(f"CORRECTO ✅ — Solución: {expected:.6f} {unit}")
                else:
                    st.error(f"INCORRECTO ❌ — Solución: {expected:.6f} {unit}")
                    st.caption("Pista: " + hint)

        with b2:
            if st.button(
                "Pedir explicación IA de este ejercicio",
                key=f"{area_code}_ai_exercise",
            ):
                prompt_ai = (
                    f"{enun_exe}\n"
                    f"La respuesta del alumno fue: {float(user):.6f} {unit} "
                    f"(el sistema conoce un valor de referencia para revisar)."
                )
                txt = ask_ai(
                    topic=f"{area_name}: {topic.name}",
                    prompt=prompt_ai,
                    expected=expected,
                    unit=unit,
                )
                st.info(txt)

        with b3:
            if st.button(
                "🔁 Nuevo ejercicio",
                key=f"{area_code}_new_exercise",
            ):
                reset_exercise(topic)
                st.experimental_rerun()


def render_pruebate_tab() -> None:
    st.subheader("🎯 PRUEBATE (mixto)")

    with st.expander(
        "⚙ Configuración de PRUEBATE y tolerancia",
        expanded=not st.session_state.pruebate_active,
    ):
        tol_pct_ui = st.slider(
            "Tolerancia (%)",
            min_value=0.1,
            max_value=50.0,
            value=float(st.session_state.tol_pct * 100),
            step=0.1,
        )
        st.session_state.tol_pct = tol_pct_ui / 100.0

        pruebate_q_ui = st.slider(
            "Número de preguntas en PRUEBATE",
            min_value=1,
            max_value=30,
            value=int(st.session_state.pruebate_q),
            step=1,
        )
        st.session_state.pruebate_q = pruebate_q_ui

        st.caption(
            f"Config actual: tolerancia = {st.session_state.tol_pct * 100:.1f}%, "
            f"preguntas PRUEBATE = {st.session_state.pruebate_q}."
        )

    st.markdown("---")

    def _start_pruebate() -> None:
        all_topics = list(MATH_TOPICS) + list(PHYS_TOPICS) + list(CHM_TOPICS)
        total_q = st.session_state.pruebate_q
        questions = []
        for _ in range(total_q):
            topic = random.choice(all_topics)
            enun, expected, unit, hint = topic.exercise()
            questions.append(
                {
                    "area": topic.area,
                    "tema": topic.name,
                    "enunciado": enun,
                    "correcto": float(expected),
                    "unit": unit,
                    "hint": hint,
                }
            )
        st.session_state.pruebate_questions = questions
        st.session_state.pruebate_idx = 0
        st.session_state.pruebate_correct = 0
        st.session_state.pruebate_misses = []
        st.session_state.pruebate_active = True

    def _finish_pruebate() -> None:
        st.session_state.pruebate_active = False

    if not st.session_state.pruebate_active and st.session_state.pruebate_idx == 0:
        st.write(
            "PRUEBATE generará preguntas aleatorias de **Matemáticas, Física y Química**.\n"
            "Se califican con la tolerancia indicada y cada respuesta queda guardada en el historial."
        )
        if st.button("🚀 Iniciar PRUEBATE"):
            _start_pruebate()
            st.experimental_rerun()

    if st.session_state.pruebate_active:
        q_list = st.session_state.pruebate_questions
        idx = st.session_state.pruebate_idx
        total = len(q_list)

        if idx >= total:
            _finish_pruebate()
        else:
            q = q_list[idx]
            st.markdown(f"**Pregunta {idx + 1} de {total}**")
            st.caption(f"{q['area']} · {q['tema']}")
            st.write(q["enunciado"])

            user_key = f"pruebate_answer_{idx}"
            user_answer = st.number_input(
                "Tu respuesta",
                value=0.0,
                step=0.1,
                format="%.6f",
                key=user_key,
            )

            c1, c2 = st.columns(2)
            with c1:
                btn_label = (
                    "Corregir y siguiente"
                    if idx < total - 1
                    else "Corregir y ver resultado final"
                )
                if st.button(btn_label, key=f"pruebate_check_{idx}"):
                    correcto_val = float(q["correcto"])
                    ok = within_tol(
                        correcto_val, float(user_answer), st.session_state.tol_pct
                    )
                    add_history(
                        area=q["area"],
                        tema=q["tema"],
                        tipo="PRUEBATE",
                        correcto=correcto_val,
                        usuario=float(user_answer),
                        acierto=ok,
                    )
                    if ok:
                        st.success(
                            f"CORRECTO ✅ — Solución: {correcto_val:.6f} {q['unit']}"
                        )
                        st.session_state.pruebate_correct += 1
                    else:
                        st.error(
                            f"INCORRECTO ❌ — Solución: {correcto_val:.6f} {q['unit']}"
                        )
                        st.caption("Pista: " + q["hint"])
                        st.session_state.pruebate_misses.append(
                            {"area": q["area"], "tema": q["tema"]}
                        )
                    st.session_state.pruebate_idx += 1
                    if st.session_state.pruebate_idx >= total:
                        _finish_pruebate()
                    st.experimental_rerun()

            with c2:
                st.info(
                    "Responde con calma. Al final verás un resumen con tu calificación "
                    "y los temas que necesitas reforzar."
                )

    if not st.session_state.pruebate_active and st.session_state.pruebate_idx > 0:
        total = len(st.session_state.pruebate_questions)
        correct = st.session_state.pruebate_correct
        score = 100.0 * correct / total if total > 0 else 0.0
        st.success(
            f"PRUEBATE terminado. Aciertos: {correct}/{total} — "
            f"Calificación: {score:.1f}/100"
        )
        if st.session_state.pruebate_misses:
            st.markdown("**Temas a reforzar:**")
            counts = {}
            for m in st.session_state.pruebate_misses:
                key = (m["area"], m["tema"])
                counts[key] = counts.get(key, 0) + 1
            for (area, tema), c in counts.items():
                st.write(f"- {area} · {tema} (errores: {c})")
        else:
            st.write("¡Excelente! No tuviste errores en este PRUEBATE. 🎉")

        st.markdown("---")
        if st.button("🔁 Hacer otro PRUEBATE"):
            st.session_state.pruebate_idx = 0
            st.session_state.pruebate_correct = 0
            st.session_state.pruebate_questions = []
            st.session_state.pruebate_misses = []
            st.session_state.pruebate_active = False
            st.experimental_rerun()


def render_history_tab() -> None:
    st.subheader("📜 Historial")
    df = get_history_df()
    if df.empty:
        st.info(
            "Todavía no hay registros. Resuelve algunos ejercicios en las materias "
            "o realiza un PRUEBATE."
        )
    else:
        st.write("Historial de intentos:")
        st.dataframe(df, use_container_width=True, height=400)
        csv_bytes = history_to_csv(df)
        st.download_button(
            "Descargar historial en CSV",
            data=csv_bytes,
            file_name="smartform_historial.csv",
            mime="text/csv",
        )


# =========================================================
#  MAIN
# =========================================================

st.set_page_config(page_title="Smart Form", page_icon="🧪", layout="wide")

init_state()
inject_global_css()
render_sidebar()
render_hero()

tabs = st.tabs(
    [
        "🏠 Inicio",
        "🧮 Matemáticas",
        "🧲 Física",
        "⚗️ Química",
        "🎯 PRUEBATE",
        "📜 Historial",
    ]
)

with tabs[0]:
    render_home_tab()

with tabs[1]:
    render_topic_tab("mat", "Matemáticas", "🧮", MATH_TOPICS)

with tabs[2]:
    render_topic_tab("fis", "Física", "🧲", PHYS_TOPICS)

with tabs[3]:
    render_topic_tab("qui", "Química", "⚗️", CHM_TOPICS)

with tabs[4]:
    render_pruebate_tab()

with tabs[5]:
    render_history_tab()