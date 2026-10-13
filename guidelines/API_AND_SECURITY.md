# API Design, Integrações e Segurança

## 1. API Design (RESTful)

- **Recursos no plural** — `/users`, `/batches`, `/shippings`.
- **Verbos HTTP corretos** — GET (leitura), POST (criação), PUT (substituição), PATCH (atualização parcial), DELETE (remoção).
- **Códigos HTTP semânticos** — 200, 201, 204, 400, 401, 403, 404, 409, 422, 500.
- **Versionamento** — `/api/v1/users`, `/api/v2/users`.
- **Paginação** — resposta com `next`, `prev`, `total`.
- **Idempotência** — POST idempotente quando possível (idempotency keys). PUT e DELETE são naturalmente idempotentes.
- **Identificação do usuário pela token** — nunca por parâmetro de rota quando a ação é do próprio usuário.

```
// ruim
DELETE /users/:userId/photo/:photoId

// bom
DELETE /photos/:photoId  (com Authorization: Bearer <token>)
```

### Ações extra-verbo
Evitar quando possível. Usar apenas para regras de negócio muito específicas.

```
// ruim: PATCH /transactions/:id
// bom:  PATCH /transactions/:id/checkout

// ruim: POST /users/create
// bom:  POST /users
```

### Healthcheck
Rota `/health` retorna status e lista dependências com suas URLs de healthcheck. A rota principal não testa dependências — cada URL específica testa a sua.

---

## 2. Integrações Externas

- **Isolamento total** — dados de APIs externas não vazam para o sistema. O service converte para modelos internos.
- **Lógica de rede no Service** — formatação/apresentação no Presenter.
- **Timeout em todas as requisições** — via `AbortController` ou timeouts configuráveis. Nunca sem limite.
- **Timeouts em variáveis de ambiente** — nunca hardcoded.
- **Nenhuma URL hardcoded** — toda URL externa vem de variável de ambiente.
- **Nunca diferenciar ambientes por `NODE_ENV`** — a diferença vem dos valores das variáveis de ambiente.

```ts
// ruim
if (process.env.NODE_ENV === 'development') { ... }

// bom
const apiUrl = process.env.API_URL
```

---

## 3. Segurança e Autenticação

- **Autenticação via middleware** — nunca em controllers. O middleware pode enriquecer o request (`userId`, `tenant`).
- **Policies para autorização** — regras encapsuladas em arquivos `*.policy.ts`.
- **Nunca expor credenciais** — `.env` no `.gitignore`. Manter `.env.example` como template.
- **Variáveis de ambiente obrigatórias validadas na inicialização.**
- **CORS com origens explícitas** — nunca `Access-Control-Allow-Origin: *` em produção.
- **Nunca logar dados sensíveis** — PII, tokens, credenciais e secrets fora dos logs.
- **Injection prevention** — nunca interpolar variáveis em queries. Usar Prisma ou query builders.
- **Tokens com expiração** — refresh tokens, invalidação no logout.
- **TLS 1.2+** em trânsito, criptografia em repouso para dados sensíveis.
