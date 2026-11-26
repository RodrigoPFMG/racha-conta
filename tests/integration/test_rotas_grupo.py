def test_home_sem_grupos_mostra_mensagem_vazia(client):
    resposta = client.get("/")

    assert "Nenhum grupo ainda." in resposta.get_data(as_text=True)


def test_criar_grupo_valido_aparece_na_home(client):
    client.post("/grupos", data={"nome": "República"})

    resposta = client.get("/")

    assert "República" in resposta.get_data(as_text=True)


def test_criar_grupo_valido_redireciona_para_pagina_do_grupo(client):
    resposta = client.post("/grupos", data={"nome": "Viagem"})

    assert resposta.headers["Location"] == "/grupos/1"


def test_criar_grupo_nome_vazio_responde_400(client):
    resposta = client.post("/grupos", data={"nome": "   "})

    assert resposta.status_code == 400


def test_criar_grupo_nome_vazio_mostra_erro(client):
    resposta = client.post("/grupos", data={"nome": ""})

    assert "Informe um nome." in resposta.get_data(as_text=True)


def test_ver_grupo_existente_mostra_nome_no_titulo(client):
    client.post("/grupos", data={"nome": "Viagem"})

    resposta = client.get("/grupos/1")

    assert "<h1>Viagem</h1>" in resposta.get_data(as_text=True)


def test_ver_grupo_sem_membros_mostra_mensagem_vazia(client):
    client.post("/grupos", data={"nome": "Viagem"})

    resposta = client.get("/grupos/1")

    assert "Nenhum membro ainda." in resposta.get_data(as_text=True)


def test_ver_grupo_inexistente_responde_404(client):
    resposta = client.get("/grupos/999")

    assert resposta.status_code == 404


def test_home_com_grupo_tem_link_para_pagina_do_grupo(client):
    client.post("/grupos", data={"nome": "Viagem"})

    resposta = client.get("/")

    assert 'href="/grupos/1"' in resposta.get_data(as_text=True)
