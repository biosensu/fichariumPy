"""
![ficharium](https://raw.githubusercontent.com/Biosensu/fichariumPy/main/fichariumPy.svg)

Cliente Python para a API [Ficharium Cloud](https://ficharium.cloud).

Permite autenticar, listar projetos, modelos e fichas de campo,
e acessar listas de espécies consolidadas.

## Início rápido

```python
from fichariumPy import *

ficharium_login("seu@email.com")
projetos = listar_projetos()
```
"""

from ._utils import FichariumError
from .auth import (
    ficharium_definir_token,
    ficharium_login,
    ficharium_logout,
    ficharium_token,
)
from .especies import listar_especies
from .expandir import expandir_coordenadas, expandir_especies, expandir_ponto
from .fichas import ficha, listar_fichas
from .modelos import campos_modelo, listar_modelos
from .projetos import fichas_projeto, listar_projetos, modelos_projeto, projeto

__all__ = [
    "FichariumError",
    "ficharium_token",
    "ficharium_definir_token",
    "ficharium_logout",
    "ficharium_login",
    "listar_projetos",
    "projeto",
    "modelos_projeto",
    "fichas_projeto",
    "listar_modelos",
    "campos_modelo",
    "listar_fichas",
    "ficha",
    "listar_especies",
    "expandir_especies",
    "expandir_coordenadas",
    "expandir_ponto",
]
