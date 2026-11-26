def test_home_get_responde_200(client):
    resposta = client.get("/")

    assert resposta.status_code == 200
