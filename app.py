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
    st.session_state.tol_pct = tol_pct_ui / 100.0

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

    if st.button("🧹 Borrar historial"):
        clear_history()
        st.success("Historial borrado.")

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
        if has_ai():
            st.success(
                "IA activada (HuggingFace). Los botones de 'Pedir explicación IA' estarán disponibles."
            )
        else:
            st.info(
                "IA no configurada. El dueño de la app debe añadir HF_TOKEN en los secrets de Streamlit "
                "para activar las explicaciones con IA."
            )

# ----- Tab MATEMÁTICAS -----
with tabs[1]:
    st.subheader("🧮 Matemáticas")

    topic_names = [t.name for t in MATH_TOPICS]
    sel_topic_name = st.selectbox("Selecciona un tema", topic_names)
    topic = MATH_TOPICS[topic_names.index(sel_topic_name)]

    col_exp, col_ex, col_exe = st.columns(3)

    # Explicación
    with col_exp:
        st.markdown("#### Explicación")
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

    # Ejemplo
    with col_ex:
        st.markdown("#### Ejemplo")
        enun_ex, sol_ex = topic.example()
        st.write(enun_ex)
        if st.toggle("Mostrar solución", key="math_show_example"):
            st.success(sol_ex)

    # Ejercicio
    with col_exe:
        st.markdown("#### Ejercicio")
        enun_exe, expected, unit, hint = topic.exercise()
        st.write(enun_exe)
        user = st.number_input(
            "Tu respuesta",
            value=0.0,
            step=0.1,
            format="%.6f",
            key="math_answer",
        )

        cols_btn = st.columns(2)
        with cols_btn[0]:
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
                    st.success(f"CORRECTO ✅  — Solución: {expected:.6f} {unit}")
                else:
                    st.error(f"INCORRECTO ❌  — Solución: {expected:.6f} {unit}")
                    st.caption("Hint: " + hint)
        with cols_btn[1]:
            if has_ai():
                if st.button("Pedir explicación IA de este ejercicio", key="math_ai_exercise"):
                    prompt_ai = f"{enun_exe}\nEl resultado correcto es aproximadamente {expected:.6f} {unit}."
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
    df = get_history_df()
    if df.empty:
        st.info("Todavía no hay registros. Resuelve algunos ejercicios primero.")
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
        

