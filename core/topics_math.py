# path: core/topics_math.py
from __future__ import annotations

import random
from typing import List

from .utils import Topic


def m_lineal_explain() -> str:
    return (
        "Ecuación lineal en una variable:\n"
        "- Forma general: a*x + b = 0, con a ≠ 0.\n"
        "- Objetivo típico: despejar x.\n\n"
        "Despeje básico:\n"
        "  a*x + b = 0  →  a*x = -b  →  x = -b / a.\n\n"
        "Checklist rápido:\n"
        "1) Asegúrate de que está en forma a*x + b = 0.\n"
        "2) Verifica que a no sea 0.\n"
        "3) Cuidado con los signos (ej: -(-6) = +6)."
    )


def m_lineal_example() -> tuple[str, str]:
    a, b = 2, -6
    x = -b / a
    enun = "Ejemplo: Resuelve la ecuación 2x - 6 = 0."
    sol = f"Despeje: 2x - 6 = 0 → 2x = 6 → x = 3.0\nResultado numérico: x = {x:.3f}"
    return enun, sol


def m_lineal_exercise() -> tuple[str, float, str, str]:
    """
    Genera un ejercicio aleatorio tipo a*x + b = 0.
    Devuelve: (enunciado, resultado_correcto, unidad, hint)
    """
    variants = [(3, 9), (-4, 8), (7, -21), (5, -10), (-6, 18), (9, -27)]
    a, b = random.choice(variants)
    expected = -b / a
    enun = f"Resuelve {a}x {b:+d} = 0. Ingresa el valor de x."
    unit = ""
    hint = "Recuerda: x = -b / a."
    return enun, expected, unit, hint


MATH_TOPICS: List[Topic] = [
    Topic(
        area="Matemáticas",
        name="Ecuación lineal (ax + b = 0)",
        explain=m_lineal_explain,
        example=m_lineal_example,
        exercise=m_lineal_exercise,
    ),
]
