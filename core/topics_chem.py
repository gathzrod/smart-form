# ============================
# path: core/topics_chem.py
# ============================
from __future__ import annotations

import random
from typing import List

from .utils import Topic


# ---------- Q1: Molaridad (M = n / V) ----------


def q_molar_explain() -> str:
    return (
        "La molaridad M indica cuántos moles de soluto hay en cada litro de solución:\n"
        "  M = n / V\n\n"
        "n es el número de moles de soluto y V el volumen de la solución en litros.\n"
        "La unidad de M es mol/L, que se suele escribir simplemente como 'M'."
    )


def q_molar_example() -> tuple[str, str]:
    n, V = 0.50, 0.25
    M = n / V
    enun = "Ejemplo: una solución contiene 0.50 mol de soluto disueltos en 0.25 L. Calcula la molaridad."
    sol = (
        "Usamos M = n / V:\n"
        "  M = 0.50 mol / 0.25 L = 2.0 mol/L.\n\n"
        f"Resultado numérico: M = {M:.3f} M."
    )
    return enun, sol


def q_molar_exercise() -> tuple[str, float, str, str]:
    pairs = [(0.75, 0.50), (0.20, 0.80), (0.90, 0.30), (0.30, 0.60), (0.44, 0.22)]
    n, V = random.choice(pairs)
    expected = n / V
    enun = (
        f"En una solución hay {n:.2f} mol de soluto disueltos en {V:.2f} L de solución.\n"
        "Calcula la molaridad M en mol/L."
    )
    unit = "M"
    hint = "Convierte a litros si fuera necesario y aplica M = n / V."
    return enun, expected, unit, hint


# ---------- Q2: Masa ↔ moles (n = m / M) ----------


def q_moles_explain() -> str:
    return (
        "Para relacionar masa y cantidad de sustancia usamos la masa molar M (g/mol):\n"
        "  n = m / M\n\n"
        "m es la masa de la muestra en gramos y M la masa molar de la sustancia en g/mol.\n"
        "El resultado n se expresa en moles.\n"
        "También se puede despejar m = n · M."
    )


def q_moles_example() -> tuple[str, str]:
    m, M_molar = 18.0, 18.0  # agua aprox.
    n = m / M_molar
    enun = "Ejemplo: ¿cuántos moles hay en 18 g de agua (M ≈ 18 g/mol)?"
    sol = (
        "Aplicamos n = m / M:\n"
        "  n = 18 g / (18 g/mol) = 1 mol.\n\n"
        f"Resultado numérico: n = {n:.3f} mol."
    )
    return enun, sol


def q_moles_exercise() -> tuple[str, float, str, str]:
    sets = [
        (12.0, 12.0),   # C
        (58.5, 58.5),   # NaCl aprox.
        (32.0, 16.0),   # O2
        (36.5, 36.5),   # HCl aprox.
        (98.0, 49.0),   # H2SO4/2, etc. (solo valores prácticos)
    ]
    m, M_molar = random.choice(sets)
    expected = m / M_molar
    enun = (
        f"Una muestra tiene una masa m = {m:.1f} g de cierta sustancia con masa molar M = {M_molar:.1f} g/mol.\n"
        "Calcula n en moles."
    )
    unit = "mol"
    hint = "Usa n = m / M (masa en g y masa molar en g/mol)."
    return enun, expected, unit, hint


# ---------- Q3: Densidad (ρ = m / V) ----------


def q_density_explain() -> str:
    return (
        "La densidad ρ relaciona la masa de una sustancia con el volumen que ocupa:\n"
        "  ρ = m / V\n\n"
        "En química es común usar g/mL o g/cm³.\n"
        "m es la masa (en g) y V el volumen (en mL o cm³, según el caso)."
    )


def q_density_example() -> tuple[str, str]:
    m, V = 10.0, 5.0
    rho = m / V
    enun = "Ejemplo: una muestra tiene masa de 10 g y volumen de 5 mL. Calcula la densidad."
    sol = (
        "Aplicamos ρ = m / V:\n"
        "  ρ = 10 g / 5 mL = 2 g/mL.\n\n"
        f"Resultado numérico: ρ = {rho:.3f} g/mL."
    )
    return enun, sol


def q_density_exercise() -> tuple[str, float, str, str]:
    sets = [(50, 25), (125, 100), (84, 42), (63, 21), (180, 90)]
    m, V = random.choice(sets)
    expected = m / V
    enun = (
        f"Una sustancia tiene masa m = {m:.0f} g y ocupa un volumen V = {V:.0f} mL.\n"
        "Calcula la densidad ρ en g/mL."
    )
    unit = "g/mL"
    hint = "Solo divide masa entre volumen: ρ = m / V."
    return enun, expected, unit, hint


# ---------- Q4: Dilución (M1 V1 = M2 V2) ----------


def q_dilution_explain() -> str:
    return (
        "En una dilución se conserva la cantidad de soluto, por eso se cumple:\n"
        "  M1 · V1 = M2 · V2\n\n"
        "M1 y V1 son concentración y volumen iniciales; M2 y V2 los finales.\n"
        "Si conoces tres de las variables, puedes despejar la cuarta:\n"
        "  M2 = M1·V1 / V2,   V2 = M1·V1 / M2,   V1 = M2·V2 / M1."
    )


def q_dilution_example() -> tuple[str, str]:
    M1, V1, V2 = 2.0, 25.0, 100.0
    M2 = (M1 * V1) / V2
    enun = (
        "Ejemplo: se diluyen 25 mL de una solución 2.0 M hasta un volumen final de 100 mL.\n"
        "Calcula la nueva concentración M2."
    )
    sol = (
        "Usamos M1·V1 = M2·V2, despejando M2:\n"
        "  M2 = M1·V1 / V2 = 2.0·25 / 100 = 0.5 M.\n\n"
        f"Resultado numérico: M2 = {M2:.3f} M."
    )
    return enun, sol


def q_dilution_exercise() -> tuple[str, float, str, str]:
    mode = random.choice(["M2", "V2", "V1"])

    if mode == "M2":
        M1, V1, V2 = 1.5, 40.0, 200.0
        expected = (M1 * V1) / V2
        enun = (
            f"Se diluyen {V1:.0f} mL de una solución {M1:.1f} M hasta un volumen final de {V2:.0f} mL.\n"
            "Calcula la nueva concentración M2."
        )
        unit = "M"
        hint = "Despeja M2 = M1·V1 / V2."
    elif mode == "V2":
        M1, V1, M2 = 3.0, 20.0, 0.5
        expected = (M1 * V1) / M2
        enun = (
            f"Se tienen {V1:.0f} mL de una solución {M1:.1f} M y se desea obtener una solución {M2:.1f} M.\n"
            "¿A qué volumen final V2 se debe diluir?"
        )
        unit = "mL"
        hint = "Despeja V2 = M1·V1 / M2."
    else:  # V1
        M1, V2, M2 = 1.2, 150.0, 0.4
        expected = (M2 * V2) / M1
        enun = (
            f"Se quiere preparar {V2:.0f} mL de una solución {M2:.1f} M a partir de una solución "
            f"{M1:.1f} M.\n"
            "¿Qué volumen V1 de la solución concentrada se debe tomar?"
        )
        unit = "mL"
        hint = "Despeja V1 = M2·V2 / M1."

    return enun, expected, unit, hint


# ---------- Lista de temas de Química ----------

CHM_TOPICS: List[Topic] = [
    Topic(
        area="Química",
        name="Molaridad (M = n / V)",
        explain=q_molar_explain,
        example=q_molar_example,
        exercise=q_molar_exercise,
    ),
    Topic(
        area="Química",
        name="Masa ↔ moles (n = m / M)",
        explain=q_moles_explain,
        example=q_moles_example,
        exercise=q_moles_exercise,
    ),
    Topic(
        area="Química",
        name="Densidad (ρ = m / V)",
        explain=q_density_explain,
        example=q_density_example,
        exercise=q_density_exercise,
    ),
    Topic(
        area="Química",
        name="Dilución (M1 V1 = M2 V2)",
        explain=q_dilution_explain,
        example=q_dilution_example,
        exercise=q_dilution_exercise,
    ),
]

