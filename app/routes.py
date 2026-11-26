"""Rotas finas: leem o formulário, chamam serviços e renderizam."""

from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")
