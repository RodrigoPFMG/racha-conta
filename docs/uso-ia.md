# Diário de uso de IA

Cada membro registra, em 2–3 linhas por tarefa: o que pediu, o que a IA errou
ou foi corrigido, e o que aprendeu.

## Rodrigo

- **Fundação (1.3–1.8):** pedi ao Claude Code o esqueleto Flask, os modelos,
  o CI e `dinheiro.py` em TDD (commit `test:` falhando, depois `feat:`).
  Correção: os testes não achavam o pacote `app`; resolvido com
  `pythonpath = .` no `pytest.ini`. Aprendi que dinheiro em centavos (int)
  elimina erro de arredondamento e deixa `dividir_igualmente` trivial de testar.

- **Telas de grupo e membros (1.10):** pedi rotas, templates com `<label>` e
  testes de integração, um commit por rota. Ajustei o redirect pós-criação para
  abrir a página do grupo (fluxo que o E2E do João espera). A validação de nome
  ficou provisória na rota até o `validacao.py` do João entrar na `main`.
