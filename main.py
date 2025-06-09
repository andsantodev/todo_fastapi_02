# para rodar o código, execute: uvicorn main: app --reload
from fastapi import FastAPI
from passlib.context import CryptContext # Importando o CryptContext para criptografia de senhas
from dotenv import load_dotenv  # Importando o load_dotenv para carregar variáveis de ambiente
import os  # Importando o módulo os para manipulação de variáveis de ambiente


load_dotenv()


# Carregando a chave secreta do ambiente
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


# Criando a instância do FastAPI
app = FastAPI()


# Usando bcrypt como o esquema de criptografia
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# importando os routers
from auth_routes import auth_router
from tarefas_routes import tarefas_router


# Incluindo os routers
app.include_router(auth_router)
app.include_router(tarefas_router)