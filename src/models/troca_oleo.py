from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from conection import Base

class TrocaOleo(Base):
    __tablename__ = "troca_oleo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    kilometragem_atual = Column(Integer, nullable=False)
    data_troca = Column(DateTime, nullable=False)
    marca_oleo = Column(String, nullable=False)
    tipo_oleo = Column(String, nullable=False)
    id_veiculo = Column(Integer, ForeignKey("veiculos.id"), nullable=False)

    veiculo = relationship("Veiculo", back_populates="trocas_oleo")