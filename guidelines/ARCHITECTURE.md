# Arquitetura e Persistência

## 1. Camadas e Fluxo

```
HTTP:    middleware → controller → useCase → (services | repositories)
Cron:    cron → useCase → (services | repositories)
Worker:  worker → useCase → (services | repositories)
```

- **Nunca pular camadas** — o fluxo acima é obrigatório.
- **Controllers finos** — extrair/normalizar inputs, chamar o useCase, montar a resposta. Sem lógica de negócio.
- **Nunca propagar `req`/`res` para camadas internas** — camadas de negócio não conhecem o framework HTTP.
- **Um useCase por operação de negócio** — ex: `createPerson.usecase.ts`.
- **Padrão Factory para UseCases** — recebe dependências e retorna `execute`.

### Validação em duas etapas
- **Controller** — parsing e validação de formato/estrutura (schema/DTO).
- **UseCase** — validação de regras de domínio. A partir daqui, dados são considerados íntegros.

### Presenters e Mappers
- **Presenter** — domínio → resposta externa (HTTP).
- **Mapper** — formato externo → domínio interno.

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
- **Usar transactions** — garantir consistência atômica em operações com múltiplas escritas.
- **Soft delete como padrão** — via campo `deletedAt`. Exceções documentadas.
- **Paginação obrigatória** — toda query de listagem tem paginação e limites.
- **Schemas Prisma separados por entidade** — em `prisma/models/*.prisma`, com script de merge.

### Nomenclatura de métodos
- Nomear pela ação de negócio, não pelo CRUD genérico.
- Não repetir o nome da entidade nos métodos — o contexto já está dado pela classe.

```ts
// ruim
UserRepository.updateUser(userId, data)

// bom
UserRepository.activate(id)
TransactionRepository.confirm(id)
```
