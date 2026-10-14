# ai-toolbox

**Uma caixa de ferramentas pronta para o seu Claude trabalhar como um time experiente.**

O ai-toolbox dá ao Claude um conjunto de "habilidades" (chamadas de *skills*) prontas para usar: transformar uma ideia em tarefa bem escrita, programar essa tarefa, revisar o resultado e avaliar a saúde de um sistema. Você pede em português, no chat, e recebe o trabalho entregue.

Sem decorar comandos. Sem configurar nada complicado.

---

## O que você ganha

- **Tarefas bem escritas:** uma conversa solta de Slack ou Discord vira uma tarefa clara no GitHub.
- **Trabalho entregue de ponta a ponta:** do código à revisão e à aprovação final.
- **Um "check-up" do seu sistema:** notas de 0 a 100 para segurança, velocidade, privacidade (LGPD) e preparo para IA.
- **Padrão de time:** o Claude passa a seguir as mesmas regras e o mesmo jeito de trabalhar para todas as pessoas.

---

## Como instalar (sem usar terminal)

Você precisa de três coisas instaladas no computador: o **aplicativo Claude** (aba **Code**), o **Git** e o **Node.js**. Se faltar algo, o próprio Claude avisa e te guia.

1. Abra o aplicativo Claude e entre na aba **Code**.
2. Escolha a pasta onde ficam os seus projetos (a "pasta pai").
3. Cole esta mensagem no chat e envie:

   > Instale o ai-toolbox: clone https://github.com/CaioGiasson/ai-toolbox.git na pasta atual, rode `npm install` e `npm run sync` dentro dele, e me diga quando terminar.

4. Aguarde o Claude confirmar. Pronto: as skills já estão no seu Claude.
5. Feche e abra uma nova conversa para as skills aparecerem na lista.

## Como atualizar

Sempre que o time lançar novidades, abra uma conversa na aba **Code** e envie:

> Atualize o ai-toolbox: entre na pasta ai-toolbox, rode `git pull` e `npm run sync`.

As skills novas e as melhorias chegam na hora.

## Como usar uma skill

Em qualquer conversa na aba **Code**, digite `/` e escolha a skill na lista que aparece. Depois, escreva o que precisa em português normal.

Exemplo:

> `/issue-refine` Quero que o cliente consiga baixar a fatura em PDF na tela de pagamentos.

Se preferir, basta descrever o que quer: o Claude também sugere a skill certa.

---

## Catálogo de skills

### 📝 Da ideia à tarefa pronta

| Skill | O que faz | O que você recebe |
|---|---|---|
| **`/issue-from-thread`** | Lê uma conversa informal (link de thread do Slack, link do Discord ou arquivo `.md`), ignora o ruído, separa decisões de dúvidas e opiniões. | Uma tarefa organizada no quadro do GitHub, sem piadas, gírias nem informações soltas. |
| **`/issue-refine`** | Pega uma ideia descrita em poucas linhas, estuda o sistema, faz perguntas objetivas e detalha tudo. | Uma tarefa completa no GitHub (objetivo, regras, o que mudar e como testar), clara o bastante para qualquer pessoa executar. Quando mexe em vários sistemas, cria uma sub-tarefa para cada um. |

### 🛠️ Do código à entrega

| Skill | O que faz | O que você recebe |
|---|---|---|
| **`/issue-start`** | Recebe o link de uma tarefa, move no quadro para "Em andamento", programa a solução, cria os testes e se revisa sozinha. | Uma *pull request* (pedido de revisão) pronta, com o código organizado em etapas e um roteiro de testes para você conferir. |
| **`/issue-review`** | Revisa uma *pull request*: confere se tudo o que foi pedido foi feito, roda os testes e analisa a qualidade do código. | Comentários de revisão publicados direto no código, nos pontos certos, depois da sua escolha do que postar. Só corrige algo se você pedir. |
| **`/issue-approve`** | Entra depois que você fez os testes manuais. Faz a última revisão antes de finalizar. | Se estiver tudo certo: comentário final, marcação "Reviewed", entrega concluída (*merge*) e limpeza das cópias de trabalho. Se encontrar problema sério, apenas avisa você e não mexe em nada. |

**O caminho completo:** `/issue-from-thread` ou `/issue-refine` → `/issue-start` → `/issue-review` → você testa → `/issue-approve`.

### 🩺 Check-up do sistema

Estas skills **só leem e avaliam**: não alteram nada no seu projeto. Cada uma entrega um relatório com **nota de 0 a 100**, uma **classificação** e uma **lista de problemas por prioridade**, pronta para virar plano de ação. O relatório é salvo na pasta `docs/assessments` do projeto avaliado.

| Nota | Classificação |
|---|---|
| 90 a 100 | 🏆 Platinum |
| 70 a 89 | 🥇 Gold |
| 50 a 69 | 🥈 Silver |
| 25 a 49 | 🥉 Bronze |
| 0 a 24 | 🚨 Dangerous |

| Skill | O que avalia | O que você recebe |
|---|---|---|
| **`/eval-security`** | Segurança: login, proteção de dados, brechas conhecidas, segredos expostos. Serve de preparação para um teste de invasão. | Relatório com a nota de segurança e os pontos fracos por gravidade. |
| **`/eval-performance`** | Velocidade, capacidade de crescer, estabilidade e custos de infraestrutura. | Relatório mostrando onde o sistema fica lento ou caro e o que priorizar. |
| **`/eval-privacy`** | Conformidade com a LGPD: consentimento, direitos dos titulares, guarda de dados pessoais. | Relatório com as lacunas legais, cada uma ligada ao artigo da lei correspondente. |
| **`/eval-ai-readiness`** | Quão preparado o projeto está para ser desenvolvido com ajuda de IA: documentação, testes, organização. | Relatório com o que melhorar para a IA trabalhar mais rápido e errar menos. |
| **`/full-assessment`** | Os quatro check-ups de uma vez. | Os quatro relatórios mais um relatório geral, com nota única, riscos que atravessam as áreas e uma lista única de prioridades. |

---

## Antes de usar as skills de tarefas (`/issue-*`)

Elas conversam com o GitHub. O Claude cuida disso com a ferramenta do GitHub que você já tiver conectada e, se não houver, avisa e usa o GitHub CLI (`gh`). Se algo pedir acesso, é só aprovar quando o Claude perguntar.

## Dúvidas comuns

**Preciso saber programar?** Não para instalar nem para usar as skills de check-up e de refinamento de tarefas.

**As skills mudam meu projeto sem avisar?** As de check-up nunca alteram nada. As demais mostram o que vão fazer e pedem confirmação nas decisões importantes.

**A skill não apareceu na lista.** Abra uma nova conversa depois de instalar ou atualizar.

**Quero criar ou editar skills, ou entender a estrutura.** Veja a [documentação técnica](docs/TECNICO.md).
