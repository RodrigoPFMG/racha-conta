import pytest

from app.models import Despesa


@pytest.fixture
def grupo_com_membros(client):
    client.post("/grupos", data={"nome": "República"})
    client.post("/grupos/1/membros", data={"nome": "Ana"})
    client.post("/grupos/1/membros", data={"nome": "Bruno"})
    return "/grupos/1"


@pytest.fixture
def despesa_valida():
    return {"descricao": "Mercado", "valor": "12,50", "pagador": "1", "participantes": ["1", "2"]}


def test_registrar_despesa_valida_redireciona_para_o_grupo(client, grupo_com_membros, despesa_valida):
    resposta = client.post(f"{grupo_com_membros}/despesas", data=despesa_valida)

    assert resposta.headers["Location"] == grupo_com_membros


def test_registrar_despesa_valida_salva_valor_em_centavos(client, grupo_com_membros, despesa_valida):
    client.post(f"{grupo_com_membros}/despesas", data=despesa_valida)

    assert Despesa.query.one().valor_centavos == 1250


def test_registrar_despesa_valor_invalido_responde_400_com_mensagem(client, grupo_com_membros, despesa_valida):
    despesa_valida["valor"] = "doze"

    resposta = client.post(f"{grupo_com_membros}/despesas", data=despesa_valida)

    assert resposta.status_code == 400
    assert "Use o formato 12,50." in resposta.get_data(as_text=True)


def test_registrar_despesa_valor_zero_mostra_erro(client, grupo_com_membros, despesa_valida):
    despesa_valida["valor"] = "0,00"

    resposta = client.post(f"{grupo_com_membros}/despesas", data=despesa_valida)

    assert "O valor deve ser maior que zero." in resposta.get_data(as_text=True)


def test_registrar_despesa_sem_participantes_mostra_erro(client, grupo_com_membros, despesa_valida):
    despesa_valida["participantes"] = []

    resposta = client.post(f"{grupo_com_membros}/despesas", data=despesa_valida)

    assert "Selecione ao menos um participante." in resposta.get_data(as_text=True)


def test_registrar_despesa_descricao_vazia_mostra_erro(client, grupo_com_membros, despesa_valida):
    despesa_valida["descricao"] = "   "

    resposta = client.post(f"{grupo_com_membros}/despesas", data=despesa_valida)

    assert "Informe a descrição da despesa (até 50 caracteres)." in resposta.get_data(as_text=True)


def test_registrar_despesa_pagador_de_outro_grupo_responde_400(client, grupo_com_membros, despesa_valida):
    client.post("/grupos", data={"nome": "Viagem"})
    client.post("/grupos/2/membros", data={"nome": "Carla"})
    despesa_valida["pagador"] = "3"

    resposta = client.post(f"{grupo_com_membros}/despesas", data=despesa_valida)

    assert resposta.status_code == 400


def test_registrar_despesa_em_grupo_inexistente_responde_404(client, despesa_valida):
    resposta = client.post("/grupos/999/despesas", data=despesa_valida)

    assert resposta.status_code == 404


def test_pagina_do_grupo_sem_membros_mostra_aviso_de_despesa(client):
    client.post("/grupos", data={"nome": "Viagem"})

    resposta = client.get("/grupos/1")

    assert "Adicione membros para registrar despesas." in resposta.get_data(as_text=True)


def test_pagina_do_grupo_lista_despesa_com_valor_formatado(client, grupo_com_membros, despesa_valida):
    client.post(f"{grupo_com_membros}/despesas", data=despesa_valida)

    resposta = client.get(grupo_com_membros)

    assert "R$ 12,50" in resposta.get_data(as_text=True)


def test_pagina_do_grupo_lista_despesa_com_nome_do_pagador(client, grupo_com_membros, despesa_valida):
    client.post(f"{grupo_com_membros}/despesas", data=despesa_valida)

    resposta = client.get(grupo_com_membros)

    assert "pago por Ana" in resposta.get_data(as_text=True)


def test_pagina_do_grupo_sem_despesas_mostra_mensagem_vazia(client, grupo_com_membros):
    resposta = client.get(grupo_com_membros)

    assert "Nenhuma despesa ainda." in resposta.get_data(as_text=True)


def test_excluir_despesa_remove_da_lista(client, grupo_com_membros, despesa_valida):
    client.post(f"{grupo_com_membros}/despesas", data=despesa_valida)
    client.post(f"{grupo_com_membros}/despesas/1/excluir")

    resposta = client.get(grupo_com_membros)

    assert "pago por Ana" not in resposta.get_data(as_text=True)


def test_excluir_despesa_redireciona_para_o_grupo(client, grupo_com_membros, despesa_valida):
    client.post(f"{grupo_com_membros}/despesas", data=despesa_valida)

    resposta = client.post(f"{grupo_com_membros}/despesas/1/excluir")

    assert resposta.headers["Location"] == grupo_com_membros


def test_excluir_despesa_de_outro_grupo_responde_404(client, grupo_com_membros, despesa_valida):
    client.post(f"{grupo_com_membros}/despesas", data=despesa_valida)
    client.post("/grupos", data={"nome": "Viagem"})

    resposta = client.post("/grupos/2/despesas/1/excluir")

    assert resposta.status_code == 404
