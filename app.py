# path: app.py
"""
Aplicación principal de Smart Form.

Esta app en Streamlit permite practicar Matemáticas, Física y Química
mediante:
- Explicaciones teóricas con notación LaTeX
- Ejemplos resueltos
- Ejercicios interactivos autocorregibles
- Un modo de examen mixto llamado PRUEBATE
- Un historial descargable en CSV
"""

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
#  CONSTANTES GENERALES
# =========================================================

# Tolerancia numérica por defecto (porcentaje) al corregir ejercicios
DEFAULT_TOL_PCT = 0.05  # 5 %

# Número de preguntas por defecto en el modo PRUEBATE
DEFAULT_PRUEBATE_Q = 8

# Pequeños tips de estudio por área, mostrados como apoyo al alumno
STUDY_TIPS = {
    "Matemáticas": (
        "Empieza identificando qué datos conoces y qué incógnita buscas. "
        "Escribe la ecuación con calma y revisa tus operaciones paso a paso."
    ),
    "Física": (
        "Subraya los datos del problema, escribe las fórmulas que conoces "
        "y elige la que conecta mejor lo que tienes con lo que te piden."
    ),
    "Química": (
        "Si hay reacción química, revisa primero que esté bien balanceada. "
        "Trabajar con moles y unidades consistentes suele aclarar mucho el procedimiento."
    ),
}

# Mapa de dificultad por tema (área, nombre) -> etiqueta
# Puedes ajustar estos niveles según qué tan complejos sean los temas.
TOPIC_DIFFICULTY = {
    ("Matemáticas", "Ecuación lineal (ax + b = 0)"): "Básico",
    ("Matemáticas", "Ecuación cuadrática"): "Intermedio",
    ("Matemáticas", "Pitágoras (c² = a² + b²)"): "Básico",
    ("Matemáticas", "Pendiente entre puntos"): "Intermedio",
    # Física y Química se pueden completar cuando revises sus topics
    # Por defecto los trataremos como "Intermedio".
}

DIFFICULTY_WEIGHTS = {
    "Básico": 1,
    "Intermedio": 2,
    "Avanzado": 3,
}


# =========================================================
#  FUNCIONES AUXILIARES DE DIFICULTAD
# =========================================================

def get_topic_difficulty(area: str, name: str) -> str:
    """
    Devuelve la dificultad asociada a un tema.
    Si no está registrado, asume 'Intermedio'.
    """
    return TOPIC_DIFFICULTY.get((area, name), "Intermedio")


def difficulty_badge_text(level: str) -> str:
    """Devuelve una pequeña etiqueta amigable para mostrar junto al tema."""
    if level == "Básico":
        return "Nivel básico · ideal para repasar fundamentos."
    if level == "Avanzado":
        return "Nivel avanzado · problemas más retadores."
    return "Nivel intermedio · combina conceptos y cálculo."


# =========================================================
#  INICIALIZACIÓN DE ESTADO (SESSION_STATE)
# =========================================================

def init_state() -> None:
    """
    Crea en session_state todas las variables que usa la app.

    Esto evita errores de clave inexistente y deja claro qué estado
    maneja la aplicación de una sesión a otra.
    """
    st.session_state.setdefault("tol_pct", DEFAULT_TOL_PCT)
    st.session_state.setdefault("pruebate_q", DEFAULT_PRUEBATE_Q)

    # Estado del modo PRUEBATE
    st.session_state.setdefault("pruebate_active", False)   # ¿hay examen en curso?
    st.session_state.setdefault("pruebate_questions", [])   # lista de preguntas generadas
    st.session_state.setdefault("pruebate_idx", 0)          # índice de la pregunta actual
    st.session_state.setdefault("pruebate_correct", 0)      # aciertos acumulados
    st.session_state.setdefault("pruebate_misses", [])      # lista de temas fallados


# =========================================================
#  FUNCIÓN GENÉRICA PARA LAS PESTAÑAS DE CADA ÁREA
# =========================================================

def render_area_tab(
    area_label: str,
    header_markdown: str,
    topics: list[Topic],
    select_label: str,
    answer_label: str,
    key_prefix: str,
) -> None:
    """
    Dibuja la interfaz completa de una pestaña de área (Matemáticas, Física, Química).

    Parámetros:
        area_label: nombre del área (se muestra en mensajes al usuario).
        header_markdown: título con emoji para la pestaña.
        topics: lista de objetos Topic definidos en core.topics_*.
        select_label: texto del selectbox donde el usuario elige el tema.
        answer_label: etiqueta del campo numérico donde escribe su respuesta.
        key_prefix: prefijo único para las claves de Streamlit (evita colisiones).
    """
    st.markdown(header_markdown)

    # 1) Selección del tema dentro del área
    topic_names = [t.name for t in topics]
    sel_topic_name = st.selectbox(
        select_label,
        topic_names,
        key=f"{key_prefix}_topic_select",
    )
    topic = topics[topic_names.index(sel_topic_name)]

    # Dificultad y tip de estudio
    difficulty_level = get_topic_difficulty(area_label, topic.name)
    st.caption(f"Dificultad: **{difficulty_level}**")
    study_tip = STUDY_TIPS.get(area_label, "")

    # 2) Bloque de explicación teórica (con LaTeX)
    with st.expander("📘 Explicación del tema", expanded=True):
        st.markdown(topic.explain())
        if study_tip:
            if st.button(
                "Ver tip rápido de estudio",
                key=f"{key_prefix}_study_tip",
            ):
                st.info(study_tip)
        st.caption(difficulty_badge_text(difficulty_level))

    # 3) Bloque de ejemplo resuelto
    with st.expander("🧪 Ejemplo resuelto", expanded=False):
        enun_ex, sol_ex = topic.example()
        st.markdown(enun_ex)
        if st.button(
            f"Mostrar solución del ejemplo ({area_label})",
            key=f"{key_prefix}_show_example",
        ):
            # st.success también interpreta Markdown/LaTeX
            st.success(sol_ex)

    # 4) Bloque de ejercicio interactivo autocorregible
    with st.expander("📝 Ejercicio interactivo", expanded=False):
        # Clave para guardar el ejercicio actual en session_state
        ex_key = f"{key_prefix}_exercise_data"
        ex_data = st.session_state.get(ex_key)

        # Si no hay ejercicio guardado o cambió el tema, generamos uno nuevo
        if ex_data is None or ex_data.get("tema") != topic.name:
            enun_exe, expected, unit, hint = topic.exercise()
            ex_data = {
                "tema": topic.name,
                "enunciado": enun_exe,
                "correcto": float(expected),
                "unit": unit,
                "hint": hint,
            }
            st.session_state[ex_key] = ex_data

        # Usamos siempre los datos guardados en session_state
        enun_exe = ex_data["enunciado"]
        expected = ex_data["correcto"]
        unit = ex_data["unit"]
        hint = ex_data["hint"]

        st.markdown(enun_exe)

        # Campo numérico para la respuesta del alumno
        user = st.number_input(
            answer_label,
            value=0.0,
            step=0.1,
            format="%.6f",
            key=f"{key_prefix}_answer",
        )

        b1, b2 = st.columns(2)

        # Botón para corregir y guardar en el historial
        with b1:
            if st.button(f"Corregir ({area_label})", key=f"{key_prefix}_check"):
                ok = within_tol(expected, float(user), st.session_state.tol_pct)

                # Registrar el intento en el historial
                add_history(
                    area=area_label,
                    tema=topic.name,
                    tipo="Ejercicio",
                    correcto=expected,
                    usuario=float(user),
                    acierto=ok,
                )

                # Feedback visual al estudiante
                if ok:
                    st.success(f"CORRECTO ✅ — Solución: {expected:.6f} {unit}")
                else:
                    st.error(f"INCORRECTO ❌ — Solución: {expected:.6f} {unit}")
                    st.caption("Pista: " + hint)

        # Botón con una guía general de metodología
        with b2:
            if st.button(
                "¿Cómo abordar este tipo de ejercicio?",
                key=f"{key_prefix}_howto",
            ):
                mensaje = (
                    "1. Lee el enunciado con calma.\n"
                    "2. Anota los datos conocidos y la incógnita.\n"
                    "3. Escribe la fórmula o idea principal del tema.\n"
                    "4. Sustituye paso a paso y revisa tus unidades.\n\n"
                    "Si el resultado no coincide, compara tu procedimiento con la "
                    "explicación y el ejemplo resuelto del tema."
                )
                st.info(mensaje)


# =========================================================
#  CONFIGURACIÓN DE PÁGINA + ESTILOS
# =========================================================

ui.apply_base_config()
init_state()


# =========================================================
#  SIDEBAR
# =========================================================

with st.sidebar:
    # Sidebar con título y botón para limpiar historial
    ui.render_sidebar(ai_on=False, on_clear_history=clear_history)


# =========================================================
#  HERO + TABS PRINCIPALES
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
        "Aquí puedes ver la configuración actual de tolerancia numérica y "
        "el número de preguntas del modo **PRUEBATE**."
    )

    tol_pct = st.session_state.tol_pct * 100.0
    q = st.session_state.pruebate_q

    helper_text = (
        "Las actividades se corrigen con la tolerancia indicada y el modo PRUEBATE "
        "mezcla preguntas de Matemáticas, Física y Química para simular un pequeño examen."
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
#  TAB 4: PRUEBATE (MODO EXAMEN MIXTO)
# =========================================================

with tabs[4]:
    st.subheader("🎯 PRUEBATE (mixto)")

    # Panel de configuración de tolerancia y número de preguntas
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

    # ---------- Funciones internas para gestionar PRUEBATE ----------

    def _build_weighted_topic_pool() -> list[Topic]:
        """
        Construye una lista de temas donde los de mayor dificultad
        aparecen más veces, para que PRUEBATE tienda a ser más retador.
        """
        all_topics = list(MATH_TOPICS) + list(PHYS_TOPICS) + list(CHM_TOPICS)
        pool: list[Topic] = []
        for t in all_topics:
            level = get_topic_difficulty(t.area, t.name)
            weight = DIFFICULTY_WEIGHTS.get(level, 2)
            pool.extend([t] * weight)
        return pool

    def _start_pruebate() -> None:
        """
        Genera la lista de preguntas aleatorias para PRUEBATE
        y reinicia todos los contadores asociados.
        """
        topic_pool = _build_weighted_topic_pool()
        total_q = st.session_state.pruebate_q
        questions = []

        for _ in range(total_q):
            topic = random.choice(topic_pool)
            enun, expected, unit, hint = topic.exercise()
            level = get_topic_difficulty(topic.area, topic.name)
            questions.append(
                {
                    "area": topic.area,
                    "tema": topic.name,
                    "enunciado": enun,
                    "correcto": expected,
                    "unit": unit,
                    "hint": hint,
                    "dificultad": level,
                }
            )

        st.session_state.pruebate_questions = questions
        st.session_state.pruebate_idx = 0
        st.session_state.pruebate_correct = 0
        st.session_state.pruebate_misses = []
        st.session_state.pruebate_active = True

    def _finish_pruebate() -> None:
        """Marca el examen como terminado (no genera nuevas preguntas)."""
        st.session_state.pruebate_active = False

    # ---------- 1) Vista inicial antes de empezar PRUEBATE ----------

    if not st.session_state.pruebate_active and st.session_state.pruebate_idx == 0:
        st.write(
            "PRUEBATE generará preguntas aleatorias de **Matemáticas, Física y Química**.\n"
            "Se califican con la tolerancia indicada y cada respuesta queda guardada "
            "en el historial."
        )
        if st.button("🚀 Iniciar PRUEBATE"):
            _start_pruebate()
            st.rerun()

    # ---------- 2) Vista durante el examen (pregunta actual) ----------

    if st.session_state.pruebate_active:
        q_list = st.session_state.pruebate_questions
        idx = st.session_state.pruebate_idx
        total = len(q_list)

        if idx >= total:
            _finish_pruebate()
        else:
            q = q_list[idx]
            st.markdown(f"**Pregunta {idx + 1} de {total}**")
            st.caption(f"{q['area']} · {q['tema']} · Dificultad: {q['dificultad']}")
            st.markdown(q["enunciado"])

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
                        correcto_val,
                        float(user_answer),
                        st.session_state.tol_pct,
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
                            {"area": q["area"], "tema": q["tema"], "dificultad": q["dificultad"]}
                        )

                    st.session_state.pruebate_idx += 1
                    if st.session_state.pruebate_idx >= total:
                        _finish_pruebate()
                    st.rerun()

            with c2:
                st.info(
                    "Responde con calma. Al final verás un resumen con tu calificación, "
                    "la dificultad promedio y los temas que necesitas reforzar."
                )

    # ---------- 3) Resumen final después de terminar PRUEBATE ----------

    if not st.session_state.pruebate_active and st.session_state.pruebate_idx > 0:
        total = len(st.session_state.pruebate_questions)
        correct = st.session_state.pruebate_correct
        score = 100.0 * correct / total if total > 0 else 0.0

        st.success(
            f"PRUEBATE terminado. Aciertos: {correct}/{total} — "
            f"Calificación: {score:.1f}/100"
        )

        # Resumen de dificultades falladas
        if st.session_state.pruebate_misses:
            st.markdown("**Temas a reforzar (con dificultad):**")
            counts: dict[tuple[str, str, str], int] = {}
            for m in st.session_state.pruebate_misses:
                key = (m["area"], m["tema"], m["dificultad"])
                counts[key] = counts.get(key, 0) + 1
            for (area, tema, dif), c in counts.items():
                st.write(f"- {area} · {tema} · {dif} (errores: {c})")
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

