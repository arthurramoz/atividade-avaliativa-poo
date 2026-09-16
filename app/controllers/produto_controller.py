from app.models.produto import carregar_produtos


class ProdutoController:
    def __init__(self):
        self._produtos = carregar_produtos()

    def listar(self):
        return [self._para_dicionario(p) for p in self._produtos]

    def listar_por_categoria(self, categoria):
        produtos = [p for p in self._produtos if p.pertence_a(categoria)]
        return [self._para_dicionario(p) for p in produtos]

    def buscar(self, id):
        for produto in self._produtos:
            if produto.mostrar_id() == id:
                return self._para_dicionario(produto)
        return None

    def _para_dicionario(self, produto):
        return {
            'id': produto.mostrar_id(),
            'nome': produto.mostrar_nome(),
            'categoria': produto.mostrar_categoria(),
            'preco': produto.mostrar_preco(),
        }
