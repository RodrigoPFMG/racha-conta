"""Sugestão pura de acertos (quem paga quanto para quem)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Acerto:
    de: int
    para: int
    centavos: int


def sugerir_acertos(saldos: dict[int, int]) -> list[Acerto]:
    """Algoritmo guloso: o maior devedor paga ao maior credor.

    Paga o mínimo entre a dívida e o crédito e repete até zerar.
    Empates vão para o menor id; saldos zerados são ignorados e o
    dict recebido não é alterado.
    """
    restante = {membro_id: saldo for membro_id, saldo in saldos.items() if saldo != 0}
    acertos = []
    while restante:
        devedor = min((m for m in restante if restante[m] < 0), key=lambda m: (restante[m], m))
        credor = min((m for m in restante if restante[m] > 0), key=lambda m: (-restante[m], m))
        centavos = min(-restante[devedor], restante[credor])
        acertos.append(Acerto(de=devedor, para=credor, centavos=centavos))
        restante[devedor] += centavos
        restante[credor] -= centavos
        restante = {membro_id: saldo for membro_id, saldo in restante.items() if saldo != 0}
    return acertos
