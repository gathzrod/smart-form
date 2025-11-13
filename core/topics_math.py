# path: core/topics_math.py
from __future__ import annotations

import random
from typing import List

from .utils import Topic


def m_lineal_explain() -> str:
    """
    Explicación de ecuación lineal con tono más de libro que de IA.
    """
    return (
        "Una ecuación lineal en una variable es una expresión del tipo a·x + b = 0, "
        "donde a y b son números reales y a no puede ser 0.\n\n"
        "La idea es encontrar el valor de x que hace verdadera la igualdad. "
        "Para ello se pasa b al otro lado cambiando de signo y después se divide entre a:\n"
        "  a·x + b = 0  →  a·x = -b  →  x = -b / a.\n\n"
        "Detalles importantes:\n"
        "- Si a = 0, la expresión deja de ser una ecuación lineal en x.\n"
        "- Hay que cuidar los signos al mover términos (por ejemplo, -(-6) = +6).\n"
        "- El resultado puede ser un número positivo, negativo o fraccionario."
    )


def m_lineal_example() -> tuple[str, str]:
    a, b = 2, -6
    x = -b / a
    enun = "Ejemplo: Resuelve la ecuación 2x - 6 = 0."
    sol = (
        "Primero pasamos el -6 al otro lado sumando 6 en ambos lados:\n"
        "  2x - 6 = 0  →  2x = 6.\n"
        "Luego dividimos entre 2:\n"
        "  x = 6 / 2 = 3.\n\n"
        f"Resultado numérico: x = {x:.3f}."
    )
    return enun, sol


def m_lineal_exercise() -> tuple[str, float, str, str]:
    """
    Genera un ejercicio aleatorio tipo a·x + b = 0.
    Devuelve: (enunciado, resultado_correcto, unidad, hint)
    """
    variants = [(3, 9), (-4, 8), (7, -21), (5, -10), (-6, 18), (9, -27)]
    a, b = random.choice(variants)
    expected = -b / a
    enun = f"Resuelve {a}x {b:+d} = 0. Ingresa el valor de x."
    unit = ""
    hint = "Piensa en: a·x + b = 0 → a·x = -b → x = -b / a."
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
