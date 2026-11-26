"""Rotas finas: leem o formulário, chamam serviços e renderizam."""

from flask import Blueprint, redirect, render_template, request, url_for

from app import db
from app.models import Grupo, Membro

bp = Blueprint("main", __name__)


def _ler_nome(campo):
    # Provisório: trocar por validacao.validar_nome quando o João fizer o merge.
    nome = request.form.get(campo, "").strip()
    if not nome:
        raise ValueError("Informe um nome.")
    return nome


@bp.route("/")
def index():
    grupos = Grupo.query.order_by(Grupo.nome).all()
    return render_template("index.html", grupos=grupos)


@bp.post("/grupos")
def criar_grupo():
    try:
        nome = _ler_nome("nome")
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
        nome = _ler_nome("nome")
    except ValueError as erro:
        return render_template("grupo.html", grupo=grupo, erro=str(erro)), 400
    db.session.add(Membro(nome=nome, grupo=grupo))
    db.session.commit()
    return redirect(url_for("main.ver_grupo", grupo_id=grupo.id))
