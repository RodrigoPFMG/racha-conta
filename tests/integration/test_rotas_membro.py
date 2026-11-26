import pytest


@pytest.fixture
def grupo_criado(client):
    client.post("/grupos", data={"nome": "República"})
    return "/grupos/1"


def test_adicionar_membro_valido_aparece_na_pagina_do_grupo(client, grupo_criado):
    client.post(f"{grupo_criado}/membros", data={"nome": "Ana"})

    resposta = client.get(grupo_criado)

    assert "<li>Ana</li>" in resposta.get_data(as_text=True)


def test_adicionar_membro_valido_redireciona_para_o_grupo(client, grupo_criado):
    resposta = client.post(f"{grupo_criado}/membros", data={"nome": "Ana"})

    assert resposta.headers["Location"] == grupo_criado


def test_adicionar_membro_remove_espacos_do_nome(client, grupo_criado):
    client.post(f"{grupo_criado}/membros", data={"nome": "  Bruno  "})

    resposta = client.get(grupo_criado)

    assert "<li>Bruno</li>" in resposta.get_data(as_text=True)


def test_adicionar_membro_nome_vazio_responde_400(client, grupo_criado):
    resposta = client.post(f"{grupo_criado}/membros", data={"nome": ""})

    assert resposta.status_code == 400


def test_adicionar_membro_nome_vazio_mostra_erro(client, grupo_criado):
    resposta = client.post(f"{grupo_criado}/membros", data={"nome": "  "})

    assert "Informe um nome." in resposta.get_data(as_text=True)


def test_adicionar_membro_em_grupo_inexistente_responde_404(client):
    resposta = client.post("/grupos/999/membros", data={"nome": "Ana"})

    assert resposta.status_code == 404
