# path: core/utils.py
"""
Utilidades centrales de Smart Form.

Este módulo define:
- La estructura Topic (representa un tema con sus funciones asociadas).
- El manejo del historial en session_state.
- La evaluación numérica con tolerancia relativa.
- La exportación del historial a CSV.

Estas funciones se usan tanto en los ejercicios interactivos
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

    En lugar de tener todo el código mezclado, cada tema se modela
    como un objeto Topic que agrupa tres funciones:

    - explain(): devuelve un texto con la explicación teórica.
    - example(): devuelve el enunciado y la solución de un ejemplo resuelto.
    - exercise(): genera un nuevo ejercicio aleatorio del tema y devuelve:

        (enunciado: str,
         valor_correcto: float,
         unidad: str,
         pista: str)

    Esto permite que la lógica de Smart Form (app.py) trate todos los temas
    de forma uniforme: sólo necesita llamar a explain(), example() y exercise().
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
    Asegura que st.session_state tenga un contenedor `history`.

    Se usa como paso previo en cualquier operación de historial
    (agregar, limpiar, convertir a DataFrame) para evitar errores
    si el usuario aún no ha contestado nada.
    """
    if "history" not in st.session_state:
        st.session_state.history: List[Dict] = []


def add_history(
    area: str,
    tema: str,
    tipo: str,
    correcto: float,
    usuario: float,
    acierto: bool,
) -> None:
    """
    Agrega un intento al historial.

    Cada registro guarda:
    - timestamp: fecha/hora del intento
    - area: área a la que pertenece el tema (Matemáticas, Física, Química)
    - tema: nombre del tema específico
    - tipo: "Ejercicio" normal o "PRUEBATE"
    - correcto: valor correcto del ejercicio (redondeado a 6 decimales)
    - usuario: respuesta del usuario (redondeada a 6 decimales)
    - resultado: "ACIERTO" o "ERROR" según la evaluación

    Este historial después se convierte en DataFrame para visualizarlo
    y exportarlo desde la pestaña Historial.
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
    Devuelve el historial como DataFrame de pandas.

    Si no hay registros aún, devuelve un DataFrame vacío pero con
    las columnas definidas. Eso evita errores cuando se lo pasamos
    a st.dataframe o cuando intentamos exportar aunque no haya datos.
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
    """
    Elimina todo el historial almacenado en session_state.

    Se usa cuando el usuario pulsa el botón "Borrar historial"
    en la barra lateral.
    """
    ensure_history_initialized()
    st.session_state.history.clear()


def history_to_csv(df: pd.DataFrame) -> bytes:
    """
    Convierte un DataFrame de historial a formato CSV (bytes).

    Este helper se usa directamente en la pestaña Historial
    para alimentar el st.download_button.
    """
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue().encode("utf-8")


# =========================================================
#  EVALUACIÓN NUMÉRICA CON TOLERANCIA
# =========================================================

def within_tol(expected: float, user: float, tol_pct: float) -> bool:
    """
    Compara la respuesta del usuario contra el valor correcto usando tolerancia.

    La tolerancia es relativa al tamaño del resultado esperado, pero con
    un mínimo absoluto para no tener problemas cuando expected es muy
    pequeño (o incluso cero):

        tol = max(|expected| * tol_pct, 1e-6)

    Se considera correcta la respuesta si:

        |user - expected| <= tol

    Esto permite, por ejemplo, aceptar 9.81 y 9.8 como equivalentes
    cuando la tolerancia está configurada lo suficientemente alta.
    """
    tol = max(abs(expected) * tol_pct, 1e-6)
    return abs(user - expected) <= tol
