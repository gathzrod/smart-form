# path: core/topics_phys.py
"""
Temas de Física para Smart Form.

Cada tema se modela como un objeto Topic (ver core.utils) con:
- Explicación teórica (con algo de notación LaTeX)
- Ejemplo resuelto
- Generador de ejercicios interactivos
"""

from __future__ import annotations

import random
from typing import List

from .utils import Topic


# =========================================================
#  F1: Velocidad media  (v = d / t)
# =========================================================

def f_vel_media_explain() -> str:
    """Explicación de velocidad media con notación LaTeX."""
    return r"""
La **velocidad media** relaciona el desplazamiento recorrido con el tiempo empleado:

$$v = \frac{d}{t}$$

donde:
- $d$ es el desplazamiento (en metros, m),
- $t$ es el tiempo (en segundos, s).

La velocidad media se expresa normalmente en m/s.
"""


def f_vel_media_example() -> tuple[str, str]:
    """Ejemplo resuelto de velocidad media."""
    d, t = 150.0, 30.0
    v = d / t
    enun = (
        "Ejemplo: un objeto recorre $150\\,\\text{m}$ en $30\\,\\text{s}$. "
        "Calcula la velocidad media."
    )
    sol = (
        "Aplicamos la fórmula $v = d/t$:\n"
        "$$v = \\dfrac{150\\,\\text{m}}{30\\,\\text{s}} = 5\\,\\text{m/s}.$$\n\n"
        f"Resultado numérico: $v = {v:.3f}\\,\\text{{m/s}}$."
    )
    return enun, sol


def f_vel_media_exercise() -> tuple[str, float, str, str]:
    """
    Genera un ejercicio de velocidad media.

    Devuelve:
        enunciado, valor_correcto, unidad, pista
    """
    pairs = [(100, 20), (250, 50), (300, 30), (420, 21), (180, 12), (125, 25)]
    d, t = random.choice(pairs)
    expected = d / t
    enun = (
        f"Un móvil se desplaza $d = {d}\\,\\text{{m}}$ en "
        f"$t = {t}\\,\\text{{s}}$. Calcula la velocidad media $v$ en m/s."
    )
    unit = "m/s"
    hint = "Escribe v = d/t y sustituye usando metros y segundos."
    return enun, expected, unit, hint


# =========================================================
#  F2: Energía cinética  (Ec = 1/2 m v²)
# =========================================================

def f_ec_explain() -> str:
    """Explicación de energía cinética con LaTeX."""
    return r"""
La **energía cinética** es la energía asociada al movimiento de un objeto:

$$E_c = \frac{1}{2} m v^2$$

donde:
- $m$ es la masa (en kilogramos, kg),
- $v$ es la rapidez (en m/s).

La energía cinética se mide en **joules** (J).

Si aumenta la masa o la rapidez, la energía cinética también aumenta.
"""


def f_ec_example() -> tuple[str, str]:
    """Ejemplo resuelto de energía cinética."""
    m, v = 2.0, 3.0
    ec = 0.5 * m * v * v
    enun = (
        "Ejemplo: una masa de $2\\,\\text{kg}$ se mueve con rapidez "
        "$3\\,\\text{m/s}$. Calcula la energía cinética."
    )
    sol = (
        "Aplicamos $E_c = \\tfrac12 m v^2$:\n"
        "$$E_c = \\tfrac12 \\cdot 2\\,\\text{kg} \\cdot (3\\,\\text{m/s})^2 "
        "= 1 \\cdot 9 = 9\\,\\text{J}.$$\n\n"
        f"Resultado numérico: $E_c = {ec:.3f}\\,\\text{{J}}$."
    )
    return enun, sol


def f_ec_exercise() -> tuple[str, float, str, str]:
    """Genera un ejercicio de energía cinética."""
    sets = [(1.5, 4.0), (3.0, 2.5), (5.0, 6.0), (2.2, 7.5), (4.5, 3.3)]
    m, v = random.choice(sets)
    expected = 0.5 * m * v * v
    enun = (
        f"Un objeto de masa $m = {m:.1f}\\,\\text{{kg}}$ se mueve a "
        f"$v = {v:.1f}\\,\\text{{m/s}}$. Calcula la energía cinética $E_c$ en J."
    )
    unit = "J"
    hint = "Eleva la velocidad al cuadrado y luego multiplica por (1/2)·m."
    return enun, expected, unit, hint


# =========================================================
#  F3: Ley de Ohm  (V = I · R)
# =========================================================

def f_ohm_explain() -> str:
    """Explicación de la ley de Ohm con LaTeX."""
    return r"""
La **ley de Ohm** relaciona voltaje, corriente y resistencia eléctrica:

$$V = I * R$$

donde:
- $V$ es el voltaje (en volts, V),
- $I$ es la corriente (en amperes, A),
- $R$ es la resistencia (en ohms).
"""


def f_ohm_example() -> tuple[str, str]:
    """Ejemplo resuelto de ley de Ohm."""
    I, R = 2.0, 10.0
    V = I * R
    enun = (
        "Ejemplo: por una resistencia de $10\\,\\Omega$ circula una corriente "
        "de $2\\,\\text{A}$. Calcula el voltaje."
    )
    sol = (
        "Usamos $V = I R$:\n"
        "$$V = 2\\,\\text{A} \\cdot 10\\,\\Omega = 20\\,\\text{V}.$$\n\n"
        f"Resultado numérico: $V = {V:.3f}\\,\\text{{V}}$."
    )
    return enun, sol


def f_ohm_exercise() -> tuple[str, float, str, str]:
    """
    Genera un ejercicio de ley de Ohm.

    El modo elige aleatoriamente si se pide V, I o R.
    """
    mode = random.choice(["V", "I", "R"])

    if mode == "V":
        I, R = 3.0, 15.0
        expected = I * R
        enun = (
            f"Por una resistencia de $R = {R:.1f}\\,\\Omega$ circula una corriente "
            f"de $I = {I:.1f}\\,\\text{{A}}$. Calcula el voltaje $V$."
        )
        unit = "V"
        hint = "Escribe V = I·R y sustituye los valores."
    elif mode == "I":
        V, R = 48.0, 12.0
        expected = V / R
        enun = (
            f"En un circuito hay un voltaje de $V = {V:.1f}\\,\\text{{V}}$ y una "
            f"resistencia de $R = {R:.1f}\\,\\Omega$. Calcula la corriente $I$."
        )
        unit = "A"
        hint = "Despeja I = V/R."
    else:
        V, I = 24.0, 3.0
        expected = V / I
        enun = (
            f"En un circuito hay un voltaje de $V = {V:.1f}\\,\\text{{V}}$ y una "
            f"corriente de $I = {I:.1f}\\,\\text{{A}}$. Calcula la resistencia $R$."
        )
        unit = "Ω"
        hint = "Despeja R = V/I."

    return enun, expected, unit, hint


# =========================================================
#  F4: MRUA básico  (v = v0 + a·t)
# =========================================================

def f_mrua_explain() -> str:
    """Explicación de MRUA (velocidad final) con LaTeX."""
    return r"""
En un **movimiento rectilíneo uniformemente acelerado (MRUA)** la velocidad cambia
de forma lineal con el tiempo:

$$v = v_0 + a t$$

donde:
- $v_0$ es la velocidad inicial,
- $a$ es la aceleración (constante),
- $t$ es el tiempo transcurrido.

Si usamos el SI:
- velocidades en m/s,
- aceleración en m/s²,
- tiempo en segundos (s),
entonces $v$ también queda en m/s.
"""


def f_mrua_example() -> tuple[str, str]:
    """Ejemplo resuelto de MRUA (cálculo de velocidad final)."""
    v0, a, t = 5.0, 2.0, 3.0
    v = v0 + a * t
    enun = (
        "Ejemplo: un móvil parte con velocidad inicial "
        "$v_0 = 5\\,\\text{m/s}$ y acelera con $a = 2\\,\\text{m/s}^2$ "
        "durante $t = 3\\,\\text{s}$. Calcula la velocidad final $v$."
    )
    sol = (
        "Aplicamos $v = v_0 + a t$:\n"
        "$$v = 5\\,\\text{m/s} + 2\\,\\text{m/s}^2 \\cdot 3\\,\\text{s} "
        "= 5 + 6 = 11\\,\\text{m/s}.$$\n\n"
        f"Resultado numérico: $v = {v:.3f}\\,\\text{{m/s}}$."
    )
    return enun, sol


def f_mrua_exercise() -> tuple[str, float, str, str]:
    """Genera un ejercicio de MRUA pidiendo la velocidad final."""
    v0_values = [2.0, 4.0, 6.0]
    a_values = [1.0, 1.5, 2.0]
    t_values = [3.0, 4.0, 5.0]

    v0 = random.choice(v0_values)
    a = random.choice(a_values)
    t = random.choice(t_values)

    expected = v0 + a * t
    enun = (
        f"Un móvil parte con velocidad inicial $v_0 = {v0:.1f}\\,\\text{{m/s}}$ y "
        f"acelera con $a = {a:.1f}\\,\\text{{m/s}}^2$ durante "
        f"$t = {t:.1f}\\,\\text{{s}}$.\n"
        "Calcula la velocidad final $v$."
    )
    unit = "m/s"
    hint = "Sustituye en la expresión v = v0 + a·t usando unidades coherentes."
    return enun, expected, unit, hint


# =========================================================
#  Lista de temas de Física
# =========================================================

PHYS_TOPICS: List[Topic] = [
    Topic(
        area="Física",
        name="Velocidad media (v = d / t)",
        explain=f_vel_media_explain,
        example=f_vel_media_example,
        exercise=f_vel_media_exercise,
    ),
    Topic(
        area="Física",
        name="Energía cinética (Ec = 1/2 m v²)",
        explain=f_ec_explain,
        example=f_ec_example,
        exercise=f_ec_exercise,
    ),
    Topic(
        area="Física",
        name="Ley de Ohm (V = I·R)",
        explain=f_ohm_explain,
        example=f_ohm_example,
        exercise=f_ohm_exercise,
    ),
    Topic(
        area="Física",
        name="MRUA básico (v = v0 + a·t)",
        explain=f_mrua_explain,
        example=f_mrua_example,
        exercise=f_mrua_exercise,
    ),
]
