# Catálogo de critérios — Performance

> Gerado a partir do *Checklist sênior para assessment de aplicações — v3* (outubro/2026). Não edite à mão: regenere com `python -X utf8 scripts/gen-assessment-catalog.py` no ai-toolbox (fonte: `docs/application-assessment-v3.md`). IDs, severidades e critérios são a base do score e precisam ser estáveis entre execuções.

**Severidade (fixa por item):** `[B]` Bloqueante → **Crítico** (peso 3) · `[A]` Alto → **Importante** (peso 2) · `[M]` Médio e `[R]` Recomendado → **Menor** (peso 1).

**Itens condicionais** (*Se: …*): quando a condição não se aplica, marque **N/A com justificativa e evidência** (ex.: busca no código sem ocorrências). N/A sem evidência conta como Não compliant.

**Total de itens:** 163 — Crítico: 9 · Importante: 82 · Menor: 72. Pontuação máxima (todos aplicáveis): 263.

## Objetivo do pilar

> **Objetivo do pilar:** a aplicação responde rápido no p75/p95/p99 real (não só no laboratório), roda bem em dispositivos antigos e redes ruins, consome o mínimo de CPU/memória/disco/rede no servidor e no cliente, escala de forma previsível, degrada com controle e entrega software sem desperdício no pipeline.
>
> **Regra de ouro:** “rápido” só vale com número, percentil, população, ambiente e baseline. Médias isoladas, uma única execução e testes em máquina de desenvolvedor não são evidência.

## PERF-1. Governança, orçamento e critérios de aceite

**Como verificar:** Procure `docs/` (SLO, budgets, capacidade, baseline), arquivos de config de budget (`.size-limit*`, `lighthouserc*`, `budget.json`), steps de CI que comparam métricas. SLO/budget só em texto sem fonte de dados ou gate = Parcial no máximo.

#### PERF-1.01 · SLOs por jornada
**Crítico** (peso 3, origem `[B]`)  
existem SLOs por jornada crítica, endpoint, operação assíncrona e dependência, com p50/p75/p95/p99, erro, throughput, disponibilidade, saturação e custo; médias não são usadas isoladamente. Cada SLO possui owner, janela, fonte de dados e ação quando violado.

#### PERF-1.02 · Política de error budget
**Importante** (peso 2, origem `[A]`)  
está definido o que acontece quando o error budget se esgota (congelamento de features, priorização de confiabilidade, revisão de release). A política é aplicada de fato: há registro de pelo menos uma decisão tomada com base nela ou de simulação.

#### PERF-1.03 · Limiares de referência para web
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: há frontend web*  
metas no p75 de dados de campo, por rota e por classe de dispositivo: LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1, TTFB ≤ 0,8 s. Metas mais rígidas são definidas para jornadas de conversão. Desvios são aceitos apenas com justificativa e prazo.

#### PERF-1.04 · Orçamentos de performance
**Importante** (peso 2, origem `[A]`)  
há budgets versionados para JavaScript/CSS/imagens/fontes, tamanho de payload, número de requests, TTFB, LCP, INP, CLS, cold start, queries por request, CPU, memória e duração de pipeline. CI falha ou exige aprovação quando o budget piora.

#### PERF-1.05 · Orçamento de terceiros
**Menor** (peso 1, origem `[M]`)  
scripts e SDKs de terceiros (analytics, chat, A/B, ads, pixels) têm budget próprio de bytes, tempo de main thread e requests, com owner de negócio. Novo terceiro só entra com medição antes/depois.

#### PERF-1.06 · Baseline reproduzível
**Importante** (peso 2, origem `[A]`)  
o baseline registra commit, dataset, ambiente, região, hardware, navegador, rede, temperatura do cache, número de usuários e versão de dependências. Benchmarks usam repetição suficiente, percentis e margem de erro (intervalo de confiança), não uma execução isolada.

#### PERF-1.07 · Dados de campo como fonte de verdade
**Importante** (peso 2, origem `[A]`)  
decisões usam RUM (Real User Monitoring) e/ou dados de campo agregados, segmentados por dispositivo, navegador, rede, região e versão. Testes de laboratório (Lighthouse, WebPageTest, k6 etc.) servem para diagnóstico e regressão, não para declarar conformidade.

#### PERF-1.08 · Perfil de usuários e dispositivos
**Importante** (peso 2, origem `[A]`)  
testes incluem dispositivos antigos (classe de entrada com 2–4 GB de RAM e CPU lenta, ou throttling de CPU 4–6× como proxy documentado), browsers suportados, telas pequenas, acessibilidade, baixa bateria/modo economia, rede 2G/3G/4G, alta latência, perda de pacotes e modo offline/intermitente quando aplicável. A matriz de suporte é publicada e coerente com o analytics real.

#### PERF-1.09 · Modelo de capacidade
**Importante** (peso 2, origem `[A]`)  
existe modelo de capacidade que relaciona RPS, concorrência, tamanho de payload, latência e consumo de recursos. Estão documentados ponto de saturação, capacidade segura, degradação, headroom, custo marginal e comportamento durante autoscaling. O modelo é revisado a cada mudança relevante de arquitetura ou crescimento de tráfego.

#### PERF-1.10 · Engenharia de caos e injeção de falhas
**Menor** (peso 1, origem `[M]`)  
injetam-se falhas controladas (latência artificial, perda de nó/zona, dependência lenta, disco cheio, DNS falhando) com hipótese, raio de impacto limitado, critério de abortar e registro de resultado. Experimentos rodam primeiro fora de produção e só em produção com guardrails aprovados.

#### PERF-1.11 · Performance como regressão
**Importante** (peso 2, origem `[A]`)  
PRs e releases com impacto mensurável executam benchmark ou teste representativo e comparam contra baseline. Exceções são justificadas, têm prazo e não permitem acumular regressões silenciosas.

#### PERF-1.12 · Custo unitário como requisito
**Menor** (peso 1, origem `[M]`)  
existe métrica de custo por transação/usuário/tenant (infraestrutura, banco, CDN, terceiros, telemetria). Mudanças que aumentam o custo unitário acima de um limite exigem aprovação, assim como regressões de latência.

## PERF-2. Observabilidade e rastreabilidade de performance

**Como verificar:** Procure instrumentação (`@opentelemetry/*`, `instrumentation.ts`, exporters, `prom-client`), logger estruturado e seus campos, dashboards/alertas como código (`*.json` Grafana, regras Prometheus, monitores Datadog/Terraform), RUM (`web-vitals`). Ausência de qualquer telemetria além de logs = Não atende na maioria dos itens.

#### PERF-2.01 · Métricas RED e USE
**Crítico** (peso 3, origem `[B]`)  
cada serviço expõe Rate, Errors e Duration por rota/versão/status, além de Utilization, Saturation e Errors por CPU, memória, disco, rede, threads, conexões, filas e pools. Labels têm cardinalidade controlada e não incluem IDs arbitrários.

#### PERF-2.02 · Padrão de instrumentação
**Menor** (peso 1, origem `[M]`)  
instrumentação segue um padrão aberto (ex.: OpenTelemetry com semantic conventions) para nomes de métricas, spans e atributos, de modo que dashboards, alertas e consultas funcionem entre serviços sem tradução manual.

#### PERF-2.03 · Métricas de negócio
**Importante** (peso 2, origem `[A]`)  
jornadas críticas possuem contadores de início, sucesso, falha, retry, abandono, timeout e degradação. É possível relacionar queda de conversão, aumento de abandono ou atraso operacional à mudança técnica correspondente sem coletar dados pessoais desnecessários.

#### PERF-2.04 · Logs estruturados
**Importante** (peso 2, origem `[A]`)  
logs incluem timestamp sincronizado (NTP), ambiente, versão, região, serviço, operação, status, duração, tamanho, retry, dependência e `trace_id`, com níveis coerentes. Não há log em excesso, PII ou segredo; sampling e retenção são explicitamente definidos. Logging é assíncrono/bufferizado e não bloqueia o caminho crítico.

#### PERF-2.05 · Tracing distribuído
**Importante** (peso 2, origem `[A]`)  
requisições atravessam browser, CDN, gateway, serviço, fila, worker, banco e terceiros com propagação de contexto (ex.: W3C Trace Context). Spans registram duração, status, eventos de retry/timeout e atributos seguros. Jobs assíncronos preservam vínculo (span links) entre requisição originadora e execução.

#### PERF-2.06 · Sampling e custo de telemetria
**Menor** (peso 1, origem `[M]`)  
sampling head/tail, retenção, agregação e exportação são dimensionados; erros, p99 e transações lentas têm prioridade. A observabilidade não consome CPU, memória, disco ou banda suficientes para alterar o comportamento medido (overhead medido e documentado).

#### PERF-2.07 · Profiling contínuo e eBPF
**Menor** (peso 1, origem `[M]`)  
CPU, heap, alocações, locks, I/O, GC, event loop, off-CPU e eBPF/profiling equivalente são acessíveis em produção com controles. Perfis são comparáveis por release e permitem atribuir custo a função, query, rota e dependência.

#### PERF-2.08 · Correlação ponta a ponta
**Importante** (peso 2, origem `[A]`)  
dado um `trace_id`, o assessor encontra request, spans, logs, métricas (via exemplars), query, evento de fila, deploy e incidente relacionados. Não existem múltiplos IDs sem mapa de correlação nem componentes que quebrem o contexto.

#### PERF-2.09 · RUM com atribuição
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: há frontend web*  
o RUM coleta LCP, INP, CLS, TTFB e tarefas longas com atribuição (elemento LCP, interação e script responsável pelo INP, frame longo via Long Animation Frames ou equivalente), segmentado por rota, versão e dispositivo, com consentimento quando exigido.

#### PERF-2.10 · Monitoramento sintético
**Menor** (peso 1, origem `[M]`)  
jornadas críticas são executadas periodicamente de múltiplas regiões, em dispositivo/rede emulados representativos, para detectar regressões antes do usuário e fora do horário de pico.

#### PERF-2.11 · Dashboards acionáveis
**Menor** (peso 1, origem `[M]`)  
há dashboards por jornada, serviço, endpoint, dependência, região, versão e tenant quando permitido. Painéis mostram percentis, volume, erro, saturação, filas, cache hit ratio, pool, GC, cold start e custo; cada alerta tem runbook e owner.

#### PERF-2.12 · Alertas sem ruído
**Importante** (peso 2, origem `[A]`)  
alertas usam SLO/burn rate multi-janela, saturação e sintomas de usuário; evitam limiares fixos sem contexto e duplicidade. Existe teste de alerta, rota de escalonamento, deduplicação, manutenção e revisão periódica de falsos positivos e falsos negativos.

#### PERF-2.13 · Rastreabilidade de mudanças
**Importante** (peso 2, origem `[A]`)  
deploy, feature flag, configuração, migration, alteração de índice, dependência e mudança de infraestrutura aparecem como eventos anotados nas séries e traces. É possível comparar antes/depois e atribuir regressão a commit, release ou rollout.

#### PERF-2.14 · Dados de telemetria seguros
**Importante** (peso 2, origem `[A]`)  
IDs, query text, headers e atributos são mascarados ou pseudonimizados; sampling não captura tokens, conteúdo de requisição ou dados sensíveis. Retenção, acesso, exportação e exclusão da telemetria são auditáveis. *(Ver também SEC-6.08 e PRIV-12.)*

## PERF-3. Cliente, navegador e renderização

**Como verificar:** Inspecione o frontend: estratégia de render por rota (RSC/SSR/CSR), `next/image`/`srcset`, `loading="lazy"`, `fetchpriority`, fontes (`next/font`, WOFF2), `next.config.*` (headers de cache, compressão), bundle analyzer, virtualização de listas, uso de `useEffect` para buscar dados iniciais. Se não há frontend web, marque N/A com o inventário como justificativa.

*(Se: há frontend web. Para apps mobile nativos, aplicar o equivalente: tempo de startup frio/quente, jank, frames congelados, ANR, tamanho do app, consumo de bateria e de dados.)*

#### PERF-3.01 · Caminho crítico de renderização
**Importante** (peso 2, origem `[A]`)  
HTML, CSSOM, DOM, fontes e JavaScript críticos estão identificados; recursos não críticos não bloqueiam a primeira renderização. O waterfall não apresenta cadeias evitáveis de dependências, redirects, fontes bloqueantes ou scripts síncronos.

#### PERF-3.02 · Estratégia de renderização
**Importante** (peso 2, origem `[A]`)  
a escolha entre SSR, SSG, ISR, streaming SSR, islands/hidratação parcial ou CSR é justificada por rota. Não se envia uma SPA inteira para páginas majoritariamente estáticas; a hidratação não duplica trabalho já feito no servidor nem bloqueia a interação.

#### PERF-3.03 · Dicas de recurso e priorização
**Menor** (peso 1, origem `[M]`)  
`preconnect` apenas para origens críticas, `preload` para recursos críticos não descobríveis, `fetchpriority` no recurso LCP e rebaixado em recursos secundários, `103 Early Hints` quando suportado. Não há excesso de preload competindo por banda.

#### PERF-3.04 · LCP
**Importante** (peso 2, origem `[A]`)  
o elemento LCP é identificado por rota e dispositivo; seu recurso é descobrível no HTML, priorizado, dimensionado, comprimido e servido próximo ao usuário. TTFB, atraso de carregamento do recurso, duração de download e atraso de renderização são medidos separadamente. O LCP não é imagem com lazy loading nem depende de JavaScript para aparecer.

#### PERF-3.05 · INP e tarefas longas
**Importante** (peso 2, origem `[A]`)  
interações críticas são medidas no dispositivo real; tarefas acima de 50 ms, handlers pesados, hidratação, parsing e compilação são localizados e otimizados. O trabalho é particionado (ex.: `scheduler.yield`/yield ao event loop), cancelável, adiado ou movido para worker sem bloquear a thread principal. Feedback visual ocorre no próximo frame após a interação.

#### PERF-3.06 · CLS e estabilidade visual
**Importante** (peso 2, origem `[A]`)  
dimensões de imagens, vídeos, anúncios, iframes e fontes são reservadas; componentes não inserem conteúdo acima do viewport sem ação do usuário; fontes não causam saltos (métricas de fallback ajustadas, ex.: `size-adjust`). Testes cobrem carregamento lento e conteúdo personalizado.

#### PERF-3.07 · JavaScript enviado
**Importante** (peso 2, origem `[A]`)  
bundle inicial, chunks, dependências, polyfills, tags e código não utilizado são medidos por rota. Tree shaking, code splitting e carregamento sob demanda são eficazes; bibliotecas pesadas não são usadas quando APIs nativas resolvem o caso. O build é direcionado à matriz de browsers suportada (sem transpilar/polyfillar para browsers fora da matriz).

#### PERF-3.08 · Scripts de terceiros
**Importante** (peso 2, origem `[A]`)  
tags de terceiros carregam de forma assíncrona/adiada, atrás de consentimento quando aplicável, preferencialmente via facade (ex.: player de vídeo e chat carregados na interação) ou fora da main thread. Falha ou lentidão de terceiro não bloqueia render nem interação.

#### PERF-3.09 · DOM e layout
**Menor** (peso 1, origem `[M]`)  
tamanho do DOM, estilo computado, layout, paint e compositing são medidos. Não há layout thrashing, seletores patológicos, re-renderização de árvore inteira, listeners duplicados ou animações em propriedades que forçam layout/paint excessivo; animações usam `transform`/`opacity` e respeitam `prefers-reduced-motion`. `content-visibility` é considerado para seções longas fora da tela.

#### PERF-3.10 · Re-renderização e estado no cliente
**Menor** (peso 1, origem `[M]`)  
o gerenciamento de estado não provoca re-render global a cada mudança; seletores, memoização e granularidade de componentes são verificados com profiler do framework. Não há fetch/efeito disparado em loop por dependências instáveis.

#### PERF-3.11 · Memória do cliente
**Importante** (peso 2, origem `[A]`)  
heap snapshots e testes longos não mostram crescimento contínuo por navegação, modal, lista, rota, listener, timer, subscription ou cache. Imagens, blobs, workers e object URLs são liberados no ciclo de vida correto. Uso de memória é testado em dispositivo de baixa RAM.

#### PERF-3.12 · Listas e dados grandes
**Importante** (peso 2, origem `[A]`)  
tabelas, feeds, árvores e selects usam paginação, virtualização, janela de renderização e busca incremental quando necessário. Ordenação/filtro não processa o dataset inteiro no cliente sem justificativa.

#### PERF-3.13 · Imagens e mídia
**Importante** (peso 2, origem `[A]`)  
dimensões responsivas, `srcset`/`sizes`, formatos modernos de alta compressão (AVIF, WebP) com fallback, compressão, lazy loading (exceto acima da dobra) e prioridade estão corretos. Não há imagem maior que o viewport, thumbnail gerada no cliente sem necessidade, vídeo sem streaming adaptativo ou pré-carregamento de mídia não crítica. GIFs animados são substituídos por vídeo.

#### PERF-3.14 · Fontes e CSS
**Menor** (peso 1, origem `[M]`)  
fontes são subsetadas, em WOFF2, com fallback, `font-display` adequado, preload apenas das críticas, e não bloqueiam a interface; CSS é dividido por rota, minificado e livre de regras mortas; CSS crítico é inline quando compensa. Não há framework de estilos inteiro enviado para poucas classes.

#### PERF-3.15 · Cache do browser e bfcache
**Importante** (peso 2, origem `[A]`)  
assets imutáveis usam hash no nome e `Cache-Control: max-age` longo + `immutable`; HTML/API usam política coerente; navegações compatíveis usam bfcache (sem `unload`, sem `Cache-Control: no-store` desnecessário). Headers são verificados em rede real e invalidação não exige limpar cache manualmente.

#### PERF-3.16 · Navegação antecipada
**Menor** (peso 1, origem `[R]`)  
prefetch/prerender (ex.: Speculation Rules) é usado em navegações de alta probabilidade, com regras conservadoras, sem disparar efeitos colaterais (analytics, mutações) e com medição de taxa de acerto versus custo.

#### PERF-3.17 · Service worker e offline
**Menor** (peso 1, origem `[M]`) · Condicional — *Se: há service worker/PWA*  
estratégia de cache por tipo de recurso (cache-first para estáticos versionados, network-first/stale-while-revalidate para dados), tamanho limitado, versionamento e limpeza de caches antigos. O service worker não adiciona latência à navegação (navigation preload) nem serve versão quebrada após deploy.

#### PERF-3.18 · Compatibilidade progressiva
**Menor** (peso 1, origem `[M]`)  
recursos de baixa capacidade possuem fallback; APIs são detectadas por feature detection; testes cobrem versões mínimas, Safari/Firefox/Chromium, zoom, teclado e preferências de movimento. Falha de terceiro não bloqueia a função primária.

#### PERF-3.19 · Respeito a dispositivo e rede restritos
**Menor** (peso 1, origem `[R]`)  
a aplicação reduz trabalho quando detecta economia de dados (`Save-Data`), rede lenta ou baixa memória: menos prefetch, mídia de menor qualidade, menos animação.

## PERF-4. Rede, API e comunicação

**Como verificar:** Procure clientes HTTP (`fetch`, `axios`, `undici`, SDKs) e verifique timeout/`AbortSignal`, retry com backoff+jitter, circuit breaker, limites de payload, paginação/projeção nas respostas, compressão e `Cache-Control`. Toda chamada de rede sem timeout explícito torna PERF-4.07 Não atende.

#### PERF-4.01 · Waterfall e latência de rede
**Importante** (peso 2, origem `[A]`)  
DNS, conexão, TLS, TTFB, download, fila do browser, redirects, CDN e terceiros são separados em métricas. O diagnóstico identifica se a latência é cliente, rede, gateway, aplicação, banco ou fornecedor.

#### PERF-4.02 · Quantidade de requisições
**Importante** (peso 2, origem `[A]`)  
não há chamadas duplicadas, cascatas evitáveis, polling agressivo, refresh redundante ou requests para dados invisíveis. Deduplicação de requests concorrentes idênticos existe no cliente. Prefetch só ocorre quando a taxa de acerto justifica o custo e possui cancelamento.

#### PERF-4.03 · Agregação de chamadas (BFF/batching)
**Menor** (peso 1, origem `[M]`)  
telas que dependem de muitas chamadas usam BFF, endpoint agregado ou batching, evitando N round-trips do cliente, especialmente em redes móveis. O agregador paraleliza chamadas internas e tem timeout global.

#### PERF-4.04 · Payload e serialização
**Importante** (peso 2, origem `[A]`)  
respostas são paginadas, filtráveis, selecionáveis por campo e comprimidas; JSON não carrega metadados ou coleções desnecessárias. Serialização/deserialização é perfilada e formatos binários/streaming são considerados para dados grandes. Existe limite máximo de payload por request e por response.

#### PERF-4.05 · HTTP e transporte
**Importante** (peso 2, origem `[A]`)  
HTTP/2 e, quando suportado pela borda, HTTP/3 (QUIC); multiplexação, keep-alive e reuso de conexão entre serviços; TLS 1.3 com resumption; compressão Brotli (ou zstd onde suportado) para texto, gzip como fallback, sem comprimir formatos já comprimidos; `Cache-Control`, `ETag`/`If-None-Match`, range requests e CDN conforme o caso. Não há desabilitação global de compressão, conexões por request ou headers impedindo cache útil.

#### PERF-4.06 · Uso da borda (edge/CDN)
**Menor** (peso 1, origem `[M]`) · Condicional — *Se: há CDN/edge*  
conteúdo estático, respostas públicas cacheáveis, redirects e roteamento simples são resolvidos na borda para reduzir TTFB e carga na origem. Validação de token na borda é aceita **apenas como filtro adicional**: a autorização definitiva continua na origem (ver SEC-3.05). Chave de cache na CDN é normalizada (query strings irrelevantes, cookies e `Vary`) e o hit ratio é monitorado.

#### PERF-4.07 · Timeouts por dependência
**Crítico** (peso 3, origem `[B]`)  
cada chamada possui timeout de conexão, leitura e total baseado em orçamento de latência. O deadline é propagado e menor que o timeout do chamador; operações expiradas são canceladas para não continuar consumindo recursos. Não existe chamada de rede sem timeout explícito (verificado por lint ou revisão de código).

#### PERF-4.08 · Retries seguros
**Importante** (peso 2, origem `[A]`)  
retry tem limite, backoff exponencial com jitter, classificação de erros (retentável vs. não retentável), orçamento de retry por serviço e idempotência. Não há retry em cascata em todas as camadas, retry de operação não idempotente ou tempestade após recuperação de dependência. `Retry-After` é respeitado.

#### PERF-4.09 · Concorrência e backpressure
**Importante** (peso 2, origem `[A]`)  
limites por cliente, rota e dependência impedem explosão de concorrência. Filas, semáforos, bulkheads e circuit breakers protegem recursos; o sistema rejeita (429/503 com `Retry-After`) ou enfileira trabalho de forma previsível quando saturado, priorizando tráfego crítico (load shedding por prioridade).

#### PERF-4.10 · Streaming e respostas parciais
**Menor** (peso 1, origem `[M]`)  
downloads, exports, relatórios e eventos grandes usam streaming ou processamento incremental quando possível. O servidor não acumula o resultado inteiro em memória e o cliente trata cancelamento, reconexão e progresso. Exports grandes são assíncronos (job + notificação + link expirável).

#### PERF-4.11 · Terceiros
**Importante** (peso 2, origem `[A]`)  
cada fornecedor possui orçamento de latência, timeout, quota, cache/fallback e métrica separada. Scripts, APIs, pagamentos, e-mail, mapas e analytics não bloqueiam jornadas não relacionadas; custo por chamada e impacto de falha são conhecidos.

#### PERF-4.12 · Contratos de API
**Menor** (peso 1, origem `[M]`)  
contratos definem limites de tamanho, paginação, ordenação, campos, status, compressão, versionamento e compatibilidade. Mudanças não obrigam clientes lentos a baixar ou processar campos novos sem necessidade.

#### PERF-4.13 · Custo de consulta em APIs flexíveis
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: GraphQL, OData ou filtros dinâmicos*  
consultas têm custo calculado (profundidade, complexidade, aliases, tamanho de listas) e limite por cliente; persisted queries/allowlist são usadas para clientes próprios; resolvers usam batching (DataLoader) para evitar N+1.

#### PERF-4.14 · Tempo real eficiente
**Menor** (peso 1, origem `[M]`) · Condicional — *Se: WebSocket, SSE, long polling*  
conexões têm heartbeat, limite por usuário, fan-out eficiente (pub/sub), mensagens compactas e reconexão com backoff; o servidor suporta o número alvo de conexões simultâneas com memória medida por conexão.

#### PERF-4.15 · Webhooks e integrações de saída
**Menor** (peso 1, origem `[M]`)  
envio de webhooks é assíncrono, com fila, retry com backoff, timeout curto, limite de concorrência por destino e desativação automática de destinos persistentemente falhos, para que um parceiro lento não degrade a plataforma.

## PERF-5. Backend, runtime e concorrência

**Como verificar:** Verifique código síncrono pesado no request (`fs.*Sync`, crypto síncrono, parsing grande), uso de workers/filas, idempotência de mutações, graceful shutdown (`SIGTERM` + fechamento de conexões), configuração de container (limites, número de workers), feature flags.

#### PERF-5.01 · Event loop/threads/workers
**Importante** (peso 2, origem `[A]`)  
I/O não bloqueia thread principal; CPU-bound usa worker/processo apropriado; pool tem tamanho, fila e timeout. São medidos event-loop lag, thread starvation, context switch e tarefas em espera. Não há chamadas síncronas de arquivo, crypto ou parsing pesado no caminho do request.

#### PERF-5.02 · Runtime ciente de container
**Importante** (peso 2, origem `[A]`)  
o runtime respeita limites do container (ex.: heap da JVM proporcional ao limite, `GOMAXPROCS`/`GOMEMLIMIT` no Go, número de workers em Python/Node calculado sobre CPU alocada, não sobre CPU do host). Não há OOMKill ou throttling de CPU recorrente não explicado.

#### PERF-5.03 · Inicialização e cold start
**Importante** (peso 2, origem `[A]`)  
startup mede carregamento de módulos, migrations, conexão, cache warming, configuração e health check. Não há trabalho de negócio ou conexão sequencial desnecessária antes de aceitar tráfego; readiness só ocorre quando dependências essenciais estão prontas; migrations não rodam no startup de cada réplica.

#### PERF-5.04 · Alocação e GC
**Menor** (peso 1, origem `[M]`)  
heap, alocações temporárias, cópias, serialização, pausas de GC e fragmentação são medidos sob carga. Objetos de grande porte, caches sem limite, closures e buffers são investigados como causa de picos.

#### PERF-5.05 · Caminho quente (hot path)
**Menor** (peso 1, origem `[M]`)  
as funções mais custosas por CPU e alocação (segundo o profiler) são conhecidas e otimizadas: sem regex recompilada por request, sem serialização repetida, sem logging com interpolação cara em nível desativado, sem reflexão desnecessária.

#### PERF-5.06 · Pools e limites de recursos
**Importante** (peso 2, origem `[A]`)  
pools de HTTP, Redis, workers, sockets, file descriptors e threads têm limites coerentes com a capacidade do downstream. O sistema mede espera, uso, rejeições, timeout e vazamento. *(Pool de banco tratado em PERF-6.37.)*

#### PERF-5.07 · Idempotência e duplicidade
**Importante** (peso 2, origem `[A]`)  
retries, mensagens duplicadas, refresh, double submit e reprocessamentos não geram trabalho ou efeitos duplicados. Chaves de idempotência têm escopo, retenção e custo controlados.

#### PERF-5.08 · Processamento assíncrono
**Importante** (peso 2, origem `[A]`)  
tarefas longas saem do request síncrono; filas têm tamanho, idade da mensagem mais antiga, throughput, concorrência, prioridade, retry, DLQ e consumidores monitorados. Não há fila infinita mascarando saturação; DLQ tem alerta e processo de reprocessamento.

#### PERF-5.09 · Agrupamento de escritas e trabalho
**Menor** (peso 1, origem `[M]`)  
escritas frequentes e pequenas (contadores, eventos, métricas, logs de auditoria) são agrupadas (batch, buffer, coalescência) quando a consistência permite, reduzindo round-trips e contenção.

#### PERF-5.10 · Serialização interna
**Menor** (peso 1, origem `[M]`)  
objetos são convertidos e copiados apenas quando necessário; schemas são eficientes; payloads internos não carregam campos que nenhum consumidor utiliza. Compressão só é aplicada quando o custo de CPU compensa a economia de rede/disco.

#### PERF-5.11 · Isolamento de vizinhos ruidosos
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: multi-tenant*  
um tenant não consegue degradar os demais: quotas, rate limits, filas e pools por tenant ou por classe de tenant; trabalho pesado de um cliente é isolado (fila própria, prioridade menor).

#### PERF-5.12 · Feature flags
**Menor** (peso 1, origem `[M]`)  
flags não introduzem dois caminhos caros simultâneos, consultas duplicadas ou avaliação remota síncrona no caminho crítico (avaliação local com cache). Flags antigas são removidas com prazo e rollout permite comparação por coorte, versão e métrica.

#### PERF-5.13 · Graceful degradation
**Importante** (peso 2, origem `[A]`)  
falha de cache, terceiro, região ou feature opcional não derruba a jornada essencial. Fallback tem custo, timeout, observabilidade e teste; não há fallback que faz full scan ou tempestade de requests.

#### PERF-5.14 · Shutdown e deploy
**Importante** (peso 2, origem `[A]`)  
graceful shutdown drena conexões e filas, respeita deadline, evita perda/duplicação de mensagens e remove instâncias do balanceador antes de parar. Rolling/blue-green/canary não concentra cold starts nem reduz headroom abaixo do necessário.

## PERF-6. Banco de dados e modelagem

**Como verificar:** Leia o schema (Prisma/ORM/migrations) e todas as queries (repositories). Para Mongo, os equivalentes são `explain('executionStats')`, índices em `@@index`/`createIndex`, profiler e `$indexStats`. Procure N+1 (query dentro de loop/`Promise.all` por item), `findMany` sem `take`, `select` ausente (overfetch), `skip` profundo, transações amplas, pool/`connection_limit`, migrations destrutivas. Itens que exigem dados de produção (plano real, inventário de consultas) só atendem com evidência versionada.

### 6.1 Modelagem

#### PERF-6.01 · Cardinalidade
**Importante** (peso 2, origem `[A]`)  
cardinalidades 1:1, 1:N e N:N refletem o domínio e os padrões reais; estimativas de volume, crescimento, distribuição e skew estão documentadas. Consultas e índices são avaliados para baixa e alta cardinalidade, não apenas dataset pequeno.

#### PERF-6.02 · Distribuição e seletividade
**Importante** (peso 2, origem `[A]`)  
colunas filtradas têm distribuição conhecida; histogramas/estatísticas capturam skew e valores populares; estatísticas estendidas (correlação entre colunas) existem onde o planner erra. O planner não escolhe plano ruim por estatísticas obsoletas, amostra insuficiente ou parâmetro que muda seletividade.

#### PERF-6.03 · Tipos de dados
**Menor** (peso 1, origem `[M]`)  
tipos têm menor representação suficiente, precisão, timezone e semântica correta. Não há texto onde inteiro/enum/data apropriado reduziria armazenamento e custo, nem conversões implícitas que impedem índice.

#### PERF-6.04 · Chaves e identificadores
**Importante** (peso 2, origem `[A]`)  
PK/FK são adequadas, compactas e indexadas conforme uso (FKs usadas em join/delete têm índice). A geração de IDs não cria hotspots nem fragmentação: IDs aleatórios (UUIDv4) em índices B-tree grandes são avaliados contra alternativas ordenáveis no tempo (UUIDv7, ULID, sequência) — considerando também a exposição de IDs previsíveis (SEC-3.02). Relações exigem integridade referencial sem cascatas destrutivas inesperadas.

#### PERF-6.05 · Normalização
**Menor** (peso 1, origem `[M]`)  
repetição de dados, anomalias de atualização e inconsistências foram avaliadas. Normalização reduz escrita e inconsistência sem obrigar joins excessivos em jornadas críticas; decisões de desnormalização têm justificativa e mecanismo de sincronização.

#### PERF-6.06 · Desnormalização controlada
**Menor** (peso 1, origem `[M]`)  
campos derivados, snapshots e documentos agregados possuem owner, evento de atualização, consistência aceitável, backfill, correção e estratégia para evitar dados obsoletos. Não há cópias sem contrato nem duplicação que aumenta custo de escrita sem ganho medido.

#### PERF-6.07 · Linhas quentes e contenção de escrita
**Importante** (peso 2, origem `[A]`)  
não há linha única atualizada por muitas transações concorrentes (contadores globais, saldo agregado, “última sequência”); usam-se contadores particionados, agregação assíncrona ou estruturas apropriadas.

#### PERF-6.08 · Exclusão lógica e multi-tenant em índices
**Menor** (peso 1, origem `[M]`)  
com soft delete, índices e constraints únicos consideram o filtro de ativos (ex.: índice parcial `WHERE deleted_at IS NULL`); em multi-tenant com tabela compartilhada, índices relevantes começam por `tenant_id` e consultas sempre o filtram.

#### PERF-6.09 · Dados semiestruturados
**Menor** (peso 1, origem `[M]`) · Condicional — *Se: JSON/JSONB/documentos*  
campos JSON consultados com frequência têm índice adequado (GIN, índice de expressão) ou são promovidos a colunas; documentos não crescem sem limite; atualização parcial não reescreve documentos enormes a cada mudança.

#### PERF-6.10 · Particionamento
**Menor** (peso 1, origem `[M]`) · Condicional — *Se: tabelas grandes*  
tabelas grandes são particionadas apenas quando filtro, retenção, manutenção ou distribuição se beneficia. Pruning ocorre nos planos; não há excesso de partições, partição padrão crescendo sem controle ou migrations que bloqueiam toda a tabela.

#### PERF-6.11 · Sharding/distribuição
**Menor** (peso 1, origem `[M]`) · Condicional — *Se: banco distribuído*  
chave de distribuição evita hotspots, joins cross-shard e scatter-gather desnecessário. Há medição de skew, rebalanceamento, consistência, transações distribuídas e impacto de consultas sem chave.

### 6.2 Planos e índices

#### PERF-6.12 · EXPLAIN
**Crítico** (peso 3, origem `[B]`)  
toda consulta crítica possui plano revisado; `EXPLAIN ANALYZE` (com buffers) ou equivalente usa dados representativos e identifica custo, rows estimadas versus reais, loops, scan, join, sort, memória e I/O. O plano é armazenado por versão para comparação.

#### PERF-6.13 · Inventário de consultas reais
**Importante** (peso 2, origem `[A]`)  
estatísticas de consultas em produção (ex.: `pg_stat_statements`, Query Store, Performance Schema, slow query log, `auto_explain`) estão habilitadas; as top consultas por tempo total, chamadas, I/O e variância são revisadas periodicamente e após cada release.

#### PERF-6.14 · Regressão de plano
**Importante** (peso 2, origem `[A]`)  
mudança de plano de consultas críticas (após deploy, analyze, upgrade de versão ou crescimento de dados) é detectada e alertada; existe procedimento para estabilizar o plano corrigindo a causa.

#### PERF-6.15 · Estimativa versus realidade
**Importante** (peso 2, origem `[A]`)  
divergências relevantes entre rows estimadas e reais são investigadas antes de tuning superficial. Estatísticas, correlação entre colunas, parâmetros, casts e distribuição são corrigidos; não se força hint sem explicar a causa.

#### PERF-6.16 · Prepared statements e cache de plano
**Menor** (peso 1, origem `[M]`)  
consultas usam prepared statements/parametrização; problemas de plano genérico versus plano específico (parameter sniffing) são conhecidos e tratados; o modo do pooler é compatível com prepared statements.

#### PERF-6.17 · Índices de filtro
**Crítico** (peso 3, origem `[B]`)  
predicados frequentes e seletivos possuem índices adequados, considerando ordem de colunas, igualdade/range, collation, NULL e operador.

#### PERF-6.18 · Índices compostos
**Importante** (peso 2, origem `[A]`)  
ordem de colunas segue padrões de filtro/ordenação/join; índices redundantes, prefixos cobertos e combinações impossíveis são removidos. Custo de escrita, tamanho, cache e manutenção são medidos.

#### PERF-6.19 · Índices parciais/funcionais/especializados
**Menor** (peso 1, origem `[M]`)  
índices parciais, funcionais, covering (`INCLUDE`), BRIN (séries temporais), GIN/GiST ou especializados são usados quando o predicado e o padrão justificam. Expressões da consulta coincidem com o índice; não há função/cast no campo que invalide o uso.

#### PERF-6.20 · Índices sem uso
**Menor** (peso 1, origem `[M]`)  
índices nunca ou raramente usados são identificados, considerando sazonalidade e réplicas; índices excessivos não consomem memória, disco e tempo de escrita sem benefício. Remoção ocorre com observação (ex.: tornar invisível antes de remover, onde suportado) e rollback.

#### PERF-6.21 · Full scan
**Importante** (peso 2, origem `[A]`)  
cada sequential/full scan em tabela grande é classificado como intencional ou defeito. Filtros ausentes, índice inadequado, baixa seletividade, estatística, cast e consulta dinâmica são verificados; scans inevitáveis usam janela, particionamento ou processamento controlado.

### 6.3 Forma das consultas

#### PERF-6.22 · N+1 e overfetching
**Crítico** (peso 3, origem `[B]`)  
traces e logs de query detectam padrão N+1 por endpoint e tamanho de coleção (idealmente com teste automatizado que falha se o número de queries por request crescer com N). A correção usa join, batch, eager loading seletivo, DataLoader ou consulta agregada sem transformar o problema em overfetch. O lazy loading padrão do ORM é conhecido e controlado.

#### PERF-6.23 · Joins desnecessários
**Menor** (peso 1, origem `[M]`)  
joins que não filtram, projetam ou garantem existência são removidos. O assessor verifica ORM que adiciona relações automaticamente, joins repetidos e tabelas incluídas apenas por conveniência.

#### PERF-6.24 · Joins redundantes
**Menor** (peso 1, origem `[M]`)  
o mesmo relacionamento não é acessado em consultas separadas ou subqueries equivalentes. CTEs, views e ORM não materializam/reexecutam trabalho sem necessidade; plano confirma eliminação ou compartilhamento eficaz.

#### PERF-6.25 · Joins cartesianos
**Importante** (peso 2, origem `[A]`)  
joins sem predicado, predicado incompleto ou multiplicação de linhas são testados com cardinalidades altas. O resultado não depende de `DISTINCT` para esconder duplicação; a causa é corrigida e o custo medido.

#### PERF-6.26 · Join order e algoritmo
**Menor** (peso 1, origem `[M]`)  
nested loop, hash join, merge join e ordem escolhida são adequados ao volume e seletividade. Memória de hash/sort evita spill para disco; `work_mem` ou equivalente é dimensionado sem causar OOM sob concorrência.

#### PERF-6.27 · Ordenações
**Menor** (peso 1, origem `[M]`)  
`ORDER BY` só ocorre quando exigido; ordem padrão não é aplicada automaticamente. Índice fornece ordem quando compensa; sort de grandes conjuntos tem limite, paginação por cursor/keyset e memória controlada.

#### PERF-6.28 · Paginação
**Importante** (peso 2, origem `[A]`)  
offsets profundos não percorrem milhões de linhas sem justificativa. Keyset/cursor, índice compatível, limite máximo e ordenação determinística (desempate por chave única) são usados; paginação não permite resposta ilimitada. `COUNT(*)` exato em tabelas grandes é evitado quando estimativa ou “há mais páginas” resolve.

#### PERF-6.29 · Agregações
**Menor** (peso 1, origem `[M]`)  
contagens, somas, agrupamentos e distinct são analisados quanto a scan, memória, spill e repetição. Pré-agregação, materialized view (com estratégia de refresh), cache ou janela temporal são usados quando o padrão justifica.

#### PERF-6.30 · Subqueries e CTEs
**Menor** (peso 1, origem `[M]`)  
subqueries correlacionadas, CTEs materializadas e views aninhadas são examinadas por reexecução e barreiras de otimização. A forma declarativa é comparada com join/window/batch usando plano real.

#### PERF-6.31 · SELECT e projeção
**Importante** (peso 2, origem `[A]`)  
a consulta retorna apenas colunas necessárias; blobs, JSON grande, texto e colunas sensíveis não são carregados por padrão. A camada de persistência oferece projeção explícita, não entidade completa em toda chamada. Não há `SELECT *` em código de produção.

#### PERF-6.32 · Filtros e sargabilidade
**Importante** (peso 2, origem `[A]`)  
predicados permitem uso de índice; funções, casts, `LIKE '%…'`, expressões e comparação de tipos diferentes não forçam scan. Alternativas por coluna normalizada, índice funcional ou busca especializada são avaliadas.

#### PERF-6.33 · Operações em massa
**Menor** (peso 1, origem `[M]`)  
cargas e atualizações em volume usam bulk insert/`COPY`/batch com tamanho de lote controlado, em vez de uma operação por linha; deletes/updates massivos são fatiados para não gerar locks longos, replicação atrasada ou bloat.

### 6.4 Concorrência, transações e conexões

#### PERF-6.34 · Locks e deadlocks
**Importante** (peso 2, origem `[A]`)  
locks adquiridos, duração, espera, deadlocks e contenção são observados. Há detecção de deadlocks, ordem consistente de aquisição de locks e retry seguro para transações abortadas por concorrência/serialização.

#### PERF-6.35 · Timeouts no banco
**Importante** (peso 2, origem `[A]`)  
existem timeouts de statement, lock e transação ociosa (ex.: `statement_timeout`, `lock_timeout`, `idle_in_transaction_session_timeout`) por papel de conexão; transações longas são alertadas, pois bloqueiam vacuum/compaction e seguram locks.

#### PERF-6.36 · Transações
**Importante** (peso 2, origem `[A]`)  
escopo transacional contém apenas operações necessárias; chamadas de rede, espera de usuário e processamento caro ficam fora. Isolamento é compatível com o caso; não se usa serializable/global lock por padrão.

#### PERF-6.37 · Pool de conexões do banco
**Crítico** (peso 3, origem `[B]`)  
tamanho considera número de réplicas, workers e capacidade do banco (conexões totais = réplicas × pool ≤ limite seguro do banco); espera e saturação são alertadas; pooler externo (ex.: PgBouncer, proxy gerenciado) é usado quando o número de instâncias é elástico. Não há pool por request, conexão vazando, transação devolvida ao pool aberta ou multiplexação incompatível.

#### PERF-6.38 · Replicação e leitura
**Menor** (peso 1, origem `[M]`) · Condicional — *Se: há réplicas*  
réplicas têm lag, capacidade e consistência monitorados. Leituras tolerantes a atraso são roteadas; leituras após escrita e decisões críticas usam garantia adequada. Failover não duplica escrita nem causa avalanche para o primário.

#### PERF-6.39 · Cache de banco
**Menor** (peso 1, origem `[M]`)  
cache de query/objeto/result set possui chave, TTL, invalidação, tamanho, stampede protection e métrica de hit/miss. Cache não mantém dados incorretos após escrita nem mascara degradação do banco.

### 6.5 Operação e ciclo de vida

#### PERF-6.40 · Retenção e arquivamento
**Importante** (peso 2, origem `[A]`)  
dados históricos são arquivados/particionados de forma que tabelas quentes permaneçam pequenas. Jobs de retenção são incrementais, limitados, observáveis e não bloqueiam o OLTP. *(Alinhar com PRIV-11.)*

#### PERF-6.41 · Migrations
**Crítico** (peso 3, origem `[B]`)  
migrations têm plano de lock, tempo estimado em volume de produção, compatibilidade expand/contract, backfill incremental, criação de índice online quando possível, `lock_timeout` curto, rollback/forward fix e impacto medido. Deploy não exige downtime inesperado nem faz alteração destrutiva antes de todos os consumidores migrarem. Migrations são testadas em cópia com volume realista.

#### PERF-6.42 · Disco e manutenção
**Importante** (peso 2, origem `[A]`)  
vacuum/compaction/analyze/reindex/checkpoint/autovacuum equivalentes são monitorados e ajustados por tabela quando necessário. Bloat, fragmentação, WAL/redo, risco de wraparound de IDs de transação, I/O e espaço livre têm alertas e capacidade; manutenção não coincide com picos sem planejamento.

#### PERF-6.43 · Carga do banco por endpoint
**Importante** (peso 2, origem `[A]`)  
observabilidade relaciona duração, rows, bytes, queries, locks e cache hit a rota, usuário técnico, release e trace (ex.: comentários SQL com `trace_id`/rota). É possível responder “qual endpoint gerou este pico?” sem inferência manual.

#### PERF-6.44 · Separação OLTP/OLAP
**Menor** (peso 1, origem `[M]`)  
relatórios pesados, analytics e exports não rodam no primário transacional; usam réplica dedicada, data warehouse, CDC ou store analítico, com latência de dados acordada.

#### PERF-6.45 · Busca especializada
**Menor** (peso 1, origem `[M]`)  
full-text, fuzzy, geoespacial, vetor ou analytics não são forçados no OLTP quando motor especializado reduz custo. Sincronização, consistência, reindexação, custo e fallback são explicitamente avaliados.

#### PERF-6.46 · Upgrade e versão do motor
**Menor** (peso 1, origem `[R]`)  
a versão do banco é suportada e recente o suficiente para não perder otimizações relevantes; upgrades são testados com comparação de planos antes/depois.

## PERF-7. Cache, armazenamento e recursos

**Como verificar:** Procure camadas de cache (Redis, `unstable_cache`, `revalidate`, CDN, headers), chaves/TTL/invalidação, proteção contra stampede, limites de recursos (quotas de upload, tamanho de arquivo), Dockerfile e manifestos de deploy/autoscaling.

#### PERF-7.01 · Estratégia de cache por camada
**Importante** (peso 2, origem `[A]`)  
browser, CDN, gateway, aplicação, objeto e banco têm propósito, TTL, chave, invalidação e fallback documentados; não há cache duplicado sem ganho medido.

#### PERF-7.02 · Cache stampede e stale-while-revalidate
**Importante** (peso 2, origem `[A]`)  
expiração simultânea, thundering herd, cache penetration e avalanche são testados. Há jitter no TTL, single-flight/request coalescing, stale-while-revalidate/stale-if-error, negative cache ou pré-aquecimento conforme o caso.

#### PERF-7.03 · Consistência
**Importante** (peso 2, origem `[A]`)  
stale data, escrita concorrente, invalidação fora de ordem e falha parcial têm comportamento definido. Cache não autoriza, não expõe tenant errado e não serve dado sensível fora do escopo (`Vary` e chave incluem identidade/tenant quando a resposta é personalizada). *(Ver SEC-5.16.)*

#### PERF-7.04 · Saúde do cache distribuído
**Menor** (peso 1, origem `[M]`) · Condicional — *Se: Redis/Memcached ou similar*  
memória, política de eviction, chaves grandes (big keys), chaves quentes (hot keys), latência de comandos e operações bloqueantes (ex.: varreduras completas de chaves) são monitoradas; comandos O(N) sobre conjuntos grandes são evitados.

#### PERF-7.05 · Disco e arquivos temporários
**Menor** (peso 1, origem `[M]`)  
uploads, exports, logs, dumps, thumbnails e temporários têm quota, streaming, cleanup, retenção e alerta de espaço. Processamento não lê arquivo inteiro em memória sem necessidade.

#### PERF-7.06 · Object storage/CDN
**Menor** (peso 1, origem `[M]`)  
objetos têm tamanho, multipart, compressão, cache e lifecycle (tiering para classes frias) adequados; URLs assinadas expiram; upload/download vai direto ao storage (pre-signed) sem passar desnecessariamente pelo servidor de aplicação.

#### PERF-7.07 · Limites de recursos
**Importante** (peso 2, origem `[A]`)  
CPU, memória, disco, sockets, threads, conexões, filas, payload e tempo possuem limites testados. O serviço falha de forma controlada e não cresce sem limite até travar o host.

#### PERF-7.08 · Container e runtime
**Menor** (peso 1, origem `[M]`)  
imagem final é mínima, camadas/cache são eficientes, requests e limits refletem perfil real medido, health/readiness não executam trabalho pesado e shutdown é gracioso. O container não usa swap/CPU sem observabilidade.

#### PERF-7.09 · Autoscaling
**Importante** (peso 2, origem `[A]`)  
escalonamento usa sinais de demanda e saturação (não apenas CPU), possui cooldown, máximo, mínimo e headroom. Métrica não reage tarde nem cria loop de scale-up/scale-down; warm-up e distribuição de carga são testados; o banco e dependências suportam o máximo de réplicas configurado.

## PERF-8. Build, CI/CD e entrega

**Como verificar:** Leia `.github/workflows/*` (ou equivalente): cache de dependências, `npm ci`, paralelismo, filtros por caminho, `concurrency`/cancelamento, gates de bundle/benchmark, Dockerfile multi-stage e `.dockerignore`, versões fixadas (`.nvmrc`, `engines`, `packageManager`).

#### PERF-8.01 · Cache de dependências
**Menor** (peso 1, origem `[M]`)  
package managers e imagens usam cache seguro, invalidado por lockfile e versão; instalação é determinística (`--frozen-lockfile`/`ci`); cache não mistura branches incompatíveis nem oculta instalação incompleta.

#### PERF-8.02 · Cache de build/teste remoto
**Menor** (peso 1, origem `[R]`)  
ferramentas de build incremental com cache remoto e hashing de entradas (ex.: Bazel, Nx, Turborepo, Gradle build cache) evitam recompilar e retestar o que não mudou; o cache é protegido contra envenenamento (escrita apenas por pipelines confiáveis).

#### PERF-8.03 · Paralelismo
**Menor** (peso 1, origem `[M]`)  
lint, unit, integration, build, scan e packaging independentes rodam em paralelo; dependências entre jobs são mínimas e explícitas; suítes longas usam sharding. O pipeline não espera por etapa que poderia iniciar antes.

#### PERF-8.04 · Execução apenas do necessário
**Menor** (peso 1, origem `[M]`)  
filtros por caminho evitam rodar jobs irrelevantes (ex.: mudança só de docs não roda e2e); execuções superadas por novo push no mesmo branch são canceladas automaticamente; merge queue evita revalidar o mesmo conteúdo várias vezes.

#### PERF-8.05 · Seleção incremental de testes
**Menor** (peso 1, origem `[M]`)  
testes por pacote/módulo/mudança são usados com uma suíte completa periódica. Grafo de dependências é correto; nenhum teste crítico é omitido por seleção excessiva.

#### PERF-8.06 · Artefatos
**Importante** (peso 2, origem `[A]`)  
build ocorre uma vez por commit e o mesmo artefato é promovido entre ambientes; não há rebuild divergente em staging/produção. Artefatos têm checksum, metadata e duração de retenção.

#### PERF-8.07 · Docker build
**Menor** (peso 1, origem `[M]`)  
contexto é pequeno (`.dockerignore`); ordem preserva cache; multi-stage separa build/test/runtime; base e dependências são mínimas; cache mounts para gerenciadores de pacote; imagem final contém apenas runtime e artefatos necessários.

#### PERF-8.08 · Reprodutibilidade
**Menor** (peso 1, origem `[M]`)  
versão de runtime, OS, compiler, package manager, timezone e flags são fixadas; dois builds equivalentes produzem resultado equivalente. Diferenças de ambiente são detectadas antes do deploy.

#### PERF-8.09 · Tempo de pipeline
**Menor** (peso 1, origem `[M]`)  
cada etapa tem duração, variância, cache hit, custo e owner. Jobs redundantes, downloads repetidos, ambientes recriados e testes flaky são eliminados ou isolados. Há meta explícita de tempo do PR até feedback (ex.: checks obrigatórios < 10–15 min).

#### PERF-8.10 · Testes instáveis (flaky)
**Importante** (peso 2, origem `[A]`)  
testes flaky são detectados automaticamente (retries registrados, taxa de falha intermitente), colocados em quarentena com owner e prazo, e não são “resolvidos” por retry silencioso que esconde problema real.

#### PERF-8.11 · Ambientes efêmeros com custo controlado
**Menor** (peso 1, origem `[R]`)  
ambientes de preview por branch têm TTL, tamanho mínimo, dados sintéticos e destruição automática.

#### PERF-8.12 · Gates de performance
**Importante** (peso 2, origem `[A]`)  
CI mede tamanho de bundle, query count, benchmark, tamanho de imagem, startup, latência e consumo conforme o componente; regressão exige aprovação explícita com justificativa.

## PERF-9. Carga, resiliência e diagnóstico

**Como verificar:** Procure scripts de carga (`k6`, `artillery`, `locust`, `tests/load`), relatórios de testes de stress/soak versionados, runbooks e postmortems em `docs/`. Script de carga sem dataset/resultado registrado = Parcial.

#### PERF-9.01 · Load test realista
**Crítico** (peso 3, origem `[B]`)  
workload usa distribuição de endpoints, think time, payloads, autenticação, cache frio/quente, tenants e dados representativos (volume próximo ao de produção, não base vazia). Resultado inclui p95/p99, erro, throughput, recursos e saturação por componente. O gerador de carga não é o gargalo (verificado).

#### PERF-9.02 · Stress e breakpoint
**Importante** (peso 2, origem `[A]`)  
carga cresce até degradação; identifica fila, timeout, OOM, lock, pool e cascata. O sistema mantém respostas controladas e recupera sem intervenção destrutiva.

#### PERF-9.03 · Soak e vazamento
**Importante** (peso 2, origem `[A]`)  
teste prolongado (horas) detecta crescimento de heap, handles, conexões, filas, logs, disco, cache e latência. A variação é comparada ao volume processado e ao ciclo de deploy.

#### PERF-9.04 · Picos e autoscaling
**Importante** (peso 2, origem `[A]`)  
bursts, cold start, scale-out, scale-in, rebalanceamento e perda de instância são testados. Não há perda de trabalho, duplicação, avalanche de conexões ou queda de SLO durante o ajuste.

#### PERF-9.05 · Falhas de dependência
**Importante** (peso 2, origem `[A]`)  
timeout, erro 5xx, resposta lenta, payload inválido, rate limit, DNS, indisponibilidade regional e resposta parcial têm teste. Fallback não piora o incidente nem produz dados incorretos.

#### PERF-9.06 · Performance em failover e DR
**Importante** (peso 2, origem `[A]`)  
failover de banco, troca de região e restauração de backup são medidos sob carga; o tempo real atinge o RTO e a capacidade do ambiente de destino suporta o tráfego. *(Ver SEC-8.06.)*

#### PERF-9.07 · Diagnóstico de regressão
**Importante** (peso 2, origem `[A]`)  
existe procedimento para comparar traces, perfis, planos de query, métricas, logs, deploys e flags entre janela boa e ruim. O time consegue chegar a causa provável sem depender de reprodução perfeita.

#### PERF-9.08 · Runbooks
**Importante** (peso 2, origem `[A]`)  
cada alerta de performance tem impacto, hipóteses, queries/dashboards, comandos seguros, mitigação reversível, critérios de escalonamento e ação pós-incidente. Runbooks são testados em exercício (game day).

#### PERF-9.09 · Postmortem de performance
**Menor** (peso 1, origem `[M]`)  
incidentes de latência/capacidade geram postmortem sem culpa, com causa raiz, teste de regressão e atualização de budget/SLO/capacidade.

## PERF-10. Eficiência de recursos e custo (FinOps)

**Como verificar:** Procure documentação/IaC de dimensionamento, políticas de lifecycle de storage, relatórios de custo versionados. Repositório sem infraestrutura própria: avalie o que está declarado em `deploy/`, `infra/`, docs de operação.

#### PERF-10.01 · Right-sizing
**Menor** (peso 1, origem `[M]`)  
requests/limits, tamanhos de instância, banco e cache são ajustados com base em uso medido (p95 de utilização), revisados periodicamente; não há recursos ociosos ou superdimensionados sem justificativa.

#### PERF-10.02 · Recursos órfãos
**Menor** (peso 1, origem `[M]`)  
volumes, snapshots, IPs, balanceadores, ambientes, buckets e filas sem uso são detectados automaticamente e removidos com processo.

#### PERF-10.03 · Tráfego de saída e entre zonas
**Menor** (peso 1, origem `[M]`)  
custo de egress, tráfego entre zonas/regiões e NAT é conhecido; comunicação intensa entre serviços evita cruzar zonas sem necessidade; respostas grandes usam CDN.

#### PERF-10.04 · Volume de telemetria
**Menor** (peso 1, origem `[M]`)  
volume e custo de logs, métricas e traces são acompanhados por serviço; logs de debug não ficam ligados em produção; métricas de alta cardinalidade são controladas.

#### PERF-10.05 · Armazenamento por camadas
**Menor** (peso 1, origem `[R]`)  
dados frios migram para classes de armazenamento mais baratas; backups e logs antigos seguem lifecycle; compressão é usada onde compensa.

#### PERF-10.06 · Capacidade elástica e barata para batch
**Menor** (peso 1, origem `[R]`)  
workloads tolerantes a interrupção (batch, CI, processamento assíncrono) avaliam instâncias preemptíveis/spot e arquiteturas de CPU com melhor custo-desempenho, com teste de compatibilidade.

## PERF-11. Workloads com IA/LLM *(Se: a aplicação chama modelos de IA)*

**Como verificar:** Procure chamadas a provedores de IA (`@anthropic-ai/sdk`, `openai`, `ai`, LangChain etc.). Se não houver, marque toda a seção N/A citando a busca feita. Se houver: streaming, `max_tokens`, timeout, retry, fallback, prompt caching, registro de tokens/custo.

#### PERF-11.01 · Latência percebida
**Importante** (peso 2, origem `[A]`)  
tempo até o primeiro token (TTFT), tokens por segundo e latência total são medidos por caso de uso; respostas longas usam streaming para o usuário; há indicador de progresso e possibilidade de cancelar (que interrompe a geração e o custo).

#### PERF-11.02 · Timeouts, limites e fallback de IA
**Importante** (peso 2, origem `[A]`)  
chamadas a modelos têm timeout, `max_tokens`, orçamento de contexto, retry com backoff para 429/5xx e circuit breaker. Se a IA demorar, falhar, exceder limites ou devolver saída fora do schema, a aplicação degrada graciosamente para fluxo tradicional/heurístico sem interromper a jornada. *(Movido de AI Readiness; ver também SEC-10.)*

#### PERF-11.03 · Economia de tokens em produção
**Importante** (peso 2, origem `[A]`)  
prompts têm tamanho controlado e versionado; prefixos estáveis aproveitam prompt caching do provedor; contexto recuperado (RAG) é limitado ao necessário; histórico de conversa é resumido/truncado; o modelo é escolhido por tarefa (modelos menores para tarefas simples, roteamento por complexidade).

#### PERF-11.04 · Cache de respostas e embeddings
**Menor** (peso 1, origem `[M]`)  
embeddings não são recalculados para conteúdo inalterado (hash de conteúdo); respostas determinísticas ou frequentes são cacheadas quando seguro, respeitando escopo de usuário/tenant e dados pessoais.

#### PERF-11.05 · Busca vetorial
**Menor** (peso 1, origem `[M]`) · Condicional — *Se: RAG/busca semântica*  
índice vetorial (ex.: HNSW/IVF) tem parâmetros ajustados com medição de recall versus latência; filtros por tenant/permissão são aplicados no índice e não depois de recuperar top-k (o que degrada recall e pode vazar dados); reindexação é incremental.

#### PERF-11.06 · Custo por requisição de IA
**Importante** (peso 2, origem `[A]`)  
tokens de entrada/saída e custo são registrados por funcionalidade, usuário/tenant e versão de prompt; há limite de gasto e alerta de anomalia; quotas por usuário impedem consumo abusivo.

#### PERF-11.07 · Dados da aplicação preparados para RAG
**Menor** (peso 1, origem `[M]`) · Condicional — *Se: RAG/busca semântica sobre dados da aplicação*  
o conteúdo indexado tem esquema semântico claro, texto limpo (sem ruído de HTML, navegação ou markup), chunking adequado ao tipo de documento, metadados de origem/data/permissão e deduplicação; a qualidade da recuperação é medida com um conjunto de perguntas de referência. *(Movido de AI Readiness: trata dos dados da aplicação, não do repositório.)*
