"""Cálculo puro de saldos. Positivo = tem a receber; negativo = deve."""

from dataclasses import dataclass

from app.services.dinheiro import dividir_igualmente


@dataclass(frozen=True)
class DespesaDTO:
    pagador_id: int
    valor_centavos: int
    participantes_ids: tuple[int, ...]


def calcular_saldos(membros_ids, despesas) -> dict[int, int]:
    """Soma o que cada membro pagou e subtrai a parte que lhe cabe.

    A divisão segue os participantes ordenados por id, então o centavo
    que sobra fica com o participante de menor id.
    """
    saldos = {membro_id: 0 for membro_id in membros_ids}
    for despesa in despesas:
        saldos[despesa.pagador_id] += despesa.valor_centavos
        participantes = sorted(despesa.participantes_ids)
        partes = dividir_igualmente(despesa.valor_centavos, len(participantes))
        for participante_id, parte in zip(participantes, partes):
            saldos[participante_id] -= parte
    return saldos
