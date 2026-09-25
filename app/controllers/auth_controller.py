from app.models.usuario import carregar_usuarios


class AuthController:
    def __init__(self):
        self._usuarios = carregar_usuarios()

    def login(self, nome, senha):
        for user in self._usuarios:
            if user.mostrar_nome() == nome and user.conferir_senha(senha):
                return self._formatar_resposta_login(user)
        return None

    def _formatar_resposta_login(self, user):
        return {
            'id': user.mostrar_id(),
            'nome': user.mostrar_nome(),
            'perfil': user.mostrar_perfil(),
            'permissoes': {
                'favoritar': user.pode_favoritar(),
                'publicar': user.pode_publicar(),
                'moderar': user.pode_moderar(),
            },
        }

    _para_dicionario = _formatar_resposta_login
