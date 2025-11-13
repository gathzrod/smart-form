# path: app.py
# Smart Form - version con sidebar de configuracion

from __future__ import annotations

import os

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
    # Logo (si existe)
    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, caption="Smart Form", use_container_width=True)
    else:
        st.markdown("### 🧪 Smart Form")

    st.markdown("## ⚙️ Configuración")

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

st.write(
    "Bienvenido a **Smart Form**. Esta es la versión con barra lateral de "
    "configuración. En los siguientes pasos vamos a agregar:"
)

st.markdown(
    """
- Pestañas de **Matemáticas**, **Física**, **Química** y **PRUEBATE**.
- Ejercicios autocorregidos usando la tolerancia que elegiste.
- (Opcional) Pistas y explicaciones generadas con IA si configuras tu API key.
"""
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
