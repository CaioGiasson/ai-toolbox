# Melhorias identificadas — claude-sync

> Consolidado a partir de feedbacks do time + pontos levantados internamente.

---

## Skills

### `/start-issue` — Branch management

**Problema:** A skill sempre cria uma nova branch incondicionalmente (Fase 3), ignorando branches já existentes criadas externamente (ex: via GitHub web). Usuários que criam a branch antes de rodar a skill ficam com duas branches paralelas sem vínculo claro.

**Melhoria esperada:**

- Antes de criar, verificar se já existe branch local ou remota correspondente ao número da issue
- Se existir, oferecer ao usuário a opção de usar a branch existente ou criar uma nova
- Aceitar branch como argumento opcional: `/start-issue <url> <branch>`

---

### `/create-issue` — Feedback de progresso em processamento pesado

**Problema:** Em tasks complexas com input denso (documentação extensa + múltiplos repositórios), a skill entra em processamento longo sem nenhuma sinalização — ficou 20+ minutos em "thinking..." sem resposta. Ausência de feedback intermediário impede o usuário de saber se está travado ou processando.

**Melhoria esperada:**

- Tornar o mapeamento incremental: processar e reportar cada repositório individualmente antes de seguir para o próximo
- Sinalizar progresso explicitamente a cada etapa (ex: `✔ clearance-api mapeado`, `→ lendo lessons.md de checkout...`)

---

### `/create-issue` — Leitura da codebase antes do refinamento

**Problema:** Atualmente a skill parte direto para as perguntas de refinamento sem entender o estado atual do código. Isso faz com que as perguntas sejam genéricas e o mapeamento de impacto seja raso — o agente não sabe o que já existe, como as coisas estão estruturadas ou quais módulos seriam afetados de fato.

**Melhoria esperada:**

- Antes de iniciar as perguntas de refinamento (Fase 1), fazer um mapeamento técnico da codebase relacionada ao contexto passado:
  - Identificar quais repositórios provavelmente são afetados
  - Ler os arquivos relevantes para entender as funcionalidades existentes
  - Entender como o ecossistema da funcionalidade/melhoria proposta está estruturado atualmente
- Usar esse contexto para fazer perguntas mais precisas e assertivas, evitando perguntas que o próprio código já responde
- Resultado: refinamento mais cirúrgico, mapeamento de impacto mais fiel à realidade

---

### `/create-issue` — Vínculo com projeto do GitHub

**Problema:** As issues são criadas soltas, sem vínculo com nenhum projeto do GitHub. O time precisa manualmente adicionar as issues ao board após a criação.

**Melhoria esperada:**

- Durante a Fase 3 (seleção do repositório), perguntar também em qual projeto do GitHub as issues devem ser vinculadas
- Vincular issue principal e sub-issues ao projeto informado via API do GitHub no momento da criação

---

## Infraestrutura

### `sync.sh` — Auto-sync via `git pull` não está funcionando

**Problema:** O hook `post-merge` configurado pelo Husky deveria rodar o `sync.sh` automaticamente após cada `git pull`, mas não está sendo disparado nas máquinas do time.

**Melhoria esperada:**

- Investigar e corrigir o registro do hook `post-merge` no Husky
- Garantir que o hook seja instalado corretamente no setup inicial (`npm install` / `prepare`)
- Validar que funciona em diferentes ambientes (Linux, macOS, WSL)
- Considerar adicionar instrução de diagnóstico no README para quando o hook não estiver ativo

