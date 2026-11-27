from playwright.sync_api import Page, expect


def _criar_grupo(page: Page, live_server: str, nome: str):
    page.goto(live_server)
    page.get_by_label("Nome do grupo").fill(nome)
    page.get_by_role("button", name="Criar grupo").click()
    expect(page.get_by_role("heading", name=nome, level=1)).to_be_visible()

def test_criar_grupo_abre_pagina_do_grupo(page: Page, live_server):
    _criar_grupo(page, live_server, "Grupo criação")