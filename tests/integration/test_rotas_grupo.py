def test_home_sem_grupos_mostra_mensagem_vazia(client):
    resposta = client.get("/")

    assert "Nenhum grupo ainda." in resposta.get_data(as_text=True)


def test_criar_grupo_valido_aparece_na_home(client):
    client.post("/grupos", data={"nome": "República"})

    resposta = client.get("/")

    assert "República" in resposta.get_data(as_text=True)


def test_criar_grupo_valido_redireciona(client):
    resposta = client.post("/grupos", data={"nome": "Viagem"})

    assert resposta.status_code == 302


def test_criar_grupo_nome_vazio_responde_400(client):
    resposta = client.post("/grupos", data={"nome": "   "})

    assert resposta.status_code == 400


def test_criar_grupo_nome_vazio_mostra_erro(client):
    resposta = client.post("/grupos", data={"nome": ""})

    assert "Informe um nome." in resposta.get_data(as_text=True)
