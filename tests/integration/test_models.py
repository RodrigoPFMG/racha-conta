from app import db
from app.models import Despesa, Grupo, Membro


def test_criar_grupo_persiste_nome(app):
    db.session.add(Grupo(nome="República"))
    db.session.commit()

    assert Grupo.query.one().nome == "República"


def test_adicionar_membro_aparece_nos_membros_do_grupo(app):
    grupo = Grupo(nome="Viagem")
    db.session.add(Membro(nome="Ana", grupo=grupo))
    db.session.commit()

    assert [m.nome for m in grupo.membros] == ["Ana"]


def test_criar_despesa_guarda_valor_em_centavos_e_pagador(app):
    grupo = Grupo(nome="Casa")
    ana = Membro(nome="Ana", grupo=grupo)
    db.session.add(Despesa(descricao="Pizza", valor_centavos=4590, pagador=ana, grupo=grupo))
    db.session.commit()

    despesa = Despesa.query.one()
    assert (despesa.valor_centavos, despesa.pagador.nome) == (4590, "Ana")


def test_criar_despesa_registra_data_de_criacao(app):
    grupo = Grupo(nome="Casa")
    ana = Membro(nome="Ana", grupo=grupo)
    db.session.add(Despesa(descricao="Gás", valor_centavos=10000, pagador=ana, grupo=grupo))
    db.session.commit()

    assert Despesa.query.one().criada_em is not None


def test_despesa_com_participantes_lista_os_membros(app):
    grupo = Grupo(nome="Casa")
    ana = Membro(nome="Ana", grupo=grupo)
    bruno = Membro(nome="Bruno", grupo=grupo)
    db.session.add(Despesa(descricao="Luz", valor_centavos=9000, pagador=ana,
                           grupo=grupo, participantes=[ana, bruno]))
    db.session.commit()

    assert {m.nome for m in Despesa.query.one().participantes} == {"Ana", "Bruno"}
