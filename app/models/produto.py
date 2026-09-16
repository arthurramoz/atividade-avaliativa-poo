from app.data.produtos_mock import PRODUTOS


class Produto:
    def __init__(self, id, nome, categoria, preco):
        self._id = id
        self._categoria = categoria
        self.alterar_nome(nome)
        self.alterar_preco(preco)

    def mostrar_id(self):
        return self._id

    def mostrar_nome(self):
        return self._nome

    def mostrar_categoria(self):
        return self._categoria

    def mostrar_preco(self):
        return self._preco

    def alterar_nome(self, novo_nome):
        if novo_nome.strip() == '':
            raise ValueError('nome não pode ser vazio')
        self._nome = novo_nome.strip()

    def alterar_preco(self, novo_preco):
        if novo_preco < 0:
            raise ValueError('preço não pode ser negativo')
        self._preco = novo_preco

    def pertence_a(self, categoria):
        return self._categoria.lower() == categoria.lower()

    def __repr__(self):
        return f'Produto({self._nome})'


def carregar_produtos():
    return [Produto(p['id'], p['nome'], p['categoria'], p['preco'])
            for p in PRODUTOS]
