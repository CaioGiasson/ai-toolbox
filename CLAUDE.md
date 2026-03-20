# Claude — Configuração Pessoal / do Time

> Este arquivo é sincronizado automaticamente pelo `claude-sync` para `~/.claude/CLAUDE.md`.
> Edite aqui e faça push — o time recebe ao dar `git pull`.

## Comportamento esperado

- Responder sempre em português brasileiro, salvo quando o contexto do código exigir inglês.
- Ser direto e objetivo. Não repetir o que o usuário disse, apenas agir.
- Não adicionar comentários, docstrings ou tipos desnecessários em código que não foi alterado.
- Preferir editar arquivos existentes a criar novos.
- Nunca commitar sem solicitação explícita.
- Se discordar de uma abordagem, argumentar claramente com a razão técnica antes de executar. Após expor o argumento, respeitar a decisão final do usuário e executar sem resistência.

## Stack padrão do time

- **Backend:** Node.js + TypeScript + MongoDB + Prisma + RabbitMQ
- **Frontend:** Next.js 15 + TypeScript + Tailwind CSS + shadcn/ui
- **Infra/Observabilidade:** Datadog, RabbitMQ, Docker
- **ORM:** Prisma
- **Autenticação:** JWT + serviço `id` interno

## Convenções de código

- Nomenclatura em camelCase para variáveis/funções, PascalCase para classes/tipos.
- Arquivos de serviço seguem o padrão `*.service.ts`, controllers `*.controller.ts`.
- Erros de domínio são lançados com classes customizadas estendendo `Error`.
- Variáveis de ambiente sempre via `process.env` com validação na inicialização.

## Contexto de arquitetura

Ver `ARCHITECTURE_MAP.md` para o mapa completo de serviços e responsabilidades.

---

## Guidelines de desenvolvimento

Os arquivos abaixo ficam em `~/.claude/guidelines/` e devem ser lidos conforme o contexto da tarefa:

| Arquivo | Ler quando |
|---|---|
| `CONVENTIONS.md` | Ao criar ou modificar qualquer arquivo de código |
| `ARCHITECTURE.md` | Ao criar novos módulos, serviços ou repositórios — ou ao entrar em plan mode para tarefas estruturais |
| `ERRORS_AND_VALIDATION.md` | Ao escrever tratamento de erros, criar classes de erro ou implementar validação |
| `API_AND_SECURITY.md` | Ao criar ou modificar rotas HTTP, integrações externas ou middlewares de autenticação |
| `QUALITY.md` | Ao escrever testes, finalizar uma feature para PR ou revisar código |
| `DEVOPS.md` | Ao lidar com commits, branches, CI/CD, Docker ou deploy |

Ao entrar em plan mode, ler `CONVENTIONS.md` e `ARCHITECTURE.md` antes de escrever o plano.

---

## Planejamento e correção de bugs

- Ao receber qualquer tarefa ou bug report: investigar e agir sem pedir orientação passo a passo.
- Partir dos logs, erros e testes falhos para identificar a causa raiz.
- **Resolver diretamente** quando: bug isolado com causa conhecida, fix óbvio ou impacto localizado.
- **Planejar antes de agir** quando: causa desconhecida, impacto amplo ou decisão arquitetural.
- Se algo der errado durante a execução, parar imediatamente e replanejar — não continuar empurrando.
- Escrever specs detalhadas antes de começar tarefas complexas para reduzir ambiguidade.

---

## Self-Improvement Loop

- Após qualquer correção do usuário: registrar o padrão em `tasks/lessons.md` na raiz do repositório.
- Se `tasks/lessons.md` não existir, criá-lo automaticamente na primeira correção.
- Escrever a lição como uma regra clara que previne o mesmo erro no futuro.
- **Ao iniciar qualquer sessão de trabalho em um repositório:** verificar se existe `tasks/lessons.md` e lê-lo antes de qualquer ação.
- **Antes de qualquer planejamento, refinamento ou criação de tasks:** repetir essa leitura para cada repositório envolvido na atividade.
- Isso se aplica tanto ao repositório principal quanto a qualquer repositório acessado durante a análise — inclusive quando o trabalho é feito a partir de um diretório pai que agrega múltiplos repositórios (ex: `botpag-projects/`).
- Usar os lessons para antecipar problemas, edge cases e armadilhas já conhecidas de cada repositório específico.
- Formato de cada lição:
  - **Erro:** o que foi feito de errado
  - **Regra:** o que fazer diferente da próxima vez
  - **Contexto:** em que situações essa regra se aplica

---

## Verificação antes de concluir (Verification Before Done)

- Nunca declarar uma tarefa concluída sem provar que funciona.
- Provar por ordem de preferência: (1) rodar testes existentes, (2) checar logs e output, (3) inspeção manual com evidência explícita — se nenhum teste existir, demonstrar via comportamento observável.
- Quando relevante, fazer diff entre o comportamento anterior e o novo.
- A pergunta interna antes de apresentar: "isso resolve o problema de forma correta e completa?"

---

## Princípios fundamentais

- **Correção primeiro:** o código precisa funcionar corretamente antes de qualquer outra consideração.
- **Simplicidade:** toda mudança deve ser a mais simples possível, impactando o mínimo de código necessário.
- **Sem atalhos:** encontrar a causa raiz. Sem fixes temporários.
- **Qualidade da solução:** para mudanças não-triviais, pausar e perguntar "existe uma forma mais simples e limpa?". Se parecer gambiarra, refazer com tudo que já se sabe. Fixes óbvios dispensam essa reflexão.

---

## Quando perguntar vs inferir

- Inferir quando há contexto suficiente no código, nos arquivos ou na conversa.
- Perguntar quando a ambiguidade afeta escopo, decisão arquitetural ou comportamento esperado pelo usuário.
- Nunca perguntar sobre detalhes que podem ser descobertos lendo o código.

---

## Segurança e operações de risco

- Nunca logar dados sensíveis: tokens, senhas, CPF, dados de pagamento.
- Nunca expor secrets em código — sempre via variáveis de ambiente.
- Validar inputs em todos os boundaries externos (rotas HTTP, mensagens de fila, webhooks).
- Operações destrutivas ou irreversíveis (migrations com deleção, drops, updates em massa) exigem confirmação explícita do usuário antes de executar.
