# path: app.py
from __future__ import annotations

import random

import streamlit as st

from core.utils import (
    Topic,
    add_history,
    clear_history,
    get_history_df,
    history_to_csv,
    within_tol,
)
from core.topics_math import MATH_TOPICS
from core.topics_chem import CHM_TOPICS
from core.topics_phys import PHYS_TOPICS
import core.ui as ui

# =========================================================
#  CONFIGURACIÓN GENERAL
# =========================================================

DEFAULT_TOL_PCT = 0.05  # 5 %
DEFAULT_PRUEBATE_Q = 8
AI_ON = False  # La IA externa ya no se usa, pero mantenemos el flag para la UI


STUDY_TIPS = {
    "Matemáticas": (
        "Empieza siempre por identificar qué datos te dan y qué incógnita buscas. "
        "Haz un dibujo o esquema rápido si ayuda, y revisa tus unidades al final."
    ),
    "Física": (
        "Subraya los datos, escribe las fórmulas que conoces y elige la que conecta "
        "mejor lo que tienes con lo que te piden. No tengas miedo de aislar la incógnita "
        "paso a paso."
    ),
    "Química": (
        "Antes de calcular, asegúrate de tener bien balanceada la reacción (si aplica) y "
        "de trabajar con las unidades correctas. A veces convertir todo a moles aclara mucho."
    ),
}


# =========================================================
#  INICIALIZACIÓN DE ESTADO
# =========================================================

def init_state() -> None:
    st.session_state.setdefault("tol_pct", DEFAULT_TOL_PCT)
    st.session_state.setdefault("pruebate_q", DEFAULT_PRUEBATE_Q)

    st.session_state.setdefault("pruebate_active", False)
    st.session_state.setdefault("pruebate_questions", [])
    st.session_state.setdefault("pruebate_idx", 0)
    st.session_state.setdefault("pruebate_correct", 0)
    st.session_state.setdefault("pruebate_misses", [])


# =========================================================
#  FUNCIÓN GENÉRICA PARA LAS PESTAÑAS DE ÁREA
# =========================================================

def render_area_tab(
    area_label: str,
    header_markdown: str,
    topics: list[Topic],
    select_label: str,
    answer_label: str,
    key_prefix: str,
) -> None:
    """Renderiza un tab de área (Matemáticas, Física, Química) con la misma estética."""
    st.markdown(header_markdown)

    topic_names = [t.name for t in topics]
    sel_topic_name = st.selectbox(
        select_label,
        topic_names,
        key=f"{key_prefix}_topic_select",
    )
    topic = topics[topic_names.index(sel_topic_name)]

    study_tip = STUDY_TIPS.get(area_label, "")

    # --- Explicación del tema ---
    with st.expander("📘 Explicación del tema", expanded=True):
        st.write(topic.explain())
        if study_tip:
            if st.button(
                "Ver tip rápido de estudio",
                key=f"{key_prefix}_study_tip",
            ):
                st.info(study_tip)

    # --- Ejemplo resuelto ---
    with st.expander("🧪 Ejemplo resuelto", expanded=False):
        enun_ex, sol_ex = topic.example()
        st.write(enun_ex)
        if st.button(
            f"Mostrar solución del ejemplo ({area_label})",
            key=f"{key_prefix}_show_example",
        ):
            st.success(sol_ex)

    # --- Ejercicio interactivo ---
    with st.expander("📝 Ejercicio interactivo", expanded=False):
        enun_exe, expected, unit, hint = topic.exercise()
        st.write(enun_exe)
        user = st.number_input(
            answer_label,
            value=0.0,
            step=0.1,
            format="%.6f",
            key=f"{key_prefix}_answer",
        )
        b1, b2 = st.columns(2)
        with b1:
            if st.button(f"Corregir ({area_label})", key=f"{key_prefix}_check"):
                ok = within_tol(expected, float(user), st.session_state.tol_pct)
                add_history(
                    area=area_label,
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
                "¿Cómo abordar este tipo de ejercicio?",
                key=f"{key_prefix}_howto",
            ):
                mensaje = (
                    "1. Lee el enunciado con calma.\n"
                    "2. Identifica los datos y la incógnita.\n"
                    "3. Escribe la fórmula o idea principal del tema.\n"
                    "4. Sustituye paso a paso y revisa el resultado.\n\n"
                    "Si algo no sale, compara tu procedimiento con la explicación del tema."
                )
                st.info(mensaje)


# =========================================================
#  CONFIG DE PÁGINA + ESTILOS
# =========================================================

ui.apply_base_config()
init_state()

# =========================================================
#  SIDEBAR
# =========================================================

with st.sidebar:
    # Mantenemos el parámetro ai_on para no romper la estética del sidebar,
    # pero la IA externa ya no se utiliza.
    ui.render_sidebar(ai_on=AI_ON, on_clear_history=clear_history)

# =========================================================
#  HERO + TABS
# =========================================================

ui.render_hero()

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

# =========================================================
#  TAB 0: INICIO
# =========================================================

with tabs[0]:
    st.subheader("Bienvenido 👋")
    st.write(
        "Esta es la vista general de **Smart Form**. "
        "Aquí puedes ver tu configuración y cómo se evaluarán tus respuestas "
        "antes de entrar a cada materia."
    )

    tol_pct = st.session_state.tol_pct * 100.0
    q = st.session_state.pruebate_q

    helper_text = (
        "Todas las explicaciones y ejercicios están diseñados para que practiques de forma "
        "guiada y sencilla. No dependemos de modelos externos: todo el contenido viene de "
        "los temas que preparamos para el curso."
    )

    ui.render_home_cards(tol_pct, q, helper_text)

    st.markdown("---")
    st.write(
        "Usa las pestañas de arriba para entrar a **Matemáticas, Física y Química**, "
        "y el modo **PRUEBATE** para un examen mixto. "
        "Cada intento se guarda en el historial para que puedas ver tu progreso."
    )

# =========================================================
#  TAB 1: MATEMÁTICAS
# =========================================================

with tabs[1]:
    render_area_tab(
        area_label="Matemáticas",
        header_markdown="## 🧮 Matemáticas",
        topics=MATH_TOPICS,
        select_label="Selecciona un tema",
        answer_label="Tu respuesta (Matemáticas)",
        key_prefix="math",
    )

# =========================================================
#  TAB 2: FÍSICA
# =========================================================

with tabs[2]:
    render_area_tab(
        area_label="Física",
        header_markdown="## 🧲 Física",
        topics=PHYS_TOPICS,
        select_label="Selecciona un tema de Física",
        answer_label="Tu respuesta (Física)",
        key_prefix="phys",
    )

# =========================================================
#  TAB 3: QUÍMICA
# =========================================================

with tabs[3]:
    render_area_tab(
        area_label="Química",
        header_markdown="## ⚗️ Química",
        topics=CHM_TOPICS,
        select_label="Selecciona un tema de Química",
        answer_label="Tu respuesta (Química)",
        key_prefix="chem",
    )

# =========================================================
#  TAB 4: PRUEBATE
# =========================================================

with tabs[4]:
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
                    "correcto": expected,
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
            st.rerun()

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
                            f"CORRECTO ✅ — Solución: {correcto_val:.6f} {q['unit']}."
                        )
                        st.session_state.pruebate_correct += 1
                    else:
                        st.error(
                            f"INCORRECTO ❌ — Solución: {correcto_val:.6f} {q['unit']}."
                        )
                        st.caption("Pista: " + q["hint"])
                        st.session_state.pruebate_misses.append(
                            {"area": q["area"], "tema": q["tema"]}
                        )
                    st.session_state.pruebate_idx += 1
                    if st.session_state.pruebate_idx >= total:
                        _finish_pruebate()
                    st.rerun()
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
            st.rerun()

# =========================================================
#  TAB 5: HISTORIAL
# =========================================================

with tabs[5]:
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
