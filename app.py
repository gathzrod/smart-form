# path: app.py
from __future__ import annotations

import streamlit as st

from core.utils import (
    within_tol,
    add_history,
    get_history_df,
    history_to_csv,
    clear_history,
)
from core.topics_math import MATH_TOPICS
from core.ai import ask_ai, has_ai


def init_state() -> None:
    """Inicializa valores en session_state una sola vez."""
    if "tol_pct" not in st.session_state:
        st.session_state.tol_pct = 0.05  # 5%
    if "pruebate_q" not in st.session_state:
        st.session_state.pruebate_q = 8


# ---------- Config de página ----------
st.set_page_config(
    page_title="Smart Form",
    page_icon="🧪",
    layout="wide",
)

init_state()

# ---------- SIDEBAR (solo branding + opciones generales) ----------
with st.sidebar:
    st.markdown("## 🧪 Smart Form")
    st.caption("Formulario interactivo para Matemáticas, Física y Química.")

    st.markdown("---")
    if has_ai():
        st.success("IA: activada (HuggingFace).")
    else:
        st.info("IA: no configurada.")

    st.markdown("---")
    if st.button("🧹 Borrar historial"):
        clear_history()
        st.success("Historial borrado en esta sesión.")

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
        "Bienvenido a **Smart Form**.\n\n"
        "• Usa las pestañas superiores para navegar entre materias.\n"
        "• La configuración de tolerancia y número de preguntas de PRUEBATE "
        "se encuentra dentro de la pestaña **PRUEBATE**.\n"
        "• Si la IA está activada, verás botones para pedir explicaciones adicionales."
    )

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Configuración actual")
        st.metric("Tolerancia", f"{st.session_state.tol_pct * 100:.1f} %")
        st.metric("Preguntas PRUEBATE", st.session_state.pruebate_q)

    with col2:
        st.subheader("Estado de IA")
        if has_ai():
            st.success(
                "IA activada (HuggingFace). Los botones de 'Pedir explicación IA' "
                "están disponibles en los ejercicios."
            )
        else:
            st.info(
                "IA no configurada. El dueño de la app puede añadir HF_TOKEN en los secrets "
                "de Streamlit para activar las explicaciones generadas."
            )

# ----- Tab MATEMÁTICAS -----
with tabs[1]:
    st.markdown("## 🧮 Matemáticas")

    topic_names = [t.name for t in MATH_TOPICS]
    sel_topic_name = st.selectbox("Selecciona un tema", topic_names)
    topic = MATH_TOPICS[topic_names.index(sel_topic_name)]

    # Diseño: un panel ancho con secciones colapsables
    with st.expander("📘 Explicación del tema", expanded=True):
        st.write(topic.explain())
        if has_ai():
            if st.button("Pedir explicación IA del tema", key="math_ai_topic"):
                txt = ask_ai(
                    topic=f"Matemáticas: {topic.name}",
                    prompt=topic.explain(),
                    expected=None,
                    unit="",
                )
                st.info(txt)

    with st.expander("🧪 Ejemplo resuelto", expanded=False):
        enun_ex, sol_ex = topic.example()
        st.write(enun_ex)
        if st.button("Mostrar solución del ejemplo", key="math_show_example"):
            st.success(sol_ex)

    with st.expander("📝 Ejercicio interactivo", expanded=False):
        enun_exe, expected, unit, hint = topic.exercise()
        st.write(enun_exe)

        user = st.number_input(
            "Tu respuesta",
            value=0.0,
            step=0.1,
            format="%.6f",
            key="math_answer",
        )

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("Corregir", key="math_check"):
                ok = within_tol(expected, float(user), st.session_state.tol_pct)
                add_history(
                    area="Matemáticas",
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

        with col_btn2:
            if has_ai():
                if st.button("Pedir explicación IA de este ejercicio", key="math_ai_exercise"):
                    prompt_ai = (
                        f"{enun_exe}\n"
                        f"El resultado correcto es aproximadamente {expected:.6f} {unit}.\n"
                        f"La respuesta del alumno fue: {float(user):.6f} {unit}."
                    )
                    txt = ask_ai(
                        topic=f"Matemáticas: {topic.name}",
                        prompt=prompt_ai,
                        expected=expected,
                        unit=unit,
                    )
                    st.info(txt)

# ----- Tab FÍSICA -----
with tabs[2]:
    st.subheader("🧲 Física")
    st.write(
        "Aquí irán los módulos de Física:\n"
        "- Velocidad media\n"
        "- Energía cinética\n"
        "- Ley de Ohm\n"
        "- MRU / MRUA\n\n"
        "Cada tema tendrá su explicación, ejemplo y ejercicio interactivo con la misma interfaz que Matemáticas."
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
        "También se integrará con el historial y, opcionalmente, con pistas IA."
    )

# ----- Tab PRUEBATE -----
with tabs[4]:
    st.subheader("🎯 PRUEBATE (mixto)")

    with st.expander("⚙ Configuración de PRUEBATE y tolerancia", expanded=True):
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
    st.write(
        "En esta versión, PRUEBATE aún no está implementado. "
        "Más adelante aquí se generarán preguntas aleatorias de Matemáticas, Física y Química, "
        "se calculará tu calificación y se guardará en el historial."
    )

# ----- Tab HISTORIAL -----
with tabs[5]:
    st.subheader("📜 Historial")
    df = get_history_df()
    if df.empty:
        st.info("Todavía no hay registros. Resuelve algunos ejercicios en Matemáticas primero.")
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
