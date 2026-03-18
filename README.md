# ficharium

Cliente Python para o [Ficharium Cloud](https://ficharium.cloud). Permite autenticar, listar projetos, modelos e fichas de campo, e acessar listas de espécies consolidadas.

## Instalação

```bash
pip install git+https://github.com/Biosensu/fichariumPy.git
```

## Autenticação

O token JWT é armazenado em `~/.ficharium_token` e reutilizado entre sessões.

```python
from ficharium import *

# Login — abre prompt seguro de senha
ficharium_login("seu@email.com")
```

## Projetos

```python
# listar todos os projetos do usuário
projetos = listar_projetos()

# detalhes de um projeto
proj = projeto(projetos["id"].iloc[0])

# modelos e fichas de um projeto
modelos_projeto("proj_id")
fichas_projeto("proj_id")
```

## Modelos e campos

```python
# modelos do usuário
modelos = listar_modelos()

# campos de um modelo (com tipos Python mapeados)
campos = campos_modelo(modelos["id"].iloc[0])
```

## Fichas de campo

```python
# DataFrame com uma linha por observação
fichas = listar_fichas("proj_id", "modelo_id")

# ficha específica
ficha("ficha_id")
```

### Expandindo campos complexos

Campos de tipo `especie`, `coordenada` e `ponto` são retornados como colunas de dicionários.
Use as funções auxiliares para expandi-los:

```python
fichas = expandir_especies(fichas, "Espécie")
fichas = expandir_coordenadas(fichas, "Coordenadas")
fichas = expandir_ponto(fichas, "Ponto amostral")
```

## Espécies

```python
# lista consolidada de espécies registradas no projeto
especies = listar_especies("proj_id")

# com filtro por nome
listar_especies("proj_id", busca="Leopardus")
```

## Configuração avançada

Defina variáveis de ambiente para sobrescrever os padrões:

```
FICHARIUM_TOKEN=seu_token_jwt
FICHARIUM_BASE_URL=https://api.ficharium.cloud
```

## Licença

MIT © Biosensu
