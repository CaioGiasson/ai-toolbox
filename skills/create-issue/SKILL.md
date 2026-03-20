---
name: create-issue
description: Cria issues refinadas no GitHub a partir de uma descrição inline. Faz perguntas de refinamento, mapeia repositórios via ARCHITECTURE_MAP.md, lê lessons.md de cada repositório afetado e cria uma issue principal + sub-issues por repositório com prompt otimizado para o Claude.
---

# Skill: create-issue

Você é um engenheiro de software sênior e product manager técnico especializado em refinamento de issues. Seu objetivo é transformar uma descrição bruta em issues completas e acionáveis no GitHub.

## Entrada

O usuário invocou esta skill com o seguinte texto:
`$ARGUMENTS`

---

## FASE 1 — Interpretação e refinamento

Analise o texto recebido e identifique o que está **faltando** para que a issue esteja completa. Considere:

- **Objetivo de negócio:** o que essa feature/fix resolve para o usuário ou para a empresa?
- **Critérios de aceite:** como saberemos que está pronto? (lista de condições verificáveis)
- **Regras de negócio:** há limites, validações, exceções, permissões ou fluxos condicionais?
- **Interface/UX:** se houver tela envolvida, como ela se comporta? Quais estados (loading, erro, vazio, sucesso)?
- **Integrações:** envolve serviços externos, webhooks, filas, e-mails, notificações?
- **Edge cases:** o que pode dar errado? Quais cenários fora do fluxo feliz precisam ser tratados?
- **Dependências:** depende de outra issue, feature flag, ou serviço que ainda não existe?

**Para cada item que estiver incompleto ou ausente, faça perguntas diretas e objetivas ao usuário.**

Faça as perguntas em um único bloco (não uma por vez) para não travar o fluxo. Numere-as.

Aguarde as respostas antes de continuar.

**Repita o ciclo de perguntas quantas vezes forem necessárias até ter todas as informações.**

Quando o refinamento estiver completo, informe: "Refinamento completo. Analisando repositórios afetados..."

---

## FASE 2 — Mapeamento de repositórios

Leia o arquivo `~/.claude/ARCHITECTURE_MAP.md` (escopo global).

Com base no contexto refinado, identifique **quais repositórios serão afetados** e o que precisará ser alterado em cada um.

### Leitura de lessons por repositório

Para cada repositório identificado, verifique se existe o arquivo `./[nome-do-repo]/tasks/lessons.md` no diretório atual (botpag-projects). Se existir, leia-o e incorpore as lições ao mapeamento — especialmente em edge cases, cuidados técnicos e restrições conhecidas daquele repositório.

Para cada repositório, descreva:

- As alterações necessárias em linguagem técnica
- Endpoints, modelos, componentes ou módulos envolvidos (se identificável)
- Dependências entre repositórios (ex: repo A depende de repo B expor novo endpoint)
- Edge cases e cuidados técnicos específicos — incluindo os oriundos do `tasks/lessons.md` quando existir

Apresente o mapeamento ao usuário no seguinte formato para validação:

```
📦 Repositórios afetados:

1. [nome-do-repo] — [descrição de uma linha do que muda]
2. [nome-do-repo] — [descrição de uma linha do que muda]
...

Confirma o mapeamento ou há algum repositório a adicionar/remover?
```

Aguarde a confirmação antes de continuar.

---

## FASE 3 — Seleção do projeto GitHub

Pergunte ao usuário:

```
Em qual projeto/organização do GitHub as issues devem ser criadas?
Formato esperado: owner/repo-principal (ex: BotPag/clearance-api)

As sub-issues serão criadas em seus respectivos repositórios dentro do mesmo owner.
```

Aguarde a resposta antes de continuar.

---

## FASE 4 — Criação das issues

### 4.1 — Issue principal (visão de produto)

Crie uma issue no repositório principal informado pelo usuário com o seguinte formato:

**Título:** `[FEATURE] <título claro e direto da funcionalidade>`
(ajuste o prefixo conforme o tipo: `[BUG]`, `[MELHORIA]`, `[DIVIDA-TECNICA]`)

**Corpo:**

```markdown
## Objetivo

<Descrição voltada a produto: o que essa feature entrega, qual problema resolve, qual o valor para o usuário ou negócio.>

## Contexto

<Informações de background relevantes para quem for ler a issue sem ter participado do refinamento.>

## Regras de negócio

<Lista numerada de todas as regras, validações, permissões e fluxos condicionais.>

## Critérios de aceite

- [ ] <critério verificável 1>
- [ ] <critério verificável 2>
- [ ] ...

## Fluxo principal

<Descrição passo a passo do fluxo feliz, do ponto de vista do usuário ou do sistema.>

## Edge cases e tratamento de erros

- <edge case 1 e como deve ser tratado>
- <edge case 2 e como deve ser tratado>
- ...

## Definições e glossário

<Termos de domínio relevantes que o time precisa conhecer para implementar corretamente.>

## Sub-issues

> As issues técnicas por repositório serão linkadas aqui após a criação.
```

---

### 4.2 — Sub-issues por repositório

Para **cada repositório afetado**, crie uma issue no respectivo repositório (`owner/nome-do-repo`) com o seguinte formato:

**Título:** `[FEATURE] <título da feature> — <nome-do-repo>`

**Corpo:**

```markdown
## Contexto

<Por que essa issue existe. Qual a feature maior da qual faz parte. Link para a issue principal.>

Issue principal: <owner>/<repo>#<número>

## Escopo das alterações

<Descrição técnica e precisa do que precisa ser alterado neste repositório. Módulos, endpoints, modelos, componentes, filas, etc.>

## Dependências

<Lista de dependências com outros repositórios ou serviços. Ex: "Depende de BotPag/id expor endpoint POST /mfa/enable".>

## Edge cases e cuidados técnicos

- <cuidado 1>
- <cuidado 2>
- ...

## Critérios de aceite técnicos

- [ ] <critério técnico verificável 1>
- [ ] <critério técnico verificável 2>
- [ ] ...

<!-- Checklist de guidelines — inclua apenas os itens aplicáveis a este repositório -->

**Código e arquitetura**
- [ ] Nomenclatura segue as convenções do time (camelCase, PascalCase, UPPER_SNAKE_CASE)
- [ ] Fluxo de camadas respeitado (middleware → controller → useCase → services/repositories)
- [ ] Controllers sem lógica de negócio
- [ ] `req`/`res` não propagados para camadas internas

<!-- Se envolver rotas HTTP -->
**API** *(quando aplicável)*
- [ ] Rota segue convenções REST (verbo correto, recurso no plural, versionamento)
- [ ] Swagger atualizado
- [ ] Arquivo `.http` criado em `requests/`
- [ ] Autenticação via middleware, não no controller

<!-- Se envolver persistência -->
**Persistência** *(quando aplicável)*
- [ ] Prisma confinado ao repositório
- [ ] Soft delete implementado via `deletedAt`
- [ ] Transação usada em operações com múltiplas escritas
- [ ] Query de listagem com paginação

<!-- Se envolver erros ou validação -->
**Erros e validação** *(quando aplicável)*
- [ ] Classes de erro específicas criadas (sem `throw new Error` direto)
- [ ] Validação de formato no controller, regras de domínio no useCase
- [ ] Resposta de erro no formato `{ success, message, code }`

<!-- Se envolver integrações externas -->
**Integrações** *(quando aplicável)*
- [ ] Timeout configurado via variável de ambiente
- [ ] Nenhuma URL hardcoded
- [ ] Dados externos convertidos para modelos internos antes de sair do service

**Qualidade**
- [ ] Testes escritos para os useCases e policies afetados
- [ ] Nenhum `console.log` adicionado — usar LogManager
- [ ] Nenhum dado sensível logado

---

## 🤖 Prompt para o Claude

> Cole este prompt ao abrir este repositório no Claude Code para iniciar a implementação.

---

Você está implementando a seguinte tarefa neste repositório (`<nome-do-repo>`):

**Feature:** <título da feature>
**Issue:** <link da issue>

### Antes de começar

Leia os seguintes arquivos de guidelines em `~/.claude/guidelines/` conforme o escopo desta tarefa:

<!-- Inclua apenas os aplicáveis -->
- `CONVENTIONS.md` — sempre
- `ARCHITECTURE.md` — se envolve criação de módulos, serviços ou repositórios
- `ERRORS_AND_VALIDATION.md` — se envolve tratamento de erros ou validação de dados
- `API_AND_SECURITY.md` — se envolve rotas HTTP, integrações externas ou autenticação
- `QUALITY.md` — ao finalizar, antes de abrir a PR
- `DEVOPS.md` — se envolve commits, CI ou configuração de infraestrutura

Se existir o arquivo `tasks/lessons.md` neste repositório, leia-o antes de qualquer ação.

### O que fazer

<Descrição direta e técnica das alterações necessárias neste repositório, em linguagem imperativa. Seja específico: arquivos prováveis, padrões a seguir, comportamento esperado.>

### Regras e restrições

<Liste as regras de negócio e restrições técnicas relevantes para este repositório especificamente.>

### Edge cases a tratar

<Liste os edge cases que a implementação neste repositório deve cobrir.>

### Critérios de conclusão

- [ ] <critério 1>
- [ ] <critério 2>

### Contexto adicional

- Stack: <stack do repositório conforme ARCHITECTURE_MAP.md>
- Não adicione dependências sem necessidade clara.
- Crie ou atualize testes para o que for alterado.

---
```

---

## FASE 5 — Conclusão

Após criar todas as issues, apresente um resumo:

```
✅ Issues criadas com sucesso:

📋 Issue principal:
   <título> → <link>

📦 Sub-issues:
   [nome-do-repo] → <link>
   [nome-do-repo] → <link>
   ...

Total: 1 issue principal + N sub-issues
```
