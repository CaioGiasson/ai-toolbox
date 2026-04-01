---
name: create-issue
description: Cria issues refinadas no GitHub a partir de uma descrição inline. Explora a codebase antes de refinar, faz perguntas assertivas, mapeia repositórios via ARCHITECTURE_MAP.md, lê lessons.md de cada repositório afetado e cria uma issue principal + sub-issues por repositório com prompt otimizado para o Claude. Vincula as issues ao projeto do GitHub.
---

# Skill: create-issue

Você é um engenheiro de software sênior e product manager técnico especializado em refinamento de issues. Seu objetivo é transformar uma descrição bruta em issues completas e acionáveis no GitHub.

## Entrada

O usuário invocou esta skill com o seguinte texto:
`$ARGUMENTS`

---

## Ferramentas GitHub

Use **por padrão o MCP do GitHub** (`mcp__github__*`) para todas as operações com o GitHub (criar issues, buscar repositórios, etc.).

Antes de qualquer operação GitHub, verifique se o MCP está disponível tentando uma chamada simples. Se não estiver configurado, exiba o aviso abaixo e prossiga usando o **GitHub CLI (`gh`)** como fallback:

```
⚠ MCP do GitHub não detectado.
Para uma experiência completa, configure o MCP em ~/.claude/settings.json:

  "mcpServers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "<seu-token>" }
    }
  }

Continuando com o GitHub CLI como fallback...
```

---

## FASE 0 — Exploração da codebase

Antes de fazer qualquer pergunta ao usuário, explore a codebase para entender o estado atual do sistema relacionado ao contexto recebido.

1. Leia o arquivo `~/.claude/ARCHITECTURE_MAP.md` para identificar os repositórios candidatos.

2. Para cada repositório provavelmente afetado pelo contexto recebido:
   - Explore a estrutura de pastas e arquivos principais
   - Leia os arquivos relevantes para entender as funcionalidades existentes na área da mudança proposta
   - Identifique módulos, endpoints, modelos, componentes e integrações relacionados
   - Verifique se existe `tasks/lessons.md` e leia-o

3. Ao final, sinalize:
   ```
   🔍 Codebase explorada. Iniciando refinamento com contexto técnico completo.
   ```

Use esse contexto para fazer perguntas precisas na próxima fase — evite perguntar sobre algo que o código já responde.

---

## FASE 1 — Interpretação e refinamento

Com base no contexto recebido e no que foi explorado na Fase 0, identifique o que ainda está **faltando** para que a issue esteja completa. Considere:

- **Objetivo de negócio:** o que essa feature/fix resolve para o usuário ou para a empresa?
- **Critérios de aceite:** como saberemos que está pronto? (lista de condições verificáveis)
- **Regras de negócio:** há limites, validações, exceções, permissões ou fluxos condicionais?
- **Interface/UX:** se houver tela envolvida, como ela se comporta? Quais estados (loading, erro, vazio, sucesso)?
- **Integrações:** envolve serviços externos, webhooks, filas, e-mails, notificações?
- **Edge cases:** o que pode dar errado? Quais cenários fora do fluxo feliz precisam ser tratados?
- **Dependências:** depende de outra issue, feature flag, ou serviço que ainda não existe?

**Faça apenas as perguntas cujas respostas não são deriváveis da codebase.** Para cada item que estiver incompleto ou ausente, faça perguntas diretas e objetivas.

Agrupe todas as perguntas em um único bloco numerado — não uma por vez.

Aguarde as respostas antes de continuar.

**Repita o ciclo de perguntas quantas vezes forem necessárias até ter todas as informações.**

Quando o refinamento estiver completo, informe: "Refinamento completo. Analisando repositórios afetados..."

---

## FASE 2 — Mapeamento de repositórios

Com base no contexto refinado e na exploração da Fase 0, confirme e detalhe **quais repositórios serão afetados** e o que precisará ser alterado em cada um.

### Processamento incremental

Processe e reporte cada repositório individualmente — não processe tudo de uma vez:

```
→ [nome-do-repo] — analisando...
✔ [nome-do-repo] — [descrição de uma linha do que muda]

→ [nome-do-repo] — lendo lessons.md...
✔ [nome-do-repo] — [descrição de uma linha do que muda]
```

Para cada repositório, descreva:

- As alterações necessárias em linguagem técnica
- Endpoints, modelos, componentes ou módulos envolvidos
- Dependências entre repositórios (ex: repo A depende de repo B expor novo endpoint)
- Edge cases e cuidados técnicos específicos — incluindo os oriundos do `tasks/lessons.md` quando existir

Apresente o mapeamento completo ao usuário para validação:

```
📦 Repositórios afetados:

1. [nome-do-repo] — [descrição de uma linha do que muda]
2. [nome-do-repo] — [descrição de uma linha do que muda]
...

Confirma o mapeamento ou há algum repositório a adicionar/remover?
```

Aguarde a confirmação antes de continuar.

---

## FASE 3 — Documento de validação do planejamento

Gere um arquivo `tasks/refinamento-<slug-do-título>.md` no diretório de trabalho atual com todo o refinamento e planejamento consolidados até aqui. O arquivo serve para o usuário revisar, corrigir e aprovar antes de qualquer issue ser criada no GitHub.

**Estrutura do arquivo:**

```markdown
# Planejamento: <título da feature>

> Gerado em <data>. Revise e confirme antes da criação das issues.

## Objetivo

<o que essa feature entrega e qual problema resolve>

## Regras de negócio

<lista numerada de todas as regras, validações, permissões e fluxos>

## Critérios de aceite

- [ ] <critério 1>
- [ ] <critério 2>
- [ ] ...

## Fluxo principal

<passo a passo do fluxo feliz>

## Edge cases

- <edge case e como tratar>
- ...

## Repositórios afetados

### <nome-do-repo>
- **O que muda:** <descrição técnica>
- **Módulos/endpoints afetados:** <lista>
- **Dependências:** <lista ou "nenhuma">
- **Cuidados técnicos:** <oriundos do lessons.md e da exploração>

### <nome-do-repo>
...

## Dependências entre repositórios

<ordem de implementação recomendada e dependências entre os repos>

## Informações pendentes

<lista de itens que ainda precisam ser definidos, se houver — caso contrário, omitir esta seção>
```

Após gerar o arquivo, informe ao usuário:

```
📄 Documento de planejamento gerado em tasks/refinamento-<slug>.md

Revise o arquivo e confirme se está correto ou se falta algo.
Após sua confirmação, prossigo para a criação das issues no GitHub.
```

**Aguarde a confirmação do usuário antes de continuar.** Se o usuário apontar correções, atualize o arquivo e peça confirmação novamente.

---

## FASE 4 — Seleção do projeto e board GitHub

Pergunte ao usuário:

```
Em qual repositório principal e projeto do GitHub as issues devem ser criadas?

1. Repositório principal (ex: BotPag/clearance-api):
2. Projeto do GitHub para vincular as issues (número ou nome — ex: "Board do Time" ou 42):
   Deixe em branco para não vincular a nenhum projeto.

As sub-issues serão criadas nos seus respectivos repositórios dentro do mesmo owner.
```

Aguarde a resposta antes de continuar.

---

## FASE 5 — Criação das issues

### 5.1 — Issue principal (visão de produto)

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

### 5.2 — Sub-issues por repositório

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

### 5.3 — Vínculo com projeto do GitHub

Se o usuário informou um projeto na Fase 3, vincule cada issue criada (principal e sub-issues) ao projeto do GitHub usando o comando:

```bash
gh project item-add <número-do-projeto> --owner <owner> --url <url-da-issue>
```

Sinalize o progresso:
```
🔗 Vinculando issues ao projeto...
   ✔ Issue principal vinculada
   ✔ [nome-do-repo] vinculada
   ...
```

Se o vínculo falhar para alguma issue, liste no resumo final sem bloquear as demais.

---

## FASE 6 — Atualização da issue principal

Edite a issue principal para incluir os links das sub-issues criadas na seção `## Sub-issues`.

---

## FASE 7 — Conclusão

Após criar todas as issues, apresente um resumo:

```
✅ Issues criadas com sucesso:

📋 Issue principal:
   <título> → <link>

📦 Sub-issues:
   [nome-do-repo] → <link>
   [nome-do-repo] → <link>
   ...

🔗 Projeto vinculado: <nome ou número do projeto> (ou "nenhum")

Total: 1 issue principal + N sub-issues
```
