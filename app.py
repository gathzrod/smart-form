# ============================
# path: app.py
# ============================
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
from core.topics_phys import PHYS_TOPICS
from core.topics_chem import CHM_TOPICS
from core.ai import ask_ai, has_ai


def init_state() -> None:
    """Inicializa valores en session_state una sola vez."""
    if "tol_pct" not in st.session_state:
        st.session_state.tol_pct = 0.05  # 5%
    if "pruebate_q" not in st.session_state:
        st.session_state.pruebate_q = 8


def inject_global_css() -> None:
    """Pequeños ajustes de estilo global para que se vea más limpio/suave."""
    st.markdown(
        """
        <style>
        .main > div {
            max-width: 1100px;
            margin: 0 auto;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 0.4rem 1.1rem;
            border-radius: 999px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .stMetric, .stAlert {
            border-radius: 12px !important;
        }
        .stButton button {
            border-radius: 999px;
        }
        .streamlit-expanderHeader {
            font-weight: 600;
        }
        .streamlit-expander {
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------- Config de página ----------
st.set_page_config(
    page_title="Smart Form",
    page_icon="🧪",
    layout="wide",
)

init_state()
inject_global_css()

# ---------- SIDEBAR ----------
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
        "• La configuración de tolerancia y número de preguntas del modo **PRUEBATE** "
        "se encuentra dentro de la pestaña correspondiente.\n"
        "• Si la IA está activa, verás botones para pedir explicaciones adicionales."
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
                "IA activada (si un modelo externo falla, se usa explicación local)."
            )
        else:
            st.info(
                "IA sin conexión a modelos externos. Se usan solo explicaciones locales "
                "basadas en el enunciado y la teoría."
            )

# ----- Tab MATEMÁTICAS -----
with tabs[1]:
    st.markdown("## 🧮 Matemáticas")

    topic_names = [t.name for t in MATH_TOPICS]
    sel_topic_name = st.selectbox("Selecciona un tema", topic_names)
    topic = MATH_TOPICS[topic_names.index(sel_topic_name)]

    with st.expander("📘 Explicación del tema", expanded=True):
        st.write(topic.explain())
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
            "Tu respuesta (Matemáticas)",
            value=0.0,
            step=0.1,
            format="%.6f",
            key="math_answer",
        )

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("Corregir (Matemáticas)", key="math_check"):
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
            if st.button("Pedir explicación IA de este ejercicio (Matemáticas)", key="math_ai_exercise"):
                prompt_ai = (
                    f"{enun_exe}\n"
                    f"La respuesta del alumno fue: {float(user):.6f} {unit} "
                    f"(el sistema conoce un valor de referencia para revisar)."
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
    st.markdown("## 🧲 Física")

    phys_names = [t.name for t in PHYS_TOPICS]
    sel_phys_name = st.selectbox("Selecciona un tema de Física", phys_names)
    phys_topic = PHYS_TOPICS[phys_names.index(sel_phys_name)]

    with st.expander("📘 Explicación del tema", expanded=True):
        st.write(phys_topic.explain())
        if st.button("Pedir explicación IA del tema (Física)", key="phys_ai_topic"):
            txt = ask_ai(
                topic=f"Física: {phys_topic.name}",
                prompt=phys_topic.explain(),
                expected=None,
                unit="",
            )
            st.info(txt)

    with st.expander("🧪 Ejemplo resuelto", expanded=False):
        enun_ex, sol_ex = phys_topic.example()
        st.write(enun_ex)
        if st.button("Mostrar solución del ejemplo (Física)", key="phys_show_example"):
            st.success(sol_ex)

    with st.expander("📝 Ejercicio interactivo", expanded=False):
        enun_exe, expected, unit, hint = phys_topic.exercise()
        st.write(enun_exe)

        user = st.number_input(
            "Tu respuesta (Física)",
            value=0.0,
            step=0.1,
            format="%.6f",
            key="phys_answer",
        )

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("Corregir (Física)", key="phys_check"):
                ok = within_tol(expected, float(user), st.session_state.tol_pct)
                add_history(
                    area="Física",
                    tema=phys_topic.name,
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
            if st.button("Pedir explicación IA de este ejercicio (Física)", key="phys_ai_exercise"):
                prompt_ai = (
                    f"{enun_exe}\n"
                    f"La respuesta del alumno fue: {float(user):.6f} {unit} "
                    f"(el sistema conoce un valor de referencia para revisar)."
                )
                txt = ask_ai(
                    topic=f"Física: {phys_topic.name}",
                    prompt=prompt_ai,
                    expected=expected,
                    unit=unit,
                )
                st.info(txt)

# ----- Tab QUÍMICA -----
with tabs[3]:
    st.markdown("## ⚗️ Química")

    chem_names = [t.name for t in CHM_TOPICS]
    sel_chem_name = st.selectbox("Selecciona un tema de Química", chem_names)
    chem_topic = CHM_TOPICS[chem_names.index(sel_chem_name)]

    with st.expander("📘 Explicación del tema", expanded=True):
        st.write(chem_topic.explain())
        if st.button("Pedir explicación IA del tema (Química)", key="chem_ai_topic"):
            txt = ask_ai(
                topic=f"Química: {chem_topic.name}",
                prompt=chem_topic.explain(),
                expected=None,
                unit="",
            )
            st.info(txt)

    with st.expander("🧪 Ejemplo resuelto", expanded=False):
        enun_ex, sol_ex = chem_topic.example()
        st.write(enun_ex)
        if st.button("Mostrar solución del ejemplo (Química)", key="chem_show_example"):
            st.success(sol_ex)

    with st.expander("📝 Ejercicio interactivo", expanded=False):
        enun_exe, expected, unit, hint = chem_topic.exercise()
        st.write(enun_exe)

        user = st.number_input(
            "Tu respuesta (Química)",
            value=0.0,
            step=0.1,
            format="%.6f",
            key="chem_answer",
        )

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("Corregir (Química)", key="chem_check"):
                ok = within_tol(expected, float(user), st.session_state.tol_pct)
                add_history(
                    area="Química",
                    tema=chem_topic.name,
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
            if st.button("Pedir explicación IA de este ejercicio (Química)", key="chem_ai_exercise"):
                prompt_ai = (
                    f"{enun_exe}\n"
                    f"La respuesta del alumno fue: {float(user):.6f} {unit} "
                    f"(el sistema conoce un valor de referencia para revisar)."
                )
                txt = ask_ai(
                    topic=f"Química: {chem_topic.name}",
                    prompt=prompt_ai,
                    expected=expected,
                    unit=unit,
                )
                st.info(txt)

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
        st.info("Todavía no hay registros. Resuelve algunos ejercicios en las materias primero.")
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