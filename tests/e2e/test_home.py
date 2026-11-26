from playwright.sync_api import Page, expect


def test_abrir_home_mostra_titulo_racha_conta(page: Page, live_server):
    page.goto(live_server)

    expect(page).to_have_title("Racha Conta")
