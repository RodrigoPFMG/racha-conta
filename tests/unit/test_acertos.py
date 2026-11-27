from app.services.acertos import Acerto, sugerir_acertos


def aplicar(saldos, acertos):
    """Devolve os saldos depois de cada acerto ser pago."""
    resultado = dict(saldos)
    for acerto in acertos:
        resultado[acerto.de] += acerto.centavos
        resultado[acerto.para] -= acerto.centavos
    return resultado


def centavos_dos(acertos):
    return [acerto.centavos for acerto in acertos]


def test_sugerir_acertos_todos_quitados_retorna_lista_vazia():
    assert sugerir_acertos({1: 0, 2: 0}) == []


def test_sugerir_acertos_duas_pessoas_gera_um_acerto_com_valor_exato():
    assert sugerir_acertos({1: 500, 2: -500}) == [Acerto(de=2, para=1, centavos=500)]


def test_sugerir_acertos_tres_pessoas_um_credor_gera_dois_acertos():
    acertos = sugerir_acertos({1: 666, 2: -333, 3: -333})

    assert acertos == [Acerto(de=2, para=1, centavos=333), Acerto(de=3, para=1, centavos=333)]


def test_sugerir_acertos_dois_devedores_dois_credores_gera_acertos_esperados():
    acertos = sugerir_acertos({1: 700, 2: 300, 3: -600, 4: -400})

    assert acertos == [
        Acerto(de=3, para=1, centavos=600),
        Acerto(de=4, para=2, centavos=300),
        Acerto(de=4, para=1, centavos=100),
    ]


def test_sugerir_acertos_aplicados_zeram_todos_os_saldos():
    saldos = {1: 1000, 2: -250, 3: -350, 4: -400, 5: 0}

    acertos = sugerir_acertos(saldos)

    assert aplicar(saldos, acertos) == {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}


def test_sugerir_acertos_nunca_gera_mais_que_n_menos_um_transferencias():
    saldos = {1: 500, 2: 300, 3: -200, 4: -350, 5: -250}

    acertos = sugerir_acertos(saldos)

    assert len(acertos) <= len(saldos) - 1


def test_sugerir_acertos_nenhum_acerto_tem_valor_zero_ou_negativo():
    acertos = sugerir_acertos({1: 500, 2: 300, 3: -200, 4: -350, 5: -250, 6: 0})

    assert min(centavos_dos(acertos)) > 0


def test_sugerir_acertos_saldo_de_um_centavo_gera_acerto_de_um_centavo():
    assert sugerir_acertos({1: 1, 2: -1}) == [Acerto(de=2, para=1, centavos=1)]


def test_sugerir_acertos_nao_altera_saldos_recebidos():
    saldos = {1: 500, 2: -500}

    sugerir_acertos(saldos)

    assert saldos == {1: 500, 2: -500}
