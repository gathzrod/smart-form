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


def _local_fallback(topic: str, prompt: str, expected: Optional[float], unit: str) -> str:
    """Genera una explicación local cuando la API externa no está disponible."""
    text = f"[IA local] Explicación generada sin conectarse a HuggingFace.\n\n"
    text += f"Tema: {topic}\n\n"

    # Resumen muy sencillo del enunciado
    text += "Resumen del ejercicio:\n"
    text += f"{prompt.strip()}\n\n"

    if expected is not None:
        text += "Resultado de referencia:\n"
        text += f"≈ {expected:.6f} {unit}\n\n"

    text += "Cómo podrías pensarlo paso a paso:\n"
    text += "- Identifica qué datos te dan y qué variable quieres encontrar.\n"
    text += "- Escribe la fórmula general del tema.\n"
    text += "- Sustituye los valores en la fórmula, con cuidado en los signos y las unidades.\n"
    text += "- Haz las operaciones con calma y revisa el orden (suma, resta, multiplicación, división, raíz, etc.).\n\n"
    text += "Chequeo rápido:\n"
    text += "1) ¿Tus unidades coinciden con lo que se pide (ej. metros, segundos, mol, etc.)?\n"
    text += "2) ¿Tu número tiene sentido (ni ridículamente grande ni 0 si no debería serlo)?\n"

    return text


def ask_ai(topic: str, prompt: str, expected: Optional[float] = None, unit: str = "") -> str:
    """
    Pide una explicación / pista a un modelo open-source en HuggingFace.

    Si algo falla (410, timeout, etc.), devuelve una explicación local
    basada en el enunciado y el resultado correcto.
    """
    token = _get_hf_token()
    if not token:
        return _local_fallback(topic, prompt, expected, unit)

    # Modelo ligero orientado a instrucciones.
    # Si tu cuenta habilita otro modelo, solo cambia este ID.
    model_id = "google/flan-t5-small"

    url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {token}"}

    system_msg = (
        "Eres un tutor de ciencias para nivel bachillerato. "
        "Explica en español, con frases cortas y claras, sin LaTeX ni símbolos raros. "
        "Máximo 7 frases. "
        "Al final añade una sección llamada 'Chequeo rápido' con 2 puntos para que el alumno revise su resultado."
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

        if isinstance(data, list) and data and "generated_text" in data[0]:
            text = data[0]["generated_text"]
        else:
            text = str(data)

        return text.strip()

    except requests.exceptions.Timeout:
        # Si tarda demasiado, usamos explicación local.
        return _local_fallback(topic, prompt, expected, unit)

    except requests.exceptions.HTTPError:
        # 410 u otros códigos: el modelo no está disponible en tu cuenta/serverless.
        return _local_fallback(topic, prompt, expected, unit)

    except Exception:
        # Cualquier otra cosa rara: también fallback local.
        return _local_fallback(topic, prompt, expected, unit)
