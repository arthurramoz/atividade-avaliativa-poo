class Oferta:
    def __init__(self, id, produto, mercado, novo_preco):
        self._id = id
        self._produto = produto  # associação: guarda o objeto Produto
        self._mercado = mercado  # associação: guarda o objeto Mercado
        self.alterar_preco(novo_preco)

    def mostrar_id(self):
        return self._id

    def mostrar_produto(self):
        return self._produto

    def mostrar_mercado(self):
        return self._mercado

    def mostrar_preco(self):
        return self._novo_preco

    def alterar_preco(self, novo_preco):
        if novo_preco <= 0:
            raise ValueError('preço da oferta precisa ser maior que zero')
        if novo_preco >= self._produto.mostrar_preco():
            raise ValueError('oferta precisa ser mais barata que o preço normal')
        self._novo_preco = novo_preco

    def __repr__(self):
        return f'Oferta({self._produto.mostrar_nome()} no {self._mercado.mostrar_nome()})'
