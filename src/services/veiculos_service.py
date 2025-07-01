from conection import SessionLocal
from models.veiculos import Veiculo

veiculo_cadastrado = {"obj": None}
from models.abastecimento import Abastecimento
from sqlalchemy.orm import Session

# logica que busca no banco a ultima kilometragem e soma para ter a media
# calcula a quantidade de litros abastecido com base nos valores
def calcular_media_consumo_por_combustivel(id_veiculo: int, tipo_combustivel: str):
    with SessionLocal() as session:
        abastecimentos = (
            session.query(Abastecimento)
            .filter_by(id_veiculo=id_veiculo, tipo_combustivel=tipo_combustivel)
            .order_by(Abastecimento.data_abastecimento.asc())
            .all()
        )
        if len(abastecimentos) < 2:
            return None  # não há registros suficientes para calcular

        total_km = 0
        total_litros = 0.0

        for i in range(1, len(abastecimentos)):
            km_rodado = abastecimentos[i].kilometragem_atual - abastecimentos[i - 1].kilometragem_atual
            litros_abastecidos = abastecimentos[i].valor_abastecido / abastecimentos[i].valor_litro

            total_km += km_rodado
            total_litros += litros_abastecidos

        if total_litros == 0:
            return None

        media = total_km / total_litros
        return round(media, 2)


def criar_veiculo(modelo, tipo_veiculo, ano_fabricacao, fabricante, kilometragem, placa, tipo_combustivel, cap_max_tanque, id_usuario):
    session = SessionLocal()
    # adicionar verificação de placa se ja foi cadastrada
    try:
        veiculo = Veiculo(
            modelo=str(modelo).upper(),
            tipo_veiculo=str(tipo_veiculo).upper(),
            ano_fabricacao=ano_fabricacao,
            fabricante=str(fabricante).upper(),
            kilometragem=kilometragem,
            placa=str(placa).upper(),
            tipo_combustivel=str(tipo_combustivel).upper(),
            cap_max_tanque=cap_max_tanque, 
            id_usuario=id_usuario
        )
        session.add(veiculo)
        session.commit()
        session.refresh(veiculo)
        return veiculo
    finally:
        session.close()

def listar_veiculos():
    session = SessionLocal()
    try:
        return session.query(Veiculo).all()
    finally:
        session.close()

def buscar_veiculo_por_id(veiculo_id):
    session = SessionLocal()
    try:
        return session.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
    finally:
        session.close()

def atualizar_veiculo(veiculo_id, **kwargs):
    session = SessionLocal()
    try:
        veiculo = session.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
        if not veiculo:
            return None
        for key, value in kwargs.items():
            if hasattr(veiculo, key):
                setattr(veiculo, key, value)
        session.commit()
        session.refresh(veiculo)
        return veiculo
    finally:
        session.close()

def deletar_veiculo(veiculo_id):
    session = SessionLocal()
    try:
        veiculo = session.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
        if not veiculo:
            return False
        session.delete(veiculo)
        session.commit()
        return True
    finally:
        session.close()

def buscar_veiculo_por_usuario_id(usuario_id):
    session = SessionLocal()
    try:
        return session.query(Veiculo).filter(Veiculo.id_usuario == usuario_id).first()
    finally:
        session.close()