import pytest

from app.services.dinheiro import dividir_igualmente, formatar_brl, reais_para_centavos


def test_reais_para_centavos_com_virgula_converte():
    assert reais_para_centavos("12,50") == 1250


def test_reais_para_centavos_com_ponto_converte():
    assert reais_para_centavos("12.50") == 1250


def test_reais_para_centavos_sem_decimais_converte():
    assert reais_para_centavos("7") == 700


def test_reais_para_centavos_com_milhar_converte():
    assert reais_para_centavos("1.234,56") == 123456


def test_reais_para_centavos_texto_invalido_lanca_erro():
    with pytest.raises(ValueError):
        reais_para_centavos("doze reais")


def test_reais_para_centavos_negativo_lanca_erro():
    with pytest.raises(ValueError):
        reais_para_centavos("-5,00")


def test_reais_para_centavos_mais_de_duas_casas_lanca_erro():
    with pytest.raises(ValueError):
        reais_para_centavos("1,999")


def test_formatar_brl_valor_simples_usa_virgula():
    assert formatar_brl(1250) == "R$ 12,50"


def test_formatar_brl_valor_com_milhar_usa_ponto():
    assert formatar_brl(123456) == "R$ 1.234,56"


def test_formatar_brl_menos_de_um_real_mostra_zero():
    assert formatar_brl(5) == "R$ 0,05"


def test_formatar_brl_negativo_mostra_sinal():
    assert formatar_brl(-3000) == "-R$ 30,00"


def test_dividir_igualmente_com_sobra_da_centavo_extra_aos_primeiros():
    assert dividir_igualmente(1000, 3) == [334, 333, 333]


def test_dividir_igualmente_divisao_exata_partes_iguais():
    assert dividir_igualmente(900, 3) == [300, 300, 300]


def test_dividir_igualmente_soma_das_partes_igual_ao_total():
    assert sum(dividir_igualmente(1001, 7)) == 1001


def test_dividir_igualmente_diferenca_maxima_de_um_centavo():
    partes = dividir_igualmente(1000, 6)

    assert max(partes) - min(partes) <= 1


def test_dividir_igualmente_por_zero_lanca_erro():
    with pytest.raises(ValueError):
        dividir_igualmente(1000, 0)


def test_dividir_igualmente_por_negativo_lanca_erro():
    with pytest.raises(ValueError):
        dividir_igualmente(1000, -2)
