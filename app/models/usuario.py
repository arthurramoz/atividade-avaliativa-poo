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
    perfis = {
        'visitante': Visitante,
        'contribuidor': Contribuidor,
        'moderador': Moderador,
    }

    usuarios = []
    for u in USUARIOS:
        classe = perfis[u['perfil']]
        usuario = classe(u['id'], u['nome'], u['senha'])
        usuarios.append(usuario)

    return usuarios
