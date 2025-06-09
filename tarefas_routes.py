from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from dependencies import pegar_sessao
from main import ALGORITHM, SECRET_KEY
from models import Tarefa


# Esquema de autenticação
auth_scheme = HTTPBearer()


# Função para verificação do token JWT
async def verificar_token(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(status_code=401, detail="Token expirado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    return payload["sub"]


# Rota para tarefas
tarefas_router = APIRouter(
    prefix="/tarefas",
    tags=["Tarefas"],
    dependencies=[Depends(verificar_token)]
)


# Rota para listar todas as tarefas
@tarefas_router.get("/")
async def listar_tarefas(session = Depends(pegar_sessao)):
    """
    Rota para listar todas as tarefas.
    Todas as rotas de tarefas precisam ser autenticadas.
    """
    tarefas = session.query(Tarefa).all()
    if not tarefas:
        return {"message": "Nenhuma tarefa encontrada"}
    return tarefas


# Rota para criar uma nova tarefa
@tarefas_router.post("/tarefa")
async def criar_tarefa(titulo: str, descricao: str, usuario_id: int, session = Depends(pegar_sessao)):
    """
    Rota para criar uma nova tarefa.
    Todas as rotas de tarefas precisam ser autenticadas.
    """
    nova_tarefa = Tarefa(
        titulo=titulo,
        descricao=descricao,
        usuario_id=usuario_id
    )
    session.add(nova_tarefa)
    session.commit()
    return {"message": "Tarefa criada com sucesso"}


# Rota para atualizar uma tarefa
@tarefas_router.put("/tarefa/{tarefa_id}")
async def atualizar_tarefa(tarefa_id: int, titulo: str, descricao: str, concluida: bool, session = Depends(pegar_sessao)):
    """
    Rota para atualizar uma tarefa existente.
    Todas as rotas de tarefas precisam ser autenticadas.
    """
    tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not tarefa:
        return {"message": "Tarefa não encontrada ou você não tem permissão para atualizá-la"}
    
    tarefa.titulo = titulo
    tarefa.descricao = descricao
    tarefa.concluida = concluida
    session.commit()
    return {"message": "Tarefa atualizada com sucesso"}


# Rota para excluir uma tarefa
@tarefas_router.delete("/tarefa/{tarefa_id}")
async def excluir_tarefa(tarefa_id: int, session = Depends(pegar_sessao)):
    """
    Rota para excluir uma tarefa existente.
    Todas as rotas de tarefas precisam ser autenticadas.
    """
    tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not tarefa:
        return {"message": "Tarefa não encontrada ou você não tem permissão para excluí-la"}
    
    session.delete(tarefa)
    session.commit()
    return {"message": "Tarefa excluída com sucesso"}