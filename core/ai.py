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


def _detect_area(topic: str) -> str:
    """Intenta detectar el área a partir del prefijo del topic."""
    t = topic.lower()
    if t.startswith("matemáticas") or t.startswith("matematicas"):
        return "mat"
    if t.startswith("física") or t.startswith("fisica"):
        return "fis"
    if t.startswith("química") or t.startswith("quimica"):
        return "qui"
    return "gen"


def _local_fallback(topic: str, prompt: str, expected: Optional[float], unit: str) -> str:
    """
    Genera una explicación local cuando la API externa no está disponible.
    Ajusta el texto según el área (mate / física / química / general).
    """
    area = _detect_area(topic)

    text = f"[IA local] Explicación generada sin conectarse a HuggingFace.\n\n"
    text += f"Tema: {topic}\n\n"

    text += "Resumen del ejercicio:\n"
    text += f"{prompt.strip()}\n\n"

    if expected is not None and area != "mat":
        # Para mate evitamos mostrar resultado numérico explícito para no spoilear tanto
        text += "Tienes un valor de referencia (usado solo para revisar tu respuesta).\n\n"

    text += "Cómo podrías abordarlo:\n"

    if area == "mat":
        text += "- Identifica qué expresión tienes (por ejemplo, ax + b = 0).\n"
        text += "- Aísla la incógnita: mueve términos al otro lado y luego divide entre el coeficiente.\n"
        text += "- Revisa signos, fracciones y el orden de operaciones.\n\n"
        text += "Chequeo rápido:\n"
        text += "1) ¿Respetaste el cambio de signo al pasar términos al otro lado?\n"
        text += "2) ¿Dividiste entre el coeficiente correcto (no entre 0)?\n"
    elif area == "fis":
        text += "- Anota las magnitudes con sus unidades (m, s, m/s, N, J, etc.).\n"
        text += "- Escribe la fórmula que relaciona esas magnitudes.\n"
        text += "- Sustituye con cuidado los valores y realiza las operaciones.\n\n"
        text += "Chequeo rápido:\n"
        text += "1) ¿Tus unidades finales coinciden con la magnitud que te piden?\n"
        text += "2) ¿El valor obtenido es razonable (ni absurdo ni negativo cuando no debería)?\n"
    elif area == "qui":
        text += "- Identifica qué se pide: concentración, volumen, moles, masa, etc.\n"
        text += "- Escribe la fórmula adecuada (por ejemplo, M = n / V o ρ = m / V).\n"
        text += "- Revisa que volumen, masa y moles estén en unidades coherentes.\n\n"
        text += "Chequeo rápido:\n"
        text += "1) ¿Usaste las unidades correctas (L, mol, g, mL, atm, K, según el tema)?\n"
        text += "2) ¿El resultado tiene sentido con los datos iniciales (no aumenta al diluir, por ejemplo)?\n"
    else:
        text += "- Identifica datos conocidos y lo que quieres calcular.\n"
        text += "- Escribe la relación o fórmula central del problema.\n"
        text += "- Sustituye y verifica cada operación.\n\n"
        text += "Chequeo rápido:\n"
        text += "1) ¿Tus pasos siguen una lógica clara de despeje o sustitución?\n"
        text += "2) ¿El número obtenido y sus unidades tienen sentido en el contexto?\n"

    return text


def ask_ai(topic: str, prompt: str, expected: Optional[float] = None, unit: str = "") -> str:
    """
    Pide una explicación / pista a un modelo open-source en HuggingFace.

    Si algo falla (410, timeout, etc.), devuelve una explicación local
    basada en el enunciado y el tema.
    """
    token = _get_hf_token()
    if not token:
        return _local_fallback(topic, prompt, expected, unit)

    # Modelo ligero orientado a instrucciones.
    # Si en el futuro habilitas otro modelo en tu cuenta, solo cambia este ID.
    model_id = "google/flan-t5-small"

    url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {token}"}

    area = _detect_area(topic)
    if area == "mat":
        area_hint = (
            "El tema es de matemáticas (nivel bachillerato). "
            "Enfatiza pasos de despeje, cuidado de signos y orden de operaciones."
        )
    elif area == "fis":
        area_hint = (
            "El tema es de física (nivel bachillerato). "
            "Enfatiza análisis de magnitudes físicas y unidades."
        )
    elif area == "qui":
        area_hint = (
            "El tema es de química (nivel bachillerato). "
            "Enfatiza concentración, moles, volumen, masa y unidades químicas."
        )
    else:
        area_hint = "Tema de ciencias a nivel bachillerato."

    system_msg = (
        f"{area_hint} "
        "Explica en español, con frases cortas y claras, sin LaTeX ni símbolos raros. "
        "Máximo 7 frases. "
        "Al final añade una sección llamada 'Chequeo rápido' con 2 puntos para que el alumno revise su resultado."
    )

    user_msg = f"Tema: {topic}\nEjercicio o situación: {prompt}\n"
    if expected is not None:
        user_msg += f"Hay un valor de referencia usado internamente para revisar la respuesta del alumno.\n"

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
        return _local_fallback(topic, prompt, expected, unit)
    except requests.exceptions.HTTPError:
        return _local_fallback(topic, prompt, expected, unit)
    except Exception:
        return _local_fallback(topic, prompt, expected, unit)
