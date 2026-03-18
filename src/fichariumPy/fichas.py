"""Funções para fichas de campo com dados expandidos."""

from __future__ import annotations

import pandas as pd

from ._utils import _converter_valor, _ficharium_erro, _ficharium_requisicao
from .modelos import campos_modelo


def listar_fichas(projeto_id: str, modelo_id: str) -> pd.DataFrame:
    """Retorna as fichas de um modelo em um projeto, com dados expandidos.

    Cada linha do DataFrame corresponde a uma observação (item de `dados`).
    Campos complexos (espécie, coordenada, ponto, lista) ficam como colunas
    de dicionários — use `expandir_especies()`, `expandir_coordenadas()` ou
    `expandir_ponto()` para separá-los.

    Args:
        projeto_id: ID do projeto.
        modelo_id: ID do modelo.

    Returns:
        DataFrame com colunas de metadados da ficha mais os campos do modelo.
    """
    res = _ficharium_erro(
        lambda: _ficharium_requisicao(
            "GET", f"fichas/projeto/{projeto_id}/modelo/{modelo_id}"
        ),
        f"Erro ao listar fichas do modelo '{modelo_id}' no projeto '{projeto_id}'",
    )

    if not res:
        return pd.DataFrame(
            columns=["ficha_id", "id_app", "created", "updated"]
        )

    campos = campos_modelo(modelo_id)
    mapa = {
        row["field_id"]: {"tipo": row["tipo"], "label": row["label"]}
        for _, row in campos.iterrows()
    }

    def converter_bloco(bloco):
        if not bloco:
            return {}
        out = {}
        for fid, valor in bloco.items():
            info = mapa.get(fid)
            if info is None:
                continue
            if info["tipo"] == "semvalor":
                continue
            out[info["label"]] = _converter_valor(valor, info["tipo"])
        return out

    linhas = []

    for ficha in res:
        base = {
            "ficha_id": ficha.get("id"),
            "id_app": ficha.get("id_app"),
            "created": ficha.get("created"),
            "updated": ficha.get("updated"),
        }

        meta_ini = converter_bloco(ficha.get("metadados_iniciais"))
        meta_fin = converter_bloco(ficha.get("metadados_finais"))

        dados = ficha.get("dados") or [{}]

        for obs in dados:
            obs_conv = converter_bloco(obs)
            linhas.append({**base, **meta_ini, **obs_conv, **meta_fin})

    if not linhas:
        return pd.DataFrame(
            columns=["ficha_id", "id_app", "created", "updated"]
        )

    return pd.DataFrame(linhas)


def ficha(ficha_id: str) -> dict:
    """Retorna os dados completos de uma ficha específica."""
    return _ficharium_erro(
        lambda: _ficharium_requisicao("GET", f"fichas/ficha/{ficha_id}"),
        f"Ficha '{ficha_id}' nao encontrada",
    )
