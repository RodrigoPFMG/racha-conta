"""Modelos do banco. Valores monetários sempre em centavos (int)."""

from datetime import datetime, timezone

from app import db


class Grupo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)


class Membro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey("grupo.id"), nullable=False)
    grupo = db.relationship("Grupo", backref=db.backref("membros", lazy=True, cascade="all, delete-orphan"))


participacao = db.Table(
    "participacao",
    db.Column("despesa_id", db.Integer, db.ForeignKey("despesa.id"), primary_key=True),
    db.Column("membro_id", db.Integer, db.ForeignKey("membro.id"), primary_key=True),
)


def _agora():
    return datetime.now(timezone.utc)


class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    valor_centavos = db.Column(db.Integer, nullable=False)
    pagador_id = db.Column(db.Integer, db.ForeignKey("membro.id"), nullable=False)
    pagador = db.relationship("Membro", foreign_keys=[pagador_id])
    grupo_id = db.Column(db.Integer, db.ForeignKey("grupo.id"), nullable=False)
    grupo = db.relationship("Grupo", backref=db.backref("despesas", lazy=True, cascade="all, delete-orphan"))
    criada_em = db.Column(db.DateTime, nullable=False, default=_agora)
    participantes = db.relationship("Membro", secondary=participacao, lazy="subquery")
