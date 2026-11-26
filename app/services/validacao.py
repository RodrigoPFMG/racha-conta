"""Validações puras para dados do domínio."""


def validar_nome(nome: str) -> str:
    """Remove espaços das pontas e exige um nome de até 50 caracteres."""
    nome_validado = nome.strip()
    if not nome_validado:
        raise ValueError("O nome não pode ficar vazio.")
    if len(nome_validado) > 50:
        raise ValueError("O nome deve ter no máximo 50 caracteres.")
    return nome_validado

def validar_valor(centavos: int) -> None:
    """Exige um valor monetário positivo, expresso em centavos."""
    if centavos <= 0:
        raise ValueError("O valor deve ser maior que zero.")

def validar_pagador(pagador, membros) -> None:
    """Exige que o pagador pertença ao grupo."""
    if pagador not in membros:
        raise ValueError("O pagador deve ser um membro do grupo.")