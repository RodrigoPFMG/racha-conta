from app import db
from app.models import Grupo


def test_criar_grupo_persiste_nome(app):
    db.session.add(Grupo(nome="República"))
    db.session.commit()

    assert Grupo.query.one().nome == "República"
