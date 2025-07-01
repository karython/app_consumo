from conection import SessionLocal
from models.historico import Historico

def criar_historico(datahora_abastecimento, kilometragem_abastecimento, id_veiculo, data_hora_troca_oleo):
    session = SessionLocal()
    try:
        historico = Historico(
            datahora_abastecimento=datahora_abastecimento,
            kilometragem_abastecimento=kilometragem_abastecimento,
            id_veiculo=id_veiculo,
            data_hora_troca_oleo=data_hora_troca_oleo
        )
        session.add(historico)
        session.commit()
        session.refresh(historico)
        return historico
    finally:
        session.close()

def listar_historicos():
    session = SessionLocal()
    try:
        return session.query(Historico).all()
    finally:
        session.close()

def buscar_historico_por_id(historico_id):
    session = SessionLocal()
    try:
        return session.query(Historico).filter(Historico.id == historico_id).first()
    finally:
        session.close()

def atualizar_historico(historico_id, **kwargs):
    session = SessionLocal()
    try:
        historico = session.query(Historico).filter(Historico.id == historico_id).first()
        if not historico:
            return None
        for key, value in kwargs.items():
            if hasattr(historico, key):
                setattr(historico, key, value)
        session.commit()
        session.refresh(historico)
        return historico
    finally:
        session.close()

def deletar_historico(historico_id):
    session = SessionLocal()
    try:
        historico = session.query(Historico).filter(Historico.id == historico_id).first()
        if not historico:
            return False
        session.delete(historico)
        session.commit()
        return True
    finally:
        session.close()