# path: core/topics_math.py
"""
Temas de Matemáticas para Smart Form.

Cada tema se modela como un objeto Topic (ver core.utils) con:
- Explicación teórica (con notación LaTeX)
- Ejemplo resuelto
- Generador de ejercicios interactivos
"""

from __future__ import annotations

import math
import random
from typing import List

from .utils import Topic


# =========================================================
#  M1: Ecuación lineal (ax + b = 0)
# =========================================================

def m_lineal_explain() -> str:
    """Explicación de la ecuación lineal en una variable (usa LaTeX)."""
    return r"""
Una **ecuación lineal** en una variable tiene la forma

$$a x + b = 0, \quad a \neq 0.$$

Para despejar $x$:

1. Pasamos $b$ al otro lado:

$$a x = -b$$

2. Dividimos entre $a$:

$$x = \frac{-b}{a}.$$

Hay que tener cuidado con los signos y recordar que **no se puede dividir entre cero**.
"""


def m_lineal_example() -> tuple[str, str]:
    """Ejemplo resuelto de una ecuación lineal sencilla."""
    a, b = 2, -6
    x = -(b) / a
    enun = r"Ejemplo: resuelve la ecuación lineal $$2x - 6 = 0.$$"
    sol = (
        "Pasos:\n"
        "1. De $2x - 6 = 0$ obtenemos $2x = 6$.\n"
        "2. Dividimos entre 2: $x = 6/2 = 3$.\n\n"
        f"Resultado numérico: $x = {x:.3f}$."
    )
    return enun, sol


def m_lineal_exercise() -> tuple[str, float, str, str]:
    """
    Genera un ejercicio de ecuación lineal.

    Devuelve:
        enunciado, valor_correcto, unidad, pista
    """
    variants = [(3, 9), (-4, 8), (7, -21), (5, -10), (-6, 18), (9, -27)]
    a, b = random.choice(variants)
    expected = -(b) / a
    enun = (
        rf"Resuelve la ecuación $$ {a}x {b:+d} = 0 $$. "
        "Escribe el valor de $x$."
    )
    unit = ""
    hint = "Pasa el término independiente al otro lado y divide entre el coeficiente de x."
    return enun, expected, unit, hint


# =========================================================
#  M2: Ecuación cuadrática
# =========================================================

def m_quad_explain() -> str:
    """Explicación de la ecuación cuadrática y la fórmula general (con LaTeX)."""
    return r"""
Una **ecuación cuadrática** tiene la forma

$$a x^2 + b x + c = 0, \quad a \neq 0.$$

La solucionamos con la **fórmula general**:

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}.$$

El término

$$D = b^2 - 4ac$$

se llama **discriminante**. Según su valor:

- Si $D > 0$: hay dos raíces reales distintas.
- Si $D = 0$: hay una raíz real doble.
- Si $D < 0$: no hay raíces reales (las soluciones son complejas).
"""


def m_quad_example() -> tuple[str, str]:
    """Ejemplo resuelto de una ecuación cuadrática sencilla."""
    a, b, c = 1, -3, 2
    D = b * b - 4 * a * c
    x1 = (-b - math.sqrt(D)) / (2 * a)
    x2 = (-b + math.sqrt(D)) / (2 * a)
    enun = r"Ejemplo: resuelve la ecuación cuadrática $$x^2 - 3x + 2 = 0.$$"
    sol = (
        "Datos: $a = 1$, $b = -3$, $c = 2$.\n\n"
        "1. Discriminante: $D = b^2 - 4ac = 9 - 8 = 1$.\n"
        "2. Fórmula general:\n"
        r"$x = \dfrac{-b \pm \sqrt{D}}{2a} = \dfrac{3 \pm \sqrt{1}}{2}$.\n"
        "3. Por tanto, $x_1 = 1$ y $x_2 = 2$.\n\n"
        f"Numéricamente: $x_1 = {x1:.3f}$, $x_2 = {x2:.3f}$."
    )
    return enun, sol


def m_quad_exercise() -> tuple[str, float, str, str]:
    """
    Genera un ejercicio de ecuación cuadrática.

    Se pide la raíz más pequeña $x_{\\min}$. Todos los casos tienen soluciones reales.
    """
    # Estos coeficientes producen raíces reales y no triviales (no todas enteras).
    presets = [
        (1, -5, 6),   # raíces 2 y 3
        (2, 5, -3),   # raíces aproximadamente -3 y 0.5
        (1, -4, 3),   # raíces 1 y 3
        (1, -2, -8),  # raíces 4 y -2
    ]
    a, b, c = random.choice(presets)
    D = float(b * b - 4 * a * c)
    if D < 0:
        D = 0.0

    x1 = (-b - math.sqrt(D)) / (2.0 * a)
    x2 = (-b + math.sqrt(D)) / (2.0 * a)
    xs = min(x1, x2)

    enun = (
        rf"Resuelve la ecuación $$ {a}x^2 {b:+d}x {c:+d} = 0 $$. "
        "Escribe la raíz más pequeña $x_{\\min}$."
    )
    unit = ""
    hint = (
        "Aplica la fórmula general $x = [-b \\pm \\sqrt{b^2 - 4ac}]/(2a)$ "
        "y quédate con el valor numérico más pequeño."
    )
    return enun, xs, unit, hint


# =========================================================
#  M3: Teorema de Pitágoras (c² = a² + b²)
# =========================================================

def m_pitagoras_explain() -> str:
    """Explicación del teorema de Pitágoras en un triángulo rectángulo."""
    return r"""
En un **triángulo rectángulo** se cumple el teorema de Pitágoras:

$$c^2 = a^2 + b^2,$$

donde:
- $c$ es la **hipotenusa** (el lado opuesto al ángulo recto),
- $a$ y $b$ son los **catetos**.

Si conoces los catetos $a$ y $b$, la hipotenusa se calcula como

$$c = \sqrt{a^2 + b^2}.$$
"""


def m_pitagoras_example() -> tuple[str, str]:
    """Ejemplo de cálculo de hipotenusa con catetos conocidos."""
    a, b = 6, 8
    c = math.sqrt(a * a + b * b)
    enun = (
        "Ejemplo: en un triángulo rectángulo los catetos valen "
        "$a = 6$ y $b = 8$. Calcula la hipotenusa $c$."
    )
    sol = (
        "Aplicamos Pitágoras: $c = \\sqrt{a^2 + b^2}$.\n"
        "$c = \\sqrt{6^2 + 8^2} = \\sqrt{36 + 64} = \\sqrt{100} = 10$.\n\n"
        f"Resultado numérico: $c = {c:.3f}$."
    )
    return enun, sol


def m_pitagoras_exercise() -> tuple[str, float, str, str]:
    """Genera un ejercicio de Pitágoras pidiendo la hipotenusa."""
    variants = [(3, 4), (5, 12), (7, 24), (9, 40), (8, 15), (12, 16)]
    a, b = random.choice(variants)
    c = math.sqrt(a * a + b * b)
    enun = (
        rf"En un triángulo rectángulo, $a = {a}$ y $b = {b}$. "
        "Calcula la hipotenusa $c$ usando $c = \\sqrt{a^2 + b^2}$."
    )
    unit = ""
    hint = "Eleva cada cateto al cuadrado, súmalos y extrae la raíz cuadrada."
    return enun, c, unit, hint


# =========================================================
#  M4: Pendiente entre dos puntos
# =========================================================

def m_slope_explain() -> str:
    """Explicación de la pendiente de una recta a partir de dos puntos."""
    return r"""
La **pendiente** $m$ de una recta que pasa por dos puntos
$(x_1, y_1)$ y $(x_2, y_2)$ se calcula como

$$m = \frac{y_2 - y_1}{x_2 - x_1}, \quad x_2 \neq x_1.$$

- El numerador $y_2 - y_1$ es el **cambio en $y$** ($\Delta y$).
- El denominador $x_2 - x_1$ es el **cambio en $x$** ($\Delta x$).

En resumen: la pendiente es “**subida entre avance**”.
"""


def m_slope_example() -> tuple[str, str]:
    """Ejemplo de cálculo de la pendiente a partir de dos puntos."""
    x1, y1, x2, y2 = 1, 2, 5, 10
    m = (y2 - y1) / (x2 - x1)
    enun = (
        "Ejemplo: calcula la pendiente de la recta que pasa por los puntos "
        f"$({x1}, {y1})$ y $({x2}, {y2})$."
    )
    sol = (
        "Primero calculamos los cambios: $\\Delta y = 10 - 2 = 8$, "
        "$\\Delta x = 5 - 1 = 4$.\n"
        "La pendiente es $m = \\Delta y / \\Delta x = 8 / 4 = 2$.\n\n"
        f"Resultado numérico: $m = {m:.3f}$."
    )
    return enun, sol


def m_slope_exercise() -> tuple[str, float, str, str]:
    """Genera un ejercicio de pendiente entre dos puntos."""
    point_sets = [
        (0, 0, 4, 6),
        (-2, 3, 1, 12),
        (2, -1, 8, 5),
        (-3, -2, 4, 7),
        (1, 5, 7, 17),
    ]
    x1, y1, x2, y2 = random.choice(point_sets)
    m = (y2 - y1) / (x2 - x1)
    enun = (
        "Calcula la pendiente $m$ de la recta que pasa por los puntos "
        rf"$({x1}, {y1})$ y $({x2}, {y2})$.\n\n"
        "Recuerda que\n"
        "$$m = \\dfrac{y_2 - y_1}{x_2 - x_1}.$$"
    )
    unit = ""
    hint = "Calcula primero Δy y Δx, luego divide: m = Δy / Δx."
    return enun, m, unit, hint


# =========================================================
#  Lista de temas de Matemáticas
# =========================================================

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
