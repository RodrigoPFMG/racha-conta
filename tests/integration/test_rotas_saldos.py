import pytest


@pytest.fixture
def grupo_com_despesa(client, grupo_com_membros):
    client.post(f"{grupo_com_membros}/despesas", data={
        "descricao": "Mercado", "valor": "60,00", "pagador": "1", "participantes": ["1", "2"],
    })
    return grupo_com_membros


def test_ver_saldos_responde_200(client, grupo_com_membros):
    resposta = client.get(f"{grupo_com_membros}/saldos")

    assert resposta.status_code == 200


def test_ver_saldos_grupo_inexistente_responde_404(client):
    resposta = client.get("/grupos/999/saldos")

    assert resposta.status_code == 404


def test_ver_saldos_pagador_aparece_com_valor_a_receber(client, grupo_com_despesa):
    resposta = client.get(f"{grupo_com_despesa}/saldos")

    assert "a receber R$ 30,00" in resposta.get_data(as_text=True)


def test_ver_saldos_participante_aparece_devendo(client, grupo_com_despesa):
    resposta = client.get(f"{grupo_com_despesa}/saldos")

    assert "deve R$ 30,00" in resposta.get_data(as_text=True)


def test_ver_saldos_mostra_frase_de_acerto(client, grupo_com_despesa):
    resposta = client.get(f"{grupo_com_despesa}/saldos")

    assert "Bruno paga R$ 30,00 para Ana" in resposta.get_data(as_text=True)


def test_ver_saldos_sem_despesas_mostra_tudo_quitado(client, grupo_com_membros):
    resposta = client.get(f"{grupo_com_membros}/saldos")

    assert "Tudo quitado!" in resposta.get_data(as_text=True)


def test_ver_saldos_apos_excluir_despesa_volta_a_tudo_quitado(client, grupo_com_despesa):
    client.post(f"{grupo_com_despesa}/despesas/1/excluir")

    resposta = client.get(f"{grupo_com_despesa}/saldos")

    assert "Tudo quitado!" in resposta.get_data(as_text=True)


def test_pagina_do_grupo_tem_link_para_saldos(client, grupo_com_membros):
    resposta = client.get(grupo_com_membros)

    assert 'href="/grupos/1/saldos"' in resposta.get_data(as_text=True)
