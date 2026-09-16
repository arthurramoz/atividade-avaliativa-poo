from app.models.usuario import carregar_usuarios


class AuthController:
    def __init__(self):
        self._usuarios = carregar_usuarios()

    def login(self, nome, senha):
        # Procura o usuário pelo nome e confere a senha
        for usuario in self._usuarios:
            if usuario.mostrar_nome() == nome and usuario.conferir_senha(senha):
                return self._para_dicionario(usuario)
        return None

    def _para_dicionario(self, usuario):
        # Monta a resposta sem nenhum if de perfil, aproveitando o polimorfismo
        return {
            'id': usuario.mostrar_id(),
            'nome': usuario.mostrar_nome(),
            'perfil': usuario.mostrar_perfil(),
            'permissoes': {
                'favoritar': usuario.pode_favoritar(),
                'publicar': usuario.pode_publicar(),
                'moderar': usuario.pode_moderar(),
            },
        }
