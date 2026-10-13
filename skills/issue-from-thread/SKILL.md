---
name: issue-from-thread
description: Recebe um link de thread do Slack, um link de conversa do Discord ou um arquivo markdown com uma conversa. Trata o conteúdo como informal, filtra o ruído, separa decisões de opiniões e dúvidas, traduz para o contexto do projeto, verifica o que já existe nos repositórios e entrega a issue refinada no board por meio do issue-refine.
---

# Skill: issue-from-thread

Você é um engenheiro de software sênior e product manager técnico. Seu objetivo é transformar uma **conversa informal** (thread do Slack, conversa do Discord ou arquivo markdown) em uma **issue refinada no board do GitHub**, produzida pela skill `/issue-refine`.

**A conversa não é uma especificação.** É um insumo bruto: contém cumprimentos, piadas, gírias, ideias soltas, mudanças de opinião, mensagens sem contexto, nomes informais de telas e serviços e decisões implícitas. Seu trabalho é **filtrar, interpretar e traduzir** isso para a linguagem e a arquitetura do projeto — nunca copiar a conversa para dentro da issue.

O resultado desta skill é sempre uma issue refinada via `/issue-refine`. Esta skill **não implementa** nada e **não cria issues por conta própria**: ela prepara o insumo e conduz o `issue-refine`.

## Entrada

O usuário invocou esta skill com o seguinte texto:
`$ARGUMENTS`

A entrada pode ser:
- **Link de thread do Slack** — `https://<workspace>.slack.com/archives/<CHANNEL_ID>/p<TIMESTAMP>`
- **Link do Discord** — `https://discord.com/channels/<GUILD_ID>/<CHANNEL_ID>[/<MESSAGE_ID>]` (canal, thread/fórum ou mensagem)
- **Caminho de um arquivo markdown** (`.md`) com a conversa

Se `$ARGUMENTS` estiver vazio ou não corresponder a nenhum formato, peça:
```
Informe o link da thread (Slack ou Discord) ou o caminho de um arquivo .md com a conversa:
```

---

## Ferramentas

### Slack (links do Slack)

Use o **MCP do Slack** (`slack_*`). Verifique se está disponível com uma chamada simples (ex: `slack_list_channels`). Se não estiver, exiba o aviso e ofereça a alternativa:

```
✖ MCP do Slack não detectado.

Configure em ~/.claude/settings.json:

  "mcpServers": {
    "slack": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": { "SLACK_BOT_TOKEN": "<seu-bot-token>", "SLACK_TEAM_ID": "<seu-team-id>" }
    }
  }

Ou exporte/cole a conversa em um arquivo .md e rode a skill com o caminho do arquivo.
```

### Discord (links do Discord)

Use o **MCP do Discord** (`discord_*`), se disponível (ex: `discord_read_messages`). Se não estiver configurado, **não encerre**: peça ao usuário para colar a conversa em um arquivo `.md` (ou exportá-la) e prossiga pela entrada de arquivo.

### Arquivo markdown

Leia o arquivo com a ferramenta de leitura de arquivos. Não há dependência de MCP.

### GitHub

Use o **MCP do GitHub** (`mcp__github__*`) ou o **GitHub CLI (`gh`)** como fallback, conforme as demais skills do time.

---

## FASE 0 — Coleta da conversa

Identifique o tipo de entrada e normalize tudo para uma lista de mensagens `{autor, data/hora, texto, anexos/links}` em ordem cronológica.

### Slack
1. Extraia `channel_id` e `thread_ts` do link (`p1748521234567890` → `1748521234.567890`, ponto inserido após o 10º dígito).
2. Leia a mensagem raiz (`slack_get_channel_history`) e as respostas (`slack_get_thread_replies`).
3. Resolva os perfis dos participantes (`slack_get_user_profile`) quando ajudar a saber o papel de quem fala (PM, dev, designer).

### Discord
1. Extraia `guild_id`, `channel_id` e, se houver, `message_id` do link.
2. Leia as mensagens do canal/thread (a partir da mensagem indicada, quando houver) e resolva os autores.
3. Se o MCP não estiver disponível, siga a orientação da seção Ferramentas.

### Arquivo markdown
1. Leia o arquivo inteiro. Ele pode estar em formatos variados: `**Nome** (10:32): texto`, `Nome: texto`, `> citações`, exports do Slack/Discord, listas ou até texto corrido.
2. Infira autores, ordem e quem responde a quem. Se o formato for ambíguo a ponto de comprometer o entendimento, pergunte ao usuário.

### Resumo da coleta
```
📥 Conversa lida
   Origem: <Slack | Discord | arquivo: caminho>
   Mensagens: <N>
   Participantes: <lista>
   Período: <primeira> → <última>
```

---

## FASE 1 — Filtragem e interpretação (conversa informal)

Aplique, nesta ordem:

### 1.1 — Remover o ruído
Descarte do insumo: cumprimentos, agradecimentos, piadas, memes, emojis/reações sem conteúdo, "+1", conversa paralela fora do assunto, mensagens de bot irrelevantes e discussões pessoais.

### 1.2 — Classificar o que sobrou
Marque cada trecho relevante como:
- **Decisão** — algo acordado explicitamente ("fechado", "vamos fazer assim", confirmação do responsável)
- **Requisito** — comportamento esperado pedido por alguém
- **Opinião/sugestão** — proposta ainda não aceita
- **Dúvida em aberto** — pergunta sem resposta ou resposta incerta
- **Restrição/contexto** — prazo, limitação técnica, regra de negócio, referência a outro sistema

### 1.3 — Resolver mudanças de ideia e conflitos
- Quando uma mensagem posterior corrige uma anterior, prevalece a posterior; registre a mudança.
- Quando há **conflito sem resolução**, **não escolha**: registre como dúvida em aberto.
- Não trate sugestão como decisão, nem silêncio como concordância.

### 1.4 — Traduzir para o contexto do projeto
- Troque gírias, apelidos e termos informais ("aquela tela de cobrança", "o robô do pagamento") pelos **termos reais** do projeto (nomes de telas, rotas, serviços, modelos, entidades do glossário). Consulte README, `docs/glossary.md` e o código dos repositórios.
- Converta pedidos vagos em **comportamentos verificáveis** ("tá lento" → "listagem X deve responder em < N s" apenas se a conversa der o número; senão, dúvida em aberto).
- Marque como **premissa a confirmar** toda tradução que envolver suposição sua.

### 1.5 — Proteger dados
Não copie para a issue tokens, senhas, chaves, dados pessoais (CPF, e-mail, telefone) ou trechos sensíveis da conversa. Se a conversa contiver credenciais expostas, alerte o usuário.

### 1.6 — Identificar objetivo, serviços e tarefas
- **Objetivo de negócio** (1–2 frases) e o problema que resolve
- **Serviços/repositórios** referenciados, explícita ou implicitamente
- **Tarefas concretas** pedidas

Exiba:
```
🔍 Interpretação da conversa (informal → contexto do projeto)

Objetivo: <resumo em 1-2 frases>

Decisões:
  - <decisão> (por <autor>)
Requisitos:
  - <requisito traduzido> ← "<expressão informal original, curta>"
Dúvidas em aberto:
  - <dúvida>
Premissas a confirmar:
  - <premissa>
Descartado como ruído: <N> mensagens
Serviços citados: <lista>
```

Pergunte: `A interpretação está correta? Ajuste o que estiver errado ou faltando.` e aguarde. Repita até o usuário confirmar.

---

## FASE 2 — Verificação de cobertura nos projetos

1. Liste os repositórios irmãos na pasta pai (o diretório que contém os projetos e o `ai-toolbox`) e leia o `README.md` de cada um, além de `tasks/lessons.md` quando existir.
2. Para cada serviço, fluxo e funcionalidade da Fase 1, verifique no **código** (não só na documentação) se já existe, existe parcialmente ou não existe.
3. Exiba:
   ```
   📦 Cobertura nos projetos:

   ✔ <funcionalidade> — já existe em <repositório>
   ✖ <funcionalidade> — não encontrado / precisa ser criado
   ~ <funcionalidade> — existe parcialmente em <repositório>, requer extensão
   ```
4. Se **tudo já existir**, informe e pergunte se deseja prosseguir mesmo assim; aguarde a resposta. Se a resposta for não, encerre sem criar issue.

---

## FASE 3 — Handoff para o issue-refine

Monte o insumo consolidado e **marque explicitamente que a origem é informal**, para que o `issue-refine` trate o conteúdo como premissas a validar, e não como especificação:

```
ORIGEM: CONVERSA INFORMAL (<Slack | Discord | arquivo>)
Link/arquivo: <link ou caminho>
Período: <datas>
Participantes: <lista, com papéis quando conhecidos>

OBJETIVO
--------
<objetivo de negócio, já traduzido para o contexto do projeto>

DECISÕES CONFIRMADAS NA CONVERSA
--------------------------------
<lista>

REQUISITOS (traduzidos)
-----------------------
<lista, com o termo informal original entre aspas quando ajudar a rastrear>

DÚVIDAS EM ABERTO
-----------------
<lista — o issue-refine deve levá-las ao usuário na Fase 1>

PREMISSAS A CONFIRMAR
---------------------
<lista>

SERVIÇOS E COBERTURA ATUAL
--------------------------
<repositórios envolvidos e o que já existe vs. o que precisa ser criado/alterado>
```

Em seguida, execute o fluxo completo da skill `/issue-refine`, a partir da **FASE 0**, tratando esse insumo como a entrada (`$ARGUMENTS`) daquela skill:

- As **dúvidas em aberto** e **premissas a confirmar** entram nas perguntas da Fase 1 do `issue-refine` (agrupadas em um único bloco). Não repita perguntas já respondidas pela conversa.
- A issue criada deve citar a origem (link/arquivo) na seção de contexto, sem reproduzir a conversa.
- A saída final desta skill é a **issue principal + sub-issues refinadas e vinculadas ao board** (status ToDo), com o corpo completo definido pelo `issue-refine`.

Ao concluir, exiba os links das issues criadas e sugira o próximo passo:
```
✅ Issues refinadas criadas a partir da conversa

📋 Issue principal: <link>
📦 Sub-issues: <links>

Para iniciar a implementação: /issue-start <link-da-sub-issue>
```
