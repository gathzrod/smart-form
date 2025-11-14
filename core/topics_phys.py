# path: core/topics_phys.py
from __future__ import annotations

import random
from typing import List

from .utils import Topic


# ---------- F1: Velocidad media (v = d / t) ----------


def f_vel_media_explain() -> str:
    return (
        "La velocidad media relaciona el desplazamiento recorrido con el tiempo que tarda:\n"
        "  v = d / t\n\n"
        "d es el desplazamiento (en metros si usamos el SI) y t es el tiempo (en segundos).\n"
        "La velocidad media se expresa en m/s.\n\n"
        "No hay que confundir desplazamiento con distancia total: aquí interesa el cambio neto "
        "de posición entre el punto inicial y el final."
    )


def f_vel_media_example() -> tuple[str, str]:
    d, t = 150.0, 30.0
    v = d / t
    enun = "Ejemplo: un objeto recorre 150 m en 30 s. Calcula la velocidad media."
    sol = (
        "Aplicamos la fórmula v = d / t:\n"
        f"  v = 150 m / 30 s = 5 m/s.\n\n"
        f"Resultado numérico: v = {v:.3f} m/s."
    )
    return enun, sol


def f_vel_media_exercise() -> tuple[str, float, str, str]:
    pairs = [(100, 20), (250, 50), (300, 30), (420, 21), (180, 12)]
    d, t = random.choice(pairs)
    expected = d / t
    enun = f"Un móvil se desplaza {d} m en {t} s. Calcula la velocidad media en m/s."
    unit = "m/s"
    hint = "Recuerda: v = d / t (usa metros y segundos)."
    return enun, expected, unit, hint


# ---------- F2: Energía cinética (Ec = 1/2 m v^2) ----------


def f_ec_explain() -> str:
    return (
        "La energía cinética es la energía asociada al movimiento de un objeto:\n"
        "  Ec = 1/2 · m · v²\n\n"
        "m es la masa (en kg) y v la rapidez (en m/s). El resultado se expresa en joules (J).\n"
        "Cuanto mayor sea la masa o la velocidad, mayor será la energía cinética."
    )


def f_ec_example() -> tuple[str, str]:
    m, v = 2.0, 3.0
    ec = 0.5 * m * v * v
    enun = "Ejemplo: una masa de 2 kg se mueve a 3 m/s. Calcula la energía cinética."
    sol = (
        "Aplicamos Ec = 1/2·m·v²:\n"
        "  Ec = 1/2 · 2 kg · (3 m/s)² = 1 · 9 = 9 J.\n\n"
        f"Resultado numérico: Ec = {ec:.3f} J."
    )
    return enun, sol


def f_ec_exercise() -> tuple[str, float, str, str]:
    sets = [(1.5, 4.0), (3.0, 2.5), (5.0, 6.0), (2.2, 7.5), (4.5, 3.3)]
    m, v = random.choice(sets)
    expected = 0.5 * m * v * v
    enun = f"Un objeto de masa {m:.1f} kg se mueve a {v:.1f} m/s. Calcula Ec en joules."
    unit = "J"
    hint = "Eleva la velocidad al cuadrado y luego multiplica por 1/2 · m."
    return enun, expected, unit, hint


# ---------- F3: Ley de Ohm (V = I·R) ----------


def f_ohm_explain() -> str:
    return (
        "La ley de Ohm relaciona voltaje, corriente y resistencia:\n"
        "  V = I · R\n\n"
        "V se mide en volts (V), I en amperes (A) y R en ohms (Ω).\n"
        "Formas despejadas:\n"
        "  I = V / R\n"
        "  R = V / I"
    )


def f_ohm_example() -> tuple[str, str]:
    I, R = 2.0, 10.0
    V = I * R
    enun = "Ejemplo: por una resistencia de 10 Ω circulan 2 A. Calcula el voltaje."
    sol = (
        "Usamos V = I·R:\n"
        "  V = 2 A · 10 Ω = 20 V.\n\n"
        f"Resultado numérico: V = {V:.3f} V."
    )
    return enun, sol


def f_ohm_exercise() -> tuple[str, float, str, str]:
    mode = random.choice(["V", "I", "R"])

    if mode == "V":
        I, R = 3.0, 15.0
        expected = I * R
        enun = (
            f"Por una resistencia de {R:.1f} Ω circula una corriente de {I:.1f} A.\n"
            "Calcula el voltaje V."
        )
        unit = "V"
        hint = "Usa V = I · R."
    elif mode == "I":
        V, R = 48.0, 12.0
        expected = V / R
        enun = (
            f"En un circuito hay un voltaje de {V:.1f} V y una resistencia de {R:.1f} Ω.\n"
            "Calcula la corriente I."
        )
        unit = "A"
        hint = "Usa I = V / R."
    else:
        V, I = 24.0, 3.0
        expected = V / I
        enun = (
            f"En un circuito hay un voltaje de {V:.1f} V y una corriente de {I:.1f} A.\n"
            "Calcula la resistencia R."
        )
        unit = "Ω"
        hint = "Usa R = V / I."

    return enun, expected, unit, hint


# ---------- F4: MRUA sencillo (v = v0 + a·t) ----------


def f_mrua_explain() -> str:
    return (
        "En un movimiento rectilíneo con aceleración constante, la velocidad cambia linealmente:\n"
        "  v = v0 + a·t\n\n"
        "v0 es la velocidad inicial, a la aceleración y t el tiempo. Todas en unidades coherentes "
        "(por ejemplo m/s para velocidades y m/s² para aceleración)."
    )


def f_mrua_example() -> tuple[str, str]:
    v0, a, t = 5.0, 2.0, 3.0
    v = v0 + a * t
    enun = "Ejemplo: un móvil parte con 5 m/s y acelera 2 m/s² durante 3 s. Calcula la velocidad final."
    sol = (
        "Aplicamos v = v0 + a·t:\n"
        "  v = 5 m/s + 2 m/s² · 3 s = 5 + 6 = 11 m/s.\n\n"
        f"Resultado numérico: v = {v:.3f} m/s."
    )
    return enun, sol


def f_mrua_exercise() -> tuple[str, float, str, str]:
    v0_values = [2.0, 4.0, 6.0]
    a_values = [1.0, 1.5, 2.0]
    t_values = [3.0, 4.0, 5.0]
    v0 = random.choice(v0_values)
    a = random.choice(a_values)
    t = random.choice(t_values)

    expected = v0 + a * t
    enun = (
        f"Un móvil parte con velocidad inicial v0 = {v0:.1f} m/s y acelera a = {a:.1f} m/s² "
        f"durante t = {t:.1f} s.\n"
        "Calcula la velocidad final v."
    )
    unit = "m/s"
    hint = "Aplica v = v0 + a·t con todas las magnitudes en unidades coherentes."
    return enun, expected, unit, hint


# ---------- Lista de temas de Física ----------

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
