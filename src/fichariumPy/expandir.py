"""Funções para expandir colunas complexas (espécie, coordenada, ponto)."""

from __future__ import annotations

import pandas as pd


def expandir_especies(df: pd.DataFrame, coluna: str = "especie") -> pd.DataFrame:
    """Expande uma coluna de espécies em `{coluna}_nc`, `{coluna}_np` e `{coluna}_grupo`.

    Args:
        df: DataFrame com a coluna a expandir.
        coluna: Nome da coluna (padrão: `"especie"`).

    Returns:
        DataFrame com as colunas expandidas e a coluna original removida.
    """
    df = df.copy()
    col = df[coluna]
    df[f"{coluna}_nc"] = col.apply(lambda x: x.get("nc") if isinstance(x, dict) else None)
    df[f"{coluna}_np"] = col.apply(lambda x: x.get("np") if isinstance(x, dict) else None)
    df[f"{coluna}_grupo"] = col.apply(lambda x: x.get("grupo") if isinstance(x, dict) else None)
    return df.drop(columns=[coluna])


def expandir_coordenadas(df: pd.DataFrame, coluna: str = "coordenadas") -> pd.DataFrame:
    """Expande uma coluna de coordenadas em `{coluna}_latitude` e `{coluna}_longitude`.

    Args:
        df: DataFrame com a coluna a expandir.
        coluna: Nome da coluna (padrão: `"coordenadas"`).

    Returns:
        DataFrame com as colunas expandidas e a coluna original removida.
    """
    df = df.copy()
    col = df[coluna]
    df[f"{coluna}_latitude"] = col.apply(lambda x: x.get("latitude") if isinstance(x, dict) else None)
    df[f"{coluna}_longitude"] = col.apply(lambda x: x.get("longitude") if isinstance(x, dict) else None)
    return df.drop(columns=[coluna])


def expandir_ponto(df: pd.DataFrame, coluna: str = "ponto") -> pd.DataFrame:
    """Expande uma coluna de ponto em `{coluna}_nome`, `{coluna}_id`, `{coluna}_latitude` e `{coluna}_longitude`.

    Args:
        df: DataFrame com a coluna a expandir.
        coluna: Nome da coluna (padrão: `"ponto"`).

    Returns:
        DataFrame com as colunas expandidas e a coluna original removida.
    """
    df = df.copy()
    col = df[coluna]
    df[f"{coluna}_nome"] = col.apply(lambda x: x.get("nome") if isinstance(x, dict) else None)
    df[f"{coluna}_id"] = col.apply(lambda x: x.get("id") if isinstance(x, dict) else None)
    df[f"{coluna}_latitude"] = col.apply(lambda x: x.get("latitude") if isinstance(x, dict) else None)
    df[f"{coluna}_longitude"] = col.apply(lambda x: x.get("longitude") if isinstance(x, dict) else None)
    return df.drop(columns=[coluna])
