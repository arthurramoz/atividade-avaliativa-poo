from app.data.usuarios_mock import USUARIOS


# Classe base para todos os usuários
class Usuario:
    def __init__(self, id, nome, senha):
        self._id = id
        self._nome = nome
        self._senha = senha  # protegido: não criamos mostrar_senha por segurança

    def mostrar_id(self):
        return self._id

    def mostrar_nome(self):
        return self._nome

    def mostrar_perfil(self):
        # Retorna o nome da classe do próprio objeto (Visitante, Contribuidor ou Moderador)
        return type(self).__name__

    def conferir_senha(self, senha):
        return self._senha == senha

    # Permissões padrão
    def pode_favoritar(self):
        return True

    def pode_publicar(self):
        return False

    def pode_moderar(self):
        return False

    def __repr__(self):
        return f'{self.mostrar_perfil()}({self._nome})'


# Subclasses com herança e polimorfismo

# Visitante herda tudo da classe base Usuario sem alterar nada
class Visitante(Usuario):
    pass


# Contribuidor herda de Usuario e só muda a permissão de publicar
class Contribuidor(Usuario):
    def pode_publicar(self):
        return True


# Moderador herda de Contribuidor (já ganha pode_publicar) e só adiciona pode_moderar
class Moderador(Contribuidor):
    def pode_moderar(self):
        return True


# Função para carregar os usuários a partir do mock
def carregar_usuarios():
    # Dicionário que mapeia o texto do mock para a respectiva classe
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
