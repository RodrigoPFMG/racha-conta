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

- **Visual (tema sobre o Pico):** em vez de migrar para React (caro e arriscado
  no prazo), pedi um CSS próprio por cima do Pico. A IA conferiu o resultado com
  screenshots do Playwright e corrigiu o campo de texto espremido pelo botão.
  No caminho apareceu um bug real: `pytest` sem argumentos falhava porque havia
  dois `test_home.py`; resolvido com `--import-mode=importlib`.

## Leo

- **Despesas (2.0–2.3):** pedi ao Claude Code o merge do `validacao.py` do João,
  a troca do `_ler_nome` por `validar_nome` e as rotas de registrar, listar e
  excluir despesa em TDD. Ajuste: o primeiro rascunho de um teste juntava status
  e mensagem numa tupla (`assert (400, True) == ...`); reescrevi em duas asserções
  legíveis antes do commit. O screenshot do Playwright mostrou que, após um erro,
  o form perde o que foi digitado (anotado, fora do escopo). Aprendi a comparar
  sempre `int` com `int` ao validar ids vindos do form.

- **Saldos e acertos (2.4–2.6):** pedi `calcular_saldos` e `sugerir_acertos`
  como funções puras, com valores esperados escritos à mão, e a tela de saldos.
  No teste de R$ 10,00 por três passei os participantes fora de ordem `(3, 1, 2)`
  para provar que o centavo extra vai para o menor id. Conferi a tela com
  screenshot (Ana a receber R$ 60,00; Bruno e Carla devem R$ 30,00). Aprendi que
  o guloso "maior devedor paga ao maior credor" gera no máximo n − 1 acertos.

- **Qualidade (2.7–2.8):** pedi cobertura e revisão dos testes da sessão. A
  cobertura (98%) apontou que pagador e participante não numéricos nunca eram
  testados na rota; viraram 3 testes e a cobertura foi a 100%. A revisão achou a
  fixture `grupo_com_membros` duplicada em dois arquivos (foi para o `conftest.py`
  da integração) e uma asserção negativa (`"pago por Ana" not in`) que passaria
  mesmo com a lista quebrada; troquei por "Nenhuma despesa ainda.". Aprendi a
  preferir asserções positivas.
