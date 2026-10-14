# Catálogo de critérios — AI Readiness

> Gerado a partir do *Checklist sênior para assessment de aplicações — v3* (outubro/2026). Não edite à mão: regenere com `python -X utf8 scripts/gen-assessment-catalog.py` no ai-toolbox (fonte: `docs/application-assessment-v3.md`). IDs, severidades e critérios são a base do score e precisam ser estáveis entre execuções.

**Severidade (fixa por item):** `[B]` Bloqueante → **Crítico** (peso 3) · `[A]` Alto → **Importante** (peso 2) · `[M]` Médio e `[R]` Recomendado → **Menor** (peso 1).

**Itens condicionais** (*Se: …*): quando a condição não se aplica, marque **N/A com justificativa e evidência** (ex.: busca no código sem ocorrências). N/A sem evidência conta como Não compliant.

**Total de itens:** 70 — Crítico: 6 · Importante: 30 · Menor: 34. Pontuação máxima (todos aplicáveis): 112.

## Objetivo do pilar

> **Objetivo do pilar:** o repositório permite que agentes de IA (Claude Code, Codex, Copilot, Cursor e similares) localizem contexto rápido, gastem poucos tokens, gerem código que compila, passa nos testes, respeita a arquitetura, performa e não introduz vulnerabilidades — e que **erros do agente sejam pegos por máquinas antes de chegar a humanos**.
>
> **Regra de ouro:** tudo que você precisaria dizer a um engenheiro novo mais de uma vez deve estar (a) num arquivo de contexto curto, (b) numa skill carregada sob demanda, ou (c) — de preferência — codificado como teste, lint ou tipo que falha automaticamente. Instrução em prosa é a camada mais fraca; invariante executável é a mais forte.
>
> **Escopo:** este pilar avalia o **repositório e o fluxo de engenharia**. Recursos de IA da própria aplicação (chatbot, RAG, agentes para usuários) são avaliados em SEC-10, PERF-11 e PRIV-14.

## AIR-1. Arquivos de contexto e instruções

**Como verificar:** Leia `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, `.github/copilot-instructions.md`, `GEMINI.md`: tamanho, conteúdo (mapa, stack, comandos, restrições), duplicação/contradição, CODEOWNERS sobre esses arquivos, verificação automática em CI.

#### AIR-1.01 · Ponto de entrada único e curto
**Crítico** (peso 3, origem `[B]`)  
existe `AGENTS.md` na raiz (padrão aberto mantido pela Agentic AI Foundation/Linux Foundation) com: objetivo do sistema em poucas linhas, mapa de diretórios, stack e versões, comandos essenciais (instalar, rodar, testar, lintar, buildar), restrições inegociáveis e links para a fonte de verdade. É curto (referência de mercado: até ~150 linhas na raiz) — não uma enciclopédia.

#### AIR-1.02 · Compatibilidade entre ferramentas
**Menor** (peso 1, origem `[M]`)  
ferramentas que leem arquivos próprios (ex.: `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursor/rules`, `GEMINI.md`) apontam para o `AGENTS.md` (import, symlink ou referência) em vez de manter cópias divergentes.

#### AIR-1.03 · Instruções no escopo correto
**Importante** (peso 2, origem `[A]`)  
regras globais, por stack, por pacote e por padrão de arquivo estão separadas; `AGENTS.md` aninhado (ex.: `frontend/AGENTS.md`, `infra/AGENTS.md`) ou regras com escopo por glob são usados quando necessário. Instruções não duplicam nem contradizem umas às outras.

#### AIR-1.04 · Instruções verificadas
**Importante** (peso 2, origem `[A]`)  
comandos, caminhos e versões citados nos arquivos de contexto são testados automaticamente em CI (ex.: script que executa os comandos documentados e verifica que os caminhos existem). Arquivo de contexto que descreve estrutura que não existe mais é pior que nenhum.

#### AIR-1.05 · Instruções acionáveis e específicas
**Menor** (peso 1, origem `[M]`)  
regras dizem o **que fazer** e **como verificar** (“use `pnpm test --filter <pacote>`; nunca rode a suíte inteira localmente”), com exemplos de código bom/ruim do próprio repositório; sem frases genéricas (“escreva código limpo”). Cada regra tem motivo curto, para que o agente generalize corretamente.

#### AIR-1.06 · Proteção dos arquivos de contexto
**Importante** (peso 2, origem `[A]`)  
`AGENTS.md`, skills, regras e configuração de ferramentas de agente estão sob CODEOWNERS e exigem revisão humana, pois alterá-los muda o comportamento de todos os agentes (vetor de ataque e de degradação).

## AIR-2. Skills, comandos e ferramentas para agentes

**Como verificar:** Procure skills (`.claude/skills`, `skills/`), geradores (`plop`, scripts de scaffold), config de MCP (`.mcp.json`), hooks (`.claude/settings.json`, Husky/lint-staged) e documentação de dependências na versão usada.

#### AIR-2.01 · Skills para procedimentos recorrentes
**Importante** (peso 2, origem `[A]`)  
tarefas repetitivas e com passos específicos (criar endpoint, criar migration segura, adicionar feature flag, criar componente com testes, investigar regressão de performance, atualizar dependência) estão empacotadas como skills (`SKILL.md` + scripts/referências, padrão Agent Skills) carregadas sob demanda, em vez de inflar o arquivo de contexto global.

#### AIR-2.02 · Geradores e scaffolding determinísticos
**Menor** (peso 1, origem `[M]`)  
estruturas padronizadas (módulo, endpoint, teste, migration) são criadas por gerador/script do repositório, não “de memória” pelo agente, garantindo conformidade com convenções.

#### AIR-2.03 · Servidores MCP e ferramentas com privilégio mínimo
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: agentes usam MCP/ferramentas externas*  
servidores MCP configurados no repositório são inventariados, de fonte confiável, com versão pinada, escopo mínimo (somente leitura por padrão, ambiente não produtivo) e credenciais próprias de baixo privilégio.

#### AIR-2.04 · Documentação de bibliotecas na versão correta
**Menor** (peso 1, origem `[M]`)  
o agente tem acesso à documentação das versões **efetivamente usadas** das dependências principais (documentação versionada no repositório, links pinados por versão ou ferramenta de documentação atualizada), reduzindo código baseado em APIs obsoletas aprendidas no treinamento.

#### AIR-2.05 · Hooks automáticos
**Menor** (peso 1, origem `[M]`)  
hooks da ferramenta de agente e/ou de Git executam formatação, lint e checagens rápidas após edições e antes de commit, de modo que o agente receba feedback sem precisar lembrar de rodar.

## AIR-3. Conhecimento de negócio e documentação

**Como verificar:** Procure README, arquitetura, ADRs, glossário, contexto de negócio, matriz de autorização e requisitos não funcionais documentados e encontráveis.

#### AIR-3.01 · Contexto de negócio
**Importante** (peso 2, origem `[A]`)  
o repositório descreve personas, invariantes de negócio, regras, permissões (matriz de autorização — ver SEC-3.01), eventos, estados e integrações. Termos de domínio são consistentes entre código, docs, API e banco (glossário).

#### AIR-3.02 · Documentação de arquitetura
**Importante** (peso 2, origem `[A]`)  
há `README`, `ARCHITECTURE` (componentes, fronteiras, fluxos de dados, decisões principais), decisões registradas (ADRs), contratos, esquema de dados e fluxos críticos versionados junto ao código.

#### AIR-3.03 · Documentação otimizada para recuperação
**Menor** (peso 1, origem `[M]`)  
documentos são em Markdown limpo, com títulos descritivos, seções curtas e autocontidas, frontmatter/metadata (owner, data de revisão, status), links relativos e um índice; isso favorece tanto a busca do agente quanto indexação semântica interna.

#### AIR-3.04 · Requisitos não funcionais explícitos
**Importante** (peso 2, origem `[A]`)  
budgets de performance, requisitos de segurança e de privacidade relevantes ao código (o que é dado pessoal, o que não pode ser logado, timeouts padrão, limites de payload) estão documentados de forma que o agente os encontre ao alterar a área correspondente.

## AIR-4. Código legível por agentes

**Como verificar:** Avalie estrutura de pastas, regras de import/arquitetura (`eslint-plugin-boundaries`, `dependency-cruiser`), tamanho de arquivos (liste os maiores), código gerado isolado, código morto, exemplos canônicos citados nas instruções.

#### AIR-4.01 · Arquitetura com fronteiras verificáveis
**Importante** (peso 2, origem `[A]`)  
módulos têm responsabilidades claras, dependências direcionais, interfaces explícitas e pontos de extensão previsíveis. Camadas e boundaries são verificados por lint/testes estruturais (ex.: regras de import, testes de arquitetura). Não há imports circulares nem abstrações opacas.

#### AIR-4.02 · Localizabilidade
**Menor** (peso 1, origem `[M]`)  
nomes de arquivos, funções e símbolos são descritivos e consistentes, permitindo achar o código por busca textual; uma regra de negócio tem um dono identificável; não há a mesma lógica duplicada em vários lugares.

#### AIR-4.03 · Tamanho de arquivos e funções
**Menor** (peso 1, origem `[M]`)  
arquivos e funções muito grandes são evitados (limites definidos por lint), pois forçam o agente a ler muito contexto para mudanças pequenas e aumentam conflitos.

#### AIR-4.04 · Código gerado e vendorizado isolado
**Menor** (peso 1, origem `[M]`)  
código gerado, vendorizado, minificado e snapshots grandes ficam em diretórios marcados, não são editados manualmente (cabeçalho “gerado — não editar”) e são regeneráveis por comando documentado.

#### AIR-4.05 · Código morto e caminhos legados removidos
**Menor** (peso 1, origem `[M]`)  
código morto, flags expiradas e implementações paralelas antigas são removidos; caso convivam, estão marcados como obsoletos com o substituto indicado — senão o agente copia o padrão errado.

#### AIR-4.06 · Padrões de referência
**Menor** (peso 1, origem `[M]`)  
para cada tipo de artefato comum (endpoint, consulta, componente, job, teste), há um exemplo canônico apontado nas instruções (“siga `src/orders/` como referência”).

## AIR-5. Contratos e tipos na fronteira

**Como verificar:** Verifique `strict` no `tsconfig`, typecheck em CI, regras contra `any`/`@ts-ignore`, validação de borda e sincronização de contratos (OpenAPI gerado/verificado), testes de contrato.

#### AIR-5.01 · Contratos e tipos na fronteira
**Importante** (peso 2, origem `[A]`)  
entradas de HTTP, eventos, filas, arquivos, banco e terceiros são parseadas/validadas na fronteira; schemas, tipos, OpenAPI/GraphQL, migrations e exemplos estão sincronizados (gerados de uma fonte única ou verificados em CI). Erros, nulabilidade, unidades, timezone, idempotência e compatibilidade de versão são explícitos.

#### AIR-5.02 · Tipagem estrita
**Importante** (peso 2, origem `[A]`)  
type checker em modo estrito (ou equivalente da linguagem) roda em CI; uso de escapes (`any`, `# type: ignore`, `@ts-ignore`, casts não verificados) é limitado por lint e exige justificativa.

#### AIR-5.03 · Testes de contrato
**Menor** (peso 1, origem `[M]`)  
contratos entre serviços e com o frontend são verificados por testes (consumer-driven ou schema diff), de modo que o agente detecte quebra de compatibilidade ao alterar uma API.

## AIR-6. Feedback executável

**Como verificar:** Execute (quando seguro) os comandos documentados: install, lint, typecheck, test, build. Verifique se existe um comando único de verificação, execução por arquivo/pacote, ambiente reproduzível (Docker Compose/dev container) e versões fixadas.

#### AIR-6.01 · Comandos curtos e determinísticos
**Crítico** (peso 3, origem `[B]`)  
instalar, formatar, lintar, testar, buildar, subir localmente, popular dados e validar funcionam em ambiente limpo com um comando cada (ex.: `make check`, `pnpm verify`), documentados no `AGENTS.md`. Um único comando de verificação completa local existe.

#### AIR-6.02 · Checagens direcionadas e rápidas
**Importante** (peso 2, origem `[A]`)  
é possível rodar lint, tipos e testes de um pacote/arquivo isolado em segundos; o agente não precisa rodar a suíte inteira a cada mudança. Tempos são medidos.

#### AIR-6.03 · Saída legível por máquina e por agente
**Menor** (peso 1, origem `[M]`)  
falhas de lint, teste e build exibem arquivo, linha, causa e correção esperada, sem ruído excessivo (modo silencioso/resumido disponível), economizando tokens na leitura de logs.

#### AIR-6.04 · Ambiente reproduzível de desenvolvimento
**Importante** (peso 2, origem `[A]`)  
dev container, Nix, Docker Compose ou equivalente sobe dependências (banco, cache, fila) com dados de exemplo versionados; nenhum passo manual não documentado é necessário.

#### AIR-6.05 · Reprodutibilidade e dependências
**Importante** (peso 2, origem `[A]`)  
versões de runtime, package manager, lockfiles, toolchains, containers e serviços locais estão fixadas ou possuem política de atualização. Builds são determinísticos, fixtures e seeds são versionados, migrations são reversíveis. Dependências e actions são pinadas, escaneadas e atualizadas por automação.

## AIR-7. Testes como especificação

**Como verificar:** Avalie a suíte de testes: tipos de teste presentes, espelhamento, factories/fixtures, determinismo (datas, rede), mutation testing, regra de "teste antes de corrigir" nas instruções.

#### AIR-7.01 · Cobertura de comportamento
**Importante** (peso 2, origem `[A]`)  
há testes unitários, integração, contrato, e2e e de propriedades para caminhos felizes, erros, autorização, concorrência, limites e regressões; regras de negócio críticas têm cobertura explícita. Testes podem ser executados por pacote/arquivo e apontam (nome/descrição) para a regra que protegem.

#### AIR-7.02 · Testes confiáveis
**Importante** (peso 2, origem `[A]`)  
testes são determinísticos (sem dependência de horário, rede externa, ordem de execução), rápidos e sem flakiness conhecida não tratada; um teste vermelho significa problema real — senão o agente aprende a ignorar falhas.

#### AIR-7.03 · Utilitários de teste
**Menor** (peso 1, origem `[M]`)  
factories/builders de dados, fixtures e helpers de autenticação por papel facilitam escrever testes corretos; existe exemplo de teste para cada camada.

#### AIR-7.04 · Qualidade dos testes medida
**Menor** (peso 1, origem `[R]`)  
além de cobertura, a efetividade dos testes é avaliada (ex.: mutation testing em módulos críticos), evitando testes gerados que passam sem verificar nada.

#### AIR-7.05 · Teste antes de corrigir
**Menor** (peso 1, origem `[M]`)  
o fluxo documentado para bugs é: reproduzir com teste que falha → corrigir → teste passa. As instruções do agente exigem isso.

## AIR-8. Guardrails de qualidade, segurança e performance

**Como verificar:** Leia o CI e as configs de lint: SAST, secret scanning, SCA, testes de arquitetura, budgets, regras específicas para erros típicos de agentes, política de dependências novas, áreas protegidas no CODEOWNERS.

#### AIR-8.01 · Invariantes codificados
**Crítico** (peso 3, origem `[B]`)  
formatter, linter, type checker, política de dependências, SAST, secret scanning, SCA, testes de segurança, budgets de performance e testes de arquitetura falham o CI quando invariantes são violadas. Mensagens de lint indicam a correção esperada. O princípio é codificar invariantes e permitir liberdade local.

#### AIR-8.02 · Regras para erros típicos de agentes
**Importante** (peso 2, origem `[A]`)  
há regras de lint/checagem para erros frequentes de código gerado no contexto do projeto: chamada de rede sem timeout (PERF-4.07), query sem paginação/limite, `SELECT *`, concatenação em SQL, log de objetos inteiros (vazamento de PII), uso de API obsoleta interna, dependências novas não aprovadas, desabilitação de verificação TLS, segredos no código, `eval`/`innerHTML`.

#### AIR-8.03 · Política de dependências novas
**Importante** (peso 2, origem `[A]`)  
adicionar dependência exige justificativa e passa por checagem automática (licença, manutenção, vulnerabilidades, tamanho de bundle, existência real do pacote — proteção contra pacotes “alucinados”/slopsquatting).

#### AIR-8.04 · Áreas protegidas
**Importante** (peso 2, origem `[A]`)  
mudanças em autenticação, autorização, criptografia, migrations destrutivas, CI/CD, IaC, arquivos de contexto de agentes e dependências exigem revisão humana de owner específico (CODEOWNERS) e checks adicionais.

#### AIR-8.05 · Gates de performance no PR
**Menor** (peso 1, origem `[M]`)  
tamanho de bundle, contagem de queries por endpoint, tempo de testes de benchmark e tamanho de imagem são comparados com a branch principal no PR (ver PERF-8.12), tornando regressões geradas por agentes visíveis.

## AIR-9. Economia de contexto e tokens

**Como verificar:** Verifique arquivos de ignore para agentes (`.cursorignore`, `.claudeignore`, `.aiexclude`, permissões em `.claude/settings.json`), tamanho somado dos arquivos de contexto, divisão de docs por domínio.

#### AIR-9.01 · Contexto progressivo
**Importante** (peso 2, origem `[A]`)  
o agente começa por poucas páginas (arquivo de contexto + índice) e segue referências conforme a tarefa; documentação longa é dividida e carregada sob demanda (skills, docs por domínio); não se injeta o repositório inteiro no prompt.

#### AIR-9.02 · Exclusão de ruído
**Importante** (peso 2, origem `[A]`)  
arquivos irrelevantes para raciocínio (lockfiles, builds, `dist/`, `node_modules`, vendorizados, minificados, fixtures e snapshots grandes, datasets, binários, logs) estão excluídos da indexação/leitura do agente via arquivos de ignore suportados pelas ferramentas.

#### AIR-9.03 · Monorepo navegável
**Menor** (peso 1, origem `[M]`) · Condicional — *Se: monorepo*  
o mapa de pacotes indica responsabilidade e dono de cada pacote; ferramentas de workspace permitem operar num pacote isolado; instruções por pacote evitam que o agente leia o repositório inteiro.

#### AIR-9.04 · Tamanho dos artefatos de contexto monitorado
**Menor** (peso 1, origem `[M]`)  
o tamanho somado dos arquivos de contexto sempre carregados é medido em CI com limite; crescimento exige revisão (mover para skill ou doc sob demanda).

#### AIR-9.05 · Respostas de ferramentas enxutas
**Menor** (peso 1, origem `[R]`)  
scripts e comandos usados pelo agente têm modo de saída resumida (ex.: apenas falhas, apenas diff), evitando despejar milhares de linhas no contexto.

## AIR-10. Segurança do uso de agentes no repositório

**Como verificar:** Verifique permissões configuradas para agentes (allowlist de comandos), bloqueio de leitura de `.env`, guardrails documentados (sem push em main, sem prod), revisão de plugins/MCP, rastreabilidade de commits gerados (trailer `Co-Authored-By`), política de uso de IA.

> Referência: OWASP Top 10 for Agentic Applications 2026 (aplicado ao próprio fluxo de desenvolvimento).

#### AIR-10.01 · Execução isolada e privilégio mínimo
**Crítico** (peso 3, origem `[B]`)  
agentes rodam em sandbox (container, VM ou ambiente remoto efêmero) ou em worktree/branch isolada, sem segredos de produção, sem credenciais pessoais amplas, com permissões explícitas de comandos (allowlist) e com acesso de rede restrito ao necessário (registries de pacotes, documentação).

#### AIR-10.02 · Ações que exigem humano
**Crítico** (peso 3, origem `[B]`)  
push para branch protegida, merge, deploy, execução de migrations em ambientes compartilhados, alteração de infraestrutura, publicação de pacotes e operações destrutivas exigem aprovação humana; o agente não tem credenciais para fazê-las sozinho.

#### AIR-10.03 · Injeção de instruções via conteúdo do repositório
**Importante** (peso 2, origem `[A]`)  
o fluxo assume que issues, comentários de PR, documentos, dependências, páginas web e saídas de ferramentas podem conter instruções maliciosas para o agente; agentes que processam conteúdo externo (ex.: triagem automática de issues públicas) rodam com permissões mínimas e sem acesso a segredos ou escrita em branches protegidas.

#### AIR-10.04 · Segredos fora do alcance
**Importante** (peso 2, origem `[A]`)  
`.env` e arquivos de credenciais locais estão bloqueados para leitura pelo agente (configuração de ignore/permissões); exemplos usam `.env.example` sem valores reais; secret scanning roda em todo commit gerado.

#### AIR-10.05 · Cadeia de suprimento de agentes
**Importante** (peso 2, origem `[A]`)  
extensões, plugins, skills e servidores MCP de terceiros são revisados antes do uso, pinados por versão e tratados como código não confiável.

#### AIR-10.06 · Rastreabilidade de mudanças geradas
**Menor** (peso 1, origem `[M]`)  
commits/PRs gerados ou coassinados por agentes são identificáveis (trailer, label ou autor), permitindo análise de qualidade e auditoria.

#### AIR-10.07 · Política de uso de IA no desenvolvimento
**Importante** (peso 2, origem `[A]`)  
está definido quais ferramentas e provedores são aprovados, que dados podem ser enviados a eles (código proprietário, dados pessoais de fixtures, logs de produção), retenção e uso para treinamento pelo provedor (preferência por contratos que vedam treinamento), alinhado a PRIV-14.05.

## AIR-11. Observabilidade e ambiente operáveis pelo agente

**Como verificar:** Verifique se a app sobe isolada por worktree (portas/bancos configuráveis), comandos de diagnóstico documentados e verificação de UI automatizada (e2e/browser).

#### AIR-11.01 · Ambiente isolado por tarefa
**Importante** (peso 2, origem `[A]`)  
a aplicação sobe em worktree/ambiente isolado (portas e bancos independentes), permitindo trabalho paralelo de agentes sem conflito.

#### AIR-11.02 · Diagnóstico por comando
**Menor** (peso 1, origem `[M]`)  
logs, métricas locais, traces, snapshots de DOM, screenshots e diagnósticos estão acessíveis por comandos documentados. O agente consegue reproduzir bug, observar causa, aplicar mudança e validar a métrica afetada.

#### AIR-11.03 · Verificação de UI
**Menor** (peso 1, origem `[R]`) · Condicional — *Se: frontend*  
existe forma automatizada de o agente abrir a aplicação, navegar e verificar resultado (testes e2e, browser automatizado, comparação visual), em vez de declarar “deve funcionar”.

## AIR-12. Planos, memória e decisões

**Como verificar:** Procure planos/specs versionados, ADRs, `tasks/lessons.md` ou equivalente e o fluxo de especificação antes do código.

#### AIR-12.01 · Planos versionados para tarefas complexas
**Menor** (peso 1, origem `[M]`)  
tarefas complexas têm plano com objetivo, não-objetivos, hipóteses, arquivos afetados, riscos, critérios de aceite e testes; planos são pequenos e atualizados durante a execução.

#### AIR-12.02 · Memória persistente fora do contexto efêmero
**Menor** (peso 1, origem `[M]`)  
decisões concluídas (ADRs), dívida técnica, incidentes e “armadilhas conhecidas” são registrados em arquivos indexados; o agente retoma trabalho sem repetir descoberta.

#### AIR-12.03 · Especificação antes do código
**Menor** (peso 1, origem `[M]`)  
features relevantes começam por especificação curta com critérios de aceite verificáveis (que viram testes), reduzindo ambiguidade para o agente.

## AIR-13. Workflow e revisão

**Como verificar:** Verifique templates de PR/issue, tamanho típico das PRs (`gh pr list`), revisão humana + automatizada documentada e checkpoints/rollback.

#### AIR-13.01 · Workflows agent-friendly
**Importante** (peso 2, origem `[A]`)  
template de PR exige intenção, escopo, risco, testes, impacto de performance/segurança/privacidade e evidência; PRs e commits são pequenos; CI publica artefatos e falhas de modo legível; ambientes efêmeros permitem preview por branch. O fluxo oferece checkpoints e rollback.

#### AIR-13.02 · Validação de resultado
**Crítico** (peso 3, origem `[B]`)  
antes de merge/deploy, agente e revisor humano verificam diff, dependências, migrations, autorização, dados sensíveis, performance, compatibilidade e observabilidade. Há testes negativos e revisão adversarial (inclusive revisão automatizada por segundo agente/ferramenta independente) para código gerado.

#### AIR-13.03 · Tamanho de mudança limitado
**Menor** (peso 1, origem `[M]`)  
há limite orientativo de tamanho de PR; mudanças grandes geradas por agente são divididas, pois revisão humana de diffs enormes é ineficaz.

## AIR-14. Medição e melhoria contínua

**Como verificar:** Procure métricas de efetividade de agentes, registro de melhorias sistêmicas após erros recorrentes e tarefas de referência para avaliação.

#### AIR-14.01 · Métricas de efetividade
**Importante** (peso 2, origem `[A]`)  
o time acompanha tempo para localizar contexto, taxa de aceitação/reversão de PRs gerados, defeitos e vulnerabilidades introduzidos, flakiness, custo de tokens por tarefa, duração do CI e retrabalho. O objetivo é reduzir incerteza e custo de contexto, mantendo qualidade, segurança, performance, privacidade e manutenção como critérios de saída.

#### AIR-14.02 · Ciclo de aprendizado
**Importante** (peso 2, origem `[A]`)  
cada erro recorrente de agente gera uma correção sistêmica: regra de lint, teste, tipo, skill ou ajuste de instrução — nesta ordem de preferência. Existe registro dessas melhorias.

#### AIR-14.03 · Avaliação de tarefas de referência
**Menor** (peso 1, origem `[R]`)  
um conjunto pequeno de tarefas representativas do repositório (ex.: “adicionar campo ao endpoint X com teste e migration”) é usado periodicamente para avaliar se mudanças em instruções, skills ou ferramentas melhoram ou pioram o resultado e o consumo de tokens.

## AIR-15. Complementos de documentação e higiene do repositório

**Como verificar:** Verifique diretamente os arquivos citados em cada item (`CONTRIBUTING.md`, `.env.example` × `process.env.*` no código, índice de scripts, catálogos de i18n, `.github/ISSUE_TEMPLATE`, `docs/assessments/`, estrutura de pastas).

> Itens incorporados a partir do assessment de AI-readiness do vitraux, não cobertos explicitamente pelas seções anteriores.

#### AIR-15.01 · CONTRIBUTING
**Menor** (peso 1, origem `[M]`)  
`CONTRIBUTING.md` (ou seção equivalente) descreve como instalar, configurar o ambiente, rodar testes e lint, nomear branches, escrever commits e abrir PR — para humanos e agentes.

#### AIR-15.02 · `.env.example` completo
**Importante** (peso 2, origem `[A]`)  
todas as variáveis de ambiente lidas pelo código (`process.env.*` ou equivalente) estão no `.env.example` com comentário de finalidade e valores fictícios; nenhuma variável usada falta no exemplo e nenhum valor real está versionado.

#### AIR-15.03 · Índice de scripts operacionais
**Menor** (peso 1, origem `[M]`)  
cada script do `package.json` (ou Makefile/equivalente) e cada script em `scripts/` está listado em um índice (`scripts/README.md` ou seção do README) com efeito, riscos e se é destrutivo/seguro em produção.

#### AIR-15.04 · Catálogos de texto centralizados
**Menor** (peso 1, origem `[M]`) · Condicional — *Se: o produto é multilíngue ou tem UI com textos*  
textos visíveis ao usuário ficam em catálogos centralizados e tipados (ex.: next-intl, i18next), com chaves presentes em todos os idiomas; não há strings de UI hardcoded em componentes.

#### AIR-15.05 · Templates de issue
**Menor** (peso 1, origem `[M]`)  
existem templates de issue (bug, feature) que exigem objetivo, critérios de aceite e escopo, e as issues recentes seguem esse formato em vez de one-liners.

#### AIR-15.06 · Assessments e relatórios com códigos estáveis
**Menor** (peso 1, origem `[M]`)  
assessments e relatórios (segurança, privacidade, performance, AI readiness) são versionados no repositório com IDs estáveis por item, permitindo que agentes citem e atualizem o status sem reescrever prosa.

#### AIR-15.07 · Separação app × operação × docs
**Menor** (peso 1, origem `[M]`)  
código de runtime da aplicação, scripts de operação/CLI e documentação ficam em diretórios separados e declarados; scripts de operador não são importados pelo código da aplicação.
