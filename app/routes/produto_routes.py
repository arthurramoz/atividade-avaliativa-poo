from fastapi import APIRouter, HTTPException

from app.controllers.produto_controller import ProdutoController

router = APIRouter(prefix='/api/produtos', tags=['produtos'])
controller = ProdutoController()


@router.get('')
def listar():
    return controller.listar()


@router.get('/categoria/{categoria}')
def listar_por_categoria(categoria: str):
    produtos = controller.listar_por_categoria(categoria)
    if not produtos:
        raise HTTPException(404, 'nenhum produto nessa categoria')
    return produtos


@router.get('/{id}')
def buscar(id: int):
    produto = controller.buscar(id)
    if produto is None:
        raise HTTPException(404, 'produto não encontrado')
    return produto
