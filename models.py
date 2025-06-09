# Criação das classes de modelo para o banco de dados.
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base
import os


# Criação do banco de dados usando SQLAlchemy
#db = create_engine("sqlite:///tarefas.db")
db = create_engine("DATABASE_URL")


# Cria a da base declarativa para os modelos
Base = declarative_base()


# Criar as classes/tabelas do banco de dados
# Usuários
class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column("id", Integer, primary_key=True, autoincrement=True, index=True)
    email = Column("email", String, nullable=False, unique=True)
    senha = Column("senha", String, nullable=False)

    # A função __init__ é usada para inicializar os atributos da classe
    def __init__(self, email: str, senha: str):
        self.email = email
        self.senha = senha


# Tarefas
class Tarefa(Base):
    __tablename__ = 'tarefas'
    
    id = Column("id", Integer, primary_key=True, autoincrement=True, index=True)
    titulo = Column("titulo", String, nullable=False)
    descricao = Column("descricao", String, nullable=False)
    concluida = Column("concluida", Boolean, default=False)
    usuario_id = Column("usuario_id", ForeignKey("usuarios.id"), nullable=False)

    # A função __init__ é usada para inicializar os atributos da classe
    def __init__(self, titulo: str, descricao: str, usuario_id: int, concluida: bool = False):
        self.titulo = titulo
        self.descricao = descricao
        self.usuario_id = usuario_id
        self.concluida = concluida


# Executa a criação das tabelas no banco de dados
Base.metadata.create_all(db)