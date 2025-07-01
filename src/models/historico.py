from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from conection import Base

class Historico(Base):
    __tablename__ = "historico"

    id = Column(Integer, primary_key=True, autoincrement=True)
    datahora_abastecimento = Column(DateTime, nullable=True)
    kilometragem_abastecimento = Column(Integer, nullable=True)
    id_veiculo = Column(Integer, ForeignKey("veiculos.id"), nullable=False)
    data_hora_troca_oleo = Column(DateTime, nullable=True)

    veiculo = relationship("Veiculo", back_populates="historicos")