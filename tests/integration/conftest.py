"""Fixtures compartilhadas pelos testes de integração das rotas."""

import pytest


@pytest.fixture
def grupo_com_membros(client):
    client.post("/grupos", data={"nome": "República"})
    client.post("/grupos/1/membros", data={"nome": "Ana"})
    client.post("/grupos/1/membros", data={"nome": "Bruno"})
    return "/grupos/1"
