# Arquitetura e Persistência

## 1. Camadas e Fluxo

```
HTTP:    rota → controller → useCase → (services | repositories)
Cron:    cron → job → (useCase | script operacional)
```

- **Nunca pular camadas** — o fluxo acima é obrigatório.
- **Controllers finos** — parse/validação HTTP (schema), middlewares (auth, rate limit, CSRF), chamar o useCase e montar a resposta. Sem lógica de negócio.
- **Nunca propagar `req`/`res` para camadas internas** — camadas de negócio não conhecem o framework HTTP.
- **Um useCase por operação de negócio** — ex: `createPerson.usecase.ts`.
- **UseCases estendem uma classe base (master port)** — `validate` → `execute` → `run`, que orquestra validação, logging e o client do banco.
- **Composition root** — um único módulo instancia e injeta as dependências; rotas obtêm use cases a partir dele.

### Validação em duas etapas
- **Controller** — parsing e validação de formato/estrutura (schema/DTO).
- **UseCase** — validação de regras de domínio. A partir daqui, dados são considerados íntegros.

### Presenters e Mappers
- **Presenter** — monta o envelope da resposta HTTP (`success`, `message`, `data` / `code`).
- **Mapper / DTO** — converte modelos internos em respostas de API (ex: `toPublicUser()`), sem vazar campos internos; e formato externo → domínio interno nas integrações.

### Princípios SOLID
- **S** — Uma classe/módulo tem apenas um motivo para mudar.
- **O** — Aberto para extensão, fechado para modificação. Preferir composição.
- **L** — Subtipos substituíveis por seus tipos base sem quebrar comportamento.
- **I** — Contratos pequenos e específicos.
- **D** — Módulos de alto nível dependem de abstrações, não de implementações.

---

## 2. Persistência e Repositórios

- **Prisma confinado a repositórios** — nenhuma outra camada invoca o Prisma Client diretamente.
- **Um repository por entidade** — toda query em `src/repositories/`.
- **Repositories não chamam outros repositories** — orquestração entre entidades é responsabilidade do UseCase.
- **Repositories convertem para entidades de domínio** — camadas superiores nunca trabalham com modelos do ORM.
- **Transactions em mutações multi-write** — consistência atômica; repositories recebem o client transacional da unidade de trabalho (nunca instanciar/obter outro client no meio da transação). Leituras puras não precisam de transação.
- **Soft delete preferido** — via campo `deletedAt`. Filtros de registros ativos devem considerar campo **ausente ou null** no Mongo. Exceções documentadas.
- **Paginação obrigatória** — toda listagem tem paginação e limites; preferir cursor (`createdAt` + `id`) com `nextCursor`.
- **Schemas Prisma separados por entidade** — em `prisma/models/*.prisma`, com script de merge.

### Nomenclatura de métodos
- Preferir nomes de negócio ao CRUD genérico quando claros.
- Não repetir o nome da entidade nos métodos — o contexto já está dado pela classe.

```ts
// ruim
UserRepository.updateUser(userId, data)

// bom
UserRepository.activate(id)
TransactionRepository.confirm(id)
```
