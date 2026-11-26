"""Modelos do banco. Valores monetários sempre em centavos (int)."""

from app import db


class Grupo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
