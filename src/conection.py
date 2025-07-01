from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Caminho do banco de dados SQLite
DATABASE_URL = "sqlite:///app_consumo.db"

# Cria o engine do SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Cria uma classe base para os modelos
Base = declarative_base()

# Cria uma fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
