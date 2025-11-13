# path: core/utils.py
from __future__ import annotations

import io
import time
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

import pandas as pd
import streamlit as st


@dataclass
class Topic:
    """Representa un tema (ej. 'Ecuación lineal') con callbacks asociados."""
    area: str
    name: str
    explain: Callable[[], str]
    example: Callable[[], Tuple[str, str]]
    exercise: Callable[[], Tuple[str, float, str, str]]


def ensure_history_initialized() -> None:
    if "history" not in st.session_state:
        st.session_state.history: List[Dict] = []


def within_tol(expected: float, user: float, tol_pct: float) -> bool:
    """Compara resultado del usuario contra el correcto usando tolerancia relativa."""
    tol = abs(expected) * tol_pct if abs(expected) >= 1e-9 else 1e-6
    return abs(user - expected) <= tol


def add_history(area: str, tema: str, tipo: str, correcto: float, usuario: float, acierto: bool) -> None:
    """Agrega un registro al historial en memoria (session_state)."""
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
    """Devuelve el historial como DataFrame (puede ser vacío)."""
    ensure_history_initialized()
    if not st.session_state.history:
        return pd.DataFrame(
            columns=["timestamp", "area", "tema", "tipo", "correcto", "usuario", "resultado"]
        )
    return pd.DataFrame(st.session_state.history)


def clear_history() -> None:
    """Limpia el historial en memoria."""
    ensure_history_initialized()
    st.session_state.history.clear()


def history_to_csv(df: pd.DataFrame) -> bytes:
    """Convierte el historial en CSV (bytes) para descarga."""
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue().encode("utf-8")