# 🎤 PARTE B: Roteiro e Apresentação de 10 Minutos
## Aplicação de Encapsulamento e Herança no KiOferta

> **Guia para a equipe (3 a 4 integrantes)**  
> **Tempo total de apresentação:** 10 minutos (divididos em 4 blocos de ~2m30s cada)

---

## 📌 Visão Geral da Divisão da Apresentação

| Bloco | Tempo | Tema | Responsável Sugerido |
|---|---|---|---|
| **1. Introdução e Arquitetura MVC** | 0:00 - 2:30 | Apresentação da equipe, contexto do KiOferta e arquitetura em camadas (MVC) | Integrante 1 |
| **2. Encapsulamento no KiOferta** | 2:30 - 5:00 | Atributos protegidos, validações de domínio e segurança da senha | Integrante 2 |
| **3. Herança e Polimorfismo no KiOferta** | 5:00 - 7:30 | Hierarquia `Usuario` $\rightarrow$ `Contribuidor` $\rightarrow$ `Moderador` e permissões sem `if` | Integrante 3 |
| **4. Demonstração Prática e Conclusão** | 7:30 - 10:00 | Swagger `/docs`, testes automatizados de asserção e encerramento | Integrante 4 (ou compartilhado) |

---

## 🛡️ Bloco 1: Introdução e Arquitetura MVC (0:00 - 2:30)

### 🎯 O que falar:
- **Cumprimento e Objetivo:**
  > *"Boa noite/dia a todos e professor! Nossa equipe vai apresentar a aplicação dos pilares de Programação Orientada a Objetos — especificamente Encapsulamento, Herança e Polimorfismo — no backend da KiOferta, estruturado sobre a arquitetura em camadas MVC com FastAPI."*
- **A mudança de paradigma:**
  > *"Antes, aplicações simples colocavam regras de negócio misturadas dentro de rotas em um único arquivo `main.py`. Isso gerava conflitos no Git e impedia testes isolados. No KiOferta, nós separamos estritamente as responsabilidades em:*
  > - *`data/`: dados brutos (mocks);*
  > - *`models/`: domínio puro, validações e regras de negócio (sem dependência de HTTP);*
  > - *`controllers/`: casos de uso e orquestração;*
  > - *`routes/`: endpoints FastAPI e tratamento de códigos HTTP (como 200 e 401);*
  > - *`main.py`: apenas conecta as rotas e inicia o servidor."*
- **Regra de ouro das dependências:**
  > *"A dependência é sempre unidirecional: `main` $\rightarrow$ `routes` $\rightarrow$ `controllers` $\rightarrow$ `models` $\rightarrow$ `data`. Nenhum arquivo de model ou controller sabe o que é FastAPI ou HTTP."*

---

## 🔒 Bloco 2: Onde foi aplicado o ENCAPSULAMENTO? (2:30 - 5:00)

### 🎯 O que falar:
> *"O encapsulamento protege o estado interno dos objetos e centraliza as regras de negócio para que ninguém altere dados de forma inválida pelo lado de fora."*

### 1. Na Model `Produto` (`app/models/produto.py`):
- **Atributos protegidos por convenção:** `_id`, `_nome`, `_categoria`, `_preco`.
- **Nenhum atributo é acessado diretamente:** Usamos métodos `mostrar_id()`, `mostrar_nome()`, `mostrar_preco()`.
- **Validação no Setter:** Os métodos `alterar_nome(novo_nome)` e `alterar_preco(novo_preco)` validam as regras de domínio antes de modificar o estado:
  - Nome não pode ser vazio (`strip() == ''`);
  - Preço não pode ser negativo (`novo_preco < 0`).
- **Garantia de integridade já no construtor:** O `__init__` do `Produto` chama `self.alterar_nome(nome)` e `self.alterar_preco(preco)`. O objeto já nasce garantidamente válido.
- **Ocultamento de lógica de negócio:** O método `pertence_a(categoria)` compara em minúsculas (`.lower()`). Quem chama não precisa saber como a categoria é tratada por dentro.

### 2. Na Model `Usuario` (`app/models/usuario.py`) — O Encapsulamento da Senha:
- **Segurança da credencial:** O atributo `_senha` é protegido.
- **Ausência intencional de `mostrar_senha()`:** Não existe esse método! A senha nunca pode ser vazada ou exposta.
- **Delegação de responsabilidade:** Para validar o login, usamos `usuario.conferir_senha(senha)`. É a própria classe que sabe comparar sua senha com a recebida, retornando um booleano (`True` ou `False`).

### 3. No Controller (`AuthController`):
- **Sanitização de saída no método privado `_para_dicionario(usuario)`:** A rota nunca devolve o objeto bruto. O controller empacota apenas os dados autorizados (id, nome, perfil e permissões), garantindo que atributos internos com underline ou senhas jamais saiam no JSON da API.

---

## 🧬 Bloco 3: Onde foi aplicada a HERANÇA e o POLIMORFISMO? (5:00 - 7:30)

### 🎯 O que falar:
> *"A herança e o polimorfismo foram a chave para criarmos a tela de login com diferentes permissões sem encher o controller de estruturas condicionais (`if/elif/else`)."*

### 1. Hierarquia de Classes:
```
           Usuario (Base)
           ├── pode_favoritar() -> True
           ├── pode_publicar() -> False
           ├── pode_moderar() -> False
           │
           ├── Visitante (Herda tudo sem alterar)
           │
           └── Contribuidor (Herda de Usuario)
               ├── sobrescreve: pode_publicar() -> True
               │
               └── Moderador (Herda de Contribuidor)
                   └── sobrescreve: pode_moderar() -> True
                   (Herda pode_publicar() automaticamente!)
```

### 2. Herança Limpa e Princípio DRY (Don't Repeat Yourself):
- `Visitante` não reescreve nada; recebe as permissões padrão da classe base `Usuario`.
- `Contribuidor` altera apenas `pode_publicar() -> True`.
- `Moderador` herda de **`Contribuidor`** (e não direto de `Usuario`). Com isso, ele **já herda `pode_publicar() = True`** de graça! Ele só precisa sobrescrever `pode_moderar() -> True`.
- Isso foi validado com rigor pelos testes:
  ```python
  assert 'pode_moderar' in Moderador.__dict__
  assert 'pode_publicar' not in Moderador.__dict__  # Herança limpa!
  ```

### 3. Polimorfismo sem `if` no Controller:
- **Identificação do perfil:** O método `mostrar_perfil()` usa reflexão (`type(self).__name__`), retornando `'Visitante'`, `'Contribuidor'` ou `'Moderador'` dinamicamente.
- **Decisão de permissões:** No `AuthController`, quando montamos a resposta:
  ```python
  'permissoes': {
      'favoritar': usuario.pode_favoritar(),
      'publicar': usuario.pode_publicar(),
      'moderar': usuario.pode_moderar(),
  }
  ```
  O controller **não pergunta** `"se for Moderador faça isso"`. Ele simplesmente envia a mensagem para o objeto, e cada subclasse responde de acordo com seu próprio comportamento polimórfico!

### 4. Fábrica de Objetos (`carregar_usuarios`):
- Em Python, classes são objetos de primeira classe (*first-class citizens*). Mapeamos o texto do mock diretamente para a classe correspondente usando um dicionário:
  ```python
  PERFIS = {'visitante': Visitante, 'contribuidor': Contribuidor, 'moderador': Moderador}
  ```
  O `if` existiu apenas na fábrica, no momento da instanciação. Depois disso, o restante do sistema opera puramente por polimorfismo.

---

## 💻 Bloco 4: Demonstração Prática e Conclusão (7:30 - 10:00)

### 🎯 O que mostrar na tela:

1. **Apresentar o resultado dos testes automatizados:**
   - Rodar no terminal:
     ```powershell
     python test_auth.py
     ```
   - Mostrar que as 4 asserções formais do slide (Pág. 34) passaram com 100%:
     - `issubclass(Visitante, Usuario)`
     - `issubclass(Contribuidor, Usuario)`
     - `issubclass(Moderador, Contribuidor)`
     - `pode_publicar in Contribuidor` e `not in Moderador`
     - `not hasattr(Usuario, 'mostrar_senha')`

2. **Demonstrar no Swagger UI (`http://127.0.0.1:8000/docs`):**
   - Abrir o Swagger e mostrar o endpoint `POST /api/auth/login`.
   - **Teste 1 (Bia):** Enviar `{"nome": "bia", "senha": "bia123"}` $\rightarrow$ Retorna Perfil: `Visitante`, `favoritar: true`, `publicar: false`, `moderar: false`.
   - **Teste 2 (Ana):** Enviar `{"nome": "ana", "senha": "ana123"}` $\rightarrow$ Retorna Perfil: `Contribuidor`, `favoritar: true`, `publicar: true`, `moderar: false`.
   - **Teste 3 (Caio):** Enviar `{"nome": "caio", "senha": "caio123"}` $\rightarrow$ Retorna Perfil: `Moderador`, `favoritar: true`, `publicar: true`, `moderar: true`.
   - **Teste 4 (Erro 401):** Enviar senha incorreta $\rightarrow$ Retorna HTTP 401 `{"detail": "nome ou senha inválidos"}`.

3. **Conclusão:**
   > *"Como pudemos ver, o encapsulamento garantiu que senhas nunca fossem expostas e que produtos nunca tivessem estados inconsistentes. E a herança com polimorfismo permitiu que novas permissões e novos tipos de usuários possam ser adicionados no futuro sem alterar uma única linha do nosso controller ou das nossas rotas. Muito obrigado e estamos abertos a perguntas!"*

---

## 📋 Resumo Rápido para Colar nos Slides / Anotações

- **Encapsulamento:**
  1. Atributos com `_` (`_id`, `_nome`, `_senha`).
  2. Métodos `alterar_*` com validação de regras de negócio.
  3. Ausência de `mostrar_senha()`.
  4. Método `_para_dicionario()` no Controller como filtro de segurança para JSON.
- **Herança:**
  1. `Usuario` $\rightarrow$ `Contribuidor` $\rightarrow$ `Moderador`.
  2. Herança em cadeia que evita duplicação de métodos.
- **Polimorfismo:**
  1. `mostrar_perfil()` via reflexão (`type(self).__name__`).
  2. Chamadas de métodos de permissão (`pode_publicar()`, etc.) sem condicionais no Controller.
