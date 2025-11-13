# path: app.py
# Smart Form - panel con sidebar + tabs básicas

from __future__ import annotations

import streamlit as st


def init_state() -> None:
    """Inicializa valores en session_state una sola vez."""
    if "tol_pct" not in st.session_state:
        st.session_state.tol_pct = 0.05  # 5%
    if "pruebate_q" not in st.session_state:
        st.session_state.pruebate_q = 8
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""


# ---------- Config de pagina ----------
st.set_page_config(
    page_title="Smart Form",
    page_icon="🧪",
    layout="wide",
)

init_state()

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🧪 Smart Form")
    st.markdown("### ⚙️ Configuración")

    # Tolerancia (porcentaje)
    tol_pct_ui = st.slider(
        "Tolerancia (%)",
        min_value=0.1,
        max_value=50.0,
        value=float(st.session_state.tol_pct * 100),
        step=0.1,
    )
    st.session_state.tol_pct = tol_pct_ui / 100.0  # guardamos como fracción

    # Preguntas de PRUEBATE
    pruebate_q_ui = st.slider(
        "Preguntas en PRUEBATE",
        min_value=1,
        max_value=30,
        value=int(st.session_state.pruebate_q),
        step=1,
    )
    st.session_state.pruebate_q = pruebate_q_ui

    st.markdown("---")

    # API key (para IA, opcional)
    st.caption("IA opcional (OpenAI):")
    api_key_ui = st.text_input(
        "OPENAI_API_KEY",
        type="password",
        value=st.session_state.api_key,
        help="Si la dejas vacía, la app funciona sin IA.",
    )
    st.session_state.api_key = api_key_ui.strip()

    st.markdown("---")
    st.caption(
        f"🧪 Config actual: tolerancia = {st.session_state.tol_pct * 100:.1f}%, "
        f"PRUEBATE = {st.session_state.pruebate_q} preguntas."
    )

# ---------- CONTENIDO PRINCIPAL ----------
st.title("Smart Form — panel principal")

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

# ----- Tab INICIO -----
with tabs[0]:
    st.subheader("Bienvenido 👋")
    st.write(
        "Esta es la versión base de **Smart Form**.\n\n"
        "Desde la barra lateral eliges tolerancia y cuántas preguntas tendrá el modo PRUEBATE.\n"
        "En las otras pestañas vamos a ir agregando ejercicios y explicaciones."
    )

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Configuración activa")
        st.metric("Tolerancia", f"{st.session_state.tol_pct * 100:.1f} %")
        st.metric("Preguntas PRUEBATE", st.session_state.pruebate_q)

    with col2:
        st.subheader("Estado de IA")
        if st.session_state.api_key:
            st.success("API key configurada. IA lista para usarse.")
        else:
            st.info("Sin API key. La app usará solo lógica local (sin IA).")

# ----- Tab MATEMÁTICAS -----
with tabs[1]:
    st.subheader("🧮 Matemáticas")
    st.write(
        "Aquí irán los módulos de Matemáticas:\n"
        "- Ecuaciones lineales\n"
        "- Ecuaciones cuadráticas\n"
        "- Pitágoras\n"
        "- Pendiente entre puntos\n\n"
        "En el siguiente paso conectaremos esta pestaña con funciones en `core/topics_math.py`."
    )

# ----- Tab FÍSICA -----
with tabs[2]:
    st.subheader("🧲 Física")
    st.write(
        "Aquí irán los módulos de Física:\n"
        "- Velocidad media\n"
        "- Energía cinética\n"
        "- Ley de Ohm\n"
        "- MRU / MRUA\n\n"
        "Más adelante cada tema tendrá explicación, ejemplo y ejercicio autocorregido."
    )

# ----- Tab QUÍMICA -----
with tabs[3]:
    st.subheader("⚗️ Química")
    st.write(
        "Aquí irán los módulos de Química:\n"
        "- Molaridad\n"
        "- Densidad\n"
        "- Dilución\n"
        "- Gas ideal\n\n"
        "También se integrará con el historial y, si quieres, con pistas IA."
    )

# ----- Tab PRUEBATE -----
with tabs[4]:
    st.subheader("🎯 PRUEBATE (mixto)")
    st.write(
        "Modo de examen rápido con preguntas aleatorias de todas las materias.\n\n"
        "Usará la tolerancia y el número de preguntas que configuras en la barra lateral."
    )

    st.markdown("---")
    st.metric("Tolerancia actual", f"{st.session_state.tol_pct * 100:.1f} %")
    st.metric("Preguntas programadas", st.session_state.pruebate_q)

    st.info(
        "En los siguientes pasos implementaremos la lógica para generar preguntas "
        "aleatorias y mostrar tu calificación."
    )

# ----- Tab HISTORIAL -----
with tabs[5]:
    st.subheader("📜 Historial")
    st.write(
        "Aquí se mostrará tu historial de ejercicios y resultados.\n\n"
        "Pronto guardaremos cada intento en una tabla para que puedas ver tu progreso."
    )
