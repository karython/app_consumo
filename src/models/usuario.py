from sqlalchemy import Column, Integer, String
from conection import Base
import hashlib
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)

    veiculos = relationship("Veiculo", back_populates="usuario")
    
    def set_senha(self, senha_clara):
        self.senha = hashlib.sha256(senha_clara.encode('utf-8')).hexdigest()

    def verificar_senha(self, senha_clara):
        return self.senha == hashlib.sha256(senha_clara.encode('utf-8')).hexdigest()