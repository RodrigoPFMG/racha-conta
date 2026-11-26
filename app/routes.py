"""Rotas finas: leem o formulário, chamam serviços e renderizam."""

from flask import Blueprint, redirect, render_template, request, url_for

from app import db
from app.models import Despesa, Grupo, Membro
from app.services import dinheiro, validacao

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    grupos = Grupo.query.order_by(Grupo.nome).all()
    return render_template("index.html", grupos=grupos)


@bp.post("/grupos")
def criar_grupo():
    try:
        nome = validacao.validar_nome(request.form.get("nome", ""))
    except ValueError as erro:
        grupos = Grupo.query.order_by(Grupo.nome).all()
        return render_template("index.html", grupos=grupos, erro=str(erro)), 400
    grupo = Grupo(nome=nome)
    db.session.add(grupo)
    db.session.commit()
    return redirect(url_for("main.ver_grupo", grupo_id=grupo.id))


@bp.get("/grupos/<int:grupo_id>")
def ver_grupo(grupo_id):
    grupo = db.get_or_404(Grupo, grupo_id)
    return render_template("grupo.html", grupo=grupo)


@bp.post("/grupos/<int:grupo_id>/membros")
def adicionar_membro(grupo_id):
    grupo = db.get_or_404(Grupo, grupo_id)
    try:
        nome = validacao.validar_nome(request.form.get("nome", ""))
    except ValueError as erro:
        return render_template("grupo.html", grupo=grupo, erro=str(erro)), 400
    db.session.add(Membro(nome=nome, grupo=grupo))
    db.session.commit()
    return redirect(url_for("main.ver_grupo", grupo_id=grupo.id))


def _ler_despesa(ids_dos_membros):
    """Lê o form de despesa; lança ValueError com a mensagem para o usuário."""
    try:
        descricao = validacao.validar_nome(request.form.get("descricao", ""))
    except ValueError:
        raise ValueError("Informe a descrição da despesa (até 50 caracteres).") from None
    valor_centavos = dinheiro.reais_para_centavos(request.form.get("valor", ""))
    validacao.validar_valor(valor_centavos)
    try:
        pagador_id = int(request.form.get("pagador", ""))
    except ValueError:
        raise ValueError("Escolha quem pagou.") from None
    validacao.validar_pagador(pagador_id, ids_dos_membros)
    try:
        participantes_ids = [int(valor) for valor in request.form.getlist("participantes")]
    except ValueError:
        raise ValueError("Selecione ao menos um participante.") from None
    validacao.validar_participantes(participantes_ids, ids_dos_membros)
    return descricao, valor_centavos, pagador_id, participantes_ids


@bp.post("/grupos/<int:grupo_id>/despesas")
def registrar_despesa(grupo_id):
    grupo = db.get_or_404(Grupo, grupo_id)
    try:
        descricao, valor_centavos, pagador_id, participantes_ids = _ler_despesa(
            [membro.id for membro in grupo.membros]
        )
    except ValueError as erro:
        return render_template("grupo.html", grupo=grupo, erro_despesa=str(erro)), 400
    participantes = Membro.query.filter(Membro.id.in_(participantes_ids)).all()
    db.session.add(Despesa(
        descricao=descricao,
        valor_centavos=valor_centavos,
        pagador_id=pagador_id,
        grupo=grupo,
        participantes=participantes,
    ))
    db.session.commit()
    return redirect(url_for("main.ver_grupo", grupo_id=grupo.id))
