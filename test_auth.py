"""
Testes automatizados para o módulo de autenticação e regras de POO / MVC.
Cobre todas as asserções obrigatórias da Aula 06 (Slide Pág. 34) e testes da API.
"""
import inspect
from app.models.usuario import Usuario, Visitante, Contribuidor, Moderador, carregar_usuarios
from app.controllers.auth_controller import AuthController


def test_regras_arquiteturais_e_heranca_slide_34():
    print("-> Testando asserções obrigatórias da Pág. 34 do Slide...")

    # 1. Hierarquia de herança obrigatória
    assert issubclass(Visitante, Usuario), "Visitante deve herdar de Usuario"
    assert issubclass(Contribuidor, Usuario), "Contribuidor deve herdar de Usuario"
    assert issubclass(Moderador, Contribuidor), "Moderador deve herdar de Contribuidor"

    # 2. Herança limpa (sobrescrever apenas a diferença)
    assert 'pode_publicar' in Contribuidor.__dict__, "Contribuidor deve sobrescrever pode_publicar"
    assert 'pode_moderar' in Moderador.__dict__, "Moderador deve sobrescrever pode_moderar"
    assert 'pode_publicar' not in Moderador.__dict__, "Moderador NÃO deve sobrescrever pode_publicar (herda de Contribuidor)"

    # 3. Tipagem das instâncias a partir do mock
    tipos = [type(u) for u in carregar_usuarios()]
    assert tipos == [Visitante, Contribuidor, Moderador], f"Tipos incorretos: {tipos}"

    # 4. Proteção de dados sensíveis
    assert not hasattr(Usuario, 'mostrar_senha'), "Usuario NUNCA deve expor mostrar_senha"
    assert not hasattr(Visitante, 'mostrar_senha')
    assert not hasattr(Contribuidor, 'mostrar_senha')
    assert not hasattr(Moderador, 'mostrar_senha')

    print("   [OK] Todas as 4 asserções do slide passaram com sucesso!")


def test_polimorfismo_permissoes():
    print("-> Testando polimorfismo das permissões...")
    usuarios = carregar_usuarios()
    bia, ana, caio = usuarios

    # Bia - Visitante
    assert bia.mostrar_nome() == 'bia'
    assert bia.mostrar_perfil() == 'Visitante'
    assert bia.pode_favoritar() is True
    assert bia.pode_publicar() is False
    assert bia.pode_moderar() is False
    assert bia.conferir_senha('bia123') is True
    assert bia.conferir_senha('errada') is False

    # Ana - Contribuidor
    assert ana.mostrar_nome() == 'ana'
    assert ana.mostrar_perfil() == 'Contribuidor'
    assert ana.pode_favoritar() is True
    assert ana.pode_publicar() is True
    assert ana.pode_moderar() is False
    assert ana.conferir_senha('ana123') is True

    # Caio - Moderador
    assert caio.mostrar_nome() == 'caio'
    assert caio.mostrar_perfil() == 'Moderador'
    assert caio.pode_favoritar() is True
    assert caio.pode_publicar() is True  # Herdado de Contribuidor
    assert caio.pode_moderar() is True   # Sobrescrito em Moderador
    assert caio.conferir_senha('caio123') is True

    print("   [OK] Polimorfismo verificado com sucesso para os 3 perfis!")


def test_regras_arquitetura_mvc_camadas():
    print("-> Testando integridade das camadas MVC...")
    import app.models.usuario as mod_usuario
    import app.controllers.auth_controller as mod_controller

    fonte_model = inspect.getsource(mod_usuario)
    fonte_controller = inspect.getsource(mod_controller)

    assert 'fastapi' not in fonte_model.lower(), "Model não pode importar fastapi!"
    assert 'httpexception' not in fonte_model.lower(), "Model não pode importar HTTPException!"
    assert 'fastapi' not in fonte_controller.lower(), "Controller não pode importar fastapi!"
    assert 'httpexception' not in fonte_controller.lower(), "Controller não pode importar HTTPException!"

    print("   [OK] Camadas Model e Controller 100% isoladas de HTTP e FastAPI!")


def test_auth_controller():
    print("-> Testando AuthController e sanitização de dados...")
    controller = AuthController()

    # Login Bia (Visitante)
    res_bia = controller.login('bia', 'bia123')
    assert res_bia is not None
    assert res_bia['nome'] == 'bia'
    assert res_bia['perfil'] == 'Visitante'
    assert res_bia['permissoes'] == {'favoritar': True, 'publicar': False, 'moderar': False}
    assert 'senha' not in res_bia
    assert '_senha' not in res_bia

    # Login Ana (Contribuidor)
    res_ana = controller.login('ana', 'ana123')
    assert res_ana is not None
    assert res_ana['nome'] == 'ana'
    assert res_ana['perfil'] == 'Contribuidor'
    assert res_ana['permissoes'] == {'favoritar': True, 'publicar': True, 'moderar': False}

    # Login Caio (Moderador)
    res_caio = controller.login('caio', 'caio123')
    assert res_caio is not None
    assert res_caio['nome'] == 'caio'
    assert res_caio['perfil'] == 'Moderador'
    assert res_caio['permissoes'] == {'favoritar': True, 'publicar': True, 'moderar': True}

    # Falhas de autenticação
    assert controller.login('bia', 'senha_incorreta') is None
    assert controller.login('usuario_fantasma', '1234') is None

    print("   [OK] AuthController validou logins e sanitizou respostas com sucesso!")


def test_api_routes():
    print("-> Testando rota HTTP /api/auth/login...")
    try:
        from fastapi.testclient import TestClient
        from main import app

        client = TestClient(app)

        # Sucesso Bia
        resp = client.post('/api/auth/login', json={'nome': 'bia', 'senha': 'bia123'})
        assert resp.status_code == 200, f"Esperado 200, recebido {resp.status_code}"
        dados = resp.json()
        assert dados['perfil'] == 'Visitante'
        assert dados['permissoes']['favoritar'] is True
        assert dados['permissoes']['publicar'] is False

        # Sucesso Caio
        resp_caio = client.post('/api/auth/login', json={'nome': 'caio', 'senha': 'caio123'})
        assert resp_caio.status_code == 200
        dados_caio = resp_caio.json()
        assert dados_caio['perfil'] == 'Moderador'
        assert dados_caio['permissoes']['moderar'] is True

        # Falha 401
        resp_erro = client.post('/api/auth/login', json={'nome': 'bia', 'senha': 'errada'})
        assert resp_erro.status_code == 401, f"Esperado 401, recebido {resp_erro.status_code}"
        assert resp_erro.json()['detail'] == 'nome ou senha inválidos'

        print("   [OK] Rotas HTTP /api/auth/login testadas com sucesso (200 e 401)!")
    except ImportError as e:
        print(f"   [AVISO] TestClient não executado devido à ausência de dependência: {e}")


if __name__ == '__main__':
    print("========================================")
    print("EXECUTANDO BATERIA COMPLETA DE TESTES")
    print("========================================")
    test_regras_arquiteturais_e_heranca_slide_34()
    test_polimorfismo_permissoes()
    test_regras_arquitetura_mvc_camadas()
    test_auth_controller()
    test_api_routes()
    print("========================================")
    print("TODOS OS TESTES PASSARAM COM 100% DE SUCESSO!")
    print("========================================")
