import pytest

from app.services.validacao import (
    validar_nome,
    validar_valor,
    validar_pagador
)


def test_validar_nome_remove_espacos_das_pontas():
    assert validar_nome(" Ana ") == "Ana"


def test_validar_nome_vazio_lanca_erro():
    with pytest.raises(ValueError):
        validar_nome(" ")


def test_validar_nome_com_mais_de_cinquenta_caracteres_lanca_erro():
    with pytest.raises(ValueError):
        validar_nome("a" * 51)

def test_validar_valor_zero_lanca_erro():
    with pytest.raises(ValueError):
        validar_valor(0)


def test_validar_valor_negativo_lanca_erro():
    with pytest.raises(ValueError):
        validar_valor(-1)

def test_validar_pagador_fora_do_grupo_lanca_erro():
    with pytest.raises(ValueError):
        validar_pagador("Bia", ["Ana"])


def test_validar_pagador_do_grupo_nao_lanca_erro():
    validar_pagador("Ana", ["Ana"])
