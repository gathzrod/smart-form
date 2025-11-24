# path: core/utils.py
"""
Utilidades centrales de Smart Form.

Este módulo define:
- La estructura Topic (representa un tema con sus funciones asociadas)
- El manejo del historial en session_state
- La evaluación numérica con tolerancia relativa
- La exportación del historial a CSV

Estas funciones son utilizadas tanto en los ejercicios interactivos
como en el modo de examen PRUEBATE.
"""

from __future__ import annotations

import io
import time
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

import pandas as pd
import streamlit as st


# =========================================================
#  DEFINICIÓN DEL TIPO Topic
# =========================================================

@dataclass
class Topic:
    """
    Representa un tema académico (Matemáticas, Física, Química).

    Cada tema contiene:
    - Una explicación teórica (explain)
    - Un ejemplo resuelto (example)
    - Un generador de ejercicios (exercise)

    Las funciones deben devolver siempre:
      explain()  -> str
      example()  -> (str, str)
      exercise() -> (enunciado: str,
                      valor_correcto: float,
                      unidad: str,
                      pista: str)
    """
    area: str
    name: str
    explain: Callable[[], str]
    example: Callable[[], Tuple[str, str]]
    exercise: Callable[[], Tuple[str, float, str, str]]


# =========================================================
#  MANEJO DEL HISTORIAL EN SESSION_STATE
# =========================================================

def ensure_history_initialized() -> None:
    """
    Garantiza que st.session_state tenga un contenedor `history`
    para almacenar los intentos de ejercicios.
    """
    if "history" not in st.session_state:
        st.session_state.history: List[Dict] = []


def add_history(area: str, tema: str, tipo: str,
                correcto: float, usuario: float, acierto: bool) -> None:
    """
    Agrega un intento al historial.

    Cada registro guarda:
    - fecha/hora del intento
    - área y tema
    - tipo de ejercicio (normal o PRUEBATE)
    - valor correcto y respuesta del usuario
    - si fue acierto o no
    """
    ensure_history_initialized()
    st.session_state.history.append(
        {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "area": area,
            "tema": tema,
            "tipo": tipo,
            "correcto": round(correcto, 6),
            "usuario": round(usuario, 6),
            "resultado": "ACIERTO" if acierto else "ERROR",
        }
    )


def get_history_df() -> pd.DataFrame:
    """
    Devuelve el historial como DataFrame.

    Si no hay registros aún, se devuelve un DataFrame vacío con
    las columnas correctas para evitar errores en Streamlit.
    """
    ensure_history_initialized()

    if not st.session_state.history:
        return pd.DataFrame(
            columns=[
                "timestamp",
                "area",
                "tema",
                "tipo",
                "correcto",
                "usuario",
                "resultado",
            ]
        )

    return pd.DataFrame(st.session_state.history)


def clear_history() -> None:
    """Elimina todo el historial almacenado en session_state."""
    ensure_history_initialized()
    st.session_state.history.clear()


def history_to_csv(df: pd.DataFrame) -> bytes:
    """
    Convierte un DataFrame de historial a formato CSV (bytes)
    para descarga mediante download_button.
    """
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue().encode("utf-8")


# =========================================================
#  EVALUACIÓN NUMÉRICA CON TOLERANCIA
# =========================================================

def within_tol(expected: float, user: float, tol_pct: float) -> bool:
    """
    Compara el resultado del usuario contra el valor correcto usando tolerancia.

    La tolerancia es relativa, pero con un mínimo absoluto para evitar
    problemas cuando expected es muy pequeño o cero.

        tol = max(|expected| * tol_pct, 1e-6)

    Retorna True si |user - expected| <= tol.
    """
    tol = max(abs(expected) * tol_pct, 1e-6)
    return abs(user - expected) <= tol
