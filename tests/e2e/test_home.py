from playwright.sync_api import Page, expect


def _criar_grupo(page: Page, live_server: str, nome: str):
    page.goto(live_server)
    page.get_by_label("Nome do grupo").fill(nome)
    page.get_by_role("button", name="Criar grupo").click()
    expect(page.get_by_role("heading", name=nome, level=1)).to_be_visible()

def _adicionar_membro(page: Page, nome: str):
    page.get_by_label("Nome do membro").fill(nome)
    page.get_by_role("button", name="Adicionar membro").click()
    expect(page.get_by_role("listitem").filter(has_text=nome)).to_be_visible()


def _adicionar_dois_membros(page: Page):
    _adicionar_membro(page, "Ana")
    _adicionar_membro(page, "Bruno")

def _registrar_despesa(page: Page, descricao: str, valor: str):
    page.get_by_label("Descrição").fill(descricao)
    page.get_by_label("Valor (R$)").fill(valor)
    page.get_by_label("Quem pagou").select_option(label="Ana")
    page.get_by_role("button", name="Registrar despesa").click()

def test_criar_grupo_abre_pagina_do_grupo(page: Page, live_server):
    _criar_grupo(page, live_server, "Grupo criação")

def test_adicionar_dois_membros_mostra_lista(page: Page, live_server):
    _criar_grupo(page, live_server, "Grupo membros")

    _adicionar_dois_membros(page)

    expect(page.get_by_role("listitem").filter(has_text="Ana")).to_be_visible()
    expect(page.get_by_role("listitem").filter(has_text="Bruno")).to_be_visible()

def test_registrar_despesa_mostra_valor_em_reais(page: Page, live_server):
    _criar_grupo(page, live_server, "Grupo despesa")
    _adicionar_dois_membros(page)

    _registrar_despesa(page, "Mercado", "12,50")

    expect(page.get_by_text("Mercado · R$ 12,50 · pago por Ana")).to_be_visible()

def test_valor_invalido_mostra_erro_e_nao_cria_despesa(page: Page, live_server):
    _criar_grupo(page, live_server, "Grupo valor inválido")
    _adicionar_dois_membros(page)

    _registrar_despesa(page, "Mercado", "doze")

    expect(page.get_by_role("alert")).to_contain_text("Use o formato 12,50.")
    expect(page.get_by_text("Nenhuma despesa ainda.")).to_be_visible()

def test_tela_de_saldos_mostra_quem_deve_e_quem_recebe(page: Page, live_server):
    _criar_grupo(page, live_server, "Grupo saldos")
    _adicionar_dois_membros(page)
    _registrar_despesa(page, "Mercado", "60,00")

    page.get_by_role("link", name="Ver saldos e acertos").click()

    expect(page.get_by_role("row", name="Ana a receber R$ 30,00")).to_be_visible()
    expect(page.get_by_role("row", name="Bruno deve R$ 30,00")).to_be_visible()

def test_tela_de_acertos_mostra_quem_paga_para_quem(page: Page, live_server):
    _criar_grupo(page, live_server, "Grupo acertos")
    _adicionar_dois_membros(page)
    _registrar_despesa(page, "Mercado", "60,00")

    page.get_by_role("link", name="Ver saldos e acertos").click()

    expect(page.get_by_text("Bruno paga R$ 30,00 para Ana", exact=True)).to_be_visible()