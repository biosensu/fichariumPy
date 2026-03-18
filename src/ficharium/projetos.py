from __future__ import annotations

import pandas as pd

from ._utils import _ficharium_erro, _ficharium_requisicao


def listar_projetos() -> pd.DataFrame:
    res = _ficharium_erro(
        lambda: _ficharium_requisicao("GET", "projetos"),
        "Erro ao listar projetos",
    )
    return pd.DataFrame(
        {
            "id": [x.get("id") for x in res],
            "nome": [x.get("nome") for x in res],
            "descricao": [x.get("descricao") for x in res],
            "fichas_na_nuvem": [x.get("fichas_na_nuvem") for x in res],
            "cargo": [x.get("cargo") for x in res],
        }
    )


def projeto(id: str) -> dict:
    return _ficharium_erro(
        lambda: _ficharium_requisicao("GET", f"projetos/{id}"),
        f"Projeto '{id}' nao encontrado",
    )


def modelos_projeto(projeto_id: str) -> pd.DataFrame:
    res = _ficharium_erro(
        lambda: _ficharium_requisicao("GET", f"projetos/{projeto_id}"),
        f"Projeto '{projeto_id}' nao encontrado",
    )
    modelos = res.get("modelos_usuario_do_projeto", []) or []
    return pd.DataFrame(
        {
            "id": [x.get("id") for x in modelos],
            "nome": [x.get("nome") for x in modelos],
            "descricao": [x.get("descricao") for x in modelos],
            "grupo": [x.get("grupo") for x in modelos],
        }
    )


def fichas_projeto(projeto_id: str) -> pd.DataFrame:
    res = _ficharium_erro(
        lambda: _ficharium_requisicao("GET", f"fichas/{projeto_id}"),
        f"Erro ao listar fichas do projeto '{projeto_id}'",
    )
    return pd.DataFrame(
        {
            "id": [x.get("id") for x in res],
            "modelo_id": [
                (x.get("modelo") or {}).get("id") for x in res
            ],
            "modelo_nome": [
                (x.get("modelo") or {}).get("nome") or x.get("modelo_bs")
                for x in res
            ],
            "criador_nome": [
                (x.get("criador") or {}).get("nome") for x in res
            ],
            "created": [x.get("created") for x in res],
            "updated": [x.get("updated") for x in res],
        }
    )
