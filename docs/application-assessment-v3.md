# Checklist sênior para assessment de aplicações — versão 3 (enriquecida)

> **Propósito:** checklist preparatório para ser executado **antes** de um pentest, de uma auditoria de LGPD, de um teste de performance formal ou da adoção de agentes de IA no repositório. Ele não substitui essas atividades; reduz a probabilidade de achados óbvios e eleva o nível do que o avaliador externo consegue encontrar.
>
> **Modo de avaliação:** para cada item, registrar **status** (Atende / Parcial / Não atende / N/A), evidência reproduzível, componente afetado, cenário de exploração ou benchmark, impacto, severidade, owner, prazo, exceção aprovada e reteste. Não considerar “atende” com base apenas em documentação: exigir código/configuração, consulta, trace, métrica, teste, captura, log ou demonstração executável.
>
> **Rastreabilidade mínima:** cada achado deve apontar para requisito (ID deste checklist e, quando houver, ID do padrão externo — ASVS, artigo da LGPD etc.), arquivo/endpoint/serviço, ambiente, versão/commit, evidência, condição de reprodução, resultado esperado/observado, risco residual e vínculo com ticket. Cada teste deve preservar timestamp, dataset, carga, dispositivo, versão, ferramenta e limitações.

---

## 0. Como usar este checklist

### 0.1 Legenda dos itens

| Marca | Significado |
|---|---|
| `[B]` | **Bloqueante.** Falha neste item reprova o pilar, independentemente do percentual. Só pode ficar aberto com aceite formal de risco assinado, com prazo. |
| `[A]` | **Alto.** Falha provável de gerar achado alto/crítico em pentest, incidente de produção, sanção regulatória ou desperdício severo. |
| `[M]` | **Médio.** Boa prática de mercado consolidada; ausência gera achado médio ou degradação mensurável. |
| `[R]` | **Recomendado.** Maturidade avançada; diferencia aplicação “boa” de “excelente”. |
| 🆕 | Item novo nesta versão. |
| ✎ | Item da v2 reformulado, dividido, fundido ou movido (ver **Anexo A — Registro de mudanças**). |
| *(Se: …)* | Item condicional. Se a condição não se aplica, marcar N/A **com justificativa registrada** (ex.: “não há GraphQL — inventário de rotas anexado”). N/A sem evidência conta como “Não atende”. |

### 0.2 Níveis de evidência

| Nível | Tipo | Aceito para |
|---|---|---|
| E0 | Declaração verbal ou do time | Nunca suficiente para “Atende” |
| E1 | Documento, política, diagrama | Itens `[R]` de governança |
| E2 | Código, configuração, IaC, pipeline versionado | Itens `[M]` e `[R]` |
| E3 | Teste automatizado, medição, trace, query plan, scan com resultado | Mínimo para `[A]` e `[B]` |
| E4 | Demonstração adversarial ou reteste independente (outra pessoa/time, outra ferramenta) | Recomendado para `[B]` de Security e Privacy |

### 0.3 Cálculo do score

- Nota por item: Atende = 1; Parcial = 0,5; Não atende = 0; N/A justificado = excluído do denominador.
- Peso por criticidade: `[B]` = 5, `[A]` = 3, `[M]` = 2, `[R]` = 1.
- **Score do pilar** = Σ(peso × nota) ÷ Σ(peso dos itens aplicáveis).
- **Gate:** qualquer `[B]` em “Não atende” reprova o pilar. `[B]` em “Parcial” exige exceção formal com prazo.

| Faixa | Interpretação |
|---|---|
| ≥ 90% e nenhum `[B]` aberto | **Excelente** — pronto para pentest/auditoria; espera-se poucos achados, majoritariamente baixos/informativos. |
| 75–89% e nenhum `[B]` aberto | **Bom** — pentest deve encontrar achados médios pontuais. |
| 60–74% | **Regular** — corrigir altos antes de contratar pentest, para não pagar por achados triviais. |
| < 60% ou `[B]` aberto | **Insuficiente** — não está pronto para pentest/auditoria. |

### 0.4 Referências normativas fixadas (revisar a cada ciclo)

Registrar no relatório a versão efetivamente usada de cada referência. Versões consideradas nesta revisão (outubro de 2026):

- **Security:** OWASP ASVS **5.0.0** (maio/2025); OWASP Top 10:**2025**; OWASP API Security Top 10 (**2023**); OWASP MASVS v2 (se houver app mobile); OWASP Top 10 for LLM Applications (**2025**); OWASP Top 10 for Agentic Applications (**2026**); OWASP WSTG; NIST SP 800-63B-4 (autenticação); NIST SP 800-61r3 (resposta a incidentes); NIST SSDF (SP 800-218); SLSA v1.x; OpenSSF Scorecard; CIS Benchmarks; CVSS v4.0, EPSS e CISA KEV para priorização; PCI DSS v4.0.1 *(Se: processa cartão)*.
- **Privacy:** Lei 13.709/2018 (LGPD); Lei 15.352/2026 (ANPD como agência reguladora); Lei 15.211/2025 (ECA Digital, vigente desde 17/03/2026) e decretos regulamentadores; Lei 12.965/2014 (Marco Civil da Internet); Resoluções CD/ANPD nº 2/2022 (agentes de pequeno porte), 4/2023 (dosimetria), 15/2024 (incidentes), 18/2024 (encarregado), 19/2024 (transferência internacional), 30/2025 (mapa de temas prioritários 2026–2027), 31/2025 (agenda regulatória), 32/2026 (adequação da União Europeia); Enunciado CD/ANPD nº 1/2023 (crianças e adolescentes); guias orientativos da ANPD (cookies, legítimo interesse, segurança para agentes de pequeno porte, encarregado); normas setoriais aplicáveis (BACEN, ANS, CFM, CVM etc.).
- **Performance:** Core Web Vitals (LCP, INP, CLS) com limiares “bons” no p75 de dados de campo; RAIL/Long Animation Frames; OpenTelemetry semantic conventions; Google SRE (SLO/burn rate).
- **AI Readiness:** `AGENTS.md` (Agentic AI Foundation / Linux Foundation); Agent Skills (`SKILL.md`, agentskills.io); Model Context Protocol (MCP); OWASP Top 10 for Agentic Applications 2026 (para a segurança do próprio uso de agentes).

> **Nota sobre legislação pendente:** o PL 2338/2023 (marco legal de IA) **não está em vigor**; itens de IA em Privacy são exigidos com base na LGPD (art. 6º, 7º, 11, 20 e 46) e não no PL. Reavaliar quando houver sanção.

---
## Performance

> **Objetivo do pilar:** a aplicação responde rápido no p75/p95/p99 real (não só no laboratório), roda bem em dispositivos antigos e redes ruins, consome o mínimo de CPU/memória/disco/rede no servidor e no cliente, escala de forma previsível, degrada com controle e entrega software sem desperdício no pipeline.
>
> **Regra de ouro:** “rápido” só vale com número, percentil, população, ambiente e baseline. Médias isoladas, uma única execução e testes em máquina de desenvolvedor não são evidência.

### 1. Governança, orçamento e critérios de aceite

- [ ] **PERF-1.01 · SLOs por jornada** `[B]` — existem SLOs por jornada crítica, endpoint, operação assíncrona e dependência, com p50/p75/p95/p99, erro, throughput, disponibilidade, saturação e custo; médias não são usadas isoladamente. Cada SLO possui owner, janela, fonte de dados e ação quando violado.
- [ ] 🆕 **PERF-1.02 · Política de error budget** `[A]` — está definido o que acontece quando o error budget se esgota (congelamento de features, priorização de confiabilidade, revisão de release). A política é aplicada de fato: há registro de pelo menos uma decisão tomada com base nela ou de simulação.
- [ ] 🆕 **PERF-1.03 · Limiares de referência para web** `[A]` *(Se: há frontend web)* — metas no p75 de dados de campo, por rota e por classe de dispositivo: LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1, TTFB ≤ 0,8 s. Metas mais rígidas são definidas para jornadas de conversão. Desvios são aceitos apenas com justificativa e prazo.
- [ ] **PERF-1.04 · Orçamentos de performance** `[A]` — há budgets versionados para JavaScript/CSS/imagens/fontes, tamanho de payload, número de requests, TTFB, LCP, INP, CLS, cold start, queries por request, CPU, memória e duração de pipeline. CI falha ou exige aprovação quando o budget piora.
- [ ] 🆕 **PERF-1.05 · Orçamento de terceiros** `[M]` — scripts e SDKs de terceiros (analytics, chat, A/B, ads, pixels) têm budget próprio de bytes, tempo de main thread e requests, com owner de negócio. Novo terceiro só entra com medição antes/depois.
- [ ] **PERF-1.06 · Baseline reproduzível** `[A]` — o baseline registra commit, dataset, ambiente, região, hardware, navegador, rede, temperatura do cache, número de usuários e versão de dependências. Benchmarks usam repetição suficiente, percentis e margem de erro (intervalo de confiança), não uma execução isolada.
- [ ] 🆕 **PERF-1.07 · Dados de campo como fonte de verdade** `[A]` — decisões usam RUM (Real User Monitoring) e/ou dados de campo agregados, segmentados por dispositivo, navegador, rede, região e versão. Testes de laboratório (Lighthouse, WebPageTest, k6 etc.) servem para diagnóstico e regressão, não para declarar conformidade.
- [ ] **PERF-1.08 · Perfil de usuários e dispositivos** `[A]` — testes incluem dispositivos antigos (classe de entrada com 2–4 GB de RAM e CPU lenta, ou throttling de CPU 4–6× como proxy documentado), browsers suportados, telas pequenas, acessibilidade, baixa bateria/modo economia, rede 2G/3G/4G, alta latência, perda de pacotes e modo offline/intermitente quando aplicável. A matriz de suporte é publicada e coerente com o analytics real.
- [ ] ✎ **PERF-1.09 · Modelo de capacidade** `[A]` — existe modelo de capacidade que relaciona RPS, concorrência, tamanho de payload, latência e consumo de recursos. Estão documentados ponto de saturação, capacidade segura, degradação, headroom, custo marginal e comportamento durante autoscaling. O modelo é revisado a cada mudança relevante de arquitetura ou crescimento de tráfego.
- [ ] ✎ **PERF-1.10 · Engenharia de caos e injeção de falhas** `[M]` — injetam-se falhas controladas (latência artificial, perda de nó/zona, dependência lenta, disco cheio, DNS falhando) com hipótese, raio de impacto limitado, critério de abortar e registro de resultado. Experimentos rodam primeiro fora de produção e só em produção com guardrails aprovados.
- [ ] **PERF-1.11 · Performance como regressão** `[A]` — PRs e releases com impacto mensurável executam benchmark ou teste representativo e comparam contra baseline. Exceções são justificadas, têm prazo e não permitem acumular regressões silenciosas.
- [ ] 🆕 **PERF-1.12 · Custo unitário como requisito** `[M]` — existe métrica de custo por transação/usuário/tenant (infraestrutura, banco, CDN, terceiros, telemetria). Mudanças que aumentam o custo unitário acima de um limite exigem aprovação, assim como regressões de latência.

### 2. Observabilidade e rastreabilidade de performance

- [ ] **PERF-2.01 · Métricas RED e USE** `[B]` — cada serviço expõe Rate, Errors e Duration por rota/versão/status, além de Utilization, Saturation e Errors por CPU, memória, disco, rede, threads, conexões, filas e pools. Labels têm cardinalidade controlada e não incluem IDs arbitrários.
- [ ] 🆕 **PERF-2.02 · Padrão de instrumentação** `[M]` — instrumentação segue um padrão aberto (ex.: OpenTelemetry com semantic conventions) para nomes de métricas, spans e atributos, de modo que dashboards, alertas e consultas funcionem entre serviços sem tradução manual.
- [ ] **PERF-2.03 · Métricas de negócio** `[A]` — jornadas críticas possuem contadores de início, sucesso, falha, retry, abandono, timeout e degradação. É possível relacionar queda de conversão, aumento de abandono ou atraso operacional à mudança técnica correspondente sem coletar dados pessoais desnecessários.
- [ ] **PERF-2.04 · Logs estruturados** `[A]` — logs incluem timestamp sincronizado (NTP), ambiente, versão, região, serviço, operação, status, duração, tamanho, retry, dependência e `trace_id`, com níveis coerentes. Não há log em excesso, PII ou segredo; sampling e retenção são explicitamente definidos. Logging é assíncrono/bufferizado e não bloqueia o caminho crítico.
- [ ] **PERF-2.05 · Tracing distribuído** `[A]` — requisições atravessam browser, CDN, gateway, serviço, fila, worker, banco e terceiros com propagação de contexto (ex.: W3C Trace Context). Spans registram duração, status, eventos de retry/timeout e atributos seguros. Jobs assíncronos preservam vínculo (span links) entre requisição originadora e execução.
- [ ] **PERF-2.06 · Sampling e custo de telemetria** `[M]` — sampling head/tail, retenção, agregação e exportação são dimensionados; erros, p99 e transações lentas têm prioridade. A observabilidade não consome CPU, memória, disco ou banda suficientes para alterar o comportamento medido (overhead medido e documentado).
- [ ] **PERF-2.07 · Profiling contínuo e eBPF** `[M]` — CPU, heap, alocações, locks, I/O, GC, event loop, off-CPU e eBPF/profiling equivalente são acessíveis em produção com controles. Perfis são comparáveis por release e permitem atribuir custo a função, query, rota e dependência.
- [ ] **PERF-2.08 · Correlação ponta a ponta** `[A]` — dado um `trace_id`, o assessor encontra request, spans, logs, métricas (via exemplars), query, evento de fila, deploy e incidente relacionados. Não existem múltiplos IDs sem mapa de correlação nem componentes que quebrem o contexto.
- [ ] 🆕 **PERF-2.09 · RUM com atribuição** `[A]` *(Se: há frontend web)* — o RUM coleta LCP, INP, CLS, TTFB e tarefas longas com atribuição (elemento LCP, interação e script responsável pelo INP, frame longo via Long Animation Frames ou equivalente), segmentado por rota, versão e dispositivo, com consentimento quando exigido.
- [ ] 🆕 **PERF-2.10 · Monitoramento sintético** `[M]` — jornadas críticas são executadas periodicamente de múltiplas regiões, em dispositivo/rede emulados representativos, para detectar regressões antes do usuário e fora do horário de pico.
- [ ] **PERF-2.11 · Dashboards acionáveis** `[M]` — há dashboards por jornada, serviço, endpoint, dependência, região, versão e tenant quando permitido. Painéis mostram percentis, volume, erro, saturação, filas, cache hit ratio, pool, GC, cold start e custo; cada alerta tem runbook e owner.
- [ ] **PERF-2.12 · Alertas sem ruído** `[A]` — alertas usam SLO/burn rate multi-janela, saturação e sintomas de usuário; evitam limiares fixos sem contexto e duplicidade. Existe teste de alerta, rota de escalonamento, deduplicação, manutenção e revisão periódica de falsos positivos e falsos negativos.
- [ ] **PERF-2.13 · Rastreabilidade de mudanças** `[A]` — deploy, feature flag, configuração, migration, alteração de índice, dependência e mudança de infraestrutura aparecem como eventos anotados nas séries e traces. É possível comparar antes/depois e atribuir regressão a commit, release ou rollout.
- [ ] **PERF-2.14 · Dados de telemetria seguros** `[A]` — IDs, query text, headers e atributos são mascarados ou pseudonimizados; sampling não captura tokens, conteúdo de requisição ou dados sensíveis. Retenção, acesso, exportação e exclusão da telemetria são auditáveis. *(Ver também SEC-6.08 e PRIV-12.)*

### 3. Cliente, navegador e renderização

*(Se: há frontend web. Para apps mobile nativos, aplicar o equivalente: tempo de startup frio/quente, jank, frames congelados, ANR, tamanho do app, consumo de bateria e de dados.)*

- [ ] **PERF-3.01 · Caminho crítico de renderização** `[A]` — HTML, CSSOM, DOM, fontes e JavaScript críticos estão identificados; recursos não críticos não bloqueiam a primeira renderização. O waterfall não apresenta cadeias evitáveis de dependências, redirects, fontes bloqueantes ou scripts síncronos.
- [ ] 🆕 **PERF-3.02 · Estratégia de renderização** `[A]` — a escolha entre SSR, SSG, ISR, streaming SSR, islands/hidratação parcial ou CSR é justificada por rota. Não se envia uma SPA inteira para páginas majoritariamente estáticas; a hidratação não duplica trabalho já feito no servidor nem bloqueia a interação.
- [ ] 🆕 **PERF-3.03 · Dicas de recurso e priorização** `[M]` — `preconnect` apenas para origens críticas, `preload` para recursos críticos não descobríveis, `fetchpriority` no recurso LCP e rebaixado em recursos secundários, `103 Early Hints` quando suportado. Não há excesso de preload competindo por banda.
- [ ] **PERF-3.04 · LCP** `[A]` — o elemento LCP é identificado por rota e dispositivo; seu recurso é descobrível no HTML, priorizado, dimensionado, comprimido e servido próximo ao usuário. TTFB, atraso de carregamento do recurso, duração de download e atraso de renderização são medidos separadamente. O LCP não é imagem com lazy loading nem depende de JavaScript para aparecer.
- [ ] **PERF-3.05 · INP e tarefas longas** `[A]` — interações críticas são medidas no dispositivo real; tarefas acima de 50 ms, handlers pesados, hidratação, parsing e compilação são localizados e otimizados. O trabalho é particionado (ex.: `scheduler.yield`/yield ao event loop), cancelável, adiado ou movido para worker sem bloquear a thread principal. Feedback visual ocorre no próximo frame após a interação.
- [ ] **PERF-3.06 · CLS e estabilidade visual** `[A]` — dimensões de imagens, vídeos, anúncios, iframes e fontes são reservadas; componentes não inserem conteúdo acima do viewport sem ação do usuário; fontes não causam saltos (métricas de fallback ajustadas, ex.: `size-adjust`). Testes cobrem carregamento lento e conteúdo personalizado.
- [ ] **PERF-3.07 · JavaScript enviado** `[A]` — bundle inicial, chunks, dependências, polyfills, tags e código não utilizado são medidos por rota. Tree shaking, code splitting e carregamento sob demanda são eficazes; bibliotecas pesadas não são usadas quando APIs nativas resolvem o caso. O build é direcionado à matriz de browsers suportada (sem transpilar/polyfillar para browsers fora da matriz).
- [ ] 🆕 **PERF-3.08 · Scripts de terceiros** `[A]` — tags de terceiros carregam de forma assíncrona/adiada, atrás de consentimento quando aplicável, preferencialmente via facade (ex.: player de vídeo e chat carregados na interação) ou fora da main thread. Falha ou lentidão de terceiro não bloqueia render nem interação.
- [ ] **PERF-3.09 · DOM e layout** `[M]` — tamanho do DOM, estilo computado, layout, paint e compositing são medidos. Não há layout thrashing, seletores patológicos, re-renderização de árvore inteira, listeners duplicados ou animações em propriedades que forçam layout/paint excessivo; animações usam `transform`/`opacity` e respeitam `prefers-reduced-motion`. `content-visibility` é considerado para seções longas fora da tela.
- [ ] 🆕 **PERF-3.10 · Re-renderização e estado no cliente** `[M]` — o gerenciamento de estado não provoca re-render global a cada mudança; seletores, memoização e granularidade de componentes são verificados com profiler do framework. Não há fetch/efeito disparado em loop por dependências instáveis.
- [ ] **PERF-3.11 · Memória do cliente** `[A]` — heap snapshots e testes longos não mostram crescimento contínuo por navegação, modal, lista, rota, listener, timer, subscription ou cache. Imagens, blobs, workers e object URLs são liberados no ciclo de vida correto. Uso de memória é testado em dispositivo de baixa RAM.
- [ ] **PERF-3.12 · Listas e dados grandes** `[A]` — tabelas, feeds, árvores e selects usam paginação, virtualização, janela de renderização e busca incremental quando necessário. Ordenação/filtro não processa o dataset inteiro no cliente sem justificativa.
- [ ] **PERF-3.13 · Imagens e mídia** `[A]` — dimensões responsivas, `srcset`/`sizes`, formatos modernos de alta compressão (AVIF, WebP) com fallback, compressão, lazy loading (exceto acima da dobra) e prioridade estão corretos. Não há imagem maior que o viewport, thumbnail gerada no cliente sem necessidade, vídeo sem streaming adaptativo ou pré-carregamento de mídia não crítica. GIFs animados são substituídos por vídeo.
- [ ] **PERF-3.14 · Fontes e CSS** `[M]` — fontes são subsetadas, em WOFF2, com fallback, `font-display` adequado, preload apenas das críticas, e não bloqueiam a interface; CSS é dividido por rota, minificado e livre de regras mortas; CSS crítico é inline quando compensa. Não há framework de estilos inteiro enviado para poucas classes.
- [ ] **PERF-3.15 · Cache do browser e bfcache** `[A]` — assets imutáveis usam hash no nome e `Cache-Control: max-age` longo + `immutable`; HTML/API usam política coerente; navegações compatíveis usam bfcache (sem `unload`, sem `Cache-Control: no-store` desnecessário). Headers são verificados em rede real e invalidação não exige limpar cache manualmente.
- [ ] 🆕 **PERF-3.16 · Navegação antecipada** `[R]` — prefetch/prerender (ex.: Speculation Rules) é usado em navegações de alta probabilidade, com regras conservadoras, sem disparar efeitos colaterais (analytics, mutações) e com medição de taxa de acerto versus custo.
- [ ] 🆕 **PERF-3.17 · Service worker e offline** `[M]` *(Se: há service worker/PWA)* — estratégia de cache por tipo de recurso (cache-first para estáticos versionados, network-first/stale-while-revalidate para dados), tamanho limitado, versionamento e limpeza de caches antigos. O service worker não adiciona latência à navegação (navigation preload) nem serve versão quebrada após deploy.
- [ ] **PERF-3.18 · Compatibilidade progressiva** `[M]` — recursos de baixa capacidade possuem fallback; APIs são detectadas por feature detection; testes cobrem versões mínimas, Safari/Firefox/Chromium, zoom, teclado e preferências de movimento. Falha de terceiro não bloqueia a função primária.
- [ ] 🆕 **PERF-3.19 · Respeito a dispositivo e rede restritos** `[R]` — a aplicação reduz trabalho quando detecta economia de dados (`Save-Data`), rede lenta ou baixa memória: menos prefetch, mídia de menor qualidade, menos animação.

### 4. Rede, API e comunicação

- [ ] **PERF-4.01 · Waterfall e latência de rede** `[A]` — DNS, conexão, TLS, TTFB, download, fila do browser, redirects, CDN e terceiros são separados em métricas. O diagnóstico identifica se a latência é cliente, rede, gateway, aplicação, banco ou fornecedor.
- [ ] **PERF-4.02 · Quantidade de requisições** `[A]` — não há chamadas duplicadas, cascatas evitáveis, polling agressivo, refresh redundante ou requests para dados invisíveis. Deduplicação de requests concorrentes idênticos existe no cliente. Prefetch só ocorre quando a taxa de acerto justifica o custo e possui cancelamento.
- [ ] 🆕 **PERF-4.03 · Agregação de chamadas (BFF/batching)** `[M]` — telas que dependem de muitas chamadas usam BFF, endpoint agregado ou batching, evitando N round-trips do cliente, especialmente em redes móveis. O agregador paraleliza chamadas internas e tem timeout global.
- [ ] **PERF-4.04 · Payload e serialização** `[A]` — respostas são paginadas, filtráveis, selecionáveis por campo e comprimidas; JSON não carrega metadados ou coleções desnecessárias. Serialização/deserialização é perfilada e formatos binários/streaming são considerados para dados grandes. Existe limite máximo de payload por request e por response.
- [ ] ✎ **PERF-4.05 · HTTP e transporte** `[A]` — HTTP/2 e, quando suportado pela borda, HTTP/3 (QUIC); multiplexação, keep-alive e reuso de conexão entre serviços; TLS 1.3 com resumption; compressão Brotli (ou zstd onde suportado) para texto, gzip como fallback, sem comprimir formatos já comprimidos; `Cache-Control`, `ETag`/`If-None-Match`, range requests e CDN conforme o caso. Não há desabilitação global de compressão, conexões por request ou headers impedindo cache útil.
- [ ] ✎ **PERF-4.06 · Uso da borda (edge/CDN)** `[M]` *(Se: há CDN/edge)* — conteúdo estático, respostas públicas cacheáveis, redirects e roteamento simples são resolvidos na borda para reduzir TTFB e carga na origem. Validação de token na borda é aceita **apenas como filtro adicional**: a autorização definitiva continua na origem (ver SEC-3.05). Chave de cache na CDN é normalizada (query strings irrelevantes, cookies e `Vary`) e o hit ratio é monitorado.
- [ ] **PERF-4.07 · Timeouts por dependência** `[B]` — cada chamada possui timeout de conexão, leitura e total baseado em orçamento de latência. O deadline é propagado e menor que o timeout do chamador; operações expiradas são canceladas para não continuar consumindo recursos. Não existe chamada de rede sem timeout explícito (verificado por lint ou revisão de código).
- [ ] **PERF-4.08 · Retries seguros** `[A]` — retry tem limite, backoff exponencial com jitter, classificação de erros (retentável vs. não retentável), orçamento de retry por serviço e idempotência. Não há retry em cascata em todas as camadas, retry de operação não idempotente ou tempestade após recuperação de dependência. `Retry-After` é respeitado.
- [ ] **PERF-4.09 · Concorrência e backpressure** `[A]` — limites por cliente, rota e dependência impedem explosão de concorrência. Filas, semáforos, bulkheads e circuit breakers protegem recursos; o sistema rejeita (429/503 com `Retry-After`) ou enfileira trabalho de forma previsível quando saturado, priorizando tráfego crítico (load shedding por prioridade).
- [ ] **PERF-4.10 · Streaming e respostas parciais** `[M]` — downloads, exports, relatórios e eventos grandes usam streaming ou processamento incremental quando possível. O servidor não acumula o resultado inteiro em memória e o cliente trata cancelamento, reconexão e progresso. Exports grandes são assíncronos (job + notificação + link expirável).
- [ ] **PERF-4.11 · Terceiros** `[A]` — cada fornecedor possui orçamento de latência, timeout, quota, cache/fallback e métrica separada. Scripts, APIs, pagamentos, e-mail, mapas e analytics não bloqueiam jornadas não relacionadas; custo por chamada e impacto de falha são conhecidos.
- [ ] **PERF-4.12 · Contratos de API** `[M]` — contratos definem limites de tamanho, paginação, ordenação, campos, status, compressão, versionamento e compatibilidade. Mudanças não obrigam clientes lentos a baixar ou processar campos novos sem necessidade.
- [ ] 🆕 **PERF-4.13 · Custo de consulta em APIs flexíveis** `[A]` *(Se: GraphQL, OData ou filtros dinâmicos)* — consultas têm custo calculado (profundidade, complexidade, aliases, tamanho de listas) e limite por cliente; persisted queries/allowlist são usadas para clientes próprios; resolvers usam batching (DataLoader) para evitar N+1.
- [ ] 🆕 **PERF-4.14 · Tempo real eficiente** `[M]` *(Se: WebSocket, SSE, long polling)* — conexões têm heartbeat, limite por usuário, fan-out eficiente (pub/sub), mensagens compactas e reconexão com backoff; o servidor suporta o número alvo de conexões simultâneas com memória medida por conexão.
- [ ] 🆕 **PERF-4.15 · Webhooks e integrações de saída** `[M]` — envio de webhooks é assíncrono, com fila, retry com backoff, timeout curto, limite de concorrência por destino e desativação automática de destinos persistentemente falhos, para que um parceiro lento não degrade a plataforma.

### 5. Backend, runtime e concorrência

- [ ] **PERF-5.01 · Event loop/threads/workers** `[A]` — I/O não bloqueia thread principal; CPU-bound usa worker/processo apropriado; pool tem tamanho, fila e timeout. São medidos event-loop lag, thread starvation, context switch e tarefas em espera. Não há chamadas síncronas de arquivo, crypto ou parsing pesado no caminho do request.
- [ ] 🆕 **PERF-5.02 · Runtime ciente de container** `[A]` — o runtime respeita limites do container (ex.: heap da JVM proporcional ao limite, `GOMAXPROCS`/`GOMEMLIMIT` no Go, número de workers em Python/Node calculado sobre CPU alocada, não sobre CPU do host). Não há OOMKill ou throttling de CPU recorrente não explicado.
- [ ] **PERF-5.03 · Inicialização e cold start** `[A]` — startup mede carregamento de módulos, migrations, conexão, cache warming, configuração e health check. Não há trabalho de negócio ou conexão sequencial desnecessária antes de aceitar tráfego; readiness só ocorre quando dependências essenciais estão prontas; migrations não rodam no startup de cada réplica.
- [ ] **PERF-5.04 · Alocação e GC** `[M]` — heap, alocações temporárias, cópias, serialização, pausas de GC e fragmentação são medidos sob carga. Objetos de grande porte, caches sem limite, closures e buffers são investigados como causa de picos.
- [ ] 🆕 **PERF-5.05 · Caminho quente (hot path)** `[M]` — as funções mais custosas por CPU e alocação (segundo o profiler) são conhecidas e otimizadas: sem regex recompilada por request, sem serialização repetida, sem logging com interpolação cara em nível desativado, sem reflexão desnecessária.
- [ ] ✎ **PERF-5.06 · Pools e limites de recursos** `[A]` — pools de HTTP, Redis, workers, sockets, file descriptors e threads têm limites coerentes com a capacidade do downstream. O sistema mede espera, uso, rejeições, timeout e vazamento. *(Pool de banco tratado em PERF-6.37.)*
- [ ] **PERF-5.07 · Idempotência e duplicidade** `[A]` — retries, mensagens duplicadas, refresh, double submit e reprocessamentos não geram trabalho ou efeitos duplicados. Chaves de idempotência têm escopo, retenção e custo controlados.
- [ ] **PERF-5.08 · Processamento assíncrono** `[A]` — tarefas longas saem do request síncrono; filas têm tamanho, idade da mensagem mais antiga, throughput, concorrência, prioridade, retry, DLQ e consumidores monitorados. Não há fila infinita mascarando saturação; DLQ tem alerta e processo de reprocessamento.
- [ ] 🆕 **PERF-5.09 · Agrupamento de escritas e trabalho** `[M]` — escritas frequentes e pequenas (contadores, eventos, métricas, logs de auditoria) são agrupadas (batch, buffer, coalescência) quando a consistência permite, reduzindo round-trips e contenção.
- [ ] **PERF-5.10 · Serialização interna** `[M]` — objetos são convertidos e copiados apenas quando necessário; schemas são eficientes; payloads internos não carregam campos que nenhum consumidor utiliza. Compressão só é aplicada quando o custo de CPU compensa a economia de rede/disco.
- [ ] 🆕 **PERF-5.11 · Isolamento de vizinhos ruidosos** `[A]` *(Se: multi-tenant)* — um tenant não consegue degradar os demais: quotas, rate limits, filas e pools por tenant ou por classe de tenant; trabalho pesado de um cliente é isolado (fila própria, prioridade menor).
- [ ] **PERF-5.12 · Feature flags** `[M]` — flags não introduzem dois caminhos caros simultâneos, consultas duplicadas ou avaliação remota síncrona no caminho crítico (avaliação local com cache). Flags antigas são removidas com prazo e rollout permite comparação por coorte, versão e métrica.
- [ ] **PERF-5.13 · Graceful degradation** `[A]` — falha de cache, terceiro, região ou feature opcional não derruba a jornada essencial. Fallback tem custo, timeout, observabilidade e teste; não há fallback que faz full scan ou tempestade de requests.
- [ ] **PERF-5.14 · Shutdown e deploy** `[A]` — graceful shutdown drena conexões e filas, respeita deadline, evita perda/duplicação de mensagens e remove instâncias do balanceador antes de parar. Rolling/blue-green/canary não concentra cold starts nem reduz headroom abaixo do necessário.

### 6. Banco de dados e modelagem

#### 6.1 Modelagem

- [ ] **PERF-6.01 · Cardinalidade** `[A]` — cardinalidades 1:1, 1:N e N:N refletem o domínio e os padrões reais; estimativas de volume, crescimento, distribuição e skew estão documentadas. Consultas e índices são avaliados para baixa e alta cardinalidade, não apenas dataset pequeno.
- [ ] **PERF-6.02 · Distribuição e seletividade** `[A]` — colunas filtradas têm distribuição conhecida; histogramas/estatísticas capturam skew e valores populares; estatísticas estendidas (correlação entre colunas) existem onde o planner erra. O planner não escolhe plano ruim por estatísticas obsoletas, amostra insuficiente ou parâmetro que muda seletividade.
- [ ] **PERF-6.03 · Tipos de dados** `[M]` — tipos têm menor representação suficiente, precisão, timezone e semântica correta. Não há texto onde inteiro/enum/data apropriado reduziria armazenamento e custo, nem conversões implícitas que impedem índice.
- [ ] ✎ **PERF-6.04 · Chaves e identificadores** `[A]` — PK/FK são adequadas, compactas e indexadas conforme uso (FKs usadas em join/delete têm índice). A geração de IDs não cria hotspots nem fragmentação: IDs aleatórios (UUIDv4) em índices B-tree grandes são avaliados contra alternativas ordenáveis no tempo (UUIDv7, ULID, sequência) — considerando também a exposição de IDs previsíveis (SEC-3.02). Relações exigem integridade referencial sem cascatas destrutivas inesperadas.
- [ ] **PERF-6.05 · Normalização** `[M]` — repetição de dados, anomalias de atualização e inconsistências foram avaliadas. Normalização reduz escrita e inconsistência sem obrigar joins excessivos em jornadas críticas; decisões de desnormalização têm justificativa e mecanismo de sincronização.
- [ ] **PERF-6.06 · Desnormalização controlada** `[M]` — campos derivados, snapshots e documentos agregados possuem owner, evento de atualização, consistência aceitável, backfill, correção e estratégia para evitar dados obsoletos. Não há cópias sem contrato nem duplicação que aumenta custo de escrita sem ganho medido.
- [ ] 🆕 **PERF-6.07 · Linhas quentes e contenção de escrita** `[A]` — não há linha única atualizada por muitas transações concorrentes (contadores globais, saldo agregado, “última sequência”); usam-se contadores particionados, agregação assíncrona ou estruturas apropriadas.
- [ ] 🆕 **PERF-6.08 · Exclusão lógica e multi-tenant em índices** `[M]` — com soft delete, índices e constraints únicos consideram o filtro de ativos (ex.: índice parcial `WHERE deleted_at IS NULL`); em multi-tenant com tabela compartilhada, índices relevantes começam por `tenant_id` e consultas sempre o filtram.
- [ ] 🆕 **PERF-6.09 · Dados semiestruturados** `[M]` *(Se: JSON/JSONB/documentos)* — campos JSON consultados com frequência têm índice adequado (GIN, índice de expressão) ou são promovidos a colunas; documentos não crescem sem limite; atualização parcial não reescreve documentos enormes a cada mudança.
- [ ] **PERF-6.10 · Particionamento** `[M]` *(Se: tabelas grandes)* — tabelas grandes são particionadas apenas quando filtro, retenção, manutenção ou distribuição se beneficia. Pruning ocorre nos planos; não há excesso de partições, partição padrão crescendo sem controle ou migrations que bloqueiam toda a tabela.
- [ ] **PERF-6.11 · Sharding/distribuição** `[M]` *(Se: banco distribuído)* — chave de distribuição evita hotspots, joins cross-shard e scatter-gather desnecessário. Há medição de skew, rebalanceamento, consistência, transações distribuídas e impacto de consultas sem chave.

#### 6.2 Planos e índices

- [ ] **PERF-6.12 · EXPLAIN** `[B]` — toda consulta crítica possui plano revisado; `EXPLAIN ANALYZE` (com buffers) ou equivalente usa dados representativos e identifica custo, rows estimadas versus reais, loops, scan, join, sort, memória e I/O. O plano é armazenado por versão para comparação.
- [ ] 🆕 **PERF-6.13 · Inventário de consultas reais** `[A]` — estatísticas de consultas em produção (ex.: `pg_stat_statements`, Query Store, Performance Schema, slow query log, `auto_explain`) estão habilitadas; as top consultas por tempo total, chamadas, I/O e variância são revisadas periodicamente e após cada release.
- [ ] 🆕 **PERF-6.14 · Regressão de plano** `[A]` — mudança de plano de consultas críticas (após deploy, analyze, upgrade de versão ou crescimento de dados) é detectada e alertada; existe procedimento para estabilizar o plano corrigindo a causa.
- [ ] **PERF-6.15 · Estimativa versus realidade** `[A]` — divergências relevantes entre rows estimadas e reais são investigadas antes de tuning superficial. Estatísticas, correlação entre colunas, parâmetros, casts e distribuição são corrigidos; não se força hint sem explicar a causa.
- [ ] 🆕 **PERF-6.16 · Prepared statements e cache de plano** `[M]` — consultas usam prepared statements/parametrização; problemas de plano genérico versus plano específico (parameter sniffing) são conhecidos e tratados; o modo do pooler é compatível com prepared statements.
- [ ] ✎ **PERF-6.17 · Índices de filtro** `[B]` — predicados frequentes e seletivos possuem índices adequados, considerando ordem de colunas, igualdade/range, collation, NULL e operador.
- [ ] **PERF-6.18 · Índices compostos** `[A]` — ordem de colunas segue padrões de filtro/ordenação/join; índices redundantes, prefixos cobertos e combinações impossíveis são removidos. Custo de escrita, tamanho, cache e manutenção são medidos.
- [ ] **PERF-6.19 · Índices parciais/funcionais/especializados** `[M]` — índices parciais, funcionais, covering (`INCLUDE`), BRIN (séries temporais), GIN/GiST ou especializados são usados quando o predicado e o padrão justificam. Expressões da consulta coincidem com o índice; não há função/cast no campo que invalide o uso.
- [ ] **PERF-6.20 · Índices sem uso** `[M]` — índices nunca ou raramente usados são identificados, considerando sazonalidade e réplicas; índices excessivos não consomem memória, disco e tempo de escrita sem benefício. Remoção ocorre com observação (ex.: tornar invisível antes de remover, onde suportado) e rollback.
- [ ] **PERF-6.21 · Full scan** `[A]` — cada sequential/full scan em tabela grande é classificado como intencional ou defeito. Filtros ausentes, índice inadequado, baixa seletividade, estatística, cast e consulta dinâmica são verificados; scans inevitáveis usam janela, particionamento ou processamento controlado.

#### 6.3 Forma das consultas

- [ ] **PERF-6.22 · N+1 e overfetching** `[B]` — traces e logs de query detectam padrão N+1 por endpoint e tamanho de coleção (idealmente com teste automatizado que falha se o número de queries por request crescer com N). A correção usa join, batch, eager loading seletivo, DataLoader ou consulta agregada sem transformar o problema em overfetch. O lazy loading padrão do ORM é conhecido e controlado.
- [ ] **PERF-6.23 · Joins desnecessários** `[M]` — joins que não filtram, projetam ou garantem existência são removidos. O assessor verifica ORM que adiciona relações automaticamente, joins repetidos e tabelas incluídas apenas por conveniência.
- [ ] **PERF-6.24 · Joins redundantes** `[M]` — o mesmo relacionamento não é acessado em consultas separadas ou subqueries equivalentes. CTEs, views e ORM não materializam/reexecutam trabalho sem necessidade; plano confirma eliminação ou compartilhamento eficaz.
- [ ] **PERF-6.25 · Joins cartesianos** `[A]` — joins sem predicado, predicado incompleto ou multiplicação de linhas são testados com cardinalidades altas. O resultado não depende de `DISTINCT` para esconder duplicação; a causa é corrigida e o custo medido.
- [ ] **PERF-6.26 · Join order e algoritmo** `[M]` — nested loop, hash join, merge join e ordem escolhida são adequados ao volume e seletividade. Memória de hash/sort evita spill para disco; `work_mem` ou equivalente é dimensionado sem causar OOM sob concorrência.
- [ ] **PERF-6.27 · Ordenações** `[M]` — `ORDER BY` só ocorre quando exigido; ordem padrão não é aplicada automaticamente. Índice fornece ordem quando compensa; sort de grandes conjuntos tem limite, paginação por cursor/keyset e memória controlada.
- [ ] **PERF-6.28 · Paginação** `[A]` — offsets profundos não percorrem milhões de linhas sem justificativa. Keyset/cursor, índice compatível, limite máximo e ordenação determinística (desempate por chave única) são usados; paginação não permite resposta ilimitada. `COUNT(*)` exato em tabelas grandes é evitado quando estimativa ou “há mais páginas” resolve.
- [ ] **PERF-6.29 · Agregações** `[M]` — contagens, somas, agrupamentos e distinct são analisados quanto a scan, memória, spill e repetição. Pré-agregação, materialized view (com estratégia de refresh), cache ou janela temporal são usados quando o padrão justifica.
- [ ] **PERF-6.30 · Subqueries e CTEs** `[M]` — subqueries correlacionadas, CTEs materializadas e views aninhadas são examinadas por reexecução e barreiras de otimização. A forma declarativa é comparada com join/window/batch usando plano real.
- [ ] **PERF-6.31 · SELECT e projeção** `[A]` — a consulta retorna apenas colunas necessárias; blobs, JSON grande, texto e colunas sensíveis não são carregados por padrão. A camada de persistência oferece projeção explícita, não entidade completa em toda chamada. Não há `SELECT *` em código de produção.
- [ ] **PERF-6.32 · Filtros e sargabilidade** `[A]` — predicados permitem uso de índice; funções, casts, `LIKE '%…'`, expressões e comparação de tipos diferentes não forçam scan. Alternativas por coluna normalizada, índice funcional ou busca especializada são avaliadas.
- [ ] 🆕 **PERF-6.33 · Operações em massa** `[M]` — cargas e atualizações em volume usam bulk insert/`COPY`/batch com tamanho de lote controlado, em vez de uma operação por linha; deletes/updates massivos são fatiados para não gerar locks longos, replicação atrasada ou bloat.

#### 6.4 Concorrência, transações e conexões

- [ ] ✎ **PERF-6.34 · Locks e deadlocks** `[A]` — locks adquiridos, duração, espera, deadlocks e contenção são observados. Há detecção de deadlocks, ordem consistente de aquisição de locks e retry seguro para transações abortadas por concorrência/serialização.
- [ ] 🆕 **PERF-6.35 · Timeouts no banco** `[A]` — existem timeouts de statement, lock e transação ociosa (ex.: `statement_timeout`, `lock_timeout`, `idle_in_transaction_session_timeout`) por papel de conexão; transações longas são alertadas, pois bloqueiam vacuum/compaction e seguram locks.
- [ ] **PERF-6.36 · Transações** `[A]` — escopo transacional contém apenas operações necessárias; chamadas de rede, espera de usuário e processamento caro ficam fora. Isolamento é compatível com o caso; não se usa serializable/global lock por padrão.
- [ ] **PERF-6.37 · Pool de conexões do banco** `[B]` — tamanho considera número de réplicas, workers e capacidade do banco (conexões totais = réplicas × pool ≤ limite seguro do banco); espera e saturação são alertadas; pooler externo (ex.: PgBouncer, proxy gerenciado) é usado quando o número de instâncias é elástico. Não há pool por request, conexão vazando, transação devolvida ao pool aberta ou multiplexação incompatível.
- [ ] **PERF-6.38 · Replicação e leitura** `[M]` *(Se: há réplicas)* — réplicas têm lag, capacidade e consistência monitorados. Leituras tolerantes a atraso são roteadas; leituras após escrita e decisões críticas usam garantia adequada. Failover não duplica escrita nem causa avalanche para o primário.
- [ ] **PERF-6.39 · Cache de banco** `[M]` — cache de query/objeto/result set possui chave, TTL, invalidação, tamanho, stampede protection e métrica de hit/miss. Cache não mantém dados incorretos após escrita nem mascara degradação do banco.

#### 6.5 Operação e ciclo de vida

- [ ] **PERF-6.40 · Retenção e arquivamento** `[A]` — dados históricos são arquivados/particionados de forma que tabelas quentes permaneçam pequenas. Jobs de retenção são incrementais, limitados, observáveis e não bloqueiam o OLTP. *(Alinhar com PRIV-11.)*
- [ ] **PERF-6.41 · Migrations** `[B]` — migrations têm plano de lock, tempo estimado em volume de produção, compatibilidade expand/contract, backfill incremental, criação de índice online quando possível, `lock_timeout` curto, rollback/forward fix e impacto medido. Deploy não exige downtime inesperado nem faz alteração destrutiva antes de todos os consumidores migrarem. Migrations são testadas em cópia com volume realista.
- [ ] **PERF-6.42 · Disco e manutenção** `[A]` — vacuum/compaction/analyze/reindex/checkpoint/autovacuum equivalentes são monitorados e ajustados por tabela quando necessário. Bloat, fragmentação, WAL/redo, risco de wraparound de IDs de transação, I/O e espaço livre têm alertas e capacidade; manutenção não coincide com picos sem planejamento.
- [ ] **PERF-6.43 · Carga do banco por endpoint** `[A]` — observabilidade relaciona duração, rows, bytes, queries, locks e cache hit a rota, usuário técnico, release e trace (ex.: comentários SQL com `trace_id`/rota). É possível responder “qual endpoint gerou este pico?” sem inferência manual.
- [ ] 🆕 **PERF-6.44 · Separação OLTP/OLAP** `[M]` — relatórios pesados, analytics e exports não rodam no primário transacional; usam réplica dedicada, data warehouse, CDC ou store analítico, com latência de dados acordada.
- [ ] **PERF-6.45 · Busca especializada** `[M]` — full-text, fuzzy, geoespacial, vetor ou analytics não são forçados no OLTP quando motor especializado reduz custo. Sincronização, consistência, reindexação, custo e fallback são explicitamente avaliados.
- [ ] 🆕 **PERF-6.46 · Upgrade e versão do motor** `[R]` — a versão do banco é suportada e recente o suficiente para não perder otimizações relevantes; upgrades são testados com comparação de planos antes/depois.

### 7. Cache, armazenamento e recursos

- [ ] **PERF-7.01 · Estratégia de cache por camada** `[A]` — browser, CDN, gateway, aplicação, objeto e banco têm propósito, TTL, chave, invalidação e fallback documentados; não há cache duplicado sem ganho medido.
- [ ] **PERF-7.02 · Cache stampede e stale-while-revalidate** `[A]` — expiração simultânea, thundering herd, cache penetration e avalanche são testados. Há jitter no TTL, single-flight/request coalescing, stale-while-revalidate/stale-if-error, negative cache ou pré-aquecimento conforme o caso.
- [ ] **PERF-7.03 · Consistência** `[A]` — stale data, escrita concorrente, invalidação fora de ordem e falha parcial têm comportamento definido. Cache não autoriza, não expõe tenant errado e não serve dado sensível fora do escopo (`Vary` e chave incluem identidade/tenant quando a resposta é personalizada). *(Ver SEC-5.16.)*
- [ ] 🆕 **PERF-7.04 · Saúde do cache distribuído** `[M]` *(Se: Redis/Memcached ou similar)* — memória, política de eviction, chaves grandes (big keys), chaves quentes (hot keys), latência de comandos e operações bloqueantes (ex.: varreduras completas de chaves) são monitoradas; comandos O(N) sobre conjuntos grandes são evitados.
- [ ] **PERF-7.05 · Disco e arquivos temporários** `[M]` — uploads, exports, logs, dumps, thumbnails e temporários têm quota, streaming, cleanup, retenção e alerta de espaço. Processamento não lê arquivo inteiro em memória sem necessidade.
- [ ] **PERF-7.06 · Object storage/CDN** `[M]` — objetos têm tamanho, multipart, compressão, cache e lifecycle (tiering para classes frias) adequados; URLs assinadas expiram; upload/download vai direto ao storage (pre-signed) sem passar desnecessariamente pelo servidor de aplicação.
- [ ] **PERF-7.07 · Limites de recursos** `[A]` — CPU, memória, disco, sockets, threads, conexões, filas, payload e tempo possuem limites testados. O serviço falha de forma controlada e não cresce sem limite até travar o host.
- [ ] **PERF-7.08 · Container e runtime** `[M]` — imagem final é mínima, camadas/cache são eficientes, requests e limits refletem perfil real medido, health/readiness não executam trabalho pesado e shutdown é gracioso. O container não usa swap/CPU sem observabilidade.
- [ ] **PERF-7.09 · Autoscaling** `[A]` — escalonamento usa sinais de demanda e saturação (não apenas CPU), possui cooldown, máximo, mínimo e headroom. Métrica não reage tarde nem cria loop de scale-up/scale-down; warm-up e distribuição de carga são testados; o banco e dependências suportam o máximo de réplicas configurado.

### 8. Build, CI/CD e entrega

- [ ] **PERF-8.01 · Cache de dependências** `[M]` — package managers e imagens usam cache seguro, invalidado por lockfile e versão; instalação é determinística (`--frozen-lockfile`/`ci`); cache não mistura branches incompatíveis nem oculta instalação incompleta.
- [ ] 🆕 **PERF-8.02 · Cache de build/teste remoto** `[R]` — ferramentas de build incremental com cache remoto e hashing de entradas (ex.: Bazel, Nx, Turborepo, Gradle build cache) evitam recompilar e retestar o que não mudou; o cache é protegido contra envenenamento (escrita apenas por pipelines confiáveis).
- [ ] **PERF-8.03 · Paralelismo** `[M]` — lint, unit, integration, build, scan e packaging independentes rodam em paralelo; dependências entre jobs são mínimas e explícitas; suítes longas usam sharding. O pipeline não espera por etapa que poderia iniciar antes.
- [ ] 🆕 **PERF-8.04 · Execução apenas do necessário** `[M]` — filtros por caminho evitam rodar jobs irrelevantes (ex.: mudança só de docs não roda e2e); execuções superadas por novo push no mesmo branch são canceladas automaticamente; merge queue evita revalidar o mesmo conteúdo várias vezes.
- [ ] **PERF-8.05 · Seleção incremental de testes** `[M]` — testes por pacote/módulo/mudança são usados com uma suíte completa periódica. Grafo de dependências é correto; nenhum teste crítico é omitido por seleção excessiva.
- [ ] **PERF-8.06 · Artefatos** `[A]` — build ocorre uma vez por commit e o mesmo artefato é promovido entre ambientes; não há rebuild divergente em staging/produção. Artefatos têm checksum, metadata e duração de retenção.
- [ ] **PERF-8.07 · Docker build** `[M]` — contexto é pequeno (`.dockerignore`); ordem preserva cache; multi-stage separa build/test/runtime; base e dependências são mínimas; cache mounts para gerenciadores de pacote; imagem final contém apenas runtime e artefatos necessários.
- [ ] **PERF-8.08 · Reprodutibilidade** `[M]` — versão de runtime, OS, compiler, package manager, timezone e flags são fixadas; dois builds equivalentes produzem resultado equivalente. Diferenças de ambiente são detectadas antes do deploy.
- [ ] **PERF-8.09 · Tempo de pipeline** `[M]` — cada etapa tem duração, variância, cache hit, custo e owner. Jobs redundantes, downloads repetidos, ambientes recriados e testes flaky são eliminados ou isolados. Há meta explícita de tempo do PR até feedback (ex.: checks obrigatórios < 10–15 min).
- [ ] 🆕 **PERF-8.10 · Testes instáveis (flaky)** `[A]` — testes flaky são detectados automaticamente (retries registrados, taxa de falha intermitente), colocados em quarentena com owner e prazo, e não são “resolvidos” por retry silencioso que esconde problema real.
- [ ] 🆕 **PERF-8.11 · Ambientes efêmeros com custo controlado** `[R]` — ambientes de preview por branch têm TTL, tamanho mínimo, dados sintéticos e destruição automática.
- [ ] **PERF-8.12 · Gates de performance** `[A]` — CI mede tamanho de bundle, query count, benchmark, tamanho de imagem, startup, latência e consumo conforme o componente; regressão exige aprovação explícita com justificativa.

### 9. Carga, resiliência e diagnóstico

- [ ] **PERF-9.01 · Load test realista** `[B]` — workload usa distribuição de endpoints, think time, payloads, autenticação, cache frio/quente, tenants e dados representativos (volume próximo ao de produção, não base vazia). Resultado inclui p95/p99, erro, throughput, recursos e saturação por componente. O gerador de carga não é o gargalo (verificado).
- [ ] **PERF-9.02 · Stress e breakpoint** `[A]` — carga cresce até degradação; identifica fila, timeout, OOM, lock, pool e cascata. O sistema mantém respostas controladas e recupera sem intervenção destrutiva.
- [ ] **PERF-9.03 · Soak e vazamento** `[A]` — teste prolongado (horas) detecta crescimento de heap, handles, conexões, filas, logs, disco, cache e latência. A variação é comparada ao volume processado e ao ciclo de deploy.
- [ ] **PERF-9.04 · Picos e autoscaling** `[A]` — bursts, cold start, scale-out, scale-in, rebalanceamento e perda de instância são testados. Não há perda de trabalho, duplicação, avalanche de conexões ou queda de SLO durante o ajuste.
- [ ] **PERF-9.05 · Falhas de dependência** `[A]` — timeout, erro 5xx, resposta lenta, payload inválido, rate limit, DNS, indisponibilidade regional e resposta parcial têm teste. Fallback não piora o incidente nem produz dados incorretos.
- [ ] 🆕 **PERF-9.06 · Performance em failover e DR** `[A]` — failover de banco, troca de região e restauração de backup são medidos sob carga; o tempo real atinge o RTO e a capacidade do ambiente de destino suporta o tráfego. *(Ver SEC-8.06.)*
- [ ] **PERF-9.07 · Diagnóstico de regressão** `[A]` — existe procedimento para comparar traces, perfis, planos de query, métricas, logs, deploys e flags entre janela boa e ruim. O time consegue chegar a causa provável sem depender de reprodução perfeita.
- [ ] **PERF-9.08 · Runbooks** `[A]` — cada alerta de performance tem impacto, hipóteses, queries/dashboards, comandos seguros, mitigação reversível, critérios de escalonamento e ação pós-incidente. Runbooks são testados em exercício (game day).
- [ ] 🆕 **PERF-9.09 · Postmortem de performance** `[M]` — incidentes de latência/capacidade geram postmortem sem culpa, com causa raiz, teste de regressão e atualização de budget/SLO/capacidade.

### 10. 🆕 Eficiência de recursos e custo (FinOps)

- [ ] 🆕 **PERF-10.01 · Right-sizing** `[M]` — requests/limits, tamanhos de instância, banco e cache são ajustados com base em uso medido (p95 de utilização), revisados periodicamente; não há recursos ociosos ou superdimensionados sem justificativa.
- [ ] 🆕 **PERF-10.02 · Recursos órfãos** `[M]` — volumes, snapshots, IPs, balanceadores, ambientes, buckets e filas sem uso são detectados automaticamente e removidos com processo.
- [ ] 🆕 **PERF-10.03 · Tráfego de saída e entre zonas** `[M]` — custo de egress, tráfego entre zonas/regiões e NAT é conhecido; comunicação intensa entre serviços evita cruzar zonas sem necessidade; respostas grandes usam CDN.
- [ ] 🆕 **PERF-10.04 · Volume de telemetria** `[M]` — volume e custo de logs, métricas e traces são acompanhados por serviço; logs de debug não ficam ligados em produção; métricas de alta cardinalidade são controladas.
- [ ] 🆕 **PERF-10.05 · Armazenamento por camadas** `[R]` — dados frios migram para classes de armazenamento mais baratas; backups e logs antigos seguem lifecycle; compressão é usada onde compensa.
- [ ] 🆕 **PERF-10.06 · Capacidade elástica e barata para batch** `[R]` — workloads tolerantes a interrupção (batch, CI, processamento assíncrono) avaliam instâncias preemptíveis/spot e arquiteturas de CPU com melhor custo-desempenho, com teste de compatibilidade.

### 11. 🆕 Workloads com IA/LLM *(Se: a aplicação chama modelos de IA)*

- [ ] 🆕 **PERF-11.01 · Latência percebida** `[A]` — tempo até o primeiro token (TTFT), tokens por segundo e latência total são medidos por caso de uso; respostas longas usam streaming para o usuário; há indicador de progresso e possibilidade de cancelar (que interrompe a geração e o custo).
- [ ] ✎ **PERF-11.02 · Timeouts, limites e fallback de IA** `[A]` — chamadas a modelos têm timeout, `max_tokens`, orçamento de contexto, retry com backoff para 429/5xx e circuit breaker. Se a IA demorar, falhar, exceder limites ou devolver saída fora do schema, a aplicação degrada graciosamente para fluxo tradicional/heurístico sem interromper a jornada. *(Movido de AI Readiness; ver também SEC-10.)*
- [ ] 🆕 **PERF-11.03 · Economia de tokens em produção** `[A]` — prompts têm tamanho controlado e versionado; prefixos estáveis aproveitam prompt caching do provedor; contexto recuperado (RAG) é limitado ao necessário; histórico de conversa é resumido/truncado; o modelo é escolhido por tarefa (modelos menores para tarefas simples, roteamento por complexidade).
- [ ] 🆕 **PERF-11.04 · Cache de respostas e embeddings** `[M]` — embeddings não são recalculados para conteúdo inalterado (hash de conteúdo); respostas determinísticas ou frequentes são cacheadas quando seguro, respeitando escopo de usuário/tenant e dados pessoais.
- [ ] 🆕 **PERF-11.05 · Busca vetorial** `[M]` *(Se: RAG/busca semântica)* — índice vetorial (ex.: HNSW/IVF) tem parâmetros ajustados com medição de recall versus latência; filtros por tenant/permissão são aplicados no índice e não depois de recuperar top-k (o que degrada recall e pode vazar dados); reindexação é incremental.
- [ ] 🆕 **PERF-11.06 · Custo por requisição de IA** `[A]` — tokens de entrada/saída e custo são registrados por funcionalidade, usuário/tenant e versão de prompt; há limite de gasto e alerta de anomalia; quotas por usuário impedem consumo abusivo.
- [ ] ✎ **PERF-11.07 · Dados da aplicação preparados para RAG** `[M]` *(Se: RAG/busca semântica sobre dados da aplicação)* — o conteúdo indexado tem esquema semântico claro, texto limpo (sem ruído de HTML, navegação ou markup), chunking adequado ao tipo de documento, metadados de origem/data/permissão e deduplicação; a qualidade da recuperação é medida com um conjunto de perguntas de referência. *(Movido de AI Readiness: trata dos dados da aplicação, não do repositório.)*

---
## Security — checklist preparatório para pentest whitebox

> **Objetivo do pilar:** ao atingir score alto aqui, a aplicação deve resistir às técnicas conhecidas de ataque (OWASP Top 10:2025, OWASP API Security Top 10, categorias da ASVS 5.0), expor o mínimo de informação útil a um atacante e, onde a exposição é inevitável, ter impacto **contido, localizado, detectável e recuperável** — incluindo um plano de Disaster Recovery explícito e testado.
>
> **Regra de ouro:** todo controle é verificado **server-side** e **por teste negativo** (o atacante tentando e falhando), não pela existência do código. “Esconder botão”, “não está documentado” e “ninguém sabe a URL” não são controles.

### 1. Escopo, arquitetura e ameaça

- [ ] **SEC-1.01 · Inventário de ativos** `[B]` — listar aplicações, APIs, frontends, mobile, workers, cron, consumers, funções serverless, gateways, bancos, caches, filas, buckets, registries, CI/CD, domínios, subdomínios, certificados, ambientes e versões; comparar o inventário declarado com descoberta ativa (DNS, Certificate Transparency, varredura de portas, rotas reais do gateway). Ativos sem owner são achado.
- [ ] **SEC-1.02 · Mapa de fluxos** `[A]` — documentar entradas, saídas, trust boundaries, identidades, dados, protocolos, terceiros, privilégios e fluxos administrativos. Cada fluxo possui owner, autenticação, autorização, logging e risco. O diagrama é atualizado a cada mudança arquitetural e versionado com o código.
- [ ] **SEC-1.03 · Threat model** `[A]` — STRIDE/abuse cases ou método equivalente cobre spoofing, tampering, repudiation, disclosure, denial of service e elevation of privilege, além de abuso de lógica de negócio; ameaças são ligadas a controles, testes e achados. O modelo é revisado em toda feature de risco (pagamento, auth, upload, integrações, IA).
- [ ] ✎ **SEC-1.04 · Padrão e nível de rigor** `[A]` — fixar **OWASP ASVS 5.0.0** e o nível aplicável (L1/L2/L3) por componente; registrar as **decisões de segurança documentadas** que a ASVS 5.0 exige para requisitos configuráveis; mapear requisitos a componentes e excluir apenas itens com justificativa. Complementar com OWASP Top 10:2025, API Security Top 10, MASVS (mobile), LLM/Agentic Top 10 (IA), supply chain e regras de negócio.
- [ ] 🆕 **SEC-1.05 · Requisitos de segurança no ciclo de desenvolvimento** `[M]` — histórias de risco têm critérios de aceite de segurança e casos de abuso; existe definição de pronto com checagens de segurança; práticas seguem um framework de desenvolvimento seguro (ex.: NIST SSDF / OWASP SAMM) com maturidade medida.
- [ ] **SEC-1.06 · Ambiente do teste** `[A]` — produção não é usada sem autorização; dados são sintéticos/mascarados; contas de teste cobrem papéis, tenants, estados e privilégios; origem, janela, limites e regras de engajamento estão documentados. O ambiente de teste é equivalente a produção em configuração de segurança (mesmos headers, WAF, IAM, versões).
- [ ] **SEC-1.07 · Modelo de impacto** `[A]` — classificar confidencialidade, integridade, disponibilidade, privacidade, fraude, impacto financeiro, lateral movement e blast radius. A severidade considera explorabilidade e impacto combinado (encadeamento de achados).
- [ ] 🆕 **SEC-1.08 · Classificação de dados** `[A]` — dados são classificados (público, interno, confidencial, pessoal, pessoal sensível, credencial, financeiro) e a classificação está anotada no schema/modelos de dados, orientando criptografia, logging, retenção e acesso.

### 2. Identidade, autenticação e sessão

- [ ] **SEC-2.01 · Registro de contas** `[A]` — e-mail/telefone/username não permitem enumeração por resposta, tempo, código, redirect ou recuperação; duplicidade, normalização (Unicode, maiúsculas, pontos/`+` em e-mail, homógrafos) e takeover de conta pré-existente são tratados. Registro automatizado em massa é limitado (rate limit, verificação de contato, desafio adaptativo).
- [ ] ✎ **SEC-2.02 · Senha** `[B]` — senha é recebida apenas por TLS, nunca logada, armazenada com hash adaptativo moderno e salt único (Argon2id, scrypt, bcrypt ou PBKDF2 com parâmetros atuais), com parâmetros revisados periodicamente; comprimento mínimo conforme NIST SP 800-63B-4 (15 caracteres quando a senha é fator único; 8 quando faz parte de MFA), máximo de pelo menos 64, aceita espaços e Unicode; checagem contra senhas vazadas/comuns; **sem** regras de composição arbitrárias e **sem** troca periódica forçada (apenas por suspeita de comprometimento). Custo do hash é limitado para não virar vetor de DoS (rate limit antes do hash, tamanho máximo de entrada).
- [ ] 🆕 **SEC-2.03 · Autenticação resistente a phishing** `[A]` — passkeys/WebAuthn (FIDO2) são oferecidos e **exigidos** para administradores e operações críticas; OTP por SMS não é o único segundo fator para contas privilegiadas.
- [ ] ✎ **SEC-2.04 · Brute force, credential stuffing e evasão de rate limit** `[B]` — login, reset, MFA, OTP, magic link, convite e API key têm rate limit por conta, IP, dispositivo e contexto; lockout progressivo não permite negação de serviço simples contra a vítima. O sistema é resiliente a evasão por spoofing de headers (`X-Forwarded-For`, `X-Real-IP`, `True-Client-IP` — o IP do cliente só é lido do proxy confiável), rotação de proxies residenciais, variação de capitalização/encoding do identificador e paralelismo (race em contador de tentativas). Há detecção de credential stuffing (taxa de falhas distribuída, senhas vazadas).
- [ ] **SEC-2.05 · MFA** `[B]` — enrollment, recovery, troca de fator, step-up e desativação resistem a takeover, SIM swap, replay, phishing previsível, fadiga de push (number matching) e bypass de endpoint (ex.: acessar rota pós-login sem completar o segundo fator). Fator forte é exigido para funções críticas. Códigos de recuperação são de uso único, armazenados com hash.
- [ ] ✎ **SEC-2.06 · Tokens JWT** `[B]` *(Se: JWT)* — validação segue RFC 8725: allowlist explícita de algoritmo (bloqueia `none` e confusão RS256/HS256), assinatura, `iss`, `aud`, `exp`, `nbf`, `iat` com tolerância de relógio pequena, `typ` quando aplicável; os cabeçalhos `kid`, `jku`, `x5u` e `jwk` não permitem path traversal, injeção de chave ou busca de chave em URL controlada pelo atacante. Tokens de acesso são de vida curta; revogação (lista de negação, versão de sessão ou introspecção) existe para logout, reset e troca de privilégio. JWT não carrega dados sensíveis em claro.
- [ ] **SEC-2.07 · Sessões** `[B]` — IDs têm ≥ 128 bits de entropia, gerados por CSPRNG, regenerados após login/elevação de privilégio (anti-fixation), invalidados no servidor em logout/reset/troca de senha e possuem expiração idle e absoluta. Cookies usam `Secure`, `HttpOnly`, `SameSite` adequado e prefixo `__Host-` quando possível; sessão não aparece em URL/referrer/log. Usuário vê e encerra sessões ativas.
- [ ] **SEC-2.08 · Recovery** `[B]` — reset usa token único, aleatório (≥ 128 bits), de vida curta, armazenado com hash, vinculado ao usuário, invalidado após uso e quando outro é emitido; não revela existência de conta. Link de reset não é construído a partir do header `Host` (host header poisoning). Não há troca de e-mail/telefone sem reautenticação; após reset ou troca, sessões e tokens existentes são invalidados e o titular é notificado no canal antigo.
- [ ] ✎ **SEC-2.09 · OAuth/OIDC** `[B]` *(Se: OAuth/OIDC)* — segue o OAuth 2.0 Security BCP (RFC 9700): authorization code + PKCE para todos os clientes, sem implicit grant nem password grant; `state`, `nonce`, allowlist exata de redirect URI (sem curingas), validação de `iss` (mix-up attack), escopos mínimos; account linking não vincula automaticamente por e-mail não verificado. Tokens não vazam por URL, referrer ou log. Tokens sender-constrained (DPoP/mTLS) avaliados para APIs de alto risco.
- [ ] **SEC-2.10 · API keys e service accounts** `[A]` — são escopadas, expiradas/rotacionadas, identificáveis (prefixo que permite secret scanning), armazenadas com hash no servidor, revogáveis e nunca embutidas no cliente. Uso, origem e falhas são auditados; chaves de teste não alcançam produção.
- [ ] **SEC-2.11 · Autenticação federada** `[A]` *(Se: SSO/SAML/OIDC corporativo)* — mapeamento de claims, grupos, domínio, assinatura (SAML: validação de assinatura do elemento correto, defesa contra XML signature wrapping), relógio, logout e provisionamento/desprovisionamento (SCIM) são validados. Claims controláveis pelo usuário não concedem privilégios; usuário removido no IdP perde acesso em prazo definido.
- [ ] 🆕 **SEC-2.12 · Reautenticação e step-up** `[A]` — ações sensíveis (troca de e-mail/senha/MFA, exportação de dados, criação de API key, alteração de dados bancários) exigem reautenticação recente ou step-up, independentemente da sessão estar ativa.
- [ ] 🆕 **SEC-2.13 · Notificações de segurança ao usuário** `[M]` — o usuário é notificado de login em novo dispositivo, troca de senha/MFA/e-mail, criação de credenciais e exportação de dados, com caminho para reagir (“não fui eu”).

### 3. Autorização, tenancy e lógica de negócio

- [ ] **SEC-3.01 · Matriz de autorização** `[B]` — existe matriz explícita de ator × ação × recurso × propriedade × estado × tenant; testes automatizados positivos e negativos cobrem cada combinação. Default deny é aplicado server-side, de forma centralizada (middleware/policy engine), não espalhado em `if`s.
- [ ] **SEC-3.02 · BOLA/IDOR** `[B]` — IDs de objetos, arquivos, mensagens, pedidos, relatórios, jobs e exports são trocados entre contas/tenants; servidor impede leitura, alteração, exclusão e inferência indireta (contagem, timing, mensagens de erro diferentes). IDs não sequenciais reduzem enumeração, mas **não** substituem a checagem de autorização.
- [ ] **SEC-3.03 · BFLA** `[B]` — funções admin, debug, internal, bulk, import/export, impersonation e maintenance são testadas por usuário comum, papel inferior e token sem escopo; troca de método HTTP (GET→DELETE/PUT), versão de API antiga e rota alternativa não contornam o controle.
- [ ] **SEC-3.04 · Property-level authorization** `[B]` — campos read-only, internos, financeiros, flags, owner, role, tenant e status não podem ser lidos ou alterados por mass assignment, JSON merge, GraphQL selection ou campos extras; respostas são serializadas por DTO/allowlist por papel.
- [ ] **SEC-3.05 · Autorização em cada camada** `[A]` — gateway, controller, service, repository, job, consumer, websocket e storage não assumem que camada anterior autorizou. Chamadas internas não são automaticamente confiáveis (zero trust entre serviços com identidade de workload).
- [ ] **SEC-3.06 · Tenant isolation e vazamento entre tenants** `[B]` *(Se: multi-tenant)* — IDs, filtros, cache keys, filas, índices de busca, índices vetoriais, exports, logs, backups e observabilidade não cruzam tenants. O tenant vem do contexto autenticado, nunca de parâmetro do cliente. Testes provam que tokens de um tenant não acessam subdomínios, endpoints ou dados (inclusive em memória/cache) de outro. Mecanismos de reforço no banco (ex.: row-level security) são considerados como defesa em profundidade.
- [ ] **SEC-3.07 · Estados e transições** `[A]` — workflow valida estado atual, ator, ordem, concorrência, expiração e pré-condições server-side. Não há salto de draft para approved, refund duplicado, pular etapa de pagamento ou cancelamento após finalização por race.
- [ ] **SEC-3.08 · Funções sensíveis** `[A]` — pagamento, saque, alteração de conta, exclusão, convite, mudança de owner, exportação e impersonation exigem step-up, confirmação, idempotência, trilha de auditoria e limites (valor, frequência). Operações de altíssimo impacto têm controle de quatro olhos.
- [ ] **SEC-3.09 · Race conditions** `[A]` — requests concorrentes (incluindo ataque de pacote único/single-packet) testam saldo, cupom, estoque, aprovação, reset, convite, upload, lock, limite de tentativas e mudança de privilégio. Resultado é atomicamente consistente (constraint, lock, transação ou operação condicional) e não depende apenas de validação anterior.
- [ ] 🆕 **SEC-3.10 · Integridade de valores de negócio** `[A]` — preço, desconto, quantidade, moeda, frete, taxa e limites são calculados ou revalidados no servidor; valores negativos, zero, decimais extremos, overflow, arredondamento e unidades trocadas são testados.
- [ ] **SEC-3.11 · Workflow abuse** `[A]` — fluxos legítimos não podem ser automatizados para fraude, spam, scraping, compra indevida, criação massiva, abuso de referral, enumeração ou consumo pago (SMS, e-mail, IA) sem controles compensatórios (limites, detecção de bot, custo progressivo, revisão).
- [ ] **SEC-3.12 · Decisões offline/async** `[A]` — autorização é revalidada no worker no momento do efeito; mensagem antiga, job de usuário removido ou evento reprocessado não executa ação indevida. Mensagens carregam identidade verificável, não apenas um `user_id` confiado.
- [ ] **SEC-3.13 · Impersonation/support** `[A]` *(Se: há acesso de suporte)* — suporte pode atuar somente com escopo, consentimento/registro, banner visível, expiração, motivo e auditoria; não há acesso invisível nem sessão compartilhada; ações destrutivas sob impersonation são bloqueadas ou exigem aprovação.
- [ ] 🆕 **SEC-3.14 · Acesso a arquivos e objetos armazenados** `[B]` — arquivos privados não ficam em bucket público nem em URL adivinhável; download passa por autorização ou URL assinada de vida curta, emitida após checagem de permissão, com escopo de um objeto.

### 4. Entrada, validação e injeções

- [ ] **SEC-4.01 · Validação de esquema** `[B]` — body, query, path, header, cookie, multipart, websocket, evento e metadata validam tipo, tamanho, charset, range, profundidade, campos desconhecidos e encoding na fronteira, com allowlist; validação no cliente é apenas UX.
- [ ] **SEC-4.02 · SQL/ORM** `[B]` — queries são parametrizadas; concatenação dinâmica, filtros opcionais, `ORDER BY`/nome de coluna controlável (exige allowlist), `IN`, `LIKE` (escape de curingas), raw queries do ORM, stored procedures e migrations são testados. ORM não é considerado proteção automática. Usuário de banco da aplicação não tem DDL nem privilégios administrativos.
- [ ] ✎ **SEC-4.03 · NoSQL e linguagens de consulta** `[B]` *(Se: NoSQL, motores de busca, linguagens de filtro)* — operadores (`$where`, `$ne`, `$regex`, `$gt`), objetos onde se espera string, JSON query, consultas de motores de busca e expressões de filtro são rejeitados ou allowlistados. *(Controles de GraphQL consolidados em SEC-5.15.)*
- [ ] **SEC-4.04 · Command/OS injection** `[B]` — argumentos são passados sem shell (array de argumentos); allowlist de comandos/opções, `--` antes de argumentos posicionais, ambiente mínimo, timeout, filesystem restrito e usuário não privilegiado. Testar metacaracteres, newline e injeção de argumentos (ex.: opções iniciadas por `-`).
- [ ] **SEC-4.05 · Template injection** `[B]` — templates, e-mail, PDF, markdown e geração de HTML não avaliam expressão controlável. Testar SSTI, XSS armazenado, escaping contextual e conteúdo rico; templates de usuário (se existirem) rodam em sandbox lógico sem acesso a objetos do runtime.
- [ ] **SEC-4.06 · LDAP/XML** `[A]` *(Se: LDAP/XML/SAML/SOAP/SVG/Office)* — filtros LDAP usam escape correto; parsers XML desabilitam DTD/entidades externas e limitam expansão, tamanho e profundidade; XXE, SSRF via XML e billion laughs são testados, inclusive em formatos baseados em XML (DOCX, XLSX, SVG).
- [ ] **SEC-4.07 · Path traversal** `[B]` — caminhos, nomes, zip/tar (zip slip), symlink e downloads são normalizados e confinados a um diretório base após resolução do caminho real; `..`, encoding duplo, null byte, UNC, separadores alternativos e links simbólicos são testados. Nome de arquivo do usuário não é usado como caminho de armazenamento.
- [ ] ✎ **SEC-4.08 · SSRF e metadados de nuvem** `[B]` *(Se: o servidor busca URLs, renderiza HTML/PDF, importa por link, recebe webhooks configuráveis)* — URLs são allowlistadas por esquema, host e porta; resolução DNS é validada no momento da conexão (anti DNS rebinding); IPv4/IPv6 privados, loopback, link-local, representações alternativas de IP (decimal, octal, IPv6-mapped) e redirects são bloqueados; esquemas `file`, `gopher`, `dict`, `ftp` desabilitados. Acesso a endpoints de metadados de nuvem a partir de input do usuário é bloqueado na aplicação **e** na infraestrutura (IMDSv2 com hop limit 1 ou equivalente, ver SEC-7.05); egress é segmentado por proxy de saída.
- [ ] **SEC-4.09 · Deserialização** `[B]` — formatos e classes permitidos são explícitos; não se desserializa objeto arbitrário de fonte não confiável (Java native serialization, pickle, YAML inseguro, BinaryFormatter etc.); assinatura/integridade e limites são verificados antes de desserializar.
- [ ] 🆕 **SEC-4.10 · Prototype pollution e mass merge** `[A]` *(Se: JavaScript/TypeScript)* — merges profundos, parsers de query string e clonagem de objetos rejeitam `__proto__`, `constructor` e `prototype`; objetos de configuração são criados sem protótipo ou congelados quando apropriado.
- [ ] **SEC-4.11 · Regex e parser DoS** `[A]` — expressões, JSON, YAML, CSV, imagem, PDF e multipart têm limites de tempo, tamanho, profundidade e memória; regex catastrófica (ReDoS) é testada ou motor de regex de tempo linear é usado para entrada não confiável.
- [ ] **SEC-4.12 · Headers e protocol smuggling** `[A]` — CRLF injection, host header poisoning, forwarded headers, headers duplicados, request desync (CL.TE, TE.CL, TE.TE, H2 downgrade), cache poisoning e normalização divergente entre proxy e app são avaliados. O header `Host` é validado contra allowlist.
- [ ] **SEC-4.13 · Upload** `[B]` *(Se: upload)* — extensão (allowlist), MIME real por conteúdo (magic bytes), tamanho, decompression bomb, polyglot, macro, SVG com script, nome de arquivo, quota, antivírus/sandbox e reprocessamento (re-encode de imagens, remoção de metadados EXIF) são controlados. Arquivos são servidos de domínio separado (sem cookies da aplicação) ou com `Content-Disposition: attachment` e `X-Content-Type-Options: nosniff`; nunca executados.
- [ ] **SEC-4.14 · Output encoding** `[B]` — HTML, atributos, JS, CSS, URL, JSON, SQL, shell, CSV (formula injection: `=`, `+`, `-`, `@`) e logs (log injection/forging) usam encoding de contexto; DOM sinks perigosos e bypass por Unicode/normalização são testados.
- [ ] 🆕 **SEC-4.15 · Canonicalização e Unicode** `[M]` — entradas são normalizadas (NFC/NFKC conforme o caso) antes de validação e comparação; homógrafos, caracteres de controle e bidi (RTL override) são tratados em nomes, URLs e identificadores exibidos.
- [ ] 🆕 **SEC-4.16 · E-mail e notificações** `[A]` *(Se: envia e-mail/SMS)* — conteúdo controlado pelo usuário não injeta headers de e-mail, links ou HTML em mensagens enviadas pelo domínio da empresa (abuso para phishing); remetente usa SPF, DKIM e DMARC com política de rejeição.

### 5. Web, browser e APIs

- [ ] **SEC-5.01 · CSRF** `[B]` *(Se: autenticação por cookie)* — operações state-changing exigem token anti-CSRF e/ou verificação de `Origin`/Fetch Metadata (`Sec-Fetch-Site`), com `SameSite` coerente; operações de mudança de estado nunca usam GET. Login CSRF, JSON CSRF (content-type simples), multipart e endpoints alternativos são testados.
- [ ] ✎ **SEC-5.02 · CORS** `[B]` — origens não são refletidas nem validadas por regex frágil (sufixo/prefixo); `null` origin é rejeitada; `Access-Control-Allow-Credentials` só com allowlist exata; métodos, headers e preflight restritos. API não expõe resposta sensível a origem não confiável.
- [ ] ✎ **SEC-5.03 · Subdomain takeover e higiene de DNS** `[A]` — registros DNS (CNAME, A, NS, MX) apontando para recursos desativados (buckets, apps de PaaS, CDNs) são detectados continuamente e removidos; subdomínios de terceiros não compartilham escopo de cookie com a aplicação; CAA restringe emissores de certificado; DNSSEC avaliado.
- [ ] ✎ **SEC-5.04 · CSP** `[A]` *(Se: frontend web)* — CSP estrita baseada em nonce ou hash (com `strict-dynamic`), sem `unsafe-inline`/`unsafe-eval`, com `object-src 'none'`, `base-uri 'none'`/`'self'`, `frame-ancestors` e relatório de violações monitorado. Trusted Types é avaliado para eliminar DOM XSS em aplicações ricas.
- [ ] 🆕 **SEC-5.05 · Headers de segurança** `[A]` — HSTS (com `includeSubDomains` e preload quando viável), `X-Content-Type-Options: nosniff`, `Referrer-Policy` restritiva, `Permissions-Policy` mínima, `Cross-Origin-Opener-Policy`, `Cross-Origin-Resource-Policy` e, quando necessário, `Cross-Origin-Embedder-Policy`; `Cache-Control: no-store` em respostas sensíveis. Verificados em **todas** as respostas relevantes, inclusive erros, redirects e assets.
- [ ] **SEC-5.06 · XSS** `[B]` — refletido, armazenado, DOM, template, markdown, SVG, e-mail, preview, PDF gerado e dados importados são testados em todos os contextos, inclusive painel admin (onde o impacto é maior). Uso de APIs de escape bypass do framework (`dangerouslySetInnerHTML`, `v-html`, `innerHTML`, `bypassSecurityTrust*`) é inventariado e justificado, com sanitizador mantido (ex.: DOMPurify).
- [ ] **SEC-5.07 · Cookies** `[A]` — escopo de domínio e path mínimo, flags corretas, prefixos `__Host-`/`__Secure-`; cookies sensíveis não são acessíveis a subdomínios menos confiáveis; logout limpa cookies e invalida a sessão no servidor.
- [ ] ✎ **SEC-5.08 · Armazenamento no cliente** `[A]` — tokens e dados sensíveis não ficam em `localStorage`, `sessionStorage`, IndexedDB, URL, analytics, crash report ou cache de service worker sem justificativa documentada; dados locais são limpos no logout; respostas autenticadas não ficam em cache compartilhado.
- [ ] **SEC-5.09 · Clickjacking e comunicação entre janelas** `[A]` — páginas sensíveis bloqueiam framing (`frame-ancestors`); `postMessage` valida `origin`, `source` e schema; `window.opener` é neutralizado (`noopener`/COOP); comunicação entre janelas não aceita comandos arbitrários.
- [ ] **SEC-5.10 · Open redirect** `[A]` — redirects aceitam apenas destinos permitidos (allowlist ou caminhos relativos validados), sem bypass por encoding, userinfo (`@`), backslash, `//`, esquema alternativo (`javascript:`, `data:`) ou domínio parecido.
- [ ] **SEC-5.11 · Inventário de API** `[A]` — especificações (OpenAPI/GraphQL schema), rotas reais, subdomínios, versões antigas, debug, health, métricas, GraphQL, websocket e endpoints de documentação são comparados; ativos esquecidos (shadow/zombie APIs) são removidos ou protegidos; versões antigas têm data de desligamento.
- [ ] **SEC-5.12 · Mass assignment** `[B]` — campos desconhecidos e privilegiados são rejeitados ou allowlistados; resposta não vaza campos internos. Testar POST/PUT/PATCH/merge, objetos aninhados e arrays.
- [ ] **SEC-5.13 · Rate limit e quotas** `[A]` — limites existem por identidade, IP, tenant, endpoint, custo e operação; headers informam limite e retry; implementação distribuída e multirregional não permite bypass simples (troca de região, IPv6 com prefixo inteiro, variação de path/case/trailing slash).
- [ ] **SEC-5.14 · Recursos caros** `[A]` — paginação, regex, export, relatório, busca, upload, envio de SMS/e-mail, biometria, chamadas pagas e IA têm custo máximo, timeout, quota e autorização (OWASP API4: consumo irrestrito de recursos).
- [ ] ✎ **SEC-5.15 · GraphQL** `[A]` *(Se: GraphQL)* — limites de profundidade, complexidade/custo, aliases, fragments e batching; autorização por campo/resolver; persisted queries/allowlist para clientes próprios; introspection **desabilitada** em produção para APIs privadas (para APIs públicas, permitida apenas se for decisão documentada, com os demais limites ativos); sugestões de campo (“did you mean”) desligadas; mensagens de erro sem detalhes internos.
- [ ] 🆕 **SEC-5.16 · Web cache poisoning e web cache deception** `[A]` *(Se: CDN/cache reverso)* — chave de cache inclui todos os inputs que alteram a resposta (headers não chaveados são testados); respostas autenticadas/personalizadas não são cacheadas publicamente; truques de path (`/conta/perfil.css`, delimitadores, normalização) não fazem a CDN cachear página privada.
- [ ] **SEC-5.17 · WebSocket/SSE** `[A]` *(Se: tempo real)* — handshake autentica, `Origin` é validada (anti cross-site WebSocket hijacking), autorização por mensagem/canal, tokens expiram e a conexão é encerrada quando a sessão é revogada; mensagens têm schema/tamanho e conexão possui quota/timeout.
- [ ] **SEC-5.18 · Erros da API** `[A]` — status, headers, mensagens, timing e paginação não revelam existência de recursos alheios, stack, versão, IDs internos, query ou dados de outros usuários. Formato de erro padronizado (ex.: Problem Details) sem campos de debug em produção.
- [ ] 🆕 **SEC-5.19 · Subresource Integrity e terceiros no browser** `[M]` — scripts/CSS de CDN de terceiros usam SRI ou são servidos do próprio domínio; inventário de scripts de terceiros por página existe, com monitoramento de mudança (proteção contra skimming/Magecart em páginas de pagamento).
- [ ] 🆕 **SEC-5.20 · Webhooks recebidos** `[A]` *(Se: recebe webhooks)* — assinatura HMAC/mTLS verificada com comparação em tempo constante, timestamp com janela curta e proteção contra replay (ID de evento único), payload validado por schema, processamento idempotente; o conteúdo do webhook é tratado como não confiável.
- [ ] 🆕 **SEC-5.21 · Métodos e content-types** `[M]` — apenas métodos HTTP necessários são aceitos por rota (TRACE desabilitado; override de método via header/parâmetro controlado); content-type é validado e o servidor não interpreta corpo em formato diferente do declarado (ex.: aceitar XML onde se espera JSON).

### 6. Criptografia, segredos e dados

- [ ] **SEC-6.01 · TLS externo** `[B]` — TLS 1.2+ (preferencialmente 1.3), cipher suites com forward secrecy e AEAD, certificados válidos com cadeia completa, renovação automática e alerta de expiração, redirect HTTP→HTTPS, HSTS; não há validação de certificado desabilitada em nenhum cliente HTTP do código (verificado por busca no código).
- [ ] 🆕 **SEC-6.02 · Comunicação interna** `[A]` — tráfego entre serviços, banco, cache e filas é cifrado (TLS/mTLS ou malha de serviço) quando atravessa rede compartilhada; serviços internos autenticam-se mutuamente com identidade de workload.
- [ ] **SEC-6.03 · Criptografia em repouso** `[A]` — banco, volumes, objetos, filas, backups, logs e dispositivos usam proteção proporcional; chave e dado não ficam no mesmo controle sem separação e auditoria.
- [ ] 🆕 **SEC-6.04 · Criptografia em nível de campo** `[A]` *(Se: dados pessoais sensíveis, documentos, dados financeiros)* — campos de maior risco (documento, saúde, dados bancários, biometria) são cifrados na aplicação ou tokenizados, de forma que um dump do banco ou acesso indevido de DBA não exponha o valor em claro; busca usa hash com chave (blind index) quando necessário.
- [ ] **SEC-6.05 · Gestão de chaves** `[A]` — geração, armazenamento, acesso, uso, rotação, revogação, destruição, backup e recuperação são documentados; KMS/HSM e envelope encryption são usados quando aplicável; chaves têm finalidade única; acesso a chaves é auditado.
- [ ] **SEC-6.06 · Segredos** `[B]` — scanner cobre histórico Git, branches, imagens de container, logs, CI, IaC, notebooks, fixtures, bundles do frontend e source maps; **push protection** bloqueia novos segredos; secret manager aplica least privilege, expiração, rotação e auditoria; segredo vazado tem procedimento de rotação imediata (remover do histórico não basta).
- [ ] **SEC-6.07 · Hardcoded/config** `[B]` — tokens, passwords, connection strings, private keys e credenciais de terceiros não aparecem em código ou configuração versionada. `.env`, dumps e arquivos de backup não são versionados nem servidos; credenciais de nuvem de longa duração são substituídas por federação de identidade (OIDC/workload identity).
- [ ] ✎ **SEC-6.08 · Dados em logs/telemetria** `[A]` — PII, credenciais, headers `Authorization`, cookies, tokens, payloads e dados de pagamento são mascarados **antes** de log/export (redação na biblioteca de logging, não por convenção). Erro, trace, crash report e suporte não viram canal de vazamento. *(Ver PERF-2.14 e PRIV-12.)*
- [ ] **SEC-6.09 · Hash, tokens e aleatoriedade** `[A]` — senhas, tokens de reset, API keys e identificadores secretos usam CSPRNG e hash adequados; comparações de segredos são em tempo constante; tokens não são previsíveis nem reutilizáveis. Não há uso de `Math.random`, `rand()` ou equivalente para segurança.
- [ ] 🆕 **SEC-6.10 · Algoritmos e implementações** `[A]` — apenas algoritmos atuais e bibliotecas maduras (sem criptografia própria); sem MD5/SHA-1 para segurança, sem ECB, sem IV/nonce reutilizado, sem RSA < 2048 bits; modos autenticados (AES-GCM, ChaCha20-Poly1305).
- [ ] 🆕 **SEC-6.11 · Inventário criptográfico e preparação pós-quântica** `[R]` — existe inventário de onde e como criptografia é usada (TLS, assinaturas, tokens, dados em repouso, integrações), permitindo trocar algoritmos sem reescrita (criptoagilidade); há plano de migração para algoritmos pós-quânticos padronizados pelo NIST e avaliação de TLS híbrido para dados com longa vida de confidencialidade (risco de “coletar agora, decifrar depois”).
- [ ] **SEC-6.12 · Minimização de exposição** `[A]` — respostas, exports, debug, documentação, diretórios, source maps, banners e metadata publicam somente o necessário. Atacante não obtém versão/stack/topologia sem necessidade. *(Detalhado na seção 9.)*

### 7. Configuração, infraestrutura e supply chain

- [ ] **SEC-7.01 · Defaults seguros** `[B]` — debug, verbose error, directory listing, admin seed, credenciais de exemplo, CORS amplo, métodos HTTP extras, consoles administrativos (actuator, profiler, admin de framework, phpMyAdmin etc.) e endpoints de teste estão desativados ou protegidos em produção — verificado por varredura, não só por configuração.
- [ ] **SEC-7.02 · Segregação de ambientes** `[A]` — contas/projetos de nuvem, redes, bancos, buckets, secrets, pipelines e observabilidade de dev/stage/prod são separados; credencial de ambiente inferior não alcança produção; dados de produção não são copiados para ambientes inferiores sem anonimização.
- [ ] **SEC-7.03 · IAM** `[B]` — usuários, roles, workloads e serviços têm permissões mínimas, escopo por recurso, acesso temporário (just-in-time) para privilégios elevados, MFA para humanos, revisão periódica e revogação no desligamento; não há wildcard administrativo por conveniência nem conta root/owner usada no dia a dia. Contas de break-glass existem, são monitoradas e testadas.
- [ ] **SEC-7.04 · Rede e egress** `[A]` — subnets, security groups, firewall, egress, DNS, metadata e administração são restritos; bancos, caches e filas não são acessíveis pela internet; acesso administrativo passa por bastion/zero-trust com MFA; segmentação limita movimento lateral; egress é allowlistado para serviços que não precisam de internet.
- [ ] ✎ **SEC-7.05 · Postura de nuvem (CSPM)** `[A]` *(Se: nuvem pública)* — configuração de nuvem é avaliada continuamente contra benchmark (ex.: CIS) por ferramenta de CSPM: buckets sem acesso público (bloqueio no nível da conta), serviço de metadados endurecido (ex.: IMDSv2 obrigatório com hop limit 1 na AWS ou equivalente), logs de auditoria da nuvem habilitados e protegidos, chaves de acesso antigas, snapshots públicos, security groups abertos. Desvios geram alerta com owner.
- [ ] **SEC-7.06 · Containers/Kubernetes** `[A]` *(Se: containers)* — não-root, `readOnlyRootFilesystem`, capabilities mínimas (`drop: ALL`), sem privileged/hostPath/hostNetwork, seccomp/AppArmor, Pod Security Standards em nível *restricted*, imagens verificadas por assinatura via admission policy, namespaces, network policies default deny, secrets não montados em pods que não precisam, service accounts sem token automático, API server não exposto publicamente, RBAC mínimo.
- [ ] 🆕 **SEC-7.07 · Imagens base e runtime** `[A]` — imagens base mínimas (distroless/slim), atualizadas com frequência definida, escaneadas no build e continuamente no registry; sem ferramentas de shell/compiladores desnecessários na imagem final.
- [ ] **SEC-7.08 · IaC** `[A]` *(Se: IaC)* — Terraform/Helm/CloudFormation/Pulumi tem scan de segurança, review, state protegido e cifrado (contém segredos), drift detection, ausência de secrets, mudanças destrutivas sinalizadas e plano auditável.
- [ ] ✎ **SEC-7.09 · Dependências (SCA)** `[B]` — lockfiles versionados, SBOM gerado por build (CycloneDX/SPDX), SCA com CVE/OSV em CI e contínuo, dependências transitivas incluídas, priorização por explorabilidade (CISA KEV, EPSS, alcançabilidade), licenças avaliadas, componentes fora de suporte (EOL) identificados, atualização automatizada com SLA.
- [ ] ✎ **SEC-7.10 · Ataques à cadeia de pacotes** `[A]` — proteção contra dependency confusion (escopos/namespaces privados reservados e registry configurado para resolver pacotes internos apenas do repositório interno), typosquatting, pacotes comprometidos e maintainer takeover: scripts de instalação desabilitados por padrão quando possível, **período de quarentena** para versões recém-publicadas antes de adoção automática, verificação de proveniência quando disponível, revisão de dependências novas (popularidade, mantenedor, permissões).
- [ ] **SEC-7.11 · Artefatos** `[A]` — imagens/pacotes/releases têm proveniência (SLSA), checksum, assinatura e verificação antes do deploy (ex.: Sigstore/cosign); registry impede sobrescrita de tags (imutabilidade) e promoção de artefato não aprovado; deploy referencia digest, não tag mutável.
- [ ] **SEC-7.12 · CI/CD** `[B]` — permissões de token mínimas por job (`permissions:` explícito); actions/workflows de terceiros pinados por SHA; PR de fork não executa com secrets nem com permissão de escrita (cuidado com `pull_request_target` e `workflow_run`); entradas não confiáveis (título de PR, nome de branch, corpo de issue) não são interpoladas em shell; deploy para nuvem usa OIDC em vez de chaves estáticas; runners self-hosted são efêmeros e isolados; logs de CI não imprimem segredos.
- [ ] **SEC-7.13 · Branch e revisão** `[A]` — proteção exige revisão independente, checks obrigatórios, branch atualizado, CODEOWNERS para áreas sensíveis (auth, crypto, CI, IaC, dependências), bloqueio de force push e de exclusão, commits assinados avaliados e auditoria de bypass de administrador.
- [ ] **SEC-7.14 · SAST/DAST/fuzz** `[A]` — SAST e secret scan rodam em todo PR; DAST autenticado roda periodicamente e antes de releases maiores; findings são triados com SLA (não apenas suprimidos — supressões têm justificativa e expiração); fuzzing cobre parsers, autenticação, autorização e propriedades críticas.
- [ ] **SEC-7.15 · Dependência de terceiros (SaaS/APIs)** `[A]` — versões, escopos, endpoints, dados enviados, SLA, fallback, suboperadores e risco de supply chain estão inventariados; respostas externas são validadas como não confiáveis; credenciais de integração têm escopo mínimo e rotação.
- [ ] **SEC-7.16 · OpenSSF Scorecard** `[M]` — checks de vulnerabilidades, updates, security policy, testes, SAST, branch protection, review, workflows perigosos, dependências pinadas, permissões de token e releases assinadas são executados e acompanhados, com meta de score.
- [ ] 🆕 **SEC-7.17 · Proteção de borda** `[M]` — WAF/regras de borda e proteção DDoS estão ativas para endpoints públicos, com regras ajustadas (modo bloqueio, não só monitoramento), sem substituir correção no código; origem não é acessível contornando a CDN/WAF (allowlist de IPs da borda ou autenticação de origem).
- [ ] 🆕 **SEC-7.18 · Hardening de host e serviços gerenciados** `[M]` — sistemas operacionais e serviços gerenciados seguem baseline (CIS ou equivalente), com patching automatizado e acesso SSH desabilitado ou via mecanismo auditado.

### 8. Logs, detecção, resposta e recuperação

- [ ] **SEC-8.01 · Eventos auditáveis** `[B]` — login (sucesso/falha), MFA, reset, alteração de role, autorização negada, export, leitura de dado sensível, uso de segredo, mudança de config, deploy, operação destrutiva, acesso administrativo e impersonation geram evento suficiente para investigação.
- [ ] 🆕 **SEC-8.02 · Conteúdo mínimo do evento** `[A]` — cada evento registra quem (identidade e tipo de ator), o quê, sobre qual recurso, quando (UTC sincronizado), de onde (IP confiável, user agent, sessão), resultado e correlação (`trace_id`), sem registrar segredo ou dado sensível em claro.
- [ ] **SEC-8.03 · Integridade e acesso aos logs** `[A]` — logs são enviados para armazenamento fora do alcance do serviço que os gera (conta/projeto separado), append-only/imutáveis (WORM), com timestamp confiável, retenção definida, controle por função e alerta para exclusão, alteração ou queda de ingestão.
- [ ] **SEC-8.04 · Detecção** `[A]` — regras correlacionam brute force, credential stuffing, impossible travel, reuso de token, escalada de privilégio, scraping, exfiltração (volume anômalo de export/download), SSRF, abuso de API, mudança de pipeline/IAM e criação de credenciais; alertas têm owner, severidade, runbook e teste periódico (simulação de ataque).
- [ ] **SEC-8.05 · Incident response** `[B]` — playbook alinhado a referência atual (ex.: NIST SP 800-61r3) cobre triagem, severidade, contenção, revogação de tokens e sessões, rotação de segredos, isolamento, preservação de evidência (cadeia de custódia), comunicação, erradicação, recuperação e postmortem; papéis e contatos 24×7 definidos.
- [ ] ✎ **SEC-8.06 · Disaster Recovery Plan** `[B]` — existe **DRP explícito e versionado**, com: RPO/RTO aprovados por serviço e por dado; cenários cobertos (perda de região, corrupção lógica, exclusão acidental, ransomware, comprometimento da conta de nuvem, indisponibilidade de fornecedor crítico); ordem de restauração e dependências; runbook passo a passo executável por quem não escreveu; owner e substituto; critérios de declaração de desastre e de retorno. O plano é **exercitado** (no mínimo anualmente e após mudanças relevantes) com tempo real medido contra RTO/RPO e lições registradas.
- [ ] 🆕 **SEC-8.07 · Backups resilientes a ataque** `[B]` — backups seguem 3-2-1 com pelo menos uma cópia imutável/isolada (outra conta ou cofre com retenção bloqueada), cifrada, com credenciais separadas das de produção (comprometer produção não permite apagar backups); restauração é testada periodicamente com verificação de integridade (restore real, não só “job concluído”); backups de dados pessoais respeitam retenção e eliminação (ver PRIV-11).
- [ ] **SEC-8.08 · Blast radius** `[A]` — comprometimento de uma conta, pod, action, fornecedor, tenant ou chave não concede acesso global; segmentação, quotas, escopos, kill switches (desabilitar feature/integração/chave rapidamente) e revogação em massa limitam dano. Existe capacidade testada de revogar todas as sessões e rotacionar todos os segredos.
- [ ] **SEC-8.09 · Privacidade do logging** `[A]` — retenção e conteúdo obedecem minimização; acesso a logs é auditado; investigação consegue trabalhar com pseudônimos e revelar identidade apenas sob autorização. *(Ver PRIV-12.)*
- [ ] **SEC-8.10 · Comunicação em incidentes** `[A]` — contatos, escalonamento, jurídico, privacidade, clientes, fornecedores e autoridades são definidos; decisões e timestamps são registrados. Incidentes com dados pessoais integram o procedimento LGPD (ver PRIV-17) e normas setoriais aplicáveis.
- [ ] **SEC-8.11 · Lições aprendidas** `[M]` — pós-incidente gera causas raiz, controles faltantes, testes de regressão, owner e prazo; findings repetidos ou aceites vencidos são escalados.
- [ ] 🆕 **SEC-8.12 · Exercícios** `[M]` — tabletop de incidente e de DR é realizado periodicamente com participação técnica, jurídica e de negócio, incluindo cenário de ransomware e de vazamento de dados.

### 9. 🆕 Superfície exposta e reconhecimento

> Objetivo: reduzir o que um atacante aprende **antes** de atacar. Cada informação exposta acelera a exploração.

- [ ] 🆕 **SEC-9.01 · Arquivos e diretórios sensíveis** `[B]` — não são acessíveis publicamente: `.git/`, `.env`, `.DS_Store`, backups (`*.bak`, `*.old`, `*.zip`, `*.sql`), dumps, arquivos de IDE, `docker-compose.yml`, `package.json` de servidor, logs, `phpinfo`, painéis de status. Verificado por varredura com wordlist.
- [ ] 🆕 **SEC-9.02 · Source maps e código do cliente** `[A]` — source maps não são publicados em produção (ou só para ferramenta de erro, com acesso autenticado); bundles não contêm comentários internos, URLs de ambientes internos, chaves, flags de features ocultas sensíveis ou lógica de autorização que dependa de segredo.
- [ ] 🆕 **SEC-9.03 · Fingerprinting** `[M]` — headers `Server`, `X-Powered-By`, versões em páginas de erro padrão, banners de serviço e caminhos característicos são removidos ou neutralizados; páginas de erro são customizadas e uniformes.
- [ ] 🆕 **SEC-9.04 · Documentação e endpoints operacionais** `[A]` — Swagger/OpenAPI UI, GraphQL playground, endpoints de métricas (`/metrics`), health detalhado, debug e profiling não são públicos em produção (ou exigem autenticação); health check público retorna apenas status mínimo.
- [ ] 🆕 **SEC-9.05 · Vazamento por metadados** `[M]` — documentos e imagens publicados não carregam metadados internos (autor, caminho, software, geolocalização); `robots.txt` e `sitemap` não listam áreas sensíveis.
- [ ] 🆕 **SEC-9.06 · Exposição em fontes públicas** `[A]` — monitoramento de vazamento de credenciais e código da organização em repositórios públicos, pastes e bases vazadas; repositórios e buckets públicos da organização são inventariados e revisados.
- [ ] 🆕 **SEC-9.07 · Canal de divulgação responsável** `[M]` — `/.well-known/security.txt` (RFC 9116) publicado com contato e política de divulgação; existe processo para receber, triar e responder relatos externos em prazo definido.

### 10. 🆕 Aplicações com LLM e agentes *(Se: a aplicação usa modelos de IA, RAG ou agentes)*

> Referências: OWASP Top 10 for LLM Applications 2025 e OWASP Top 10 for Agentic Applications 2026.

- [ ] 🆕 **SEC-10.01 · Prompt injection direta e indireta** `[B]` — o sistema assume que **todo** conteúdo que chega ao modelo (input do usuário, documentos, páginas web, e-mails, resultados de ferramentas, dados recuperados por RAG) pode conter instruções maliciosas. Mitigação é em camadas: separação clara entre instruções e dados, classificadores/guardrails de entrada e saída, privilégio mínimo das ferramentas, confirmação humana para ações de impacto e testes adversariais com corpus de ataques conhecidos. **Sanitização de texto isolada não é considerada controle suficiente.**
- [ ] 🆕 **SEC-10.02 · Saída do modelo como entrada não confiável** `[B]` — a saída do modelo é validada por schema e codificada por contexto antes de ser renderizada (XSS), executada (código, SQL, shell), usada em URLs (SSRF, exfiltração por imagem/markdown) ou passada a outra ferramenta. Renderização de links e imagens gerados pelo modelo é restrita a domínios permitidos.
- [ ] 🆕 **SEC-10.03 · Agência excessiva e privilégio de ferramentas** `[B]` — ferramentas expostas ao modelo/agente são mínimas, com escopo e permissões do **usuário final** (não de uma conta de serviço onipotente); ações destrutivas, financeiras, de envio externo ou irreversíveis exigem confirmação humana explícita; há limites de passos, de gasto e de taxa por sessão de agente.
- [ ] 🆕 **SEC-10.04 · Vazamento de informação sensível** `[A]` — o modelo não tem acesso a dados que o usuário não poderia ver; system prompts não contêm segredos (considerar que serão extraídos); respostas são filtradas para dados pessoais e segredos; logs de prompts/respostas seguem a mesma política de dados sensíveis.
- [ ] 🆕 **SEC-10.05 · RAG e bancos vetoriais** `[A]` — documentos indexados carregam metadados de permissão e tenant; a recuperação filtra por autorização **antes** de enviar ao modelo; ingestão valida a origem do conteúdo (envenenamento de base); exclusão de documento remove também embeddings e caches.
- [ ] 🆕 **SEC-10.06 · Memória e estado de agentes** `[A]` *(Se: agentes com memória)* — memória persistente é isolada por usuário/tenant, validada antes de ser gravada, expirável e auditável; conteúdo não confiável não se torna instrução permanente (memory poisoning).
- [ ] 🆕 **SEC-10.07 · Consumo ilimitado e abuso de custo** `[A]` — limites de tokens por requisição, por usuário e por período; proteção contra prompts que forçam saídas longas ou loops de ferramentas; alerta de gasto anômalo. *(Ver PERF-11.06.)*
- [ ] 🆕 **SEC-10.08 · Cadeia de suprimento de IA** `[A]` — modelos, provedores, SDKs, servidores MCP/plugins e datasets são inventariados, versionados, de fontes confiáveis e revisados; servidores MCP de terceiros são tratados como código não confiável (pinados, revisados, com permissões mínimas).
- [ ] 🆕 **SEC-10.09 · Execução de código gerado** `[B]` *(Se: o agente executa código)* — execução ocorre em sandbox isolado (sem rede por padrão, sem credenciais, com limites de CPU/memória/tempo, filesystem efêmero), nunca no host da aplicação.
- [ ] 🆕 **SEC-10.10 · Testes adversariais de IA** `[A]` — existe suíte de red teaming (jailbreak, injeção indireta, exfiltração, abuso de ferramenta, extração de system prompt) executada em CI ou antes de cada mudança de prompt/modelo, com métricas de taxa de sucesso de ataque.

### 11. 🆕 Tratamento de exceções e condições anômalas

> Referência: categoria A10:2025 “Mishandling of Exceptional Conditions” do OWASP Top 10:2025.

- [ ] 🆕 **SEC-11.01 · Falha fechada** `[B]` — erro em checagem de autorização, validação de token, verificação de assinatura, consulta a serviço de permissões ou feature flag de segurança resulta em **negação**, nunca em liberação.
- [ ] 🆕 **SEC-11.02 · Exceções não tratadas** `[A]` — existe handler global que captura exceções, registra com contexto e responde com erro genérico; rejeições de promises/exceções em threads não derrubam o processo de forma silenciosa nem deixam estado inconsistente.
- [ ] 🆕 **SEC-11.03 · Consistência após falha** `[A]` — falha no meio de operação multi-etapa faz rollback ou compensação (saga), sem deixar recurso criado sem dono, pagamento sem pedido ou permissão parcialmente aplicada; recursos (arquivos, locks, conexões) são liberados em `finally`/equivalente.
- [ ] 🆕 **SEC-11.04 · Condições de limite** `[M]` — overflow/underflow numérico, divisão por zero, datas inválidas, fuso horário, ano bissexto, valores nulos e coleções vazias são testados nos caminhos de segurança e de negócio.
- [ ] 🆕 **SEC-11.05 · Comportamento sob esgotamento** `[A]` — disco cheio, memória esgotada, pool esgotado ou dependência indisponível não desativam controles de segurança (ex.: log de auditoria falhando silenciosamente, rate limit desligado quando o Redis cai). O comportamento em falha de cada controle é decidido e documentado (fail-open vs. fail-closed).

### 12. 🆕 Gestão de vulnerabilidades

- [ ] 🆕 **SEC-12.01 · SLA de correção** `[B]` — prazos de correção por severidade definidos e medidos (referência comum: crítico ≤ 7 dias, alto ≤ 30, médio ≤ 90), com aceleração para vulnerabilidades em exploração ativa (CISA KEV) ou alta probabilidade de exploração (EPSS); idade dos findings abertos é reportada.
- [ ] 🆕 **SEC-12.02 · Priorização por contexto** `[A]` — a priorização considera alcançabilidade do código vulnerável, exposição do ativo, dados envolvidos e controles compensatórios, além do score base (CVSS v4.0).
- [ ] 🆕 **SEC-12.03 · Fim de vida** `[A]` — runtimes, frameworks, bancos, sistemas operacionais e bibliotecas fora de suporte são identificados com plano de migração datado.
- [ ] 🆕 **SEC-12.04 · Testes externos recorrentes** `[M]` — pentest independente periódico (no mínimo anual e após mudanças significativas) e, quando maduro, bug bounty; achados retornam ao backlog com SLA.

### 13. 🆕 Aplicativos mobile *(Se: há app iOS/Android)*

- [ ] 🆕 **SEC-13.01 · Padrão MASVS** `[A]` — o app é avaliado contra OWASP MASVS v2 (armazenamento, criptografia, autenticação, rede, plataforma, código, resiliência, privacidade).
- [ ] 🆕 **SEC-13.02 · Armazenamento seguro** `[A]` — tokens e segredos ficam no Keychain/Keystore; dados sensíveis não vão para backup, logs, screenshots do app switcher ou área de transferência.
- [ ] 🆕 **SEC-13.03 · Comunicação** `[A]` — apenas TLS, sem exceções de cleartext; pinning avaliado para operações de alto risco, com estratégia de rotação.
- [ ] 🆕 **SEC-13.04 · Backend não confia no app** `[B]` — toda regra de autorização e de negócio está no servidor; o app é considerado engenharia-reversível; chaves embutidas são tratadas como públicas; atestação de app/dispositivo é usada como sinal adicional, não como controle único.
- [ ] 🆕 **SEC-13.05 · Deep links e componentes exportados** `[A]` — deep links/app links validam parâmetros e origem; activities, services, content providers e URL schemes exportados são mínimos e protegidos.

### 14. Execução e relatório do pentest whitebox

- [ ] **SEC-14.01 · Revisão de código orientada a risco** `[A]` — priorizar auth, autorização, parsing, crypto, secrets, SSRF, uploads, pagamentos, admin, exports, webhooks, jobs, migrations, integrações e IA; registrar arquivos, linhas e call paths (source → sink).
- [ ] **SEC-14.02 · Teste dinâmico autenticado** `[A]` — executar com cada papel, tenant e estado; comparar respostas, timing, side effects e logs. Testar endpoints descobertos fora da documentação e versões antigas.
- [ ] **SEC-14.03 · Teste negativo** `[A]` — validar entradas malformadas, limites, Unicode, encoding duplo, concorrência, requests fora de ordem, replay, timeout, falha de terceiro e mensagens duplicadas.
- [ ] 🆕 **SEC-14.04 · Testes de segurança como regressão** `[A]` — cada vulnerabilidade corrigida ganha teste automatizado que falharia se ela voltasse; testes de autorização (matriz SEC-3.01) rodam em CI.
- [ ] **SEC-14.05 · Evidência de exploração** `[A]` — cada finding tem request/response ou teste automatizado, pré-condições, impacto demonstrado, alcance, probabilidade, screenshots/logs sanitizados e instrução de reprodução.
- [ ] ✎ **SEC-14.06 · Severidade** `[A]` — score usa metodologia declarada (ex.: CVSS v4.0 com métricas de ambiente) e considera exploração remota, autenticação necessária, complexidade, interação, confidencialidade, integridade, disponibilidade, privacidade, multi-tenancy e impacto de negócio; risco residual é separado da severidade técnica; achados encadeáveis são avaliados em conjunto.
- [ ] **SEC-14.07 · Remediação verificável** `[A]` — recomendação aponta correção no boundary correto, não só workaround; reteste confirma exploit bloqueado, ausência de bypass e manutenção de funcionalidade legítima.
- [ ] **SEC-14.08 · Critério de aprovação** `[B]` — não há crítico/alto aberto sem aceite formal; médios têm prazo e compensação; exceções possuem owner, justificativa, expiração, monitoramento e plano de correção.

---
## Privacy — LGPD

> **Objetivo do pilar:** identificar **toda** lacuna que impeça a aplicação (e a operação que a sustenta) de estar em conformidade com a LGPD e normas conexas, de forma rastreável a artigo de lei ou resolução da ANPD. A conformidade é avaliada no **comportamento real do sistema** (o que é coletado, enviado, armazenado e apagado de fato), não apenas na política publicada.
>
> **Regras de avaliação deste pilar:**
> - Cada item indica o fundamento legal entre colchetes. Ao registrar um achado, citar o artigo.
> - Divergência entre o aviso de privacidade e o comportamento observado (captura de rede, banco, logs) é sempre achado `[A]` ou superior.
> - Quando a ANPD ainda não regulamentou um tema (ex.: RIPD, portabilidade), aplica-se a lei, os guias orientativos vigentes e a melhor prática; o item registra essa condição.
> - Agentes de pequeno porte (Res. CD/ANPD nº 2/2022) podem ter regime simplificado — marcar quando aplicável e verificar se o tratamento é de alto risco (o que afasta parte dos benefícios).
> - Verificar sempre a versão vigente das resoluções; a ANPD tornou-se agência reguladora (Lei 15.352/2026), tem agenda regulatória ativa e mapa de temas prioritários de fiscalização para 2026–2027 (Res. 30/2025), com foco declarado em direitos dos titulares, dados sensíveis, crianças e adolescentes e poder público.

### 1. Aplicabilidade, papéis e escopo

- [ ] ✎ **PRIV-1.01 · Aplicabilidade territorial e material** `[B]` [arts. 3º e 4º] — está documentado por que a LGPD se aplica (tratamento no Brasil, oferta de bens/serviços a pessoas no Brasil ou dados coletados no Brasil) e quais tratamentos estão fora do escopo (art. 4º), com justificativa. Outras jurisdições aplicáveis (ex.: GDPR para titulares na UE) são identificadas.
- [ ] ✎ **PRIV-1.02 · Papéis por operação** `[B]` [art. 5º, VI–IX; arts. 37–40] — para **cada operação de tratamento** está definido quem é controlador, cocontrolador, operador e suboperador, com base em quem decide finalidade e elementos essenciais (não no que diz o contrato). Situações em que a empresa atua como operadora de clientes (SaaS B2B) são separadas das em que é controladora.
- [ ] 🆕 **PRIV-1.03 · Porte do agente** `[M]` [Res. 2/2022] — está avaliado se a organização se enquadra como agente de pequeno porte e, em caso positivo, se realiza tratamento de alto risco (larga escala ou impacto significativo **e** uso de tecnologia inovadora, vigilância, decisão automatizada ou dados sensíveis/de crianças/de idosos), o que limita as flexibilizações.
- [ ] 🆕 **PRIV-1.04 · Categorias de titulares** `[A]` — estão identificadas todas as categorias de titulares (clientes, usuários finais de clientes, visitantes, leads, colaboradores, candidatos, representantes de PJ, dependentes, terceiros mencionados em conteúdo), inclusive titulares indiretos.

### 2. Inventário e registro das operações (ROPA)

- [ ] ✎ **PRIV-2.01 · Inventário de dados ponta a ponta** `[B]` [art. 37; art. 6º, X] — o inventário mapeia cada fluxo desde a coleta até a eliminação: sistemas, tabelas/campos, integrações, regiões, categorias de titulares, volume, dados pessoais e sensíveis, finalidade, base legal, compartilhamentos, retenção e controles. Inclui coleta direta e indireta, cookies, SDKs, pixels, logs, analytics, gravação de sessão, suporte/CRM, backups, ambientes não produtivos, planilhas exportadas, treinamento/avaliação de modelos e dados enviados a provedores de IA.
- [ ] 🆕 **PRIV-2.02 · Inventário verificado contra o sistema real** `[A]` — o inventário é conferido por evidência técnica: varredura de schemas/bancos por dados pessoais (data discovery), captura de tráfego do frontend e app (quais terceiros recebem o quê), revisão de payloads de logs e eventos. Campos pessoais não inventariados são achado.
- [ ] 🆕 **PRIV-2.03 · Classificação no código** `[M]` — campos com dados pessoais e sensíveis são anotados no schema/modelos (tags, comentários estruturados ou catálogo de dados), permitindo que testes, linters, mascaramento e pipelines de eliminação os localizem automaticamente.
- [ ] ✎ **PRIV-2.04 · Registro das operações** `[A]` [art. 37; Res. 2/2022] — existe registro das operações de tratamento atualizado, com owner por finalidade, especialmente para tratamentos baseados em legítimo interesse; formato simplificado apenas para agentes de pequeno porte elegíveis. Mudanças de produto disparam atualização (gatilho no processo de desenvolvimento).

### 3. Princípios (art. 6º)

- [ ] ✎ **PRIV-3.01 · Boa-fé e finalidade** `[B]` [art. 6º, caput e I] — cada tratamento tem propósito legítimo, específico, explícito e informado; não há tratamento posterior incompatível (ex.: dados de suporte usados para marketing, dados de cadastro usados para treinar modelo sem avaliação).
- [ ] 🆕 **PRIV-3.02 · Adequação** `[A]` [art. 6º, II] — o tratamento é compatível com o contexto e a expectativa do titular (avaliado pelo que o titular razoavelmente espera ao usar a funcionalidade).
- [ ] ✎ **PRIV-3.03 · Necessidade e minimização** `[B]` [art. 6º, III] — cada campo coletado tem justificativa vinculada à finalidade; campos opcionais são realmente opcionais; não há coleta “por precaução”; dados são truncados/agregados quando a precisão total não é necessária (ex.: data de nascimento → faixa etária; geolocalização precisa → cidade). Formulários, APIs e eventos de analytics são revisados campo a campo.
- [ ] 🆕 **PRIV-3.04 · Livre acesso** `[A]` [art. 6º, IV; art. 9º] — o titular consegue consultar, de forma facilitada e gratuita, a forma e duração do tratamento e a integralidade dos seus dados.
- [ ] 🆕 **PRIV-3.05 · Qualidade dos dados** `[M]` [art. 6º, V] — há mecanismos de correção e atualização (pelo titular e por processo interno); dados desatualizados que geram decisões sobre o titular são revisados.
- [ ] 🆕 **PRIV-3.06 · Transparência** `[A]` [art. 6º, VI] — informações claras, precisas e acessíveis sobre o tratamento e os agentes, respeitados segredos comercial e industrial (detalhado na seção 9).
- [ ] 🆕 **PRIV-3.07 · Segurança e prevenção** `[A]` [art. 6º, VII e VIII] — medidas técnicas e administrativas protegem contra acessos não autorizados e situações acidentais ou ilícitas, e previnem danos (detalhado na seção 12 e no pilar Security).
- [ ] 🆕 **PRIV-3.08 · Não discriminação** `[A]` [art. 6º, IX] — não há tratamento para fins discriminatórios ilícitos ou abusivos; modelos, regras de score, precificação e segmentações são avaliados quanto a efeitos discriminatórios (inclusive por variáveis proxy).
- [ ] ✎ **PRIV-3.09 · Responsabilização e prestação de contas** `[B]` [art. 6º, X] — o controlador consegue **demonstrar**, com evidência, a adoção de medidas eficazes e a eficácia delas (ver seção 24).

### 4. Bases legais

- [ ] ✎ **PRIV-4.01 · Base legal por finalidade** `[B]` [art. 7º] — cada finalidade tem **uma** base legal documentada e coerente entre as dez hipóteses do art. 7º (consentimento; obrigação legal/regulatória; políticas públicas; pesquisa; execução de contrato ou procedimentos preliminares; exercício regular de direitos; proteção da vida; tutela da saúde; legítimo interesse; proteção do crédito). Não se usa consentimento quando o tratamento ocorreria de qualquer forma (base incorreta gera expectativa falsa de revogação).
- [ ] 🆕 **PRIV-4.02 · Execução de contrato aplicada com rigor** `[A]` [art. 7º, V] — a base “contrato” cobre apenas o estritamente necessário para entregar o serviço contratado; marketing, analytics não essenciais, perfilamento e compartilhamento com parceiros não são justificados por ela.
- [ ] 🆕 **PRIV-4.03 · Obrigação legal identificada** `[M]` [art. 7º, II] — quando a base é obrigação legal/regulatória, a norma específica e o prazo exigido estão citados (ex.: registros fiscais, guarda de registros de acesso do Marco Civil).
- [ ] 🆕 **PRIV-4.04 · Dados públicos e manifestamente públicos** `[A]` [art. 7º, §§ 3º, 4º e 7º] — dados obtidos de fontes públicas ou tornados públicos pelo titular são tratados considerando a finalidade, a boa-fé e o interesse público que justificaram sua disponibilização; scraping e enriquecimento de dados têm base legal e avaliação própria.
- [ ] 🆕 **PRIV-4.05 · Mudança de base ou finalidade** `[A]` [art. 9º, § 2º] — alteração de finalidade incompatível com o consentimento original é informada **previamente**, com possibilidade de revogação; a troca de base legal não é usada para contornar revogação de consentimento.

### 5. Consentimento

*(Se: alguma finalidade usa consentimento.)*

- [ ] ✎ **PRIV-5.01 · Requisitos de validade** `[B]` [art. 5º, XII; art. 8º] — consentimento é livre, informado e inequívoco, para finalidades determinadas (autorizações genéricas são nulas), fornecido por escrito ou meio que demonstre a manifestação de vontade; cláusula destacada das demais quando em contrato; não é condição para serviço que não depende daquele tratamento.
- [ ] 🆕 **PRIV-5.02 · Granularidade** `[A]` [art. 8º, § 4º] — finalidades distintas têm opções distintas (ex.: newsletter, ofertas de parceiros, personalização, analytics); não há “aceito tudo” como única opção.
- [ ] 🆕 **PRIV-5.03 · Prova do consentimento** `[B]` [art. 8º, § 2º] — o ônus da prova é do controlador: cada consentimento é registrado com titular, finalidade, versão do texto apresentado, data/hora, canal, interface/versão do app e evidência da ação afirmativa; o registro é íntegro e recuperável.
- [ ] ✎ **PRIV-5.04 · Revogação** `[B]` [art. 8º, § 5º; art. 18, IX] — revogação é gratuita, facilitada, pelo mesmo canal ou mais simples que a concessão, e **efetiva tecnicamente**: o sistema para de tratar (eventos deixam de ser enviados, listas são atualizadas, terceiros são notificados) em prazo definido e verificado por teste.
- [ ] 🆕 **PRIV-5.05 · Aplicação do consentimento no código** `[A]` — o estado de consentimento é consultado no ponto de uso (envio de e-mail marketing, disparo de pixel, uso para personalização), não apenas na coleta; existe teste automatizado que garante que nenhum tracker/evento opcional dispara sem consentimento (verificação por captura de rede).
- [ ] 🆕 **PRIV-5.06 · Vícios de consentimento** `[A]` [art. 8º, § 3º] — não há consentimento obtido mediante erro, dolo, coação ou interface enganosa (ver PRIV-9.04 sobre dark patterns).

### 6. Legítimo interesse

*(Se: alguma finalidade usa legítimo interesse.)*

- [ ] ✎ **PRIV-6.01 · Teste de balanceamento documentado** `[B]` [art. 10; art. 7º, IX; guia orientativo da ANPD sobre legítimo interesse] — para cada finalidade há avaliação registrada de: (i) finalidade legítima e situação concreta; (ii) necessidade (apenas dados estritamente necessários, sem alternativa menos invasiva); (iii) balanceamento com expectativas legítimas e direitos do titular; (iv) salvaguardas (transparência, opt-out, minimização, segurança).
- [ ] 🆕 **PRIV-6.02 · Vedação para dados sensíveis** `[B]` [art. 11] — legítimo interesse **não** é usado como base para dados pessoais sensíveis.
- [ ] 🆕 **PRIV-6.03 · Transparência e oposição** `[A]` [art. 10, § 2º; art. 18, § 2º] — o titular é informado sobre o tratamento por legítimo interesse e pode se opor por canal simples; a oposição é avaliada e, quando procedente, efetivada tecnicamente.
- [ ] 🆕 **PRIV-6.04 · Disponibilidade para a ANPD** `[M]` [art. 10, § 3º; art. 37] — o teste de balanceamento e o registro das operações estão prontos para entrega à ANPD; a ANPD pode exigir RIPD nesses casos.

### 7. Dados pessoais sensíveis

- [ ] ✎ **PRIV-7.01 · Identificação de dados sensíveis** `[B]` [art. 5º, II] — estão mapeados todos os dados sobre origem racial ou étnica, convicção religiosa, opinião política, filiação sindical ou a organização religiosa/filosófica/política, saúde, vida sexual, genéticos e **biométricos** — inclusive dados **inferidos** (ex.: compras que revelam condição de saúde, foto usada para reconhecimento facial).
- [ ] ✎ **PRIV-7.02 · Base legal do art. 11** `[B]` [art. 11] — cada tratamento sensível usa uma hipótese do art. 11 (consentimento específico e destacado para finalidades específicas, ou as hipóteses sem consentimento, como obrigação legal, exercício regular de direitos inclusive em contrato, proteção da vida, tutela da saúde e prevenção à fraude e segurança do titular em processos de identificação e autenticação de cadastro). Biometria para login/antifraude cita expressamente a hipótese usada.
- [ ] 🆕 **PRIV-7.03 · Vedações específicas** `[A]` [art. 11, §§ 4º e 5º] — não há comunicação ou uso compartilhado de dados de saúde para vantagem econômica fora das exceções legais; operadoras de planos de saúde não tratam dados para seleção de riscos.
- [ ] 🆕 **PRIV-7.04 · Proteção reforçada** `[A]` [arts. 11, 46] — dados sensíveis têm controles adicionais: criptografia em nível de campo, acesso restrito e auditado por pessoa, exclusão de logs/analytics, segregação, retenção mínima e RIPD (ver SEC-6.04 e seção 19).
- [ ] 🆕 **PRIV-7.05 · Uso em publicidade e perfilamento** `[A]` [arts. 6º, IX; 11; Res. 30/2025] — dados sensíveis (inclusive inferidos) não alimentam segmentação publicitária nem públicos de plataformas de anúncios sem base legal adequada; esse ponto é tema prioritário de fiscalização da ANPD.

### 8. Crianças, adolescentes e outros vulneráveis

- [ ] ✎ **PRIV-8.01 · Determinação de público e de acesso provável** `[B]` [art. 14; Lei 15.211/2025 — ECA Digital] — está avaliado se o produto é direcionado a crianças/adolescentes **ou de acesso provável** por eles (conceito do ECA Digital, vigente desde 17/03/2026), com evidência (natureza do serviço, analytics, público de marketing). A conclusão “não se aplica” é documentada.
- [ ] ✎ **PRIV-8.02 · Melhor interesse e base legal** `[B]` [art. 14, caput; Enunciado CD/ANPD nº 1/2023] — o tratamento de dados de crianças e adolescentes observa o melhor interesse e usa as hipóteses legais dos arts. 7º ou 11, com consentimento específico e em destaque de um dos pais ou responsável quando o consentimento for a base para crianças (art. 14, § 1º), e esforços razoáveis para verificar que o consentimento foi dado pelo responsável (§ 5º).
- [ ] 🆕 **PRIV-8.03 · Minimização em jogos e aplicações** `[A]` [art. 14, § 4º] — a participação em jogos, aplicações e atividades não é condicionada ao fornecimento de dados além do estritamente necessário.
- [ ] 🆕 **PRIV-8.04 · Transparência adequada à idade** `[A]` [art. 14, §§ 2º e 6º] — são públicos os tipos de dados coletados, a forma de utilização e o procedimento para exercício de direitos; as informações são simples, claras, acessíveis e adequadas ao entendimento da criança, com recursos audiovisuais quando apropriado.
- [ ] 🆕 **PRIV-8.05 · Obrigações do ECA Digital** `[B]` *(Se: direcionado ou de acesso provável por menores)* [Lei 15.211/2025 e decretos regulamentadores de 18/03/2026] — verificar, por tipo de serviço: mecanismo **confiável** de verificação de idade (autodeclaração isolada não é suficiente); configurações protetivas por padrão (*safety by default*); ferramentas de supervisão parental; vedação de perfilamento para publicidade direcionada a crianças e adolescentes; vedação de caixas de recompensa (loot boxes) em jogos; canais de denúncia e remoção; e demais obrigações específicas por categoria (redes sociais, jogos, lojas de aplicativos, plataformas de vídeo). A ANPD é a autoridade fiscalizadora.
- [ ] 🆕 **PRIV-8.06 · Verificação de idade proporcional e com privacidade** `[A]` — o método de verificação de idade coleta o mínimo necessário (preferência por estimativa/atestação que não retenha documento ou imagem), elimina dados de verificação após uso e não cria nova base de dados biométricos desnecessária.
- [ ] ✎ **PRIV-8.07 · Idosos e outros vulneráveis** `[M]` [art. 6º; Res. 2/2022] — idosos, pessoas com deficiência e outros grupos vulneráveis são considerados na avaliação de risco, no desenho do consentimento, na acessibilidade das interfaces (WCAG) e na comunicação.

### 9. Transparência, aviso de privacidade e cookies

- [ ] ✎ **PRIV-9.01 · Conteúdo mínimo do aviso** `[B]` [art. 9º; art. 18] — o aviso informa: finalidade específica; forma e duração do tratamento; identificação e contato do controlador; identidade e contato do encarregado; uso compartilhado e sua finalidade; responsabilidades dos agentes; direitos do titular e como exercê-los; transferência internacional; base legal por finalidade; critérios de retenção; e, quando o tratamento for condição para o serviço, esse fato e os meios de exercer direitos (art. 9º, § 3º).
- [ ] 🆕 **PRIV-9.02 · Aviso consistente com o comportamento real** `[B]` — cada terceiro que recebe dados (detectado em captura de rede, integrações e contratos) está no aviso; cada dado coletado está no aviso; não há coleta não declarada. Diferenças são achado.
- [ ] 🆕 **PRIV-9.03 · Aviso contextual e versionado** `[M]` [art. 8º, § 6º; art. 9º] — além da política geral, há avisos no momento da coleta (just-in-time) para dados não óbvios (localização, contatos, câmera, biometria); versões do aviso são datadas e arquivadas; alterações relevantes são comunicadas ao titular.
- [ ] ✎ **PRIV-9.04 · Ausência de dark patterns** `[B]` [art. 6º, I e VI; art. 8º; guia orientativo da ANPD sobre cookies] — o banner/fluxo de consentimento não usa padrões enganosos: recusar é tão fácil e visível quanto aceitar (mesma camada, mesmo destaque), não há caixas pré-marcadas, contraste ou linguagem enganosa, cansaço por repetição (re-perguntar após recusa em curto intervalo), “cookie wall” injustificado ou interpretação de rolagem/navegação como consentimento.
- [ ] 🆕 **PRIV-9.05 · Cookies e tecnologias de rastreamento** `[A]` [guia orientativo da ANPD sobre cookies] — cookies, local storage, pixels, SDKs, fingerprinting e server-side tagging são inventariados por categoria (necessários, desempenho, funcionais, publicidade); apenas os estritamente necessários operam antes da escolha; a escolha é registrada, pode ser alterada a qualquer momento por link sempre acessível e é respeitada também no tagueamento server-side e em integrações de conversão (ex.: envio de e-mail/telefone com hash a plataformas de anúncio continua sendo dado pessoal).
- [ ] 🆕 **PRIV-9.06 · Gravação de sessão e ferramentas de comportamento** `[A]` *(Se: session replay, heatmaps)* — campos de entrada, dados pessoais exibidos e telas sensíveis são mascarados por padrão; a ferramenta está no aviso, tem base legal e retenção curta.
- [ ] 🆕 **PRIV-9.07 · Acessibilidade da informação** `[M]` — aviso e central de privacidade são acessíveis (leitores de tela, linguagem simples, português), encontráveis a partir de qualquer página e no app.

### 10. Direitos dos titulares

- [ ] ✎ **PRIV-10.01 · Canal e verificação de identidade** `[B]` [art. 18, caput e §§ 3º e 5º] — há canal gratuito, acessível e divulgado (autosserviço na conta e canal alternativo para quem não tem conta); a verificação de identidade é proporcional ao risco (não exige mais dados do que o necessário nem vira barreira); pedidos por representante legal são tratados.
- [ ] ✎ **PRIV-10.02 · Cobertura de todos os direitos do art. 18** `[B]` [art. 18, I–IX e § 2º] — o processo e o sistema atendem: (I) confirmação da existência de tratamento; (II) acesso; (III) correção de dados incompletos, inexatos ou desatualizados; (IV) anonimização, bloqueio ou eliminação de dados desnecessários, excessivos ou tratados em desconformidade; (V) portabilidade; (VI) eliminação dos dados tratados com consentimento (ressalvado o art. 16); (VII) informação sobre entidades com as quais houve uso compartilhado; (VIII) informação sobre a possibilidade de não consentir e suas consequências; (IX) revogação do consentimento; e oposição (§ 2º).
- [ ] 🆕 **PRIV-10.03 · Prazos do art. 19** `[B]` [art. 19] — confirmação de existência ou acesso: **imediatamente**, em formato simplificado, ou em até **15 dias** por declaração clara e completa (origem, inexistência de registro, critérios e finalidade). Prazos são medidos por pedido, com alerta antes do vencimento. Quando a providência não puder ser imediata, o titular recebe resposta com as razões (art. 18, § 4º). Agentes de pequeno porte: verificar regra de prazo diferenciado da Res. 2/2022.
- [ ] 🆕 **PRIV-10.04 · Formato da resposta e cópia integral** `[A]` [art. 19, §§ 1º a 3º] — dados são armazenados de forma que favoreça o exercício do acesso; a resposta pode ser eletrônica ou impressa; quando o tratamento se basear em consentimento ou contrato, o titular pode obter cópia eletrônica integral em formato que permita uso subsequente.
- [ ] 🆕 **PRIV-10.05 · Compilação automatizada (DSAR)** `[A]` — o sistema gera a exportação de dados de um titular a partir de **todas** as fontes do inventário (banco principal, serviços satélites, data warehouse, ferramentas de suporte/CRM, logs relevantes, terceiros), por processo automatizado e testado; o pacote não inclui dados de outros titulares.
- [ ] 🆕 **PRIV-10.06 · Portabilidade** `[M]` [art. 18, V; art. 40] — a exportação é estruturada e em formato interoperável (ex.: JSON/CSV documentado); a regulamentação específica da ANPD sobre portabilidade é acompanhada (tema de agenda regulatória).
- [ ] 🆕 **PRIV-10.07 · Correção propagada** `[A]` [art. 18, § 6º] — correção, eliminação, anonimização e bloqueio são comunicados **de imediato** aos agentes com quem houve uso compartilhado, para que repitam o procedimento (exceto quando comprovadamente impossível ou desproporcional, com registro).
- [ ] 🆕 **PRIV-10.08 · Registro e auditoria de pedidos** `[A]` — cada pedido tem protocolo, data de recebimento, verificação, ações executadas por sistema, data de resposta, conteúdo enviado e evidência de cumprimento; métricas (volume, prazo médio, atrasos) são reportadas ao encarregado.
- [ ] 🆕 **PRIV-10.09 · Teste ponta a ponta de direitos** `[A]` — existe teste (automatizado ou roteiro periódico) que cria um titular sintético, gera dados em todas as funcionalidades, executa acesso, correção, eliminação e revogação, e verifica o resultado em cada sistema e terceiro.

### 11. Término do tratamento, retenção e eliminação

- [ ] ✎ **PRIV-11.01 · Tabela de retenção** `[B]` [arts. 15 e 16; art. 6º, III] — cada dado/categoria tem prazo, justificativa (finalidade, obrigação legal, exercício de direitos), evento que inicia a contagem, ação no fim (eliminar, anonimizar, bloquear), exceções legais e owner. Dados não são mantidos indefinidamente “por via das dúvidas”.
- [ ] 🆕 **PRIV-11.02 · Hipóteses de término** `[A]` [art. 15] — o sistema reconhece o término do tratamento quando a finalidade é alcançada ou os dados deixam de ser necessários, quando o período acaba, quando o titular revoga/solicita (respeitado o interesse público) ou por determinação da ANPD.
- [ ] 🆕 **PRIV-11.03 · Conservação autorizada** `[A]` [art. 16] — dados mantidos após o término se enquadram em: obrigação legal/regulatória; estudo por órgão de pesquisa (com anonimização sempre que possível); transferência a terceiro respeitados os requisitos; ou uso exclusivo do controlador com dados anonimizados e vedado o acesso por terceiro. Cada exceção está registrada.
- [ ] 🆕 **PRIV-11.04 · Guarda mínima obrigatória do Marco Civil** `[A]` [Lei 12.965/2014, art. 15] *(Se: provedor de aplicação constituído como pessoa jurídica com fins econômicos)* — registros de acesso a aplicações (data, hora, IP) são guardados por 6 meses, em ambiente controlado e seguro, com sigilo — e **não** são estendidos sem justificativa; o conflito aparente entre “guardar” e “minimizar” está resolvido na tabela de retenção.
- [ ] ✎ **PRIV-11.05 · Eliminação efetiva e completa** `[B]` — eliminação, anonimização ou bloqueio alcançam produção, réplicas, caches, índices de busca, índices vetoriais/embeddings, filas e DLQs, data warehouse, logs, exports, arquivos em storage, ambientes não produtivos, backups (eliminação na expiração ou mecanismo de “não restaurar” documentado, ex.: lista de exclusões reaplicada após restore) e suboperadores.
- [ ] ✎ **PRIV-11.06 · Propagação a terceiros** `[A]` [art. 18, § 6º] — pedidos de exclusão são propagados por API/webhook aos SaaS integrados (CRM, e-mail marketing, analytics, suporte, plataformas de anúncio), com confirmação e registro.
- [ ] 🆕 **PRIV-11.07 · Jobs de retenção testados** `[A]` — rotinas de expurgo são automatizadas, idempotentes, observáveis (quantos registros removidos), alertam em falha e são testadas; não dependem de execução manual.
- [ ] 🆕 **PRIV-11.08 · Contas inativas** `[M]` — há política para contas e dados de usuários inativos (aviso e eliminação/anonimização após período definido).

### 12. Segurança, privacy by design e privacy by default

- [ ] ✎ **PRIV-12.01 · Medidas de segurança proporcionais** `[B]` [arts. 46, 47 e 49] — medidas técnicas e administrativas aptas a proteger dados de acessos não autorizados e de situações acidentais ou ilícitas, proporcionais ao risco — verificadas pelo pilar Security (mínimo: score de Security sem `[B]` aberto nos itens que tocam dados pessoais). Todos que intervêm no tratamento mantêm a segurança mesmo após o término (art. 47).
- [ ] ✎ **PRIV-12.02 · Privacy by design** `[A]` [art. 46, § 2º] — privacidade é considerada desde a concepção: template de design/PR inclui perguntas de privacidade (novos dados? nova finalidade? novo terceiro? retenção?); revisão de privacidade é obrigatória para mudanças que alteram o inventário.
- [ ] 🆕 **PRIV-12.03 · Privacy by default** `[A]` [art. 6º, III; art. 46, § 2º] — configurações padrão são as mais protetivas: perfis não públicos por padrão, compartilhamentos opcionais desligados, rastreamentos opcionais desligados, retenção mínima.
- [ ] ✎ **PRIV-12.04 · Acesso interno** `[A]` — acesso de colaboradores a dados pessoais é baseado em função e necessidade, com justificativa, aprovação, revisão periódica e trilha de auditoria por consulta a dados de titular identificado; acesso direto a produção é excepcional e registrado.
- [ ] 🆕 **PRIV-12.05 · Ambientes não produtivos** `[A]` — dev, teste, staging, demos e análises não usam dados pessoais reais, ou usam dados anonimizados/sintéticos; cópias de produção para esses ambientes passam por mascaramento irreversível automatizado.
- [ ] ✎ **PRIV-12.06 · Logs e telemetria** `[A]` — logs, traces, métricas, crash reports e ferramentas de erro não contêm dados pessoais além do necessário, com mascaramento automático e retenção definida (ver SEC-6.08, PERF-2.14).
- [ ] 🆕 **PRIV-12.07 · Exportações e planilhas** `[M]` — exports de dados pessoais são limitados por permissão, registrados, com expiração de link e marca d'água/identificação quando apropriado; dados não circulam em planilhas e e-mails fora de sistemas controlados.
- [ ] 🆕 **PRIV-12.08 · Treinamento e conscientização** `[M]` — colaboradores com acesso a dados pessoais recebem treinamento periódico e registrado sobre LGPD, segurança e procedimentos internos.

### 13. Anonimização e pseudonimização

- [ ] 🆕 **PRIV-13.01 · Critério de anonimização** `[A]` [art. 5º, III e XI; art. 12] — dados declarados como “anonimizados” resistem à reidentificação com meios técnicos razoáveis (considerando custo, tempo, tecnologia disponível e combinação com outras bases); remoção de nome/CPF com manutenção de dados quase identificadores (CEP, data de nascimento, gênero, IDs de dispositivo) **não** é anonimização.
- [ ] 🆕 **PRIV-13.02 · Pseudonimização tratada como dado pessoal** `[A]` [art. 13, § 4º] — dados pseudonimizados (hash, tokens, IDs internos) continuam tratados como pessoais; a informação adicional que permite reverter é mantida separada, com controle de acesso.
- [ ] 🆕 **PRIV-13.03 · Perfis comportamentais** `[A]` [art. 12, § 2º] — dados usados para formar perfil comportamental de pessoa natural identificada são tratados como pessoais, mesmo que “sem nome”.
- [ ] 🆕 **PRIV-13.04 · Técnica documentada** `[M]` — a técnica de anonimização (agregação, k-anonimato, generalização, ruído/privacidade diferencial) e o teste de risco de reidentificação são documentados; a regulamentação da ANPD sobre anonimização e pseudonimização é acompanhada (agenda regulatória).

### 14. Decisões automatizadas, perfilamento e IA

- [ ] ✎ **PRIV-14.01 · Inventário de decisões automatizadas** `[B]` [art. 20] — estão identificadas as decisões tomadas unicamente com base em tratamento automatizado que afetam interesses do titular (crédito, preço, elegibilidade, moderação, bloqueio de conta, antifraude, recrutamento, score, perfil de consumo).
- [ ] 🆕 **PRIV-14.02 · Direito de revisão** `[B]` [art. 20, caput] — o titular pode solicitar revisão dessas decisões; o canal existe, o pedido é registrado e a revisão é efetivamente executada com análise substantiva (preferencialmente humana e com poder de alterar a decisão).
- [ ] 🆕 **PRIV-14.03 · Explicabilidade** `[A]` [art. 20, § 1º] — o controlador fornece, quando solicitado, informações claras e adequadas sobre critérios e procedimentos usados na decisão, observados segredos comercial e industrial; a explicação é gerada a partir de registro da decisão (entradas, versão do modelo/regra, fatores principais).
- [ ] 🆕 **PRIV-14.04 · Auditoria de discriminação** `[A]` [art. 20, § 2º; art. 6º, IX] — modelos e regras são avaliados quanto a vieses e efeitos discriminatórios antes da implantação e periodicamente; resultados são registrados e disponíveis para eventual auditoria da ANPD.
- [ ] ✎ **PRIV-14.05 · Dados pessoais e modelos de IA** `[A]` [arts. 6º, 7º, 11, 46] — uso de dados pessoais para treinar, ajustar ou avaliar modelos tem finalidade compatível, base legal, minimização e RIPD quando de alto risco; prompts e respostas com dados pessoais enviados a provedores têm contrato que veda treinamento pelo provedor e define retenção; modelos não expõem dados de outros titulares (ver SEC-10.04).
- [ ] ✎ **PRIV-14.06 · Opt-out de uso em IA** `[A]` [arts. 8º, § 5º; 18, § 2º] *(Se: dados do usuário alimentam indexação semântica, personalização por IA ou treinamento)* — o usuário tem opção granular e efetiva de excluir seus dados dessas finalidades quando a base legal permite oposição/revogação; a escolha é respeitada no pipeline de ingestão e remove dados já indexados. *(Movido de AI Readiness.)*
- [ ] 🆕 **PRIV-14.07 · Acompanhamento regulatório de IA** `[M]` — a organização acompanha a regulamentação da ANPD sobre IA e decisões automatizadas (agenda regulatória) e a tramitação do PL 2338/2023, que ainda não está em vigor; obrigações normativas setoriais já vigentes (ex.: saúde, financeiro) são verificadas.

### 15. Compartilhamento, operadores e terceiros

- [ ] ✎ **PRIV-15.01 · Contratos com operadores** `[B]` [arts. 37–39, 42] — contratos (DPA) definem: instruções e finalidade, confidencialidade, medidas de segurança, subcontratação apenas com autorização, localização dos dados e transferência internacional, retorno/eliminação ao fim, auditoria e evidências, apoio ao atendimento de direitos, notificação de incidentes em prazo compatível com o prazo do controlador, cooperação com a ANPD e responsabilidades.
- [ ] 🆕 **PRIV-15.02 · Due diligence de fornecedores** `[A]` — fornecedores que tratam dados pessoais passam por avaliação de privacidade e segurança antes da contratação e periodicamente, proporcional ao risco; lista de suboperadores é conhecida e mudanças são notificadas.
- [ ] ✎ **PRIV-15.03 · Compartilhamento necessário e registrado** `[A]` [art. 7º, § 5º; art. 9º, V; art. 18, VII] — cada compartilhamento interno (entre empresas do grupo) e externo tem finalidade, base legal, minimização dos campos enviados, registro e menção no aviso; não há venda ou cessão de dados fora da finalidade e da base.
- [ ] 🆕 **PRIV-15.04 · Controle técnico do que sai** `[A]` — integrações enviam apenas os campos contratados/necessários (verificado no payload real); SDKs e pixels de terceiros não coletam automaticamente mais do que o declarado (configurações de coleta automática revisadas).
- [ ] 🆕 **PRIV-15.05 · Responsabilidade solidária** `[M]` [arts. 42–45] — a organização entende e gerencia o risco de responsabilização solidária (operador que descumpre a lei ou instruções; controladores diretamente envolvidos) e mantém evidências que sustentem excludentes (art. 43).
- [ ] 🆕 **PRIV-15.06 · Quando a empresa é operadora** `[A]` *(Se: SaaS B2B)* — a aplicação permite ao cliente (controlador) cumprir suas obrigações: exportar e eliminar dados dos titulares dele, configurar retenção, obter registro de suboperadores, receber notificação de incidente e auditar; a empresa não usa dados dos clientes para finalidades próprias sem base.

### 16. Transferência internacional

- [ ] ✎ **PRIV-16.01 · Inventário de transferências** `[B]` [arts. 33–36; Res. 19/2024] — cada transferência é inventariada, incluindo hospedagem em nuvem fora do Brasil, acesso remoto por equipes ou suporte no exterior, provedores de SaaS, IA, e-mail e analytics estrangeiros e suboperadores. “Está na nuvem” não é exceção.
- [ ] 🆕 **PRIV-16.02 · Mecanismo válido por transferência** `[B]` [art. 33; Res. 19/2024; Res. 32/2026] — cada transferência tem mecanismo válido: decisão de adequação (a União Europeia/EEE é reconhecida como adequada pela Res. 32/2026), cláusulas-padrão contratuais da ANPD, cláusulas específicas aprovadas, normas corporativas globais ou outra hipótese do art. 33. Transferências para destinos sem adequação usam as cláusulas-padrão da ANPD **incorporadas na íntegra e sem alteração** (prazo de adequação encerrado em 23/08/2025); cláusulas de outras jurisdições sozinhas (ex.: SCCs europeias) não bastam.
- [ ] 🆕 **PRIV-16.03 · Transparência sobre transferência** `[A]` [Res. 19/2024; art. 9º] — o titular é informado sobre transferências internacionais e pode obter as informações e cláusulas aplicáveis, conforme a Res. 19/2024.
- [ ] ✎ **PRIV-16.04 · Transferências ulteriores e mudanças** `[A]` — transferências posteriores pelo importador estão cobertas pelas cláusulas; troca de provedor, de região de hospedagem ou novo suboperador estrangeiro dispara revisão antes da mudança.

### 17. Incidentes de segurança com dados pessoais

- [ ] ✎ **PRIV-17.01 · Procedimento integrado** `[B]` [art. 48; Res. 15/2024] — playbook integrado entre segurança, privacidade, jurídico, comunicação e operadores, com papéis, contatos, critérios de avaliação de risco ou dano relevante, preservação de evidências, contenção, investigação e mitigação.
- [ ] 🆕 **PRIV-17.02 · Avaliação de risco ou dano relevante** `[A]` [Res. 15/2024] — existe critério documentado para decidir se o incidente pode gerar risco ou dano relevante (considerando dados sensíveis, de crianças/adolescentes/idosos, financeiros, de autenticação, protegidos por sigilo, volume e possibilidade de dano material ou moral), com decisão registrada.
- [ ] ✎ **PRIV-17.03 · Comunicação à ANPD e aos titulares** `[B]` [art. 48, § 1º; Res. 15/2024] — quando houver risco ou dano relevante, o controlador comunica a ANPD **e** os titulares em até **3 dias úteis** a partir do conhecimento de que o incidente afetou dados pessoais (prazo em dobro para agentes de pequeno porte), contendo: natureza e categorias de dados e titulares afetados, medidas técnicas e de segurança utilizadas, riscos, motivos de eventual demora, medidas adotadas para reverter ou mitigar, data do incidente e contato do encarregado. A comunicação aos titulares é em linguagem simples, direta e individual quando possível. Informações complementares são enviadas no prazo regulamentar.
- [ ] 🆕 **PRIV-17.04 · Registro de incidentes** `[A]` [Res. 15/2024] — **todos** os incidentes com dados pessoais (inclusive os não comunicados) são registrados com data, descrição, dados e titulares afetados, avaliação de risco, medidas e justificativa da não comunicação, mantidos por no mínimo 5 anos.
- [ ] 🆕 **PRIV-17.05 · Capacidade técnica de dimensionar o incidente** `[A]` — logs e trilhas permitem responder rapidamente quais titulares e quais dados foram afetados (escopo exato), evitando notificação excessiva ou insuficiente.
- [ ] ✎ **PRIV-17.06 · Operadores** `[A]` [art. 39] — operadores e suboperadores comunicam incidentes ao controlador sem demora injustificada, em prazo contratual compatível com os 3 dias úteis, e cooperam na investigação.
- [ ] 🆕 **PRIV-17.07 · Simulação** `[M]` — o procedimento é exercitado periodicamente (tabletop) e o tempo para decidir e comunicar é medido.

### 18. Encarregado (DPO)

- [ ] ✎ **PRIV-18.01 · Designação formal** `[B]` [art. 41; Res. 18/2024] — encarregado indicado por ato formal (pessoa natural ou jurídica, interna ou externa), com substituto para ausências; dispensa só se agente de pequeno porte elegível, que ainda assim mantém canal de comunicação com titulares (Res. 2/2022).
- [ ] 🆕 **PRIV-18.02 · Divulgação** `[A]` [art. 41, § 1º; Res. 18/2024] — identidade e contato do encarregado são divulgados publicamente, de forma clara e objetiva, em local de destaque no site/app.
- [ ] 🆕 **PRIV-18.03 · Atribuições, recursos e independência** `[A]` [art. 41, § 2º; Res. 18/2024] — o encarregado recebe reclamações e comunicações de titulares e da ANPD, orienta colaboradores, participa das decisões relevantes de privacidade, tem acesso à alta gestão, recursos e autonomia técnica; conflitos de interesse são avaliados e documentados; consegue se comunicar com clareza em português com titulares e ANPD.

### 19. RIPD e gestão de risco

- [ ] ✎ **PRIV-19.01 · Gatilhos de RIPD** `[B]` [art. 5º, XVII; art. 10, § 3º; art. 38; Res. 2/2022] — está definido quando o RIPD é elaborado: tratamentos de alto risco (usar como referência os critérios da Res. 2/2022 enquanto não houver regulamento específico: larga escala ou impacto significativo combinados com tecnologia inovadora, vigilância, decisão automatizada, dados sensíveis ou de crianças/adolescentes/idosos), tratamento por legítimo interesse quando solicitado, e sempre que a ANPD determinar. A regulamentação específica do RIPD ainda é tema da agenda regulatória — acompanhar.
- [ ] ✎ **PRIV-19.02 · Conteúdo do RIPD** `[A]` [art. 38, parágrafo único] — contém, no mínimo, descrição dos tipos de dados coletados, metodologia de coleta e de garantia da segurança, e análise do controlador sobre medidas, salvaguardas e mecanismos de mitigação de risco; recomenda-se também: agentes, sistemas, operações, titulares, fontes, finalidades, bases legais, compartilhamentos, retenção, necessidade e proporcionalidade, matriz de risco (probabilidade × impacto), riscos residuais, aprovação e data de revisão.
- [ ] 🆕 **PRIV-19.03 · Momento e atualização** `[A]` — o RIPD é feito **antes** de iniciar o tratamento de alto risco (ou assim que identificado), revisado em mudanças relevantes e periodicamente, e está pronto para entrega à ANPD quando solicitado.
- [ ] 🆕 **PRIV-19.04 · Integração ao desenvolvimento** `[M]` — o processo de produto tem triagem de privacidade (questionário curto) que indica quando é necessário RIPD, para que ele não seja feito depois do lançamento.

### 20. Governança, boas práticas e accountability

- [ ] ✎ **PRIV-20.01 · Programa de governança em privacidade** `[A]` [art. 50, § 2º, I] — existe programa que demonstra: comprometimento da gestão; aplicação a todo o conjunto de dados; adaptação à estrutura, escala e volume; políticas e salvaguardas baseadas em avaliação sistemática de risco; relação de confiança com o titular; integração à governança corporativa; planos de resposta a incidentes e remediação; atualização constante com monitoramento contínuo e avaliações periódicas.
- [ ] 🆕 **PRIV-20.02 · Políticas internas** `[M]` — políticas de privacidade interna, retenção, classificação, uso aceitável, gestão de fornecedores, resposta a incidentes e atendimento a titulares estão aprovadas, publicadas internamente e revisadas.
- [ ] 🆕 **PRIV-20.03 · Indicadores** `[M]` — indicadores de privacidade são acompanhados pela gestão: pedidos de titulares e prazos, incidentes, achados abertos, RIPDs pendentes, fornecedores avaliados, treinamentos concluídos.
- [ ] 🆕 **PRIV-20.04 · Auditoria interna periódica** `[M]` — este checklist (ou equivalente) é executado periodicamente, com resultados reportados e plano de ação; boas práticas adotadas são documentadas, pois são consideradas na dosimetria de sanções (Res. 4/2023).

### 21. Poder público *(Se: o controlador é órgão/entidade pública ou trata dados em nome do poder público)*

- [ ] 🆕 **PRIV-21.01 · Finalidade pública e competência legal** `[B]` [art. 23] — o tratamento atende à finalidade pública, na persecução do interesse público, com objetivo de executar competências legais; hipóteses e procedimentos são divulgados.
- [ ] 🆕 **PRIV-21.02 · Uso compartilhado e transferência a entes privados** `[A]` [arts. 25–27] — dados são mantidos em formato interoperável; compartilhamento com entes privados segue as hipóteses legais, com informação à ANPD quando exigido e regulamentação aplicável.
- [ ] 🆕 **PRIV-21.03 · Encarregado e publicidade** `[A]` [art. 23, III] — encarregado indicado e informações sobre tratamentos publicadas em veículos de fácil acesso.

### 22. Normas conexas e setoriais

- [ ] 🆕 **PRIV-22.01 · Marco Civil da Internet** `[A]` [Lei 12.965/2014, arts. 7º, 10, 11, 15] — guarda de registros (ver PRIV-11.04), sigilo das comunicações, informações claras sobre coleta, uso e proteção, e jurisdição brasileira para dados coletados no Brasil.
- [ ] 🆕 **PRIV-22.02 · Código de Defesa do Consumidor** `[M]` [CDC, arts. 43 e 44] *(Se: relação de consumo)* — direitos de acesso e correção de cadastros de consumidores e comunicação de abertura de cadastro são observados em conjunto com a LGPD.
- [ ] 🆕 **PRIV-22.03 · Normas setoriais** `[A]` — normas aplicáveis ao setor estão mapeadas e cumpridas (ex.: Banco Central para instituições financeiras e Open Finance, ANS e CFM para saúde, CVM, Cadastro Positivo, normas de telemedicina, normas trabalhistas para dados de empregados).

### 23. Fiscalização e preparação

- [ ] 🆕 **PRIV-23.01 · Prontidão para fiscalização** `[A]` [arts. 52–54; Lei 15.352/2026; Res. 4/2023; Res. 30/2025] — a organização consegue responder a uma requisição da ANPD em prazo curto com: ROPA, avisos e versões, registros de consentimento, testes de legítimo interesse, RIPDs, contratos com operadores, registro de incidentes, evidências de segurança e de atendimento a titulares. Temas prioritários de fiscalização 2026–2027 recebem atenção reforçada.
- [ ] 🆕 **PRIV-23.02 · Conhecimento das sanções** `[M]` [art. 52] — o mapa de risco considera as sanções possíveis (advertência; multa de até 2% do faturamento no Brasil, limitada a R$ 50 milhões por infração; multa diária; publicização; bloqueio ou eliminação dos dados; suspensão do banco de dados ou da atividade; proibição do tratamento) e o impacto de cada uma no negócio.
- [ ] 🆕 **PRIV-23.03 · Reclamações e petições** `[M]` — reclamações de titulares (canal próprio, consumidor.gov, Procon, ANPD) são monitoradas e tratadas como indicador de falha de processo.

### 24. Evidência de conformidade

- [ ] ✎ **PRIV-24.01 · Repositório de evidências** `[B]` [art. 6º, X; art. 50] — RIPDs, ROPA, avisos e versões, consentimentos, logs de preferências, testes de legítimo interesse, contratos, avaliações de terceiros, pedidos de titulares, registro de incidentes, treinamentos, testes técnicos e decisões de risco são versionados, datados e recuperáveis.
- [ ] 🆕 **PRIV-24.02 · Matriz requisito → evidência** `[A]` — cada item deste pilar mapeia para owner, sistema, evidência, frequência de verificação e status; evidências técnicas (capturas de rede, testes de eliminação, testes de consentimento) são regeneradas a cada ciclo.

#### Matriz de cobertura LGPD (artigo → itens)

| Dispositivo | Tema | Itens |
|---|---|---|
| Arts. 1º–4º | Escopo e aplicabilidade | PRIV-1.01 |
| Art. 5º | Definições (sensível, anonimização, papéis, consentimento, RIPD) | PRIV-1.02, 5.01, 7.01, 13.01, 19.01 |
| Art. 6º | Princípios | PRIV-3.01 a 3.09 |
| Art. 7º | Bases legais | PRIV-4.01 a 4.04 |
| Art. 8º | Consentimento | PRIV-5.01 a 5.06 |
| Art. 9º | Informação ao titular | PRIV-4.05, 9.01 a 9.03 |
| Art. 10 | Legítimo interesse | PRIV-6.01 a 6.04 |
| Arts. 11–13 | Dados sensíveis, anonimização, pesquisa | PRIV-7.01 a 7.05, 13.01 a 13.04 |
| Art. 14 | Crianças e adolescentes | PRIV-8.01 a 8.06 |
| Arts. 15–16 | Término do tratamento | PRIV-11.01 a 11.08 |
| Arts. 17–22 | Direitos do titular | PRIV-10.01 a 10.09, 14.01 a 14.04 |
| Arts. 23–32 | Poder público | PRIV-21.01 a 21.03 |
| Arts. 33–36 | Transferência internacional | PRIV-16.01 a 16.04 |
| Arts. 37–40 | Agentes de tratamento | PRIV-1.02, 2.04, 15.01, 15.06 |
| Art. 41 | Encarregado | PRIV-18.01 a 18.03 |
| Arts. 42–45 | Responsabilidade e ressarcimento | PRIV-15.05 |
| Arts. 46–49 | Segurança e sigilo | PRIV-12.01 a 12.08, pilar Security |
| Art. 48 | Comunicação de incidentes | PRIV-17.01 a 17.07 |
| Arts. 50–51 | Boas práticas e governança | PRIV-20.01 a 20.04 |
| Arts. 52–54 | Sanções | PRIV-23.01 a 23.03 |
| Lei 15.211/2025 | ECA Digital | PRIV-8.01, 8.05, 8.06 |
| Lei 12.965/2014 | Marco Civil | PRIV-11.04, 22.01 |

---
## AI Readiness

> **Objetivo do pilar:** o repositório permite que agentes de IA (Claude Code, Codex, Copilot, Cursor e similares) localizem contexto rápido, gastem poucos tokens, gerem código que compila, passa nos testes, respeita a arquitetura, performa e não introduz vulnerabilidades — e que **erros do agente sejam pegos por máquinas antes de chegar a humanos**.
>
> **Regra de ouro:** tudo que você precisaria dizer a um engenheiro novo mais de uma vez deve estar (a) num arquivo de contexto curto, (b) numa skill carregada sob demanda, ou (c) — de preferência — codificado como teste, lint ou tipo que falha automaticamente. Instrução em prosa é a camada mais fraca; invariante executável é a mais forte.
>
> **Escopo:** este pilar avalia o **repositório e o fluxo de engenharia**. Recursos de IA da própria aplicação (chatbot, RAG, agentes para usuários) são avaliados em SEC-10, PERF-11 e PRIV-14.

### 1. Arquivos de contexto e instruções

- [ ] ✎ **AIR-1.01 · Ponto de entrada único e curto** `[B]` — existe `AGENTS.md` na raiz (padrão aberto mantido pela Agentic AI Foundation/Linux Foundation) com: objetivo do sistema em poucas linhas, mapa de diretórios, stack e versões, comandos essenciais (instalar, rodar, testar, lintar, buildar), restrições inegociáveis e links para a fonte de verdade. É curto (referência de mercado: até ~150 linhas na raiz) — não uma enciclopédia.
- [ ] 🆕 **AIR-1.02 · Compatibilidade entre ferramentas** `[M]` — ferramentas que leem arquivos próprios (ex.: `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursor/rules`, `GEMINI.md`) apontam para o `AGENTS.md` (import, symlink ou referência) em vez de manter cópias divergentes.
- [ ] ✎ **AIR-1.03 · Instruções no escopo correto** `[A]` — regras globais, por stack, por pacote e por padrão de arquivo estão separadas; `AGENTS.md` aninhado (ex.: `frontend/AGENTS.md`, `infra/AGENTS.md`) ou regras com escopo por glob são usados quando necessário. Instruções não duplicam nem contradizem umas às outras.
- [ ] 🆕 **AIR-1.04 · Instruções verificadas** `[A]` — comandos, caminhos e versões citados nos arquivos de contexto são testados automaticamente em CI (ex.: script que executa os comandos documentados e verifica que os caminhos existem). Arquivo de contexto que descreve estrutura que não existe mais é pior que nenhum.
- [ ] 🆕 **AIR-1.05 · Instruções acionáveis e específicas** `[M]` — regras dizem o **que fazer** e **como verificar** (“use `pnpm test --filter <pacote>`; nunca rode a suíte inteira localmente”), com exemplos de código bom/ruim do próprio repositório; sem frases genéricas (“escreva código limpo”). Cada regra tem motivo curto, para que o agente generalize corretamente.
- [ ] 🆕 **AIR-1.06 · Proteção dos arquivos de contexto** `[A]` — `AGENTS.md`, skills, regras e configuração de ferramentas de agente estão sob CODEOWNERS e exigem revisão humana, pois alterá-los muda o comportamento de todos os agentes (vetor de ataque e de degradação).

### 2. Skills, comandos e ferramentas para agentes

- [ ] 🆕 **AIR-2.01 · Skills para procedimentos recorrentes** `[A]` — tarefas repetitivas e com passos específicos (criar endpoint, criar migration segura, adicionar feature flag, criar componente com testes, investigar regressão de performance, atualizar dependência) estão empacotadas como skills (`SKILL.md` + scripts/referências, padrão Agent Skills) carregadas sob demanda, em vez de inflar o arquivo de contexto global.
- [ ] 🆕 **AIR-2.02 · Geradores e scaffolding determinísticos** `[M]` — estruturas padronizadas (módulo, endpoint, teste, migration) são criadas por gerador/script do repositório, não “de memória” pelo agente, garantindo conformidade com convenções.
- [ ] 🆕 **AIR-2.03 · Servidores MCP e ferramentas com privilégio mínimo** `[A]` *(Se: agentes usam MCP/ferramentas externas)* — servidores MCP configurados no repositório são inventariados, de fonte confiável, com versão pinada, escopo mínimo (somente leitura por padrão, ambiente não produtivo) e credenciais próprias de baixo privilégio.
- [ ] 🆕 **AIR-2.04 · Documentação de bibliotecas na versão correta** `[M]` — o agente tem acesso à documentação das versões **efetivamente usadas** das dependências principais (documentação versionada no repositório, links pinados por versão ou ferramenta de documentação atualizada), reduzindo código baseado em APIs obsoletas aprendidas no treinamento.
- [ ] 🆕 **AIR-2.05 · Hooks automáticos** `[M]` — hooks da ferramenta de agente e/ou de Git executam formatação, lint e checagens rápidas após edições e antes de commit, de modo que o agente receba feedback sem precisar lembrar de rodar.

### 3. Conhecimento de negócio e documentação

- [ ] ✎ **AIR-3.01 · Contexto de negócio** `[A]` — o repositório descreve personas, invariantes de negócio, regras, permissões (matriz de autorização — ver SEC-3.01), eventos, estados e integrações. Termos de domínio são consistentes entre código, docs, API e banco (glossário).
- [ ] ✎ **AIR-3.02 · Documentação de arquitetura** `[A]` — há `README`, `ARCHITECTURE` (componentes, fronteiras, fluxos de dados, decisões principais), decisões registradas (ADRs), contratos, esquema de dados e fluxos críticos versionados junto ao código.
- [ ] ✎ **AIR-3.03 · Documentação otimizada para recuperação** `[M]` — documentos são em Markdown limpo, com títulos descritivos, seções curtas e autocontidas, frontmatter/metadata (owner, data de revisão, status), links relativos e um índice; isso favorece tanto a busca do agente quanto indexação semântica interna.
- [ ] 🆕 **AIR-3.04 · Requisitos não funcionais explícitos** `[A]` — budgets de performance, requisitos de segurança e de privacidade relevantes ao código (o que é dado pessoal, o que não pode ser logado, timeouts padrão, limites de payload) estão documentados de forma que o agente os encontre ao alterar a área correspondente.

### 4. Código legível por agentes

- [ ] ✎ **AIR-4.01 · Arquitetura com fronteiras verificáveis** `[A]` — módulos têm responsabilidades claras, dependências direcionais, interfaces explícitas e pontos de extensão previsíveis. Camadas e boundaries são verificados por lint/testes estruturais (ex.: regras de import, testes de arquitetura). Não há imports circulares nem abstrações opacas.
- [ ] 🆕 **AIR-4.02 · Localizabilidade** `[M]` — nomes de arquivos, funções e símbolos são descritivos e consistentes, permitindo achar o código por busca textual; uma regra de negócio tem um dono identificável; não há a mesma lógica duplicada em vários lugares.
- [ ] 🆕 **AIR-4.03 · Tamanho de arquivos e funções** `[M]` — arquivos e funções muito grandes são evitados (limites definidos por lint), pois forçam o agente a ler muito contexto para mudanças pequenas e aumentam conflitos.
- [ ] 🆕 **AIR-4.04 · Código gerado e vendorizado isolado** `[M]` — código gerado, vendorizado, minificado e snapshots grandes ficam em diretórios marcados, não são editados manualmente (cabeçalho “gerado — não editar”) e são regeneráveis por comando documentado.
- [ ] 🆕 **AIR-4.05 · Código morto e caminhos legados removidos** `[M]` — código morto, flags expiradas e implementações paralelas antigas são removidos; caso convivam, estão marcados como obsoletos com o substituto indicado — senão o agente copia o padrão errado.
- [ ] 🆕 **AIR-4.06 · Padrões de referência** `[M]` — para cada tipo de artefato comum (endpoint, consulta, componente, job, teste), há um exemplo canônico apontado nas instruções (“siga `src/orders/` como referência”).

### 5. Contratos e tipos na fronteira

- [ ] **AIR-5.01 · Contratos e tipos na fronteira** `[A]` — entradas de HTTP, eventos, filas, arquivos, banco e terceiros são parseadas/validadas na fronteira; schemas, tipos, OpenAPI/GraphQL, migrations e exemplos estão sincronizados (gerados de uma fonte única ou verificados em CI). Erros, nulabilidade, unidades, timezone, idempotência e compatibilidade de versão são explícitos.
- [ ] 🆕 **AIR-5.02 · Tipagem estrita** `[A]` — type checker em modo estrito (ou equivalente da linguagem) roda em CI; uso de escapes (`any`, `# type: ignore`, `@ts-ignore`, casts não verificados) é limitado por lint e exige justificativa.
- [ ] 🆕 **AIR-5.03 · Testes de contrato** `[M]` — contratos entre serviços e com o frontend são verificados por testes (consumer-driven ou schema diff), de modo que o agente detecte quebra de compatibilidade ao alterar uma API.

### 6. Feedback executável

- [ ] ✎ **AIR-6.01 · Comandos curtos e determinísticos** `[B]` — instalar, formatar, lintar, testar, buildar, subir localmente, popular dados e validar funcionam em ambiente limpo com um comando cada (ex.: `make check`, `pnpm verify`), documentados no `AGENTS.md`. Um único comando de verificação completa local existe.
- [ ] 🆕 **AIR-6.02 · Checagens direcionadas e rápidas** `[A]` — é possível rodar lint, tipos e testes de um pacote/arquivo isolado em segundos; o agente não precisa rodar a suíte inteira a cada mudança. Tempos são medidos.
- [ ] 🆕 **AIR-6.03 · Saída legível por máquina e por agente** `[M]` — falhas de lint, teste e build exibem arquivo, linha, causa e correção esperada, sem ruído excessivo (modo silencioso/resumido disponível), economizando tokens na leitura de logs.
- [ ] 🆕 **AIR-6.04 · Ambiente reproduzível de desenvolvimento** `[A]` — dev container, Nix, Docker Compose ou equivalente sobe dependências (banco, cache, fila) com dados de exemplo versionados; nenhum passo manual não documentado é necessário.
- [ ] **AIR-6.05 · Reprodutibilidade e dependências** `[A]` — versões de runtime, package manager, lockfiles, toolchains, containers e serviços locais estão fixadas ou possuem política de atualização. Builds são determinísticos, fixtures e seeds são versionados, migrations são reversíveis. Dependências e actions são pinadas, escaneadas e atualizadas por automação.

### 7. Testes como especificação

- [ ] **AIR-7.01 · Cobertura de comportamento** `[A]` — há testes unitários, integração, contrato, e2e e de propriedades para caminhos felizes, erros, autorização, concorrência, limites e regressões; regras de negócio críticas têm cobertura explícita. Testes podem ser executados por pacote/arquivo e apontam (nome/descrição) para a regra que protegem.
- [ ] 🆕 **AIR-7.02 · Testes confiáveis** `[A]` — testes são determinísticos (sem dependência de horário, rede externa, ordem de execução), rápidos e sem flakiness conhecida não tratada; um teste vermelho significa problema real — senão o agente aprende a ignorar falhas.
- [ ] 🆕 **AIR-7.03 · Utilitários de teste** `[M]` — factories/builders de dados, fixtures e helpers de autenticação por papel facilitam escrever testes corretos; existe exemplo de teste para cada camada.
- [ ] 🆕 **AIR-7.04 · Qualidade dos testes medida** `[R]` — além de cobertura, a efetividade dos testes é avaliada (ex.: mutation testing em módulos críticos), evitando testes gerados que passam sem verificar nada.
- [ ] 🆕 **AIR-7.05 · Teste antes de corrigir** `[M]` — o fluxo documentado para bugs é: reproduzir com teste que falha → corrigir → teste passa. As instruções do agente exigem isso.

### 8. Guardrails de qualidade, segurança e performance

- [ ] ✎ **AIR-8.01 · Invariantes codificados** `[B]` — formatter, linter, type checker, política de dependências, SAST, secret scanning, SCA, testes de segurança, budgets de performance e testes de arquitetura falham o CI quando invariantes são violadas. Mensagens de lint indicam a correção esperada. O princípio é codificar invariantes e permitir liberdade local.
- [ ] 🆕 **AIR-8.02 · Regras para erros típicos de agentes** `[A]` — há regras de lint/checagem para erros frequentes de código gerado no contexto do projeto: chamada de rede sem timeout (PERF-4.07), query sem paginação/limite, `SELECT *`, concatenação em SQL, log de objetos inteiros (vazamento de PII), uso de API obsoleta interna, dependências novas não aprovadas, desabilitação de verificação TLS, segredos no código, `eval`/`innerHTML`.
- [ ] 🆕 **AIR-8.03 · Política de dependências novas** `[A]` — adicionar dependência exige justificativa e passa por checagem automática (licença, manutenção, vulnerabilidades, tamanho de bundle, existência real do pacote — proteção contra pacotes “alucinados”/slopsquatting).
- [ ] 🆕 **AIR-8.04 · Áreas protegidas** `[A]` — mudanças em autenticação, autorização, criptografia, migrations destrutivas, CI/CD, IaC, arquivos de contexto de agentes e dependências exigem revisão humana de owner específico (CODEOWNERS) e checks adicionais.
- [ ] 🆕 **AIR-8.05 · Gates de performance no PR** `[M]` — tamanho de bundle, contagem de queries por endpoint, tempo de testes de benchmark e tamanho de imagem são comparados com a branch principal no PR (ver PERF-8.12), tornando regressões geradas por agentes visíveis.

### 9. Economia de contexto e tokens

- [ ] ✎ **AIR-9.01 · Contexto progressivo** `[A]` — o agente começa por poucas páginas (arquivo de contexto + índice) e segue referências conforme a tarefa; documentação longa é dividida e carregada sob demanda (skills, docs por domínio); não se injeta o repositório inteiro no prompt.
- [ ] 🆕 **AIR-9.02 · Exclusão de ruído** `[A]` — arquivos irrelevantes para raciocínio (lockfiles, builds, `dist/`, `node_modules`, vendorizados, minificados, fixtures e snapshots grandes, datasets, binários, logs) estão excluídos da indexação/leitura do agente via arquivos de ignore suportados pelas ferramentas.
- [ ] 🆕 **AIR-9.03 · Monorepo navegável** `[M]` *(Se: monorepo)* — o mapa de pacotes indica responsabilidade e dono de cada pacote; ferramentas de workspace permitem operar num pacote isolado; instruções por pacote evitam que o agente leia o repositório inteiro.
- [ ] 🆕 **AIR-9.04 · Tamanho dos artefatos de contexto monitorado** `[M]` — o tamanho somado dos arquivos de contexto sempre carregados é medido em CI com limite; crescimento exige revisão (mover para skill ou doc sob demanda).
- [ ] 🆕 **AIR-9.05 · Respostas de ferramentas enxutas** `[R]` — scripts e comandos usados pelo agente têm modo de saída resumida (ex.: apenas falhas, apenas diff), evitando despejar milhares de linhas no contexto.

### 10. Segurança do uso de agentes no repositório

> Referência: OWASP Top 10 for Agentic Applications 2026 (aplicado ao próprio fluxo de desenvolvimento).

- [ ] ✎ **AIR-10.01 · Execução isolada e privilégio mínimo** `[B]` — agentes rodam em sandbox (container, VM ou ambiente remoto efêmero) ou em worktree/branch isolada, sem segredos de produção, sem credenciais pessoais amplas, com permissões explícitas de comandos (allowlist) e com acesso de rede restrito ao necessário (registries de pacotes, documentação).
- [ ] 🆕 **AIR-10.02 · Ações que exigem humano** `[B]` — push para branch protegida, merge, deploy, execução de migrations em ambientes compartilhados, alteração de infraestrutura, publicação de pacotes e operações destrutivas exigem aprovação humana; o agente não tem credenciais para fazê-las sozinho.
- [ ] ✎ **AIR-10.03 · Injeção de instruções via conteúdo do repositório** `[A]` — o fluxo assume que issues, comentários de PR, documentos, dependências, páginas web e saídas de ferramentas podem conter instruções maliciosas para o agente; agentes que processam conteúdo externo (ex.: triagem automática de issues públicas) rodam com permissões mínimas e sem acesso a segredos ou escrita em branches protegidas.
- [ ] 🆕 **AIR-10.04 · Segredos fora do alcance** `[A]` — `.env` e arquivos de credenciais locais estão bloqueados para leitura pelo agente (configuração de ignore/permissões); exemplos usam `.env.example` sem valores reais; secret scanning roda em todo commit gerado.
- [ ] 🆕 **AIR-10.05 · Cadeia de suprimento de agentes** `[A]` — extensões, plugins, skills e servidores MCP de terceiros são revisados antes do uso, pinados por versão e tratados como código não confiável.
- [ ] 🆕 **AIR-10.06 · Rastreabilidade de mudanças geradas** `[M]` — commits/PRs gerados ou coassinados por agentes são identificáveis (trailer, label ou autor), permitindo análise de qualidade e auditoria.
- [ ] 🆕 **AIR-10.07 · Política de uso de IA no desenvolvimento** `[A]` — está definido quais ferramentas e provedores são aprovados, que dados podem ser enviados a eles (código proprietário, dados pessoais de fixtures, logs de produção), retenção e uso para treinamento pelo provedor (preferência por contratos que vedam treinamento), alinhado a PRIV-14.05.

### 11. Observabilidade e ambiente operáveis pelo agente

- [ ] ✎ **AIR-11.01 · Ambiente isolado por tarefa** `[A]` — a aplicação sobe em worktree/ambiente isolado (portas e bancos independentes), permitindo trabalho paralelo de agentes sem conflito.
- [ ] ✎ **AIR-11.02 · Diagnóstico por comando** `[M]` — logs, métricas locais, traces, snapshots de DOM, screenshots e diagnósticos estão acessíveis por comandos documentados. O agente consegue reproduzir bug, observar causa, aplicar mudança e validar a métrica afetada.
- [ ] 🆕 **AIR-11.03 · Verificação de UI** `[R]` *(Se: frontend)* — existe forma automatizada de o agente abrir a aplicação, navegar e verificar resultado (testes e2e, browser automatizado, comparação visual), em vez de declarar “deve funcionar”.

### 12. Planos, memória e decisões

- [ ] **AIR-12.01 · Planos versionados para tarefas complexas** `[M]` — tarefas complexas têm plano com objetivo, não-objetivos, hipóteses, arquivos afetados, riscos, critérios de aceite e testes; planos são pequenos e atualizados durante a execução.
- [ ] ✎ **AIR-12.02 · Memória persistente fora do contexto efêmero** `[M]` — decisões concluídas (ADRs), dívida técnica, incidentes e “armadilhas conhecidas” são registrados em arquivos indexados; o agente retoma trabalho sem repetir descoberta.
- [ ] 🆕 **AIR-12.03 · Especificação antes do código** `[M]` — features relevantes começam por especificação curta com critérios de aceite verificáveis (que viram testes), reduzindo ambiguidade para o agente.

### 13. Workflow e revisão

- [ ] ✎ **AIR-13.01 · Workflows agent-friendly** `[A]` — template de PR exige intenção, escopo, risco, testes, impacto de performance/segurança/privacidade e evidência; PRs e commits são pequenos; CI publica artefatos e falhas de modo legível; ambientes efêmeros permitem preview por branch. O fluxo oferece checkpoints e rollback.
- [ ] ✎ **AIR-13.02 · Validação de resultado** `[B]` — antes de merge/deploy, agente e revisor humano verificam diff, dependências, migrations, autorização, dados sensíveis, performance, compatibilidade e observabilidade. Há testes negativos e revisão adversarial (inclusive revisão automatizada por segundo agente/ferramenta independente) para código gerado.
- [ ] 🆕 **AIR-13.03 · Tamanho de mudança limitado** `[M]` — há limite orientativo de tamanho de PR; mudanças grandes geradas por agente são divididas, pois revisão humana de diffs enormes é ineficaz.

### 14. Medição e melhoria contínua

- [ ] ✎ **AIR-14.01 · Métricas de efetividade** `[A]` — o time acompanha tempo para localizar contexto, taxa de aceitação/reversão de PRs gerados, defeitos e vulnerabilidades introduzidos, flakiness, custo de tokens por tarefa, duração do CI e retrabalho. O objetivo é reduzir incerteza e custo de contexto, mantendo qualidade, segurança, performance, privacidade e manutenção como critérios de saída.
- [ ] 🆕 **AIR-14.02 · Ciclo de aprendizado** `[A]` — cada erro recorrente de agente gera uma correção sistêmica: regra de lint, teste, tipo, skill ou ajuste de instrução — nesta ordem de preferência. Existe registro dessas melhorias.
- [ ] 🆕 **AIR-14.03 · Avaliação de tarefas de referência** `[R]` — um conjunto pequeno de tarefas representativas do repositório (ex.: “adicionar campo ao endpoint X com teste e migration”) é usado periodicamente para avaliar se mudanças em instruções, skills ou ferramentas melhoram ou pioram o resultado e o consumo de tokens.

---
## Anexo A — Registro de mudanças em relação à v2

> **Resumo:** nenhum item da v2 foi eliminado sem substituto. Todos os itens foram mantidos (com o texto original preservado ou enriquecido), divididos, fundidos ou movidos para o pilar correto. As únicas supressões de conteúdo foram **trechos** com premissa incorreta ou exemplo de fornecedor, listados em A.5 com o motivo.

### A.1 Itens divididos

| Item v2 | Itens v3 | Motivo |
|---|---|---|
| Performance §1 “Teste de capacidade e Chaos Engineering” | PERF-1.09, PERF-1.10 | São práticas distintas, com evidências distintas (modelo de capacidade vs. experimento de falha). Num único item, atender uma e não a outra impedia marcar o status com precisão. |
| Performance §6 “Índices de filtro e Locks/Deadlocks” | PERF-6.17, PERF-6.34 | Indexação e concorrência são temas sem relação; misturados, o item não era pontuável. |
| Security §4 “NoSQL/GraphQL Abuse” | SEC-4.03 (NoSQL) + SEC-5.15 (GraphQL) | A parte GraphQL duplicava o item “GraphQL” de §5; foi consolidada lá. |
| Security §5 “CORS e Subdomain Takeover” | SEC-5.02, SEC-5.03 | Controles diferentes (configuração HTTP vs. higiene de DNS), owners diferentes. |
| Security §5 “CSP e headers” | SEC-5.04, SEC-5.05 | CSP estrita exige avaliação própria; os demais headers são checagem objetiva. |
| Security §5 “Cookies e armazenamento” | SEC-5.07, SEC-5.08 | Atributos de cookie e armazenamento no cliente são verificados de forma distinta. |
| Security §7 “Dependências e Dependency Confusion” | SEC-7.09, SEC-7.10 | Gestão de vulnerabilidades conhecidas (SCA) e ataques à cadeia de pacotes têm controles diferentes. |
| Security §8 “Disaster Recovery” | SEC-8.06, SEC-8.07 | DRP e resiliência de backups a ataque (ransomware) merecem verificação separada. |
| AI Readiness “Segurança contra Prompt Injection para agentes” | AIR-10.01, AIR-10.03 (agentes no repositório) + SEC-10.01 (aplicação) | O item misturava a segurança do **agente que programa** com a segurança da **funcionalidade de IA da aplicação**. |
| Privacy — os 15 itens da v2 | PRIV-1 a PRIV-24 | Cada item agregava vários artigos da LGPD; foram decompostos por dispositivo legal para que cada lacuna seja identificável individualmente (ver matriz de cobertura no fim do pilar Privacy). O conteúdo original foi preservado nos itens marcados ✎. |

### A.2 Itens fundidos

| Itens v2 | Item v3 | Motivo |
|---|---|---|
| Performance §5 “Pools e limites (Connection Pool Exhaustion)” (parte de banco) + §6 “Pool de conexões” | PERF-6.37 (banco) e PERF-5.06 (demais pools) | Pool de banco aparecia duas vezes; agora há um item para banco e outro para os demais recursos. |
| Security §4 parte GraphQL + Security §5 “GraphQL” | SEC-5.15 | Duplicidade. |

### A.3 Itens movidos de pilar ou seção

| Item v2 | Destino v3 | Motivo |
|---|---|---|
| Security §1 “Modelagem de Ameaças em Nuvem (CSPM)” | SEC-7.05 “Postura de nuvem (CSPM)” | CSPM é verificação contínua de configuração, não modelagem de ameaças; o título original era tecnicamente impreciso. A proteção de metadados (IMDSv2) continua exigida e também referenciada em SEC-4.08. |
| AI Readiness “Circuit Breakers de IA e Degradação Graciosa” | PERF-11.02 | Trata do comportamento em runtime da aplicação que chama modelos, não da prontidão do repositório para agentes. |
| AI Readiness “Contexto de negócio e RAG Readiness” (parte RAG dos dados da aplicação) | PERF-11.07 e SEC-10.05; parte de documentação permanece em AIR-3.01 e AIR-3.03 | A preparação de dados da aplicação para RAG é funcionalidade do produto. |
| AI Readiness “AI responsável e Gestão de Dados (Opt-Out)” | PRIV-14.05, PRIV-14.06 (privacidade), SEC-10.08 (inventário de modelos), AIR-10.07 (política de uso no desenvolvimento) | Opt-out e base legal para uso de dados em IA são obrigações de privacidade sobre dados de titulares; não medem prontidão do repositório. |

### A.4 Itens reformulados (conteúdo corrigido ou atualizado)

| Item | Mudança | Motivo |
|---|---|---|
| PERF-4.06 (ex-“Edge Computing”) | Tornado condicional; validação de token na borda passa a ser **filtro adicional**, nunca substituto da autorização na origem. | A redação original tornava obrigatória arquitetura de edge para todas as aplicações e podia induzir a confiar apenas na borda (risco de BFLA/BOLA se a origem for alcançável). |
| PERF-4.05 “HTTP e transporte” | HTTP/3 condicionado ao suporte da borda; inclusão de TLS 1.3, reuso de conexão entre serviços e zstd. | Precisão técnica. |
| PERF-6.04 “Chaves e identificadores” | Inclui avaliação de IDs ordenáveis no tempo (UUIDv7/ULID) versus UUIDv4. | Impacto conhecido de IDs aleatórios em índices B-tree grandes. |
| SEC-1.04 “ASVS” | Fixada a versão 5.0.0 e a exigência de decisões de segurança documentadas. | A v2 pedia para “fixar versão” sem indicar a atual. |
| SEC-2.02 “Senha” | Alinhado ao NIST SP 800-63B-4 (comprimento, sem composição arbitrária, sem troca periódica forçada). | Atualização normativa. |
| SEC-2.06 “JWT” | Alinhado à RFC 8725; inclui `jku`, `x5u`, `jwk`, `typ`. | Cobrir vetores conhecidos não listados. |
| SEC-2.09 “OAuth/OIDC” | Alinhado à RFC 9700 (OAuth 2.0 Security BCP); PKCE para todos os clientes; sem implicit/password grant. | Atualização normativa. |
| SEC-5.15 “GraphQL” | Introspection desabilitada para APIs privadas; para APIs públicas, permitida como decisão documentada. | “Estritamente desabilitada” é inadequado para APIs GraphQL públicas por design; o controle relevante é o conjunto de limites e autorização por campo. |
| SEC-14.06 “Severidade” | Metodologia declarada (CVSS v4.0 com métricas de ambiente) e avaliação de encadeamento. | Padronização e rigor. |
| PRIV-17.03 “Incidentes” | Explicita comunicação à ANPD **e** aos titulares, conteúdo mínimo e registro de 5 anos (Res. 15/2024). | Completude regulatória. |
| PRIV-16.02 “Transferência internacional” | Inclui Res. 19/2024 (cláusulas-padrão sem alteração, prazo encerrado em 23/08/2025) e Res. 32/2026 (UE/EEE adequados). | Atualização regulatória. |
| PRIV-8.01/8.05 “Crianças e adolescentes” | Inclui o ECA Digital (vigente desde 17/03/2026) e o conceito de acesso provável. | Nova lei aplicável. |
| PRIV-19.01 “RIPD” | Mantida a exigência; registrado que o regulamento específico ainda é tema da agenda regulatória e adotados os critérios de alto risco da Res. 2/2022 como referência. | A v2 afirmava obrigação “antes do início” de forma absoluta; a lei obriga quando a ANPD determina e no legítimo interesse sob solicitação — a elaboração prévia para alto risco é mantida como boa prática exigida pelo checklist. |

### A.5 Trechos suprimidos

| Trecho v2 | Motivo da supressão |
|---|---|
| “inputs do usuário fornecidos ao modelo de IA passam por sanitização prévia (ex: NeMo Guardrails) para evitar jailbreaks” | Premissa incorreta: sanitização de texto **não** impede prompt injection de forma confiável; manter o trecho levaria a marcar “Atende” com um controle insuficiente. Substituído por defesa em camadas em SEC-10.01. A menção a um produto específico foi removida para manter o checklist neutro em relação a fornecedores. |
| “A introspecção do GraphQL é estritamente desabilitada em produção” (redação absoluta) | Ver A.4 (SEC-5.15). |

### A.6 Principais adições por pilar

- **Performance:** sistema de limiares de referência (Core Web Vitals no p75 de campo), error budget, RUM com atribuição, estratégia de renderização/hidratação, scripts de terceiros, runtime ciente de container, linhas quentes, inventário de consultas reais e regressão de plano, timeouts de banco, separação OLTP/OLAP, operações em massa, flaky tests, execução apenas do necessário no CI, FinOps e workloads de IA.
- **Security:** autenticação resistente a phishing, step-up, integridade de valores de negócio, acesso a objetos armazenados, prototype pollution, e-mail/SPF/DKIM/DMARC, cache poisoning/deception, SRI, webhooks, criptografia em nível de campo, criptoagilidade/pós-quântico, imagens base, ataques à cadeia de pacotes, proteção de borda, conteúdo mínimo de eventos de auditoria, backups resilientes a ransomware, e quatro seções novas: **superfície exposta**, **LLM/agentes**, **tratamento de exceções** (A10:2025) e **gestão de vulnerabilidades**, além de mobile condicional.
- **Privacy:** decomposição por artigo, matriz de cobertura LGPD, porte do agente, verificação do inventário contra o sistema real, prova e aplicação técnica do consentimento, legítimo interesse, vedações de dados sensíveis, ECA Digital, cookies e session replay, prazos do art. 19, propagação de correções, Marco Civil, anonimização vs. pseudonimização, revisão de decisões automatizadas, transferência internacional atualizada, registro de incidentes, poder público, normas setoriais e prontidão para fiscalização.
- **AI Readiness:** interoperabilidade de arquivos de contexto, verificação automática das instruções, skills, MCP com privilégio mínimo, documentação versionada de bibliotecas, hooks, regras de lint para erros típicos de agentes, política de dependências novas (pacotes inexistentes), exclusão de ruído de contexto, segurança do uso de agentes, rastreabilidade de commits gerados e ciclo de aprendizado.

---

## Anexo B — Roteiro sugerido de execução

1. **Inventários primeiro:** SEC-1.01 (ativos), PRIV-2.01 (dados), SEC-5.11 (APIs), PERF-6.13 (consultas reais). Sem inventário, os demais itens não podem ser verificados com completude.
2. **Varredura dos `[B]`:** executar todos os itens bloqueantes dos quatro pilares; corrigir antes de avançar.
3. **Automação:** transformar em checagem de CI tudo que for automatizável (scans, budgets, testes de autorização, testes de consentimento por captura de rede, verificação de comandos do `AGENTS.md`).
4. **Itens `[A]`, depois `[M]` e `[R]`.**
5. **Reteste e score:** recalcular o score conforme a seção 0.3 e anexar evidências.
6. **Contratar o pentest/auditoria** com o relatório deste checklist como insumo, para que o avaliador externo concentre esforço em lógica de negócio, encadeamento de falhas e ataques criativos — onde ele agrega mais valor.

---

## Anexo C — Ferramentas de apoio (exemplos, não exaustivo)

| Área | Exemplos |
|---|---|
| Performance web | Lighthouse, WebPageTest, Chrome DevTools (Performance, Coverage), biblioteca `web-vitals`, RUM do provedor de observabilidade |
| Carga | k6, Gatling, Locust, JMeter |
| Observabilidade | OpenTelemetry, Prometheus, Grafana, Jaeger/Tempo, profilers contínuos (Pyroscope/Parca ou equivalente) |
| Banco | `EXPLAIN (ANALYZE, BUFFERS)`, `pg_stat_statements`, `auto_explain`, Query Store, Performance Schema, pgBadger |
| SAST / segredos | Semgrep, CodeQL, gitleaks, TruffleHog, push protection do provedor Git |
| SCA / SBOM / containers | OSV-Scanner, Trivy, Grype, Syft, Dependabot/Renovate |
| DAST / pentest | OWASP ZAP, Burp Suite, Nuclei, ffuf, sqlmap (com autorização) |
| Infra / nuvem | Checkov, tfsec/Trivy config, kube-bench, kube-score, Prowler/ScoutSuite, CSPM do provedor |
| Supply chain | OpenSSF Scorecard, Sigstore/cosign, verificação de proveniência SLSA |
| TLS / headers | testssl.sh, verificadores de headers e de CSP |
| Privacidade | Captura HAR/proxy para inventário de terceiros, scanners de cookies, ferramentas de data discovery/classificação de PII |
| IA (aplicação) | Suítes de red teaming e avaliação de LLM (ex.: garak, promptfoo ou equivalentes) |
