# Diário de uso de IA

Cada membro registra, em 2–3 linhas por tarefa: o que pediu, o que a IA errou
ou foi corrigido, e o que aprendeu.

## Rodrigo

- **Fundação (1.3–1.8):** pedi ao Claude Code o esqueleto Flask, os modelos,
  o CI e `dinheiro.py` em TDD (commit `test:` falhando, depois `feat:`).
  Correção: os testes não achavam o pacote `app`; resolvido com
  `pythonpath = .` no `pytest.ini`. Aprendi que dinheiro em centavos (int)
  elimina erro de arredondamento e deixa `dividir_igualmente` trivial de testar.
