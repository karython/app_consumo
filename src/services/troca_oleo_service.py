from conection import SessionLocal
from models.troca_oleo import TrocaOleo

def criar_troca_oleo(kilometragem_atual, data_troca, marca_oleo, tipo_oleo, id_veiculo):
    session = SessionLocal()
    try:
        troca = TrocaOleo(
            kilometragem_atual=kilometragem_atual,
            data_troca=data_troca,
            marca_oleo=marca_oleo,
            tipo_oleo=tipo_oleo,
            id_veiculo=id_veiculo
        )
        session.add(troca)
        session.commit()
        session.refresh(troca)
        return troca
    finally:
        session.close()

def listar_trocas_oleo():
    session = SessionLocal()
    try:
        return session.query(TrocaOleo).all()
    finally:
        session.close()

def buscar_troca_oleo_por_id(troca_id):
    session = SessionLocal()
    try:
        return session.query(TrocaOleo).filter(TrocaOleo.id == troca_id).first()
    finally:
        session.close()

def atualizar_troca_oleo(troca_id, **kwargs):
    session = SessionLocal()
    try:
        troca = session.query(TrocaOleo).filter(TrocaOleo.id == troca_id).first()
        if not troca:
            return None
        for key, value in kwargs.items():
            if hasattr(troca, key):
                setattr(troca, key, value)
        session.commit()
        session.refresh(troca)
        return troca
    finally:
        session.close()

def deletar_troca_oleo(troca_id):
    session = SessionLocal()
    try:
        troca = session.query(TrocaOleo).filter(TrocaOleo.id == troca_id).first()
        if not troca:
            return False
        session.delete(troca)
        session.commit()
        return True
    finally:
        session.close()