from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from conection import Base

class Veiculo(Base):
    __tablename__ = "veiculos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    modelo = Column(String, nullable=False)
    tipo_veiculo = Column(String, nullable=False)
    ano_fabricacao = Column(Integer, nullable=False)
    fabricante = Column(String, nullable=False)
    kilometragem = Column(Integer, nullable=False)
    placa = Column(String, unique=True, nullable=False)
    tipo_combustivel = Column(String, nullable=False)
    cap_max_tanque = Column(Integer, nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)  # <-- relação

    historicos = relationship("Historico", back_populates="veiculo")
    trocas_oleo = relationship("TrocaOleo", back_populates="veiculo")
    usuario = relationship("Usuario", back_populates="veiculos")
    abastecimentos = relationship("Abastecimento", back_populates="veiculo", cascade="all, delete-orphan")

    from models.abastecimento import Abastecimento 