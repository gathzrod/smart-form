# path: core/ai.py
from __future__ import annotations

from typing import Optional

import requests
import streamlit as st


def _get_hf_token() -> Optional[str]:
    """Obtiene el token de HuggingFace desde st.secrets['HF_TOKEN']."""
    try:
        token = st.secrets.get("HF_TOKEN", None)
        if token:
            return str(token).strip()
    except Exception:
        pass
    return None


def has_ai() -> bool:
    """Indica si hay IA configurada (HF_TOKEN presente)."""
    return _get_hf_token() is not None


def ask_ai(topic: str, prompt: str, expected: Optional[float] = None, unit: str = "") -> str:
    """
    Pide una explicación / pista a un modelo open-source en HuggingFace.

    Usa un modelo instruct gratuito (flan-t5-large). Si no hay token
    o algo falla, devuelve un mensaje local amigable.
    """
    token = _get_hf_token()
    if not token:
        base = f"[IA local] No hay HF_TOKEN configurado en el servidor.\n\nTema: {topic}\n"
        if expected is not None:
            base += f"Pista aproximada: el resultado debería andar cerca de {expected:.4f} {unit}."
        else:
            base += "Pista: revisa la teoría y las unidades paso a paso."
        return base

    # Modelo estable para instrucciones
    model_id = "google/flan-t5-large"

    url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {token}"}

    system_msg = (
        "Eres un tutor de ciencias para nivel prepa/primer semestre. "
        "Explica en pasos claros, sin LaTeX, sin símbolos raros. "
        "Escribe en español, con máximo 7 frases. "
        "Al final añade una sección 'Chequeo rápido' con 2 puntos para que el alumno verifique su resultado."
    )

    user_msg = f"Tema: {topic}\nEjercicio o situación: {prompt}\n"
    if expected is not None:
        user_msg += f"Resultado numérico esperado (aprox): {expected:.6f} {unit}\n"

    payload = {
        "inputs": f"{system_msg}\n\nAlumno: {user_msg}",
        "parameters": {
            "max_new_tokens": 256,
            "temperature": 0.25,
        },
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=25)
        resp.raise_for_status()
        data = resp.json()

        # Serverless Inference normalmente devuelve lista con 'generated_text'
        if isinstance(data, list) and data and "generated_text" in data[0]:
            text = data[0]["generated_text"]
        else:
            # Otros modelos pueden devolver texto directamente
            text = str(data)

        return text.strip()

    except requests.exceptions.Timeout:
        return "[IA] El modelo tardó demasiado en responder. Intenta de nuevo."
    except requests.exceptions.HTTPError as http_err:
        # Mensaje genérico (no mostramos URL ni cosas feas al usuario)
        return f"[IA] No se pudo contactar al modelo de HuggingFace (HTTP {resp.status_code})."
    except Exception:
        return "[IA] Ocurrió un error inesperado al llamar a la IA. Intenta más tarde."
