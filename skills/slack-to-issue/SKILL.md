---
name: slack-to-issue
description: Lê uma thread do Slack, identifica objetivos e serviços referenciados, verifica se já existem fluxos que atendam a necessidade, classifica o impacto da mudança e cria a issue (via create-issue) ou inicia a implementação diretamente (via start-issue) para mudanças de baixo impacto.
---

# Skill: slack-to-issue

Você é um engenheiro de software sênior e product manager técnico. Seu objetivo é transformar uma thread de Slack em uma issue refinada do GitHub — ou iniciar a implementação diretamente caso a mudança seja de baixo impacto.

## Entrada

O usuário invocou esta skill com o seguinte texto:
`$ARGUMENTS`

---

## Ferramentas

### Slack MCP

Use o **MCP do Slack** (`slack_*`) para ler a thread. Antes de qualquer operação, verifique se o MCP está disponível tentando uma chamada simples (ex: `slack_list_channels`).

Se **não estiver configurado**, exiba o aviso abaixo e encerre — esta skill depende do MCP do Slack e não possui fallback de CLI:

```
✖ MCP do Slack não detectado. Esta skill requer o MCP do Slack configurado.

Configure em ~/.claude/settings.json:

  "mcpServers": {
    "slack": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "<seu-bot-token>",
        "SLACK_TEAM_ID": "<seu-team-id>"
      }
    }
  }

Após configurar, reabra o Claude Code e tente novamente.
```

### GitHub MCP

Use o **MCP do GitHub** (`mcp__github__*`) para operações com o GitHub. Se não estiver configurado, use o **GitHub CLI (`gh`)** como fallback — conforme o padrão já descrito nas demais skills do time.

---

## FASE 0 — Extração da thread do Slack

1. Extraia o link da thread a partir de `$ARGUMENTS`. Se não houver link, peça ao usuário:
   ```
   Cole o link da thread do Slack para iniciar o refinamento:
   ```

2. Parse o link para extrair `channel_id` e `thread_ts`:
   - Formato de URL do Slack: `https://<workspace>.slack.com/archives/<CHANNEL_ID>/p<TIMESTAMP>`
   - O timestamp no link está no formato `p1234567890123456` → converter para `1234567890.123456` (inserindo ponto na 10ª posição)
   - Exemplo: `p1748521234567890` → `1748521234.567890`

3. Leia a mensagem raiz da thread:
   ```
   slack_get_channel_history(channel=<CHANNEL_ID>, limit=1)
   ```

4. Leia todas as respostas da thread:
   ```
   slack_get_thread_replies(channel=<CHANNEL_ID>, thread_ts=<THREAD_TS>)
   ```

5. Para cada mensagem, resolva os perfis dos participantes via `slack_get_user_profile` quando útil para entender quem está falando (ex: PM, dev, designer).

6. Exiba um resumo da coleta:
   ```
   📥 Thread lida com sucesso
      Canal: <nome ou ID>
      Mensagens: <N>
      Participantes: <lista de nomes>
   ```

---

## FASE 1 — Análise da thread

Com base nas mensagens coletadas, extraia:

### 1.1 — Objetivos e contexto de negócio
- O que está sendo pedido ou discutido?
- Qual problema ou necessidade essa demanda resolve?
- Há uma decisão tomada ou ainda é uma discussão em aberto?

### 1.2 — Serviços e repositórios referenciados
- Quais serviços internos são mencionados explicitamente? (ex: `parcelatudo-backend-api`, `id`, `checkout`, `detran`, etc.)
- Quais fluxos ou funcionalidades são citados? (ex: "tela de pagamento", "webhook do Cielo", "wallet", "notificação por WhatsApp")
- Há menção a telas, componentes, endpoints, filas ou modelos específicos?

### 1.3 — Tasks identificadas
- Liste as ações concretas mencionadas na thread (ex: "adicionar campo X", "mudar cor do botão", "criar endpoint Y", "integrar com serviço Z").

Ao final desta fase, exiba:
```
🔍 Análise concluída:

Objetivo: <resumo em 1-2 frases>

Serviços citados: <lista>
Tasks identificadas:
  - <task 1>
  - <task 2>
  ...
```

---

## FASE 2 — Verificação de cobertura na arquitetura

1. Leia `~/.claude/ARCHITECTURE_MAP.md`.

2. Para cada serviço e funcionalidade identificada na Fase 1, verifique:
   - O serviço já existe no mapa de arquitetura?
   - A funcionalidade solicitada já está descrita como existente em algum serviço?
   - Há fluxos ou integrações que já atendem parcialmente a necessidade?

3. Se possível, explore brevemente os repositórios relevantes para confirmar se a funcionalidade existe no código (não apenas no mapa).

4. Exiba o resultado da verificação:
   ```
   📦 Cobertura na arquitetura:

   ✔ <serviço/funcionalidade> — já existe em <repositório>
   ✖ <serviço/funcionalidade> — não encontrado / precisa ser criado
   ~ <serviço/funcionalidade> — existe parcialmente em <repositório>, requer extensão
   ```

5. Se **tudo que foi pedido já existir** e nenhuma alteração for necessária, informe o usuário:
   ```
   ℹ Esta funcionalidade já parece estar coberta pela arquitetura atual.

   Repositórios relevantes:
   - <repositório> — <descrição do que já existe>

   Deseja prosseguir mesmo assim? (sim/não)
   ```
   Aguarde a resposta antes de continuar.

---

## FASE 3 — Classificação do impacto

Com base na análise e na verificação de arquitetura, classifique a mudança como **baixo impacto** ou **alto impacto** usando os critérios abaixo.

### Critérios de baixo impacto (→ usar `/start-issue`)

A mudança é de **baixo impacto** se **todos** os critérios abaixo forem verdadeiros:

- Não altera fluxos de negócio existentes
- Não cria nem modifica endpoints, modelos de banco, filas ou integrações externas
- Não afeta mais de 1 repositório
- É exclusivamente uma das seguintes naturezas:
  - Mudança visual: cor, fonte, espaçamento, layout, ícone
  - Mudança de texto: labels, mensagens, traduções, copy
  - Configuração de componente existente sem nova lógica
  - Correção de typo ou ajuste cosmético

### Critérios de alto impacto (→ usar `/create-issue`)

A mudança é de **alto impacto** se **qualquer** condição abaixo for verdadeira:

- Cria ou modifica lógica de negócio
- Adiciona ou altera endpoints, modelos, filas ou integrações
- Afeta 2 ou mais repositórios
- Requer novo serviço, módulo ou fluxo
- Envolve autenticação, pagamento, dados sensíveis ou permissões

Exiba a classificação:
```
⚖️  Classificação: <BAIXO IMPACTO | ALTO IMPACTO>

Motivo: <justificativa em 1-2 frases baseada nos critérios acima>
```

Se a classificação for **incerta**, apresente os dois lados e pergunte ao usuário:
```
⚠ Classificação incerta.

Indicadores de baixo impacto: <lista>
Indicadores de alto impacto: <lista>

Como você classificaria esta mudança?
  [1] Baixo impacto — iniciar implementação diretamente
  [2] Alto impacto — refinar e criar issue técnica completa
```
Aguarde a resposta do usuário.

---

## FASE 4 — ROTA A: Baixo impacto → Iniciar implementação

> Siga esta fase apenas se a classificação da Fase 3 foi **BAIXO IMPACTO**.

### 4.1 — Identificação do repositório

Com base nos serviços identificados na Fase 1 e na verificação da Fase 2, determine o repositório onde a mudança será feita. Se houver ambiguidade, pergunte ao usuário.

### 4.2 — Criação de issue enxuta

Crie uma issue no repositório identificado com o seguinte formato:

**Título:** `[MELHORIA] <título direto descrevendo a mudança>`

**Corpo:**
```markdown
## Contexto

<De onde veio essa demanda: thread do Slack com data e participantes principais.>

Thread de origem: <link da thread>

## O que fazer

<Descrição direta e objetiva das alterações visuais/textuais a realizar.>

## Critérios de aceite

- [ ] <critério 1>
- [ ] <critério 2>

## 🤖 Prompt para o Claude

---

Você está implementando a seguinte tarefa neste repositório (`<nome-do-repo>`):

**Feature:** <título>
**Issue:** <link da issue>

### Antes de começar

Leia `~/.claude/guidelines/CONVENTIONS.md`.
Se existir `tasks/lessons.md`, leia antes de qualquer ação.

### O que fazer

<Descrição direta e imperativa das alterações: arquivos prováveis, valores a mudar, comportamento esperado. Sem lógica de negócio nova.>

### Critérios de conclusão

- [ ] <critério 1>
- [ ] <critério 2>

### Contexto adicional

- Stack: <stack do repositório conforme ARCHITECTURE_MAP.md>
- Mudança de baixo impacto: não alterar fluxos, endpoints ou modelos existentes.
- Limite o escopo ao que foi descrito acima.

---
```

### 4.3 — Handoff para start-issue

Após criar a issue, exiba:
```
✅ Issue criada: <link>

Esta é uma mudança de baixo impacto. Para iniciar a implementação:

  /start-issue <link-da-issue>
```

---

## FASE 4 — ROTA B: Alto impacto → Criar issue refinada

> Siga esta fase apenas se a classificação da Fase 3 foi **ALTO IMPACTO**.

### 4.1 — Preparação do contexto para create-issue

Monte uma descrição consolidada a partir de tudo que foi extraído nas fases anteriores:

```
CONTEXTO DA THREAD
==================
Thread: <link>
Data: <data das mensagens>
Participantes: <lista>

OBJETIVO
--------
<Descrição do objetivo de negócio identificado na análise>

SERVIÇOS ENVOLVIDOS
-------------------
<Lista dos serviços e repositórios identificados>

TASKS IDENTIFICADAS
-------------------
<Lista de tasks da thread>

COBERTURA ATUAL
---------------
<O que já existe vs o que precisa ser criado/modificado>

CONTEXTO ADICIONAL
------------------
<Trechos relevantes das mensagens do Slack que ajudam a entender a demanda>
```

### 4.2 — Execução do fluxo create-issue

Com o contexto preparado acima, execute o fluxo completo da skill `/create-issue` a partir da **FASE 0**, tratando o contexto montado no passo 4.1 como a entrada (`$ARGUMENTS`) daquela skill.

Siga todas as fases do create-issue:
- Fase 0: Exploração da codebase (use os repositórios já identificados como ponto de partida)
- Fase 1: Refinamento — faça perguntas apenas sobre o que a thread **não** responde
- Fase 2: Mapeamento de repositórios
- Fase 3: Documento de validação
- Fase 4: Seleção do projeto GitHub
- Fase 5: Criação das issues
- Fase 6: Atualização da issue principal
- Fase 7: Conclusão

> **Nota:** Ao chegar na Fase 1 do create-issue, prefira perguntas focadas nas lacunas — muito do contexto de negócio já foi coletado da thread do Slack. Não repita perguntas sobre o que as mensagens já respondem.
