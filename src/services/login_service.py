from conection import SessionLocal
from models.usuario import Usuario

def autenticar_usuario(email, senha_clara):
    session = SessionLocal()
    try:
        usuario = session.query(Usuario).filter(Usuario.email == email).first()
        if usuario and usuario.verificar_senha(senha_clara):
            return usuario
        return None
    finally:
        session.close()