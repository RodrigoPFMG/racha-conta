from app import db
from app.models import Grupo, Membro


def test_criar_grupo_persiste_nome(app):
    db.session.add(Grupo(nome="República"))
    db.session.commit()

    assert Grupo.query.one().nome == "República"


def test_adicionar_membro_aparece_nos_membros_do_grupo(app):
    grupo = Grupo(nome="Viagem")
    db.session.add(Membro(nome="Ana", grupo=grupo))
    db.session.commit()

    assert [m.nome for m in grupo.membros] == ["Ana"]
