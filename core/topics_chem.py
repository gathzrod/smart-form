# ============================
# path: core/topics_chem.py
# ============================
"""
Temas de Química para Smart Form.

Incluye:
- Explicación teórica con LaTeX limpio.
- Ejemplo resuelto.
- Generador de ejercicios interactivos.
"""

from __future__ import annotations

import random
from typing import List

from .utils import Topic


# =========================================================
#  Q1: Molaridad (M = n/V)
# =========================================================

def q_molar_explain() -> str:
    """Explicación de molaridad con notación LaTeX."""
    return r"""
La **molaridad** $M$ indica cuántos moles de soluto hay por litro de solución:

$$M = \frac{n}{V}$$

donde:
- $n$ = cantidad de soluto en moles,
- $V$ = volumen de la solución en litros (L).

La unidad de molaridad es $\text{mol/L}$ o simplemente **M**.
"""


def q_molar_example() -> tuple[str, str]:
    """Ejemplo resuelto de molaridad."""
    n, V = 0.50, 0.25
    M = n / V
    enun = (
        "Ejemplo: una solución contiene $0.50\\,\\text{mol}$ de soluto en "
        "$0.25\\,\\text{L}$. Calcula la molaridad."
    )
    sol = (
        "Aplicamos $M = n/V$:\n"
        "$$M = \\frac{0.50}{0.25} = 2.0\\,\\text{mol/L}.$$\n\n"
        f"Resultado numérico: $M = {M:.3f}\\,\\text{{M}}$."
    )
    return enun, sol


def q_molar_exercise() -> tuple[str, float, str, str]:
    """Genera un ejercicio de molaridad."""
    pairs = [(0.75, 0.50), (0.20, 0.80), (0.90, 0.30), (0.30, 0.60), (0.44, 0.22)]
    n, V = random.choice(pairs)
    expected = n / V
    enun = (
        f"Una solución contiene $n = {n:.2f}\\,\\text{{mol}}$ de soluto en "
        f"$V = {V:.2f}\\,\\text{{L}}$. Calcula la molaridad $M$."
    )
    unit = "M"
    hint = "Divide los moles entre los litros: $M = n/V$."
    return enun, expected, unit, hint


# =========================================================
#  Q2: Masa ↔ moles (n = m/M)
# =========================================================

def q_moles_explain() -> str:
    """Explicación de relación masa ↔ moles."""
    return r"""
Para convertir masa en moles usamos la **masa molar** $M$:

$$n = \frac{m}{M}$$

donde:
- $m$ = masa en gramos (g),
- $M$ = masa molar en g/mol.

El resultado $n$ queda en moles.  
También puede despejarse:

- $m = nM$
"""


def q_moles_example() -> tuple[str, str]:
    """Ejemplo resuelto de masa ↔ moles."""
    m, M_molar = 18.0, 18.0  # agua aprox.
    n = m / M_molar
    enun = "Ejemplo: ¿cuántos moles hay en $18\\,\\text{g}$ de agua $(M\\approx18\\,\\text{g/mol})$?"
    sol = (
        "Aplicamos $n = m/M$:\n"
        "$$n = \\frac{18}{18} = 1\\,\\text{mol}.$$\n\n"
        f"Resultado: $n = {n:.3f}\\,\\text{{mol}}$."
    )
    return enun, sol


def q_moles_exercise() -> tuple[str, float, str, str]:
    """Genera un ejercicio de masa ↔ moles."""
    sets = [
        (12.0, 12.0),      # Carbono
        (58.5, 58.5),      # Sal común (aprox)
        (32.0, 32.0),      # Oxígeno O2
        (36.5, 36.5),      # HCl aprox.
        (98.0, 98.0),      # H2SO4 aprox.
    ]
    m, M_molar = random.choice(sets)
    expected = m / M_molar
    enun = (
        f"Una muestra tiene masa $m = {m:.1f}\\,\\text{{g}}$ y masa molar "
        f"$M = {M_molar:.1f}\\,\\text{{g/mol}}$. Calcula los moles $n$."
    )
    unit = "mol"
    hint = "Aplica $n = m/M$ usando gramos y g/mol."
    return enun, expected, unit, hint


# =========================================================
#  Q3: Densidad (ρ = m/V)
# =========================================================

def q_density_explain() -> str:
    """Explicación de densidad."""
    return r"""
La **densidad** $\\rho$ relaciona la masa y el volumen de una sustancia:

$$\\rho = \frac{m}{V}$$

donde:
- $m$ = masa en g,
- $V$ = volumen en mL o cm³.

Unidades comunes: **g/mL** o **g/cm³**.
"""


def q_density_example() -> tuple[str, str]:
    """Ejemplo resuelto de densidad."""
    m, V = 10.0, 5.0
    rho = m / V
    enun = "Ejemplo: una muestra tiene $m=10\\,\\text{g}$ y $V=5\\,\\text{mL}$. Calcula la densidad."
    sol = (
        "Aplicamos $\\rho = m/V$:\n"
        "$$\\rho = \\frac{10}{5} = 2\\,\\text{g/mL}.$$\n\n"
        f"Resultado: $\\rho = {rho:.3f}\\,\\text{{g/mL}}$."
    )
    return enun, sol


def q_density_exercise() -> tuple[str, float, str, str]:
    """Genera un ejercicio de densidad."""
    sets = [(50, 25), (125, 100), (84, 42), (63, 21), (180, 90)]
    m, V = random.choice(sets)
    expected = m / V
    enun = (
        f"Una sustancia tiene masa $m = {m:.0f}\\,\\text{{g}}$ y volumen "
        f"$V = {V:.0f}\\,\\text{{mL}}$. Calcula la densidad $\\rho$."
    )
    unit = "g/mL"
    hint = "Divide masa entre volumen: $\\rho = m/V$."
    return enun, expected, unit, hint


# =========================================================
#  Q4: Dilución (M₁V₁ = M₂V₂)
# =========================================================

def q_dilution_explain() -> str:
    """Explicación de diluciones."""
    return r"""
En una **dilución** la cantidad de soluto permanece constante. Por ello se cumple:

$$M_1 V_1 = M_2 V_2$$

donde:
- $M_1$, $V_1$ = molaridad y volumen iniciales,
- $M_2$, $V_2$ = molaridad y volumen finales.

Formas despejadas útiles:

- $M_2 = \dfrac{M_1 V_1}{V_2}$
- $V_2 = \dfrac{M_1 V_1}{M_2}$
- $V_1 = \dfrac{M_2 V_2}{M_1}$
"""


def q_dilution_example() -> tuple[str, str]:
    """Ejemplo resuelto de dilución."""
    M1, V1, V2 = 2.0, 25.0, 100.0
    M2 = (M1 * V1) / V2
    enun = (
        "Ejemplo: se diluyen $25\\,\\text{mL}$ de una solución $2.0\\,\\text{M}$ "
        "hasta un volumen final de $100\\,\\text{mL}$. Calcula la nueva concentración $M_2$."
    )
    sol = (
        "Usamos $M_1V_1 = M_2V_2$:\n"
        "$$M_2 = \\frac{2.0 \\cdot 25}{100} = 0.5\\,\\text{M}.$$\n\n"
        f"Resultado numérico: $M_2 = {M2:.3f}\\,\\text{{M}}$."
    )
    return enun, sol


def q_dilution_exercise() -> tuple[str, float, str, str]:
    """Genera un ejercicio de dilución."""
    mode = random.choice(["M2", "V2", "V1"])

    if mode == "M2":
        M1, V1, V2 = 1.5, 40.0, 200.0
        expected = (M1 * V1) / V2
        enun = (
            f"Se diluyen $V_1 = {V1:.0f}\\,\\text{{mL}}$ de una solución "
            f"$M_1 = {M1:.1f}\\,\\text{{M}}$ hasta un volumen final "
            f"$V_2 = {V2:.0f}\\,\\text{{mL}}$. Calcula la nueva concentración $M_2$."
        )
        unit = "M"
        hint = "Despeja $M_2 = M_1V_1/V_2$."

    elif mode == "V2":
        M1, V1, M2 = 3.0, 20.0, 0.5
        expected = (M1 * V1) / M2
        enun = (
            f"Se tienen $V_1 = {V1:.0f}\\,\\text{{mL}}$ de una solución $M_1 = {M1:.1f}\\,\\text{{M}}$ "
            f"y se desea obtener una solución $M_2 = {M2:.1f}\\,\\text{{M}}$. "
            "¿A qué volumen final $V_2$ se debe diluir?"
        )
        unit = "mL"
        hint = "Despeja $V_2 = M_1V_1/M_2$."

    else:  # V1
        M1, V2, M2 = 1.2, 150.0, 0.4
        expected = (M2 * V2) / M1
        enun = (
            f"Se quiere preparar $V_2 = {V2:.0f}\\,\\text{{mL}}$ de una solución "
            f"$M_2 = {M2:.1f}\\,\\text{{M}}$ usando una solución concentrada "
            f"$M_1 = {M1:.1f}\\,\\text{{M}}$. ¿Qué volumen $V_1$ se debe tomar?"
        )
        unit = "mL"
        hint = "Despeja $V_1 = M_2V_2/M_1$."

    return enun, expected, unit, hint


# =========================================================
#  Lista de temas de Química
# =========================================================

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
        name="Dilución (M₁ V₁ = M₂ V₂)",
        explain=q_dilution_explain,
        example=q_dilution_example,
        exercise=q_dilution_exercise,
    ),
]
