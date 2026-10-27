import os
import re

import httpx


MODELO = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent"

_MENSAJES_HTTP = {
    400: "Solicitud inválida a Gemini (400). Revisa el contenido y los parámetros enviados.",
    403: "Gemini rechazó la solicitud (403). Verifica la API key y los permisos del proyecto.",
    404: "No se encontró el modelo o endpoint de Gemini (404). Verifica GEMINI_MODEL.",
    429: "Se alcanzó el límite de solicitudes de Gemini (429). Inténtalo más tarde.",
}


def ia(instruccion, texto, como_json=False):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta configurar la variable de entorno GEMINI_API_KEY.")

    payload = {
        "systemInstruction": {"parts": [{"text": instruccion}]},
        "contents": [{"parts": [{"text": texto}]}],
    }
    if como_json:
        payload["generationConfig"] = {"responseMimeType": "application/json"}

    try:
        respuesta = httpx.post(
            URL,
            headers={"x-goog-api-key": api_key},
            json=payload,
            timeout=60.0,
        )
    except httpx.RequestError as error:
        raise RuntimeError(f"No se pudo conectar con Gemini: {error}") from error

    if respuesta.status_code in _MENSAJES_HTTP:
        raise RuntimeError(_MENSAJES_HTTP[respuesta.status_code])

    try:
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as error:
        raise RuntimeError(
            f"Error HTTP de Gemini ({respuesta.status_code}): {respuesta.text}"
        ) from error

    datos = respuesta.json()
    try:
        resultado = datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError("Gemini devolvió una respuesta sin texto utilizable.") from error

    if como_json:
        resultado = resultado.strip()
        resultado = re.sub(r"^```(?:json)?\s*", "", resultado, flags=re.IGNORECASE)
        resultado = re.sub(r"\s*```$", "", resultado)

    return resultado
