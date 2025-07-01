from conection import SessionLocal
from models.usuario import Usuario

def criar_usuario(nome, email, senha_clara):
    session = SessionLocal()
    try:
        usuario = Usuario(nome=nome, email=email)
        usuario.set_senha(senha_clara)
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario
    finally:
        session.close()

def listar_usuarios():
    session = SessionLocal()
    try:
        return session.query(Usuario).all()
    finally:
        session.close()

def buscar_usuario_por_id(usuario_id):
    session = SessionLocal()
    try:
        return session.query(Usuario).filter(Usuario.id == usuario_id).first()
    finally:
        session.close()

def buscar_usuario_por_email(email):
    session = SessionLocal()
    try:
        return session.query(Usuario).filter(Usuario.email == email).first()
    finally:
        session.close()

def atualizar_usuario(usuario_id, **kwargs):
    session = SessionLocal()
    try:
        usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            return None
        for key, value in kwargs.items():
            if key == "senha":
                usuario.set_senha(value)
            elif hasattr(usuario, key):
                setattr(usuario, key, value)
        session.commit()
        session.refresh(usuario)
        return usuario
    finally:
        session.close()

def deletar_usuario(usuario_id):
    session = SessionLocal()
    try:
        usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            return False
        session.delete(usuario)
        session.commit()
        return True
    finally:
        session.close()