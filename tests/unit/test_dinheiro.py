import pytest

from app.services.dinheiro import reais_para_centavos


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
