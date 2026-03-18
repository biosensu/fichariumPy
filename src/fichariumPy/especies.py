"""Funções para espécies registradas em projetos."""

from __future__ import annotations

import pandas as pd

from ._utils import _ficharium_erro, _ficharium_requisicao


def listar_especies(
    projeto_id: str, busca: str | None = None
) -> pd.DataFrame:
    """Retorna a lista consolidada de espécies registradas em um projeto.

    Args:
        projeto_id: ID do projeto.
        busca: Filtro parcial pelo nome científico (case-insensitive).

    Returns:
        DataFrame com colunas `nc`, `grupo`, `total_registros`, `metodologias`.
    """
    res = _ficharium_erro(
        lambda: _ficharium_requisicao(
            "GET", f"fichas/{projeto_id}/especies"
        ),
        f"Erro ao listar especies do projeto '{projeto_id}'",
    )

    df = pd.DataFrame(
        {
            "nc": [x.get("especie") for x in res],
            "grupo": [x.get("grupo") for x in res],
            "total_registros": [x.get("total_registros") for x in res],
            "metodologias": [
                [str(m) for m in (x.get("metodologias") or [])] for x in res
            ],
        }
    )

    if busca:
        df = df[df["nc"].str.contains(busca, case=False, na=False)]

    return df
