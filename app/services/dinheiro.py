"""Funções puras de dinheiro. Todo valor monetário é int em centavos."""

import re

_FORMATO_BR = re.compile(r"^\d{1,3}(\.\d{3})+(,\d{1,2})?$|^\d+(,\d{1,2})?$")
_FORMATO_PONTO = re.compile(r"^\d+(\.\d{1,2})?$")


def reais_para_centavos(texto: str) -> int:
    """Converte "12,50", "12.50" ou "1.234,56" em centavos.

    Lança ValueError para texto inválido, negativo ou com mais de 2 casas.
    """
    valor = str(texto).strip().removeprefix("R$").strip()
    if _FORMATO_PONTO.match(valor):
        inteiro, _, decimal = valor.partition(".")
    elif _FORMATO_BR.match(valor):
        inteiro, _, decimal = valor.replace(".", "").partition(",")
    else:
        raise ValueError(f"Valor inválido: {texto!r}. Use o formato 12,50.")
    return int(inteiro) * 100 + int(decimal.ljust(2, "0"))


def formatar_brl(centavos: int) -> str:
    """Formata centavos como moeda brasileira: 123456 -> "R$ 1.234,56"."""
    sinal = "-" if centavos < 0 else ""
    reais, resto = divmod(abs(centavos), 100)
    reais_com_milhar = f"{reais:,}".replace(",", ".")
    return f"{sinal}R$ {reais_com_milhar},{resto:02d}"


def dividir_igualmente(centavos: int, n: int) -> list[int]:
    """Divide o total em n partes inteiras que somam exatamente o total.

    Os centavos que sobram vão um a um para as primeiras partes, então
    a diferença entre quaisquer duas partes é no máximo 1 centavo.
    """
    if n <= 0:
        raise ValueError("É preciso dividir entre pelo menos uma pessoa.")
    base, sobra = divmod(centavos, n)
    return [base + 1] * sobra + [base] * (n - sobra)
