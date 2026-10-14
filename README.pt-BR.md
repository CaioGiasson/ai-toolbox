<p align="right"><a href="README.md">🇺🇸 English</a> · <b>🇧🇷 Português</b></p>

<div align="center">

# Seu Claude, com jeito de time

**O ai-toolbox ensina o Claude a trabalhar do jeito do seu time: da ideia à tarefa, da tarefa ao código, do código à revisão. Você pede em português. Ele entrega.**

<table>
<tr>
<td align="center" width="25%"><h3>10 skills</h3>prontas para usar<br><sub><a href="#catálogo-de-skills">ver catálogo</a></sub></td>
<td align="center" width="25%"><h3>4 check-ups</h3>segurança, velocidade, LGPD e preparo para IA<br><sub><a href="#check-up-do-sistema">ver como funciona</a></sub></td>
<td align="center" width="25%"><h3>512 critérios</h3>avaliados no check-up completo<br><sub><a href="#check-up-do-sistema">ver detalhes</a></sub></td>
<td align="center" width="25%"><h3>1 mensagem</h3>para instalar, direto no chat<br><sub><a href="#como-instalar">ver instalação</a></sub></td>
</tr>
</table>

**[Instalar](#como-instalar) · [Antes e depois](#antes-e-depois) · [Catálogo](#catálogo-de-skills) · [Como usar](#como-usar) · [Atualizar](#como-atualizar) · [Dúvidas](#dúvidas-comuns) · [Privacidade](#privacidade)**

</div>

---

## Antes e depois

<table>
<tr>
<th width="50%">Sem o ai-toolbox</th>
<th width="50%">Com o ai-toolbox</th>
</tr>
<tr>
<td valign="top">

> "Precisamos de um jeito de baixar a fatura."

Uma frase solta. Cada pessoa entende de um jeito, o desenvolvedor faz perguntas por dias e o resultado depende de quem pegou a tarefa.

</td>
<td valign="top">

> Tarefa completa no GitHub: objetivo, regras, o que mudar, como testar. Código pronto para revisão e um roteiro de testes na mão.

O Claude estuda o sistema, pergunta só o que falta e entrega no padrão do time.

</td>
</tr>
</table>

<sub>Exemplo ilustrativo do tipo de resultado que cada skill produz.</sub>

**Mesma ideia. Entrega organizada, no padrão do time.**

## Como instalar

Você não precisa abrir terminal. Precisa de três coisas instaladas: o **aplicativo Claude** (aba **Code**), o **Git** e o **Node.js**. Se faltar algo, o próprio Claude avisa e te guia.

1. Abra o aplicativo Claude e entre na aba **Code**.
2. Escolha a pasta onde ficam os seus projetos (a "pasta pai").
3. Cole esta mensagem no chat e envie:

   > Instale o ai-toolbox: clone https://github.com/CaioGiasson/ai-toolbox.git na pasta atual, rode `npm install` e `npm run sync` dentro dele, e me diga quando terminar.

4. Espere o Claude confirmar e abra uma **nova conversa**. As skills já aparecem na lista.

Uma mensagem. Só isso.

<sub>Prefere o terminal? Veja a <a href="docs/TECNICO.md#instalação-via-terminal">instalação técnica</a>.</sub>

## Como atualizar

Quando o time lançar novidades, abra uma conversa na aba **Code** e envie:

> Atualize o ai-toolbox: entre na pasta ai-toolbox, rode `git pull` e `npm run sync`.

Skills novas e melhorias chegam na hora.

## Como usar

Em qualquer conversa na aba **Code**, digite `/` e escolha a skill na lista. Depois escreva o que precisa em português normal.

> `/issue-refine` Quero que o cliente consiga baixar a fatura em PDF na tela de pagamentos.

Se preferir, só descreva o que quer. O Claude também sugere a skill certa.

## Catálogo de skills

Dez skills em três grupos. Cada uma diz o que faz e qual resultado você recebe.

| Grupo | Para que serve | Skills |
|---|---|---|
| **[Da ideia à tarefa](#da-ideia-à-tarefa-pronta)** | Transformar conversa solta em tarefa clara | `/issue-from-thread` · `/issue-refine` |
| **[Do código à entrega](#do-código-à-entrega)** | Programar, revisar e finalizar | `/issue-start` · `/issue-review` · `/issue-approve` |
| **[Check-up do sistema](#check-up-do-sistema)** | Medir a saúde do projeto, sem alterar nada | `/eval-security` · `/eval-performance` · `/eval-privacy` · `/eval-ai-readiness` · `/full-assessment` |

**O caminho completo de uma tarefa:** `/issue-from-thread` ou `/issue-refine` → `/issue-start` → `/issue-review` → você testa → `/issue-approve`.

### Da ideia à tarefa pronta

| Skill | O que faz | O que você recebe |
|---|---|---|
| **`/issue-from-thread`** | Lê uma conversa informal (link de thread do Slack, link do Discord ou arquivo `.md`), ignora o ruído e separa decisões de dúvidas e opiniões. | Uma tarefa organizada no quadro do GitHub, sem piadas, gírias nem informações soltas. |
| **`/issue-refine`** | Pega uma ideia descrita em poucas linhas, estuda o sistema, faz perguntas objetivas e detalha tudo. | Uma tarefa completa no GitHub (objetivo, regras, o que mudar e como testar), clara o bastante para qualquer pessoa executar. Quando envolve vários sistemas, cria uma sub-tarefa para cada um. |

### Do código à entrega

| Skill | O que faz | O que você recebe |
|---|---|---|
| **`/issue-start`** | Recebe o link de uma tarefa, move no quadro para "Em andamento", programa a solução, cria os testes e se revisa sozinha. | Uma *pull request* (pedido de revisão) pronta, com o código em etapas organizadas e um roteiro de testes para você conferir. |
| **`/issue-review`** | Revisa uma *pull request*: confere se tudo o que foi pedido foi feito, roda os testes e analisa a qualidade do código. | Comentários de revisão publicados no trecho certo do código, depois que você escolhe o que postar. Só corrige algo se você pedir. |
| **`/issue-approve`** | Entra depois dos seus testes manuais e faz a última revisão antes de finalizar. | Se estiver tudo certo: comentário final, marcação "Reviewed", entrega concluída (*merge*) e limpeza das cópias de trabalho. Se achar problema sério, apenas avisa você e não mexe em nada. |

### Check-up do sistema

**Só leem e avaliam. Não alteram nada no seu projeto.** Cada check-up entrega um relatório com **nota de 0 a 100**, uma **classificação** e uma **lista de problemas por prioridade**, pronta para virar plano de ação. O relatório fica salvo na pasta `docs/assessments` do projeto avaliado.

| Skill | O que avalia | Critérios | O que você recebe |
|---|---|---:|---|
| **`/eval-security`** | Segurança: login, proteção de dados, brechas conhecidas, segredos expostos. Serve de preparação para um teste de invasão. | 153 | Nota de segurança e pontos fracos por gravidade. |
| **`/eval-performance`** | Velocidade, capacidade de crescer, estabilidade e custos de infraestrutura. | 163 | Onde o sistema fica lento ou caro e o que priorizar. |
| **`/eval-privacy`** | Conformidade com a LGPD: consentimento, direitos dos titulares, guarda de dados pessoais. | 126 | Lacunas legais, cada uma ligada ao artigo da lei. |
| **`/eval-ai-readiness`** | Quão preparado o projeto está para ser desenvolvido com ajuda de IA: documentação, testes, organização. | 70 | O que melhorar para a IA trabalhar mais rápido e errar menos. |
| **`/full-assessment`** | Os quatro check-ups de uma vez. | 512 | Os quatro relatórios mais um geral, com nota única, riscos que atravessam as áreas e uma lista única de prioridades. |

Como ler a nota:

| Nota | Classificação |
|---|---|
| 90 a 100 | 🏆 Platinum |
| 70 a 89 | 🥇 Gold |
| 50 a 69 | 🥈 Silver |
| 25 a 49 | 🥉 Bronze |
| 0 a 24 | 🚨 Dangerous |

## Antes de usar as skills de tarefas

As skills `/issue-*` conversam com o GitHub. O Claude usa a conexão com o GitHub que você já tiver e, se não houver, avisa e usa o GitHub CLI (`gh`). Se algo pedir acesso, é só aprovar quando o Claude perguntar.

## Dúvidas comuns

**Preciso saber programar?** Não para instalar nem para usar o refinamento de tarefas e os check-ups.

**As skills mudam meu projeto sem avisar?** Os check-ups nunca alteram nada. As demais mostram o que vão fazer e pedem confirmação nas decisões importantes.

**A skill não apareceu na lista.** Abra uma nova conversa depois de instalar ou atualizar.

**Quero criar ou editar skills, ou entender a estrutura de pastas.** Veja a [documentação técnica](docs/TECNICO.md).

## Privacidade

- O ai-toolbox é só um conjunto de arquivos de texto. A instalação **copia** esses arquivos para a pasta `.claude` do seu computador e não envia nada para fora.
- As skills rodam dentro do seu Claude, com a sua conta e as suas permissões.
- As skills `/issue-*` leem e escrevem no GitHub porque esse é o trabalho delas, sempre com a sua conta.

---

<div align="center">

**Um time, um jeito de trabalhar. Cada pessoa com o seu Claude.**

<sub>
<a href="docs/TECNICO.md">Documentação técnica</a> ·
<a href="https://github.com/CaioGiasson/ai-toolbox/issues">Issues</a>
</sub>

</div>
