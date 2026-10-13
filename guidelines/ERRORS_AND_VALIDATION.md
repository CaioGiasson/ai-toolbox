# Erros e Validação

## 1. Tratamento de Erros

### Hierarquia de erros

```
AppError
  ├── ClientError     → dados inválidos do cliente (HTTP 4xx)
  ├── DomainError     → regras de negócio (HTTP 5xx)
  │     └── UseCaseError
  └── InfraError      → falhas de infraestrutura (HTTP 5xx)
        ├── RepositoryError
        ├── ServiceError
        └── IntegrationError
```

- **Nunca usar `throw new Error` diretamente** — criar classes específicas por contexto.

```ts
export class UserNotFoundError extends DomainError {
  constructor(userId: string) {
    super(`User ${userId} not found`)
    this.name = 'UserNotFoundError'
  }
}
```

- **Resposta de erro padronizada** — todas as rotas retornam `{ success, message, code }`.
- **Global error handler** — manter handler de fallback no `app.ts` para erros não capturados.
- **`catch (error: unknown)`** — nunca `catch (error: any)`.
- **Try/catch obrigatório em integrações externas** — toda chamada a serviços externos tem tratamento de erro.

---

## 2. Validação

- **Validar em duas etapas:**
  - **Controller** — formato e estrutura (schema/DTO).
  - **UseCase** — regras de domínio.
- **Nenhum dado não validado chega à lógica de negócio** — validar body, query params, path params e headers.
- **Centralizar validações reutilizáveis** — regras como CPF, telefone, email em módulos dedicados.
- **Fail fast** — em pipelines de processamento (OCR, scraping), sanitizar e validar antes de aceitar o resultado.
