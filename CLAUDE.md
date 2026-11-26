# Racha Conta — instruções para o Claude Code

## Projeto
App web Flask para dividir despesas em grupo. Trabalho prático de
Engenharia de Software II (UFMG). Equipe: Rodrigo, Leo, João.

## Comandos
- Instalar: pip install -r requirements-dev.txt
- Rodar: flask --app app run --debug
- Unidade + integração com cobertura:
  pytest tests/unit tests/integration --cov=app --cov-report=term-missing
- E2E: pytest tests/e2e

## Regras de código
- Dinheiro SEMPRE em centavos (int). Nunca float.
- Lógica de negócio só em app/services/, como funções puras
  (sem Flask, sem banco). Rotas só leem o form, chamam o serviço e renderizam.
- Nomes de domínio em português (grupo, membro, despesa, saldo, acerto).

## Regras de teste
- Todo código novo vem com teste. Cobertura mínima: 80%.
- Testar pela API pública, um comportamento por teste.
- Nome descreve o comportamento: test_<acao>_<cenario>_<resultado>.
- Sem lógica (if/for) dentro dos testes. Arrange / Act / Assert.

## Regras de git
- Commits pequenos: uma mudança lógica por commit.
- Rode os testes antes de cada commit.
- Mensagem em português, Conventional Commits:
  feat: / fix: / test: / refactor: / docs: / ci: / chore:
- Não faça push e não altere .github/workflows sem eu pedir.
