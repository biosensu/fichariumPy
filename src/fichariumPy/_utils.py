from __future__ import annotations

import os
from datetime import date, datetime, time

import httpx

__version__ = "1.1.0"


class FichariumError(Exception):
    pass


def ficharium_base_url() -> str:
    return os.environ.get("FICHARIUM_BASE_URL", "https://api.ficharium.cloud")


def _ficharium_requisicao(
    method: str,
    path: str,
    *,
    body: dict | None = None,
    query: dict | None = None,
    token: str | None = None,
) -> dict | list:
    if token is None:
        from .auth import ficharium_token
        token = ficharium_token()

    url = f"{ficharium_base_url()}/{path}"

    if query is not None:
        query = {k: v for k, v in query.items() if v is not None}
        if not query:
            query = None

    resp = httpx.request(
        method,
        url,
        json=body,
        params=query,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": f"ficharium-py/{__version__}",
        },
    )

    if resp.status_code >= 400:
        try:
            msg = resp.json().get("message", f"Erro HTTP {resp.status_code}")
        except Exception:
            msg = f"Erro HTTP {resp.status_code}"
        raise FichariumError(msg)

    return resp.json()


def _ficharium_erro(fn, contexto: str):
    try:
        return fn()
    except Exception as e:
        raise FichariumError(f"{contexto}: {e}") from e


_TIPO_PARA_PYTHON = {
    "especie": "dict",
    "inteiro": "int",
    "decimal": "float",
    "data": "date",
    "hora": "time",
    "coordenada": "dict",
    "porcentagem": "float",
    "booleano": "bool",
    "select": "str",
    "texto": "str",
    "lista": "list",
    "ponto": "dict",
    "duracao": "float",
    "semvalor": "None",
}


def _tipo_para_python(tipo: str) -> str:
    return _TIPO_PARA_PYTHON.get(tipo, "str")


def _converter_valor(valor, tipo: str):
    if valor is None:
        return None

    match tipo:
        case "especie":
            if isinstance(valor, dict):
                return {
                    "nc": valor.get("nc"),
                    "np": valor.get("np"),
                    "grupo": valor.get("grupo"),
                }
            return {"nc": str(valor), "np": None, "grupo": None}
        case "inteiro":
            return int(valor)
        case "decimal" | "porcentagem" | "duracao":
            return float(valor)
        case "data":
            s = str(valor)
            try:
                return date.fromisoformat(s)
            except ValueError:
                return datetime.strptime(s, "%d-%m-%Y").date()
        case "hora":
            partes = str(valor).split(":")
            if len(partes) >= 2:
                h = int(partes[0])
                m = int(partes[1])
                s = int(float(partes[2])) if len(partes) >= 3 else 0
                return time(h, m, s)
            return None
        case "coordenada":
            return {
                "latitude": valor.get("latitude"),
                "longitude": valor.get("longitude"),
            }
        case "booleano":
            return bool(valor)
        case "select" | "texto":
            return str(valor)
        case "lista":
            if isinstance(valor, list):
                return [str(v) for v in valor]
            return [str(valor)]
        case "ponto":
            return {
                "nome": valor.get("nome"),
                "id": valor.get("id"),
                "latitude": valor.get("latitude"),
                "longitude": valor.get("longitude"),
            }
        case "semvalor":
            return None
        case _:
            return str(valor)
