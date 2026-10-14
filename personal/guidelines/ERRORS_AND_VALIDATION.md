# Erros e Validação

## 1. Tratamento de Erros

### Hierarquia de erros

```
AppError
  ├── ClientError     → dados inválidos do cliente (HTTP 4xx)
  │     ├── ValidationError, NotFoundError, UnauthorizedError
  │     └── ForbiddenError, ConflictError, TooManyRequestsError (+ Retry-After)
  ├── DomainError     → regras de negócio (HTTP 4xx, ex: 409/422)
  │     └── UseCaseError
  └── InfraError      → falhas de infraestrutura (HTTP 5xx)
        ├── RepositoryError
        ├── ServiceError
        └── IntegrationError
```

- **Preferir subclasses tipadas a `throw new Error` genérico** — criar classes específicas por contexto.

```ts
export class UserNotFoundError extends DomainError {
  constructor(userId: string) {
    super(`User ${userId} not found`)
    this.name = 'UserNotFoundError'
  }
}
```

- **Resposta de erro padronizada** — todas as rotas retornam `{ success: false, message, code }`.
- **Handler central de rotas** — converte `AppError` em JSON; erros não mapeados viram 500 com mensagem genérica, sem vazar stack ao cliente.
- **`catch (error: unknown)`** — nunca `catch (error: any)`.
- **Try/catch obrigatório em integrações externas** — toda chamada a serviços externos tem timeout e tratamento de erro (erro tipado); aplicar retry com jitter em 429/5xx transitórios e circuit breaker em dependências críticas.

---

## 2. Validação

- **Validar em duas etapas:**
  - **Controller / rota** — formato e estrutura (Zod: body, query, params).
  - **UseCase** — regras de domínio.
- **Nenhum dado não validado chega à lógica de negócio** — validar body, query params, path params e headers.
- **Centralizar validações reutilizáveis** — regras como CPF, telefone, email em módulos dedicados.
- **Fail fast** — em pipelines de processamento (OCR, scraping), sanitizar e validar antes de aceitar o resultado.
