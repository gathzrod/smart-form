# path: core/topics_math.py
from __future__ import annotations

import math
import random
from typing import List

from .utils import Topic


# ---------- M1: Ecuación lineal (ax + b = 0) ----------


def m_lineal_explain() -> str:
    return (
        "Ecuación lineal en una variable:\n"
        "  a·x + b = 0 con a ≠ 0.\n\n"
        "La idea es dejar a x sola en un lado:\n"
        "  a·x + b = 0  →  a·x = -b  →  x = -b / a.\n"
        "Solo hay que tener cuidado con los signos y con no dividir entre cero."
    )


def m_lineal_example() -> tuple[str, str]:
    a, b = 2, -6
    x = -(b) / a
    enun = "Ejemplo: resuelve 2x - 6 = 0."
    sol = (
        "Pasamos el -6 al otro lado: 2x = 6.\n"
        "Luego dividimos entre 2: x = 6 / 2 = 3.\n\n"
        f"Resultado numérico: x = {x:.3f}."
    )
    return enun, sol


def m_lineal_exercise() -> tuple[str, float, str, str]:
    variants = [(3, 9), (-4, 8), (7, -21), (5, -10), (-6, 18), (9, -27)]
    a, b = random.choice(variants)
    expected = -(b) / a
    enun = f"Resuelve la ecuación {a}x {b:+d} = 0. Ingresa el valor de x."
    unit = ""
    hint = "Aísla x: pasa el término independiente al otro lado y divide entre a."
    return enun, expected, unit, hint


# ---------- M2: Ecuación cuadrática (ax² + bx + c = 0) ----------


def m_quad_explain() -> str:
    return (
        "Ecuación cuadrática general:\n"
        "  a·x² + b·x + c = 0 con a ≠ 0.\n\n"
        "Las soluciones se obtienen con la fórmula general:\n"
        "  x = [-b ± √(b² - 4ac)] / (2a).\n\n"
        "Al término b² - 4ac se le llama discriminante D.\n"
        "Si D > 0 hay dos raíces reales distintas, si D = 0 hay una raíz doble "
        "y si D < 0 las soluciones son complejas."
    )


def m_quad_example() -> tuple[str, str]:
    a, b, c = 1, -3, 2
    D = b * b - 4 * a * c
    x1 = (-b - math.sqrt(D)) / (2 * a)
    x2 = (-b + math.sqrt(D)) / (2 * a)
    enun = "Ejemplo: resuelve x² - 3x + 2 = 0."
    sol = (
        "Identificamos a = 1, b = -3, c = 2.\n"
        "Calculamos D = b² - 4ac = 9 - 8 = 1.\n"
        "Las raíces son x = [3 ± √1] / 2 → x1 = 1, x2 = 2.\n\n"
        f"Resultado numérico: x1 = {x1:.3f}, x2 = {x2:.3f}."
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
    hint = "Usa la fórmula general y elige la raíz con el signo menos en el numerador."
    return enun, xs, unit, hint


# ---------- M3: Pitágoras (c² = a² + b²) ----------


def m_pitagoras_explain() -> str:
    return (
        "En un triángulo rectángulo, la hipotenusa c y los catetos a y b cumplen:\n"
        "  c² = a² + b².\n\n"
        "Si conoces los catetos, la hipotenusa es c = √(a² + b²).\n"
        "Si conoces c y un cateto, puedes despejar el otro."
    )


def m_pitagoras_example() -> tuple[str, str]:
    a, b = 6, 8
    c = math.sqrt(a * a + b * b)
    enun = "Ejemplo: un triángulo rectángulo tiene catetos de 6 y 8. Calcula la hipotenusa."
    sol = (
        "Aplicamos c = √(a² + b²):\n"
        "  c = √(6² + 8²) = √(36 + 64) = √100 = 10.\n\n"
        f"Resultado numérico: c = {c:.3f}."
    )
    return enun, sol


def m_pitagoras_exercise() -> tuple[str, float, str, str]:
    variants = [(3, 4), (5, 12), (7, 24), (9, 40), (8, 15), (12, 16)]
    a, b = random.choice(variants)
    c = math.sqrt(a * a + b * b)
    enun = f"En un triángulo rectángulo, los catetos miden a = {a} y b = {b}. Calcula la hipotenusa c."
    unit = ""
    hint = "Eleva cada cateto al cuadrado, suma y saca la raíz cuadrada."
    return enun, c, unit, hint


# ---------- M4: Pendiente entre dos puntos ----------


def m_slope_explain() -> str:
    return (
        "La pendiente m de la recta que pasa por dos puntos (x₁, y₁) y (x₂, y₂) es:\n"
        "  m = (y₂ - y₁) / (x₂ - x₁).\n\n"
        "Solo hay que verificar que x₂ ≠ x₁ para no dividir entre cero."
    )


def m_slope_example() -> tuple[str, str]:
    x1, y1, x2, y2 = 1, 2, 5, 10
    m = (y2 - y1) / (x2 - x1)
    enun = "Ejemplo: calcula la pendiente de la recta que pasa por (1, 2) y (5, 10)."
    sol = (
        "Calculamos diferencias: Δy = 10 - 2 = 8 y Δx = 5 - 1 = 4.\n"
        "Luego m = Δy / Δx = 8 / 4 = 2.\n\n"
        f"Resultado numérico: m = {m:.3f}."
    )
    return enun, sol


def m_slope_exercise() -> tuple[str, float, str, str]:
    sets = [(0, 0, 4, 6), (-2, 3, 1, 12), (2, -1, 8, 5), (-3, -2, 4, 7), (1, 5, 7, 17)]
    x1, y1, x2, y2 = random.choice(sets)
    m = (y2 - y1) / (x2 - x1)
    enun = (
        f"Calcula la pendiente m de la recta que pasa por los puntos "
        f"({x1}, {y1}) y ({x2}, {y2})."
    )
    unit = ""
    hint = "Resta primero las y, luego las x, y divide: m = Δy / Δx."
    return enun, m, unit, hint


# ---------- Lista de temas de Matemáticas ----------

MATH_TOPICS: List[Topic] = [
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