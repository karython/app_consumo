from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from conection import Base

class Abastecimento(Base):
    __tablename__ = "abastecimentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_veiculo = Column(Integer, ForeignKey("veiculos.id"), nullable=False)
    tipo_combustivel = Column(String(20), nullable=False)
    valor_litro = Column(Float, nullable=False)
    valor_abastecido = Column(Float, nullable=False)
    kilometragem_atual = Column(Integer, nullable=False)
    data_abastecimento = Column(DateTime, default=datetime.now())

    veiculo = relationship("Veiculo", back_populates="abastecimentos")