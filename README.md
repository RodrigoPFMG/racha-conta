# Racha Conta

[![CI](https://github.com/RodrigoPFMG/racha-conta/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/RodrigoPFMG/racha-conta/actions/workflows/ci.yml)

**Produção:** https://racha-conta.onrender.com (plano free do Render: o primeiro acesso após um período parado pode levar ~1 min)

## Membros

- Rodrigo Gonçalves
- Leonardo Chiari
- João Pedro Bicalho

## Descrição do sistema

O Racha Conta é um app web para dividir despesas entre amigos ou moradores de
uma república. O usuário cria um grupo, adiciona os membros, registra quem pagou
cada despesa e entre quem ela deve ser dividida. O sistema calcula quanto cada
membro deve ou tem a receber e sugere os acertos ("Bruno paga R$ 30,00 para Ana").

## Tecnologias

| Peça | Escolha |
|---|---|
| Linguagem | Python 3.12 |
| Web | Flask + templates Jinja2 |
| Banco | SQLite via Flask-SQLAlchemy |
| Estilo | Pico.css via CDN |
| Testes de unidade e integração | pytest |
| Cobertura | pytest-cov (Coverage.py), mínimo de 80% no CI |
| Testes E2E | Playwright (pytest-playwright) |
| CI | GitHub Actions em Ubuntu, macOS e Windows |
| Deploy (CD) | Render (web service free + gunicorn), deploy automático na `main` |

A lógica de negócio fica em `app/services/` como funções puras (sem Flask e sem
banco), e todo valor monetário é guardado como inteiro em centavos.

## Uso de Inteligência Artificial

Durante o desenvolvimento, utilizamos ferramentas como Claude Code e ChatGPT para auxiliar na implementação de funcionalidades, criação e revisão de testes, configuração do ambiente e melhorias na interface.

A IA foi utilizada como apoio no desenvolvimento em TDD, na criação de testes unitários, de integração e E2E com Playwright, além da revisão de código e identificação de problemas de configuração e cobertura.

As sugestões geradas foram revisadas e ajustadas pela equipe. Entre os principais aprendizados estão a importância de utilizar valores monetários em centavos (`int`), escrever asserções positivas e claras, reutilizar fixtures e funções auxiliares e utilizar seletores acessíveis (`get_by_label` e `get_by_role`) nos testes E2E.

A IA foi utilizada como ferramenta de apoio, mantendo a equipe responsável pelas decisões técnicas, validação e integração do código.

## Como rodar os testes localmente

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python -m playwright install chromium

# rodar o app em http://127.0.0.1:5000
flask --app app run --debug

# testes de unidade + integração com cobertura
pytest tests/unit tests/integration --cov=app --cov-report=term-missing

# testes end-to-end (use --headed para ver o navegador)
pytest tests/e2e
```
