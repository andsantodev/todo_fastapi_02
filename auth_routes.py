from fastapi import APIRouter, Depends, HTTPException
from dependencies import pegar_sessao
from models import Usuario
from main import ALGORITHM, SECRET_KEY, bcrypt_context
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


auth_router = APIRouter(prefix="/auth", tags=["Atenticação"])


# Função para criar um token JWT
def criar_token(id_usuario):
    data_expiracao = datetime.now(timezone.utc) + timedelta(hours=24)
    dic_infos = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_infos, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado


# Rota de autenticação para login
@auth_router.get("/login")
async def login(email: str, senha: str, session = Depends(pegar_sessao)):
    """
    Rota de autenticação para login.
    """
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if not bcrypt_context.verify(senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Senha incorreta")
    else:
        access_token = criar_token(usuario.id)
        return {
            "message": f"Usuário {usuario.email} autenticado com sucesso",
            "autenticado": True,
            "access_token": access_token,
            "token_type": "Bearer"
        }


# Rota de autenticação para criar conta
@auth_router.get("/criar_conta")
async def criar_conta(email: str, senha: str, session = Depends(pegar_sessao)):
    """
    Rota de autenticação para criar uma nova conta.
    """
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    else:
        senha_criptografada = bcrypt_context.hash(senha)
        novo_usuario = Usuario(email=email, senha=senha_criptografada)
        session.add(novo_usuario)
        session.commit()
        return {"message": f"Usuário criado com sucesso {novo_usuario.email}", "autenticado": True}


# Rota de autenticação para logout
@auth_router.get("/logout")
async def logout():
    """
    Rota de autenticação para logout.
    """
    return {"message": "Saindo do aplicativo", "autenticado": False}