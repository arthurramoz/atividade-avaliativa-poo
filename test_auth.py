import inspect
from app.models.usuario import Usuario, Visitante, Contribuidor, Moderador, carregar_usuarios
from app.controllers.auth_controller import AuthController


def test_regras_arquiteturais_e_heranca_slide_34():
    assert issubclass(Visitante, Usuario), "Visitante deve herdar de Usuario"
    assert issubclass(Contribuidor, Usuario), "Contribuidor deve herdar de Usuario"
    assert issubclass(Moderador, Contribuidor), "Moderador deve herdar de Contribuidor"

    assert 'pode_publicar' in Contribuidor.__dict__, "Contribuidor deve sobrescrever pode_publicar"
    assert 'pode_moderar' in Moderador.__dict__, "Moderador deve sobrescrever pode_moderar"
    assert 'pode_publicar' not in Moderador.__dict__, "Moderador NÃO deve sobrescrever pode_publicar (herda de Contribuidor)"

    tipos = [type(u) for u in carregar_usuarios()]
    assert tipos == [Visitante, Contribuidor, Moderador], f"Tipos incorretos: {tipos}"

    assert not hasattr(Usuario, 'mostrar_senha'), "Usuario NUNCA deve expor mostrar_senha"
    assert not hasattr(Visitante, 'mostrar_senha')
    assert not hasattr(Contribuidor, 'mostrar_senha')
    assert not hasattr(Moderador, 'mostrar_senha')


def test_polimorfismo_permissoes():
    usuarios = carregar_usuarios()
    bia, ana, caio = usuarios

    assert bia.mostrar_nome() == 'bia'
    assert bia.mostrar_perfil() == 'Visitante'
    assert bia.pode_favoritar() is True
    assert bia.pode_publicar() is False
    assert bia.pode_moderar() is False
    assert bia.conferir_senha('bia123') is True
    assert bia.conferir_senha('errada') is False

    assert ana.mostrar_nome() == 'ana'
    assert ana.mostrar_perfil() == 'Contribuidor'
    assert ana.pode_favoritar() is True
    assert ana.pode_publicar() is True
    assert ana.pode_moderar() is False
    assert ana.conferir_senha('ana123') is True

    assert caio.mostrar_nome() == 'caio'
    assert caio.mostrar_perfil() == 'Moderador'
    assert caio.pode_favoritar() is True
    assert caio.pode_publicar() is True
    assert caio.pode_moderar() is True
    assert caio.conferir_senha('caio123') is True


def test_regras_arquitetura_mvc_camadas():
    import app.models.usuario as mod_usuario
    import app.controllers.auth_controller as mod_controller

    fonte_model = inspect.getsource(mod_usuario)
    fonte_controller = inspect.getsource(mod_controller)

    assert 'fastapi' not in fonte_model.lower(), "Model não pode importar fastapi!"
    assert 'httpexception' not in fonte_model.lower(), "Model não pode importar HTTPException!"
    assert 'fastapi' not in fonte_controller.lower(), "Controller não pode importar fastapi!"
    assert 'httpexception' not in fonte_controller.lower(), "Controller não pode importar HTTPException!"


def test_auth_controller():
    controller = AuthController()

    res_bia = controller.login('bia', 'bia123')
    assert res_bia is not None
    assert res_bia['nome'] == 'bia'
    assert res_bia['perfil'] == 'Visitante'
    assert res_bia['permissoes'] == {'favoritar': True, 'publicar': False, 'moderar': False}
    assert 'senha' not in res_bia
    assert '_senha' not in res_bia

    res_ana = controller.login('ana', 'ana123')
    assert res_ana is not None
    assert res_ana['nome'] == 'ana'
    assert res_ana['perfil'] == 'Contribuidor'
    assert res_ana['permissoes'] == {'favoritar': True, 'publicar': True, 'moderar': False}

    res_caio = controller.login('caio', 'caio123')
    assert res_caio is not None
    assert res_caio['nome'] == 'caio'
    assert res_caio['perfil'] == 'Moderador'
    assert res_caio['permissoes'] == {'favoritar': True, 'publicar': True, 'moderar': True}

    assert controller.login('bia', 'senha_incorreta') is None
    assert controller.login('usuario_fantasma', '1234') is None


def test_api_routes():
    try:
        from fastapi.testclient import TestClient
        from main import app

        client = TestClient(app)

        resp = client.post('/api/auth/login', json={'nome': 'bia', 'senha': 'bia123'})
        assert resp.status_code == 200, f"Esperado 200, recebido {resp.status_code}"
        dados = resp.json()
        assert dados['perfil'] == 'Visitante'
        assert dados['permissoes']['favoritar'] is True
        assert dados['permissoes']['publicar'] is False

        resp_caio = client.post('/api/auth/login', json={'nome': 'caio', 'senha': 'caio123'})
        assert resp_caio.status_code == 200
        dados_caio = resp_caio.json()
        assert dados_caio['perfil'] == 'Moderador'
        assert dados_caio['permissoes']['moderar'] is True

        resp_erro = client.post('/api/auth/login', json={'nome': 'bia', 'senha': 'errada'})
        assert resp_erro.status_code == 401, f"Esperado 401, recebido {resp_erro.status_code}"
        assert resp_erro.json()['detail'] == 'nome ou senha inválidos'
    except ImportError as e:
        print(f"TestClient não executado: {e}")


if __name__ == '__main__':
    print("Executando bateria de testes...")
    test_regras_arquiteturais_e_heranca_slide_34()
    test_polimorfismo_permissoes()
    test_regras_arquitetura_mvc_camadas()
    test_auth_controller()
    test_api_routes()
    print("TODOS OS TESTES PASSARAM COM 100% DE SUCESSO!")
