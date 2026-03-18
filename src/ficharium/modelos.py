from __future__ import annotations

import pandas as pd

from ._utils import _ficharium_erro, _ficharium_requisicao, _tipo_para_python


def listar_modelos() -> pd.DataFrame:
    res = _ficharium_erro(
        lambda: _ficharium_requisicao("GET", "modelos"),
        "Erro ao listar modelos",
    )
    return pd.DataFrame(
        {
            "id": [x.get("id") for x in res],
            "nome": [x.get("nome") for x in res],
            "descricao": [x.get("descricao") for x in res],
            "grupo": [x.get("grupo") for x in res],
            "created": [x.get("created") for x in res],
        }
    )


def campos_modelo(modelo_id: str) -> pd.DataFrame:
    res = _ficharium_erro(
        lambda: _ficharium_requisicao("GET", f"modelos/{modelo_id}"),
        f"Modelo '{modelo_id}' nao encontrado",
    )

    def extrair_campos(lista, secao):
        if not lista:
            return []
        campos = []
        for campo in lista:
            tipo = campo.get("tipo", "")
            campos.append(
                {
                    "field_id": campo.get("id"),
                    "label": campo.get("nome") or campo.get("nome_widget"),
                    "widget": campo.get("widget") or campo.get("tipo"),
                    "tipo": tipo,
                    "py_tipo": _tipo_para_python(tipo),
                    "secao": secao,
                }
            )
        return campos

    todos = (
        extrair_campos(res.get("metadados_iniciais"), "metadados_iniciais")
        + extrair_campos(res.get("campos"), "campos")
        + extrair_campos(res.get("metadados_finais"), "metadados_finais")
    )

    if not todos:
        return pd.DataFrame(
            columns=["field_id", "label", "widget", "tipo", "py_tipo", "secao"]
        )

    return pd.DataFrame(todos)
