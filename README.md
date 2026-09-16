# KiOferta API - Atividade Avaliativa POO (Aula 06)

Projeto desenvolvido para a disciplina de Programação Orientada a Objetos (POO), aplicando arquitetura em camadas **MVC (Model-View-Controller)** com **FastAPI**, com foco em **Herança**, **Polimorfismo** e **Encapsulamento** no módulo de autenticação e login.

---

## 🏗️ Arquitetura do Projeto

A aplicação segue a direção única de dependência (top-down):

$$\text{main.py} \longrightarrow \text{routes (View)} \longrightarrow \text{controllers} \longrightarrow \text{models} \longrightarrow \text{data (Mock)}$$

- **`app/models/`**: Domínio e regras de negócio (`Usuario`, `Visitante`, `Contribuidor`, `Moderador`, `Produto`).
- **`app/controllers/`**: Orquestração dos casos de uso (`AuthController`, `ProdutoController`).
- **`app/routes/`**: Endpoints da API HTTP (`auth_routes.py`, `produto_routes.py`).
- **`app/data/`**: Dados mockados em memória (`usuarios_mock.py`, `produtos_mock.py`).

---

## 🚀 Como Rodar o Projeto (Passo a Passo)

### 1. Clonar o repositório
```bash
git clone https://github.com/arthurramoz/atividade-avaliativa-poo.git
cd atividade-avaliativa-poo
```

### 2. Criar e ativar o ambiente virtual (Opcional, mas recomendado)
- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
- **Linux / MacOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Instalar as dependências
```bash
python -m pip install -r requirements.txt
```

### 4. Rodar os testes automatizados
Para validar a herança, permissões polimórficas e integridade arquitetural:
```bash
python test_auth.py
```
*(Todos os testes devem passar com 100% de sucesso).*

### 5. Iniciar o servidor da API
Utilize o comando com `python -m` para garantir a execução no Windows:
```bash
python -m uvicorn main:app --reload
```

O servidor iniciará em: **http://127.0.0.1:8000**

---

## 🧪 Como Testar no Swagger (Documentação Interativa)

1. Abra no navegador: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**
2. Localize a seção **`auth`** e clique em **`POST /api/auth/login`**.
3. Clique em **Try it out** e teste os usuários nesta ordem:

#### Teste 1: Bia (Visitante)
- **Body:**
  ```json
  {
    "nome": "bia",
    "senha": "bia123"
  }
  ```
- **Retorno esperado (HTTP 200):**
  ```json
  {
    "id": 1,
    "nome": "bia",
    "perfil": "Visitante",
    "permissoes": {
      "favoritar": true,
      "publicar": false,
      "moderar": false
    }
  }
  ```

#### Teste 2: Ana (Contribuidor)
- **Body:**
  ```json
  {
    "nome": "ana",
    "senha": "ana123"
  }
  ```
- **Retorno esperado (HTTP 200):**
  ```json
  {
    "id": 2,
    "nome": "ana",
    "perfil": "Contribuidor",
    "permissoes": {
      "favoritar": true,
      "publicar": true,
      "moderar": false
    }
  }
  ```

#### Teste 3: Caio (Moderador)
- **Body:**
  ```json
  {
    "nome": "caio",
    "senha": "caio123"
  }
  ```
- **Retorno esperado (HTTP 200):**
  ```json
  {
    "id": 3,
    "nome": "caio",
    "perfil": "Moderador",
    "permissoes": {
      "favoritar": true,
      "publicar": true,
      "moderar": true
    }
  }
  ```

#### Teste 4: Senha Inválida
- **Body:**
  ```json
  {
    "nome": "bia",
    "senha": "senha_errada"
  }
  ```
- **Retorno esperado (HTTP 401 Unauthorized):**
  ```json
  {
    "detail": "nome ou senha inválidos"
  }
  ```

---

## 🎤 Apresentação da Equipe (Parte B)

O roteiro completo estruturado para a apresentação de 10 minutos da equipe sobre Encapsulamento e Herança no KiOferta encontra-se no arquivo:
👉 **[PARTE_B_APRESENTACAO.md](PARTE_B_APRESENTACAO.md)**