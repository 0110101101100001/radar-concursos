# Radar Concursos

TUI (Terminal User Interface) em Python para extrair e filtrar editais de concursos públicos de múltiplas bancas: PCI Concursos, IBFC, Cebraspe, FCC e Quadrix.

## Estrutura

- `main.py` — ponto de entrada Python
- `src/ui/tui.py` — interface textual com sidebar, DataTable e animação de gato
- `src/scrapers/` — scrapers das bancas (PCI, IBFC, Cebraspe, FCC, Quadrix)
- `src/scrapers/base.py` — classe base com sessão HTTP e retry
- `src/core/filter.py` — processamento e filtragem por região e palavra-chave
- `database.py` — SQLite local para salvar concursos novos
- `scripts/download_fixtures.py` — baixa HTMLs para testes
- `tests/test_scrapers.py` — testes com pytest

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
python main.py
```

## Atalhos da TUI

- `q` — Sair
- `r` — Atualizar varredura
- `Enter` — Abrir link do concurso focado no navegador

## Bancas suportadas

PCI Concursos, IBFC, Cebraspe, FCC, Quadrix.

## Requisitos

Python 3.10+ e as dependências em `requirements.txt`.
