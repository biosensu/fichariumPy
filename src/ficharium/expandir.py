from __future__ import annotations

import pandas as pd


def expandir_especies(df: pd.DataFrame, coluna: str = "especie") -> pd.DataFrame:
    df = df.copy()
    col = df[coluna]
    df[f"{coluna}_nc"] = col.apply(lambda x: x.get("nc") if isinstance(x, dict) else None)
    df[f"{coluna}_np"] = col.apply(lambda x: x.get("np") if isinstance(x, dict) else None)
    df[f"{coluna}_grupo"] = col.apply(lambda x: x.get("grupo") if isinstance(x, dict) else None)
    return df.drop(columns=[coluna])


def expandir_coordenadas(df: pd.DataFrame, coluna: str = "coordenadas") -> pd.DataFrame:
    df = df.copy()
    col = df[coluna]
    df[f"{coluna}_latitude"] = col.apply(lambda x: x.get("latitude") if isinstance(x, dict) else None)
    df[f"{coluna}_longitude"] = col.apply(lambda x: x.get("longitude") if isinstance(x, dict) else None)
    return df.drop(columns=[coluna])


def expandir_ponto(df: pd.DataFrame, coluna: str = "ponto") -> pd.DataFrame:
    df = df.copy()
    col = df[coluna]
    df[f"{coluna}_nome"] = col.apply(lambda x: x.get("nome") if isinstance(x, dict) else None)
    df[f"{coluna}_id"] = col.apply(lambda x: x.get("id") if isinstance(x, dict) else None)
    df[f"{coluna}_latitude"] = col.apply(lambda x: x.get("latitude") if isinstance(x, dict) else None)
    df[f"{coluna}_longitude"] = col.apply(lambda x: x.get("longitude") if isinstance(x, dict) else None)
    return df.drop(columns=[coluna])
