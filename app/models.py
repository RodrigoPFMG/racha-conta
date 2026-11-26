"""Modelos do banco. Valores monetários sempre em centavos (int)."""

from app import db


class Grupo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)


class Membro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey("grupo.id"), nullable=False)
    grupo = db.relationship("Grupo", backref=db.backref("membros", lazy=True, cascade="all, delete-orphan"))
