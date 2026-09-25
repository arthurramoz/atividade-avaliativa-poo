from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.controllers.auth_controller import AuthController

router = APIRouter(prefix='/api/auth', tags=['auth'])
controller = AuthController()


class LoginRequest(BaseModel):
    nome: str
    senha: str


@router.post('/login')
def login(credenciais: LoginRequest):
    usuario_logado = controller.login(credenciais.nome, credenciais.senha)
    if usuario_logado is None:
        raise HTTPException(401, 'nome ou senha inválidos')
    return usuario_logado
