from conection import SessionLocal
from models.abastecimento import Abastecimento

def criar_abastecimento(id_veiculo, tipo_combustivel, valor_litro, valor_abastecido, kilometragem_atual, data_abastecimento=None):
    session = SessionLocal()
    try:
        abastecimento = Abastecimento(
            id_veiculo=id_veiculo,
            tipo_combustivel=tipo_combustivel,
            valor_litro=valor_litro,
            valor_abastecido=valor_abastecido,
            kilometragem_atual=kilometragem_atual,
            data_abastecimento=data_abastecimento
        )
        session.add(abastecimento)
        session.commit()
        session.refresh(abastecimento)
        return abastecimento
    finally:
        session.close()

def buscar_ultimo_km_por_veiculo(id_veiculo):
    session = SessionLocal()
    resultado = (
        session.query(Abastecimento)
        .filter_by(id_veiculo=id_veiculo)
        .order_by(Abastecimento.kilometragem_atual.desc())
        .first()
    )
    session.close()
    if resultado:
        return resultado.kilometragem_atual
    return None


def listar_abastecimentos():
    session = SessionLocal()
    try:
        return session.query(Abastecimento).all()
    finally:
        session.close()

def buscar_abastecimento_por_id(abastecimento_id):
    session = SessionLocal()
    try:
        return session.query(Abastecimento).filter(Abastecimento.id == abastecimento_id).first()
    finally:
        session.close()

def listar_abastecimentos_por_veiculo(id_veiculo):
    session = SessionLocal()
    try:
        return session.query(Abastecimento).filter(Abastecimento.id_veiculo == id_veiculo).all()
    finally:
        session.close()

def deletar_abastecimento(abastecimento_id):
    session = SessionLocal()
    try:
        abastecimento = session.query(Abastecimento).filter(Abastecimento.id == abastecimento_id).first()
        if abastecimento:
            session.delete(abastecimento)
            session.commit()
            return True
        return False
    finally:
        session.close()