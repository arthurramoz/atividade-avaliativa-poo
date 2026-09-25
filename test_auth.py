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
    arthur, bianca, maria = usuarios

    assert arthur.mostrar_nome() == 'arthur'
    assert arthur.mostrar_perfil() == 'Visitante'
    assert arthur.pode_favoritar() is True
    assert arthur.pode_publicar() is False
    assert arthur.pode_moderar() is False
    assert arthur.conferir_senha('arthur123') is True
    assert arthur.conferir_senha('errada') is False

    assert bianca.mostrar_nome() == 'bianca'
    assert bianca.mostrar_perfil() == 'Contribuidor'
    assert bianca.pode_favoritar() is True
    assert bianca.pode_publicar() is True
    assert bianca.pode_moderar() is False
    assert bianca.conferir_senha('bianca123') is True

    assert maria.mostrar_nome() == 'maria'
    assert maria.mostrar_perfil() == 'Moderador'
    assert maria.pode_favoritar() is True
    assert maria.pode_publicar() is True
    assert maria.pode_moderar() is True
    assert maria.conferir_senha('maria123') is True


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

    res_arthur = controller.login('arthur', 'arthur123')
    assert res_arthur is not None
    assert res_arthur['nome'] == 'arthur'
    assert res_arthur['perfil'] == 'Visitante'
    assert res_arthur['permissoes'] == {'favoritar': True, 'publicar': False, 'moderar': False}
    assert 'senha' not in res_arthur
    assert '_senha' not in res_arthur

    res_bianca = controller.login('bianca', 'bianca123')
    assert res_bianca is not None
    assert res_bianca['nome'] == 'bianca'
    assert res_bianca['perfil'] == 'Contribuidor'
    assert res_bianca['permissoes'] == {'favoritar': True, 'publicar': True, 'moderar': False}

    res_maria = controller.login('maria', 'maria123')
    assert res_maria is not None
    assert res_maria['nome'] == 'maria'
    assert res_maria['perfil'] == 'Moderador'
    assert res_maria['permissoes'] == {'favoritar': True, 'publicar': True, 'moderar': True}

    assert controller.login('arthur', 'senha_incorreta') is None
    assert controller.login('usuario_fantasma', '1234') is None


def test_api_routes():
    try:
        from fastapi.testclient import TestClient
        from main import app

        client = TestClient(app)

        resp = client.post('/api/auth/login', json={'nome': 'arthur', 'senha': 'arthur123'})
        assert resp.status_code == 200, f"Esperado 200, recebido {resp.status_code}"
        dados = resp.json()
        assert dados['perfil'] == 'Visitante'
        assert dados['permissoes']['favoritar'] is True
        assert dados['permissoes']['publicar'] is False

        resp_maria = client.post('/api/auth/login', json={'nome': 'maria', 'senha': 'maria123'})
        assert resp_maria.status_code == 200
        dados_maria = resp_maria.json()
        assert dados_maria['perfil'] == 'Moderador'
        assert dados_maria['permissoes']['moderar'] is True

        resp_erro = client.post('/api/auth/login', json={'nome': 'arthur', 'senha': 'errada'})
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
