# path: app.py
from __future__ import annotations

import random
import math

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
    # noqa: E402
from core.topics_chem import CHM_TOPICS
from core.ai import ask_ai, has_ai
# Intentamos importar el módulo de UI (estilos)
try:
    import core.ui as ui
except Exception:
    ui = None


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
#  INICIALIZACIÓN DE ESTADO
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


# =========================================================
#  CONFIG DE PÁGINA + ESTILOS
# =========================================================

if ui is not None and hasattr(ui, "apply_base_config"):
    ui.apply_base_config()
else:
    # Fallback simple por si el módulo core.ui no se cargara bien
    st.set_page_config(page_title="Smart Form", page_icon="🧪", layout="wide")

init_state()

# =========================================================
#  SIDEBAR
# =========================================================

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
        "Aquí ves tu configuración y el estado de la IA antes de entrar a cada materia."
    )

    tol_pct = st.session_state.tol_pct * 100.0
    q = st.session_state.pruebate_q

    if has_ai():
        ai_text = "IA activada. Si un modelo externo falla, se usa explicación local."
    else:
        ai_text = "IA local: por ahora solo se usan explicaciones sin modelo externo."

    ui.render_home_cards(tol_pct=tol_pct, q=q, ai_text=ai_text)

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
        b1, b2 = st.columns(2)
        with b1:
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
        with b2:
            if st.button(
                "Pedir explicación IA de este ejercicio (Matemáticas)",
                key="math_ai_exercise",
            ):
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


# =========================================================
#  TAB 2: FÍSICA
# =========================================================

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
        b1, b2 = st.columns(2)
        with b1:
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
        with b2:
            if st.button(
                "Pedir explicación IA de este ejercicio (Física)",
                key="phys_ai_exercise",
            ):
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


# =========================================================
#  TAB 3: QUÍMICA
# =========================================================

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
        b1, b2 = st.columns(2)
        with b1:
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
        with b2:
            if st.button(
                "Pedir explicación IA de este ejercicio (Química)",
                key="chem_ai_exercise",
            ):
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
                    st.rerun()
            with c2:
                st.info(
                    "Responde con calma. Al final verás un resumen con tu "
                    "calificación y los temas que necesitas reforzar."
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