from app.services.saldos import DespesaDTO, calcular_saldos


def test_calcular_saldos_sem_despesas_deixa_todos_zerados():
    assert calcular_saldos([1, 2], []) == {1: 0, 2: 0}


def test_calcular_saldos_despesa_dividida_por_dois_pagador_recebe_metade():
    despesas = [DespesaDTO(pagador_id=1, valor_centavos=1000, participantes_ids=(1, 2))]

    assert calcular_saldos([1, 2], despesas) == {1: 500, 2: -500}


def test_calcular_saldos_pagador_fora_da_divisao_recebe_valor_inteiro():
    despesas = [DespesaDTO(pagador_id=1, valor_centavos=900, participantes_ids=(2, 3))]

    assert calcular_saldos([1, 2, 3], despesas) == {1: 900, 2: -450, 3: -450}


def test_calcular_saldos_despesas_de_pagadores_diferentes_se_compensam():
    despesas = [
        DespesaDTO(pagador_id=1, valor_centavos=1000, participantes_ids=(1, 2)),
        DespesaDTO(pagador_id=2, valor_centavos=1000, participantes_ids=(1, 2)),
    ]

    assert calcular_saldos([1, 2], despesas) == {1: 0, 2: 0}


def test_calcular_saldos_soma_de_todos_os_saldos_e_zero():
    despesas = [
        DespesaDTO(pagador_id=1, valor_centavos=1000, participantes_ids=(1, 2, 3)),
        DespesaDTO(pagador_id=2, valor_centavos=701, participantes_ids=(2, 3)),
    ]

    assert sum(calcular_saldos([1, 2, 3], despesas).values()) == 0


def test_calcular_saldos_dez_reais_por_tres_nao_perde_centavo():
    despesas = [DespesaDTO(pagador_id=1, valor_centavos=1000, participantes_ids=(3, 1, 2))]

    assert calcular_saldos([1, 2, 3], despesas) == {1: 666, 2: -333, 3: -333}


def test_calcular_saldos_membro_sem_despesas_fica_zerado():
    despesas = [DespesaDTO(pagador_id=1, valor_centavos=1000, participantes_ids=(1, 2))]

    assert calcular_saldos([1, 2, 3], despesas)[3] == 0


def test_calcular_saldos_despesa_com_um_participante_que_e_o_pagador_fica_zerado():
    despesas = [DespesaDTO(pagador_id=1, valor_centavos=1000, participantes_ids=(1,))]

    assert calcular_saldos([1, 2], despesas) == {1: 0, 2: 0}
