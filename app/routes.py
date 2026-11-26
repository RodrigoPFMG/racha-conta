"""Rotas finas: leem o formulário, chamam serviços e renderizam."""

from flask import Blueprint, redirect, render_template, request, url_for

from app import db
from app.models import Grupo, Membro
from app.services import validacao

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
