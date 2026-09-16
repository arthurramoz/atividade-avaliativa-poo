from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.controllers.auth_controller import AuthController

router = APIRouter(prefix='/api/auth', tags=['auth'])
controller = AuthController()


# Modelo simples para receber os dados do login no body
class LoginRequest(BaseModel):
    nome: str
    senha: str


@router.post('/login')
def login(dados: LoginRequest):
    usuario = controller.login(dados.nome, dados.senha)
    if usuario is None:
        raise HTTPException(401, 'nome ou senha inválidos')
    return usuario
