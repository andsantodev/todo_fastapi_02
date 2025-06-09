from models import db
from sqlalchemy.orm import sessionmaker

def pegar_sessao():
    """
    Retorna a sessão do banco de dados.
    """
    try:
      Session = sessionmaker(bind=db)
      session = Session()
      yield session
    finally:
       session.close()