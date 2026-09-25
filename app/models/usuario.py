from app.data.usuarios_mock import USUARIOS


class Usuario:
    def __init__(self, id, nome, senha):
        self._id = id
        self._nome = nome
        self._senha = senha

    def mostrar_id(self):
        return self._id

    def mostrar_nome(self):
        return self._nome

    def mostrar_perfil(self):
        return type(self).__name__

    def conferir_senha(self, senha):
        return self._senha == senha

    def pode_favoritar(self):
        return True

    def pode_publicar(self):
        return False

    def pode_moderar(self):
        return False

    def __repr__(self):
        return f'{self.mostrar_perfil()}({self._nome})'


class Visitante(Usuario):
    pass


class Contribuidor(Usuario):
    def pode_publicar(self):
        return True


class Moderador(Contribuidor):
    def pode_moderar(self):
        return True


def carregar_usuarios():
    catalogo_perfis = {
        'visitante': Visitante,
        'contribuidor': Contribuidor,
        'moderador': Moderador,
    }

    lista_usuarios = []
    for dados in USUARIOS:
        classe_usuario = catalogo_perfis[dados['perfil']]
        novo_usuario = classe_usuario(dados['id'], dados['nome'], dados['senha'])
        lista_usuarios.append(novo_usuario)

    return lista_usuarios
