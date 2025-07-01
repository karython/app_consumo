from conection import engine, Base
from models.usuario import Usuario
from models.veiculos import Veiculo
from models.historico import Historico
from models.troca_oleo import TrocaOleo
from models.abastecimento import Abastecimento

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")