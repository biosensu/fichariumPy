"""Autenticação com a API Ficharium."""

from __future__ import annotations

import getpass
import os
from pathlib import Path

import httpx

from ._utils import FichariumError, ficharium_base_url, __version__

_TOKEN_FILE = Path.home() / ".ficharium_token"


def ficharium_token() -> str:
    """Obtém o token JWT armazenado.

    Procura primeiro na variável de ambiente `FICHARIUM_TOKEN`,
    depois no arquivo `~/.ficharium_token`.

    Raises:
        FichariumError: Se nenhum token for encontrado.
    """
    token = os.environ.get("FICHARIUM_TOKEN", "")
    if token:
        return token
    if _TOKEN_FILE.exists():
        token = _TOKEN_FILE.read_text().strip()
        if token:
            return token
    raise FichariumError(
        "Token nao encontrado. Use ficharium_login() ou defina FICHARIUM_TOKEN."
    )


def ficharium_definir_token(token: str) -> None:
    """Salva o token JWT na variável de ambiente e em `~/.ficharium_token`."""
    os.environ["FICHARIUM_TOKEN"] = token
    _TOKEN_FILE.write_text(token)


def ficharium_logout() -> None:
    """Remove o token da sessão atual e apaga `~/.ficharium_token`."""
    os.environ.pop("FICHARIUM_TOKEN", None)
    if _TOKEN_FILE.exists():
        _TOKEN_FILE.unlink()
    print("Logout realizado com sucesso.")


def ficharium_login(
    email: str,
    senha: str | None = None,
    base_url: str | None = None,
) -> str:
    """Autentica com email e senha e armazena o token automaticamente.

    Args:
        email: Email do usuário.
        senha: Senha. Se omitida, um prompt seguro é exibido.
        base_url: URL base da API (padrão: `https://api.ficharium.cloud`).

    Returns:
        Mensagem de boas-vindas.

    Raises:
        FichariumError: Se as credenciais forem inválidas.
    """
    if senha is None:
        senha = getpass.getpass(f"Senha Ficharium para {email}: ")

    if base_url is None:
        base_url = ficharium_base_url()

    resp = httpx.post(
        f"{base_url}/usuario/login",
        json={"email": email, "senha": senha},
        headers={"User-Agent": f"ficharium-py/{__version__}"},
    )

    if resp.status_code >= 400:
        try:
            msg = resp.json().get("message", f"Erro HTTP {resp.status_code}")
        except Exception:
            msg = f"Erro HTTP {resp.status_code}"
        raise FichariumError(msg)

    res = resp.json()
    ficharium_definir_token(res["token"])
    msg = f"Login realizado com sucesso. Bem-vindo, {res.get('nome', '')}!"
    print(msg)
    return msg
