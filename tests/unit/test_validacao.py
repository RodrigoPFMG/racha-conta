import pytest

from app.services.validacao import (
    validar_nome
)


def test_validar_nome_remove_espacos_das_pontas():
    assert validar_nome(" Ana ") == "Ana"


def test_validar_nome_vazio_lanca_erro():
    with pytest.raises(ValueError):
        validar_nome(" ")


def test_validar_nome_com_mais_de_cinquenta_caracteres_lanca_erro():
    with pytest.raises(ValueError):
        validar_nome("a" * 51)
