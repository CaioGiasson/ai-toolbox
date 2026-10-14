# Criteria catalog — Performance

> Derived from the *Senior checklist for application assessment — v3* (October 2026). This file is maintained directly in this repository. Item IDs, severities and criteria are the basis of the score and must stay stable between runs: changing an ID or a severity breaks score comparison across runs, so record any such change in the pull request.

**Severity (fixed per item):** `[B]` Blocking → **Critical** (weight 3) · `[A]` High → **Important** (weight 2) · `[M]` Medium and `[R]` Recommended → **Minor** (weight 1).

**Conditional items** (*If: …*): when the condition does not apply, mark **N/A with justification and evidence** (e.g., a code search with no hits). N/A without evidence counts as Non-compliant.

**Total items:** 163 — Critical: 9 · Important: 82 · Minor: 72. Maximum score (all applicable): 263.

## Pillar goal

> **Pillar goal:** the application responds fast at real p75/p95/p99 (not just in the lab), runs well on old devices and poor networks, consumes minimal CPU/memory/disk/network on the server and the client, scales predictably, degrades in a controlled way and ships software without waste in the pipeline.
>
> **Golden rule:** “fast” only counts with a number, percentile, population, environment and baseline. Isolated averages, a single run and tests on a developer machine are not evidence.

## PERF-1. Governance, budget and acceptance criteria

**How to verify:** Look in `docs/` (SLO, budgets, capacity, baseline), budget config files (`.size-limit*`, `lighthouserc*`, `budget.json`), CI steps that compare metrics. An SLO/budget only in text with no data source or gate = Partial at most.

#### PERF-1.01 · SLOs per journey
**Critical** (weight 3, origin `[B]`)  
SLOs exist per critical journey, endpoint, asynchronous operation and dependency, with p50/p75/p95/p99, error, throughput, availability, saturation and cost; averages are not used in isolation. Each SLO has an owner, window, data source and an action when violated.

#### PERF-1.02 · Error budget policy
**Important** (weight 2, origin `[A]`)  
it is defined what happens when the error budget runs out (feature freeze, reliability prioritization, release review). The policy is actually applied: there is a record of at least one decision taken based on it, or of a simulation.

#### PERF-1.03 · Reference thresholds for the web
**Important** (weight 2, origin `[A]`) · Conditional — *If: there is a web frontend*  
targets at p75 of field data, per route and device class: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1, TTFB ≤ 0.8 s. Stricter targets are set for conversion journeys. Deviations are accepted only with justification and a deadline.

#### PERF-1.04 · Performance budgets
**Important** (weight 2, origin `[A]`)  
there are versioned budgets for JavaScript/CSS/images/fonts, payload size, number of requests, TTFB, LCP, INP, CLS, cold start, queries per request, CPU, memory and pipeline duration. CI fails or requires approval when the budget worsens.

#### PERF-1.05 · Third-party budget
**Minor** (weight 1, origin `[M]`)  
third-party scripts and SDKs (analytics, chat, A/B, ads, pixels) have their own budget of bytes, main-thread time and requests, with a business owner. A new third party only comes in with before/after measurement.

#### PERF-1.06 · Reproducible baseline
**Important** (weight 2, origin `[A]`)  
the baseline records commit, dataset, environment, region, hardware, browser, network, cache temperature, number of users and dependency versions. Benchmarks use enough repetitions, percentiles and margin of error (confidence interval), not a single run.

#### PERF-1.07 · Field data as the source of truth
**Important** (weight 2, origin `[A]`)  
decisions use RUM (Real User Monitoring) and/or aggregated field data, segmented by device, browser, network, region and version. Lab tests (Lighthouse, WebPageTest, k6 etc.) serve for diagnosis and regression, not to declare compliance.

#### PERF-1.08 · User and device profile
**Important** (weight 2, origin `[A]`)  
tests include old devices (entry-level class with 2–4 GB of RAM and a slow CPU, or 4–6× CPU throttling as a documented proxy), supported browsers, small screens, accessibility, low battery/power-saving mode, 2G/3G/4G networks, high latency, packet loss and offline/intermittent mode where applicable. The support matrix is published and consistent with real analytics.

#### PERF-1.09 · Capacity model
**Important** (weight 2, origin `[A]`)  
a capacity model exists that relates RPS, concurrency, payload size, latency and resource consumption. The saturation point, safe capacity, degradation, headroom, marginal cost and behavior during autoscaling are documented. The model is reviewed on every relevant architecture change or traffic growth.

#### PERF-1.10 · Chaos engineering and fault injection
**Minor** (weight 1, origin `[M]`)  
controlled faults are injected (artificial latency, loss of a node/zone, slow dependency, full disk, failing DNS) with a hypothesis, limited blast radius, abort criterion and a record of the result. Experiments run first outside production and in production only with approved guardrails.

#### PERF-1.11 · Performance as regression
**Important** (weight 2, origin `[A]`)  
PRs and releases with measurable impact run a benchmark or representative test and compare against the baseline. Exceptions are justified, have a deadline and do not allow silent regressions to accumulate.

#### PERF-1.12 · Unit cost as a requirement
**Minor** (weight 1, origin `[M]`)  
a cost-per-transaction/user/tenant metric exists (infrastructure, database, CDN, third parties, telemetry). Changes that raise the unit cost above a limit require approval, just like latency regressions.

## PERF-2. Performance observability and traceability

**How to verify:** Look for instrumentation (`@opentelemetry/*`, `instrumentation.ts`, exporters, `prom-client`), a structured logger and its fields, dashboards/alerts as code (Grafana `*.json`, Prometheus rules, Datadog/Terraform monitors), RUM (`web-vitals`). The absence of any telemetry beyond logs = Not met on most items.

#### PERF-2.01 · RED and USE metrics
**Critical** (weight 3, origin `[B]`)  
each service exposes Rate, Errors and Duration per route/version/status, plus Utilization, Saturation and Errors for CPU, memory, disk, network, threads, connections, queues and pools. Labels have controlled cardinality and do not include arbitrary IDs.

#### PERF-2.02 · Instrumentation standard
**Minor** (weight 1, origin `[M]`)  
instrumentation follows an open standard (e.g., OpenTelemetry with semantic conventions) for metric, span and attribute names, so dashboards, alerts and queries work across services without manual translation.

#### PERF-2.03 · Business metrics
**Important** (weight 2, origin `[A]`)  
critical journeys have counters for start, success, failure, retry, abandonment, timeout and degradation. A drop in conversion, an increase in abandonment or an operational delay can be tied to the corresponding technical change without collecting unnecessary personal data.

#### PERF-2.04 · Structured logs
**Important** (weight 2, origin `[A]`)  
logs include a synchronized timestamp (NTP), environment, version, region, service, operation, status, duration, size, retry, dependency and `trace_id`, with coherent levels. There is no excessive logging, PII or secrets; sampling and retention are explicitly defined. Logging is asynchronous/buffered and does not block the critical path.

#### PERF-2.05 · Distributed tracing
**Important** (weight 2, origin `[A]`)  
requests cross browser, CDN, gateway, service, queue, worker, database and third parties with context propagation (e.g., W3C Trace Context). Spans record duration, status, retry/timeout events and safe attributes. Asynchronous jobs preserve the link (span links) between the originating request and the execution.

#### PERF-2.06 · Sampling and telemetry cost
**Minor** (weight 1, origin `[M]`)  
head/tail sampling, retention, aggregation and export are sized; errors, p99 and slow transactions have priority. Observability does not consume enough CPU, memory, disk or bandwidth to change the measured behavior (overhead measured and documented).

#### PERF-2.07 · Continuous profiling and eBPF
**Minor** (weight 1, origin `[M]`)  
CPU, heap, allocations, locks, I/O, GC, event loop, off-CPU and eBPF/equivalent profiling are accessible in production with controls. Profiles are comparable by release and allow attributing cost to a function, query, route and dependency.

#### PERF-2.08 · End-to-end correlation
**Important** (weight 2, origin `[A]`)  
given a `trace_id`, the assessor can find the related request, spans, logs, metrics (via exemplars), query, queue event, deploy and incident. There are no multiple IDs without a correlation map and no components that break the context.

#### PERF-2.09 · RUM with attribution
**Important** (weight 2, origin `[A]`) · Conditional — *If: there is a web frontend*  
RUM collects LCP, INP, CLS, TTFB and long tasks with attribution (LCP element, the interaction and script responsible for INP, long frame via Long Animation Frames or equivalent), segmented by route, version and device, with consent when required.

#### PERF-2.10 · Synthetic monitoring
**Minor** (weight 1, origin `[M]`)  
critical journeys are run periodically from multiple regions, on representative emulated device/network, to detect regressions before users do and outside peak hours.

#### PERF-2.11 · Actionable dashboards
**Minor** (weight 1, origin `[M]`)  
there are dashboards per journey, service, endpoint, dependency, region, version and tenant where allowed. Panels show percentiles, volume, error, saturation, queues, cache hit ratio, pool, GC, cold start and cost; each alert has a runbook and an owner.

#### PERF-2.12 · Alerts without noise
**Important** (weight 2, origin `[A]`)  
alerts use SLO/multi-window burn rate, saturation and user symptoms; they avoid fixed thresholds without context and duplication. There is alert testing, an escalation route, deduplication, maintenance and periodic review of false positives and false negatives.

#### PERF-2.13 · Change traceability
**Important** (weight 2, origin `[A]`)  
deploys, feature flags, configuration, migrations, index changes, dependencies and infrastructure changes appear as annotated events in the series and traces. A before/after comparison is possible and a regression can be attributed to a commit, release or rollout.

#### PERF-2.14 · Safe telemetry data
**Important** (weight 2, origin `[A]`)  
IDs, query text, headers and attributes are masked or pseudonymized; sampling does not capture tokens, request content or sensitive data. Telemetry retention, access, export and deletion are auditable. *(See also SEC-6.08 and PRIV-12.)*

## PERF-3. Client, browser and rendering

**How to verify:** Inspect the frontend: rendering strategy per route (RSC/SSR/CSR), `next/image`/`srcset`, `loading="lazy"`, `fetchpriority`, fonts (`next/font`, WOFF2), `next.config.*` (cache headers, compression), bundle analyzer, list virtualization, use of `useEffect` to fetch initial data. If there is no web frontend, mark N/A with the inventory as the justification.

*(If: there is a web frontend. For native mobile apps, apply the equivalent: cold/warm startup time, jank, frozen frames, ANR, app size, battery and data consumption.)*

#### PERF-3.01 · Critical rendering path
**Important** (weight 2, origin `[A]`)  
critical HTML, CSSOM, DOM, fonts and JavaScript are identified; non-critical resources do not block the first render. The waterfall shows no avoidable chains of dependencies, redirects, blocking fonts or synchronous scripts.

#### PERF-3.02 · Rendering strategy
**Important** (weight 2, origin `[A]`)  
the choice between SSR, SSG, ISR, streaming SSR, islands/partial hydration or CSR is justified per route. A whole SPA is not shipped for mostly static pages; hydration neither duplicates work already done on the server nor blocks interaction.

#### PERF-3.03 · Resource hints and prioritization
**Minor** (weight 1, origin `[M]`)  
`preconnect` only for critical origins, `preload` for critical resources that cannot be discovered, `fetchpriority` on the LCP resource and lowered on secondary resources, `103 Early Hints` when supported. There is no excess of preloads competing for bandwidth.

#### PERF-3.04 · LCP
**Important** (weight 2, origin `[A]`)  
the LCP element is identified per route and device; its resource is discoverable in the HTML, prioritized, sized, compressed and served close to the user. TTFB, resource load delay, download duration and render delay are measured separately. The LCP is not a lazy-loaded image and does not depend on JavaScript to appear.

#### PERF-3.05 · INP and long tasks
**Important** (weight 2, origin `[A]`)  
critical interactions are measured on the real device; tasks above 50 ms, heavy handlers, hydration, parsing and compilation are located and optimized. Work is partitioned (e.g., `scheduler.yield`/yielding to the event loop), cancelable, deferred or moved to a worker without blocking the main thread. Visual feedback occurs in the next frame after the interaction.

#### PERF-3.06 · CLS and visual stability
**Important** (weight 2, origin `[A]`)  
dimensions of images, videos, ads, iframes and fonts are reserved; components do not insert content above the viewport without user action; fonts do not cause jumps (adjusted fallback metrics, e.g., `size-adjust`). Tests cover slow loading and personalized content.

#### PERF-3.07 · JavaScript shipped
**Important** (weight 2, origin `[A]`)  
the initial bundle, chunks, dependencies, polyfills, tags and unused code are measured per route. Tree shaking, code splitting and on-demand loading are effective; heavy libraries are not used when native APIs solve the case. The build targets the supported browser matrix (no transpiling/polyfilling for browsers outside the matrix).

#### PERF-3.08 · Third-party scripts
**Important** (weight 2, origin `[A]`)  
third-party tags load asynchronously/deferred, behind consent when applicable, preferably via a facade (e.g., video player and chat loaded on interaction) or off the main thread. A third-party failure or slowness does not block rendering or interaction.

#### PERF-3.09 · DOM and layout
**Minor** (weight 1, origin `[M]`)  
DOM size, computed style, layout, paint and compositing are measured. There is no layout thrashing, pathological selectors, whole-tree re-rendering, duplicate listeners or animations on properties that force excessive layout/paint; animations use `transform`/`opacity` and respect `prefers-reduced-motion`. `content-visibility` is considered for long off-screen sections.

#### PERF-3.10 · Re-rendering and client state
**Minor** (weight 1, origin `[M]`)  
state management does not trigger a global re-render on every change; selectors, memoization and component granularity are checked with the framework's profiler. No fetch/effect fires in a loop because of unstable dependencies.

#### PERF-3.11 · Client memory
**Important** (weight 2, origin `[A]`)  
heap snapshots and long tests show no continuous growth per navigation, modal, list, route, listener, timer, subscription or cache. Images, blobs, workers and object URLs are released at the right point in the lifecycle. Memory use is tested on a low-RAM device.

#### PERF-3.12 · Lists and large data
**Important** (weight 2, origin `[A]`)  
tables, feeds, trees and selects use pagination, virtualization, a render window and incremental search when needed. Sorting/filtering does not process the whole dataset on the client without justification.

#### PERF-3.13 · Images and media
**Important** (weight 2, origin `[A]`)  
responsive dimensions, `srcset`/`sizes`, modern high-compression formats (AVIF, WebP) with fallback, compression, lazy loading (except above the fold) and priority are correct. There is no image larger than the viewport, no thumbnail generated on the client without need, no video without adaptive streaming and no preloading of non-critical media. Animated GIFs are replaced by video.

#### PERF-3.14 · Fonts and CSS
**Minor** (weight 1, origin `[M]`)  
fonts are subsetted, in WOFF2, with fallback, adequate `font-display`, preloading only the critical ones, and do not block the interface; CSS is split per route, minified and free of dead rules; critical CSS is inlined when worthwhile. A whole styling framework is not shipped for a few classes.

#### PERF-3.15 · Browser cache and bfcache
**Important** (weight 2, origin `[A]`)  
immutable assets use a hash in the name and a long `Cache-Control: max-age` + `immutable`; HTML/API use a coherent policy; compatible navigations use bfcache (no `unload`, no unnecessary `Cache-Control: no-store`). Headers are verified on a real network and invalidation does not require clearing the cache manually.

#### PERF-3.16 · Anticipated navigation
**Minor** (weight 1, origin `[R]`)  
prefetch/prerender (e.g., Speculation Rules) is used on high-probability navigations, with conservative rules, without triggering side effects (analytics, mutations) and with measurement of hit rate versus cost.

#### PERF-3.17 · Service worker and offline
**Minor** (weight 1, origin `[M]`) · Conditional — *If: there is a service worker/PWA*  
a cache strategy per resource type (cache-first for versioned static files, network-first/stale-while-revalidate for data), limited size, versioning and cleanup of old caches. The service worker does not add latency to navigation (navigation preload) nor serve a broken version after a deploy.

#### PERF-3.18 · Progressive compatibility
**Minor** (weight 1, origin `[M]`)  
low-capability fallbacks exist; APIs are detected by feature detection; tests cover minimum versions, Safari/Firefox/Chromium, zoom, keyboard and motion preferences. A third-party failure does not block the primary function.

#### PERF-3.19 · Respect for constrained devices and networks
**Minor** (weight 1, origin `[R]`)  
the application reduces work when it detects data saving (`Save-Data`), a slow network or low memory: less prefetch, lower-quality media, less animation.

## PERF-4. Network, API and communication

**How to verify:** Look for HTTP clients (`fetch`, `axios`, `undici`, SDKs) and check timeout/`AbortSignal`, retry with backoff+jitter, circuit breaker, payload limits, pagination/projection in responses, compression and `Cache-Control`. Any network call without an explicit timeout makes PERF-4.07 Not met.

#### PERF-4.01 · Waterfall and network latency
**Important** (weight 2, origin `[A]`)  
DNS, connection, TLS, TTFB, download, browser queue, redirects, CDN and third parties are separated into metrics. The diagnosis identifies whether the latency is client, network, gateway, application, database or vendor.

#### PERF-4.02 · Number of requests
**Important** (weight 2, origin `[A]`)  
there are no duplicate calls, avoidable cascades, aggressive polling, redundant refreshes or requests for invisible data. Deduplication of identical concurrent requests exists on the client. Prefetch only happens when the hit rate justifies the cost and has cancellation.

#### PERF-4.03 · Call aggregation (BFF/batching)
**Minor** (weight 1, origin `[M]`)  
screens that depend on many calls use a BFF, an aggregated endpoint or batching, avoiding N client round-trips, especially on mobile networks. The aggregator parallelizes internal calls and has a global timeout.

#### PERF-4.04 · Payload and serialization
**Important** (weight 2, origin `[A]`)  
responses are paginated, filterable, field-selectable and compressed; JSON does not carry unnecessary metadata or collections. Serialization/deserialization is profiled and binary/streaming formats are considered for large data. A maximum payload limit exists per request and per response.

#### PERF-4.05 · HTTP and transport
**Important** (weight 2, origin `[A]`)  
HTTP/2 and, when the edge supports it, HTTP/3 (QUIC); multiplexing, keep-alive and connection reuse between services; TLS 1.3 with resumption; Brotli compression (or zstd where supported) for text, gzip as a fallback, without compressing already-compressed formats; `Cache-Control`, `ETag`/`If-None-Match`, range requests and CDN as appropriate. There is no global disabling of compression, connections per request or headers preventing useful caching.

#### PERF-4.06 · Use of the edge (edge/CDN)
**Minor** (weight 1, origin `[M]`) · Conditional — *If: there is a CDN/edge*  
static content, cacheable public responses, redirects and simple routing are resolved at the edge to reduce TTFB and load on the origin. Token validation at the edge is accepted **only as an additional filter**: the definitive authorization stays at the origin (see SEC-3.05). The CDN cache key is normalized (irrelevant query strings, cookies and `Vary`) and the hit ratio is monitored.

#### PERF-4.07 · Timeouts per dependency
**Critical** (weight 3, origin `[B]`)  
each call has a connection, read and total timeout based on a latency budget. The deadline is propagated and shorter than the caller's timeout; expired operations are canceled so they do not keep consuming resources. There is no network call without an explicit timeout (verified by lint or code review).

#### PERF-4.08 · Safe retries
**Important** (weight 2, origin `[A]`)  
retry has a limit, exponential backoff with jitter, error classification (retryable vs. non-retryable), a retry budget per service and idempotency. There is no cascading retry at every layer, no retry of a non-idempotent operation and no storm after a dependency recovers. `Retry-After` is respected.

#### PERF-4.09 · Concurrency and backpressure
**Important** (weight 2, origin `[A]`)  
limits per client, route and dependency prevent a concurrency explosion. Queues, semaphores, bulkheads and circuit breakers protect resources; when saturated, the system rejects (429/503 with `Retry-After`) or queues work predictably, prioritizing critical traffic (load shedding by priority).

#### PERF-4.10 · Streaming and partial responses
**Minor** (weight 1, origin `[M]`)  
large downloads, exports, reports and events use streaming or incremental processing where possible. The server does not accumulate the entire result in memory and the client handles cancellation, reconnection and progress. Large exports are asynchronous (job + notification + expiring link).

#### PERF-4.11 · Third parties
**Important** (weight 2, origin `[A]`)  
each vendor has a latency budget, timeout, quota, cache/fallback and a separate metric. Scripts, APIs, payments, e-mail, maps and analytics do not block unrelated journeys; cost per call and the impact of failure are known.

#### PERF-4.12 · API contracts
**Minor** (weight 1, origin `[M]`)  
contracts define limits on size, pagination, ordering, fields, status, compression, versioning and compatibility. Changes do not force slow clients to download or process new fields unnecessarily.

#### PERF-4.13 · Query cost in flexible APIs
**Important** (weight 2, origin `[A]`) · Conditional — *If: GraphQL, OData or dynamic filters*  
queries have a computed cost (depth, complexity, aliases, list sizes) and a per-client limit; persisted queries/allowlists are used for first-party clients; resolvers use batching (DataLoader) to avoid N+1.

#### PERF-4.14 · Efficient real time
**Minor** (weight 1, origin `[M]`) · Conditional — *If: WebSocket, SSE, long polling*  
connections have a heartbeat, a per-user limit, efficient fan-out (pub/sub), compact messages and reconnection with backoff; the server supports the target number of simultaneous connections with memory measured per connection.

#### PERF-4.15 · Webhooks and outbound integrations
**Minor** (weight 1, origin `[M]`)  
sending webhooks is asynchronous, with a queue, retry with backoff, a short timeout, a concurrency limit per destination and automatic deactivation of persistently failing destinations, so a slow partner does not degrade the platform.

## PERF-5. Backend, runtime and concurrency

**How to verify:** Check for heavy synchronous code in the request (`fs.*Sync`, synchronous crypto, large parsing), use of workers/queues, idempotency of mutations, graceful shutdown (`SIGTERM` + closing connections), container configuration (limits, number of workers), feature flags.

#### PERF-5.01 · Event loop/threads/workers
**Important** (weight 2, origin `[A]`)  
I/O does not block the main thread; CPU-bound work uses a suitable worker/process; the pool has a size, queue and timeout. Event-loop lag, thread starvation, context switches and waiting tasks are measured. There are no synchronous file, crypto or heavy parsing calls on the request path.

#### PERF-5.02 · Container-aware runtime
**Important** (weight 2, origin `[A]`)  
the runtime respects container limits (e.g., JVM heap proportional to the limit, `GOMAXPROCS`/`GOMEMLIMIT` in Go, number of workers in Python/Node computed from the allocated CPU, not the host's CPU). There is no unexplained recurring OOMKill or CPU throttling.

#### PERF-5.03 · Startup and cold start
**Important** (weight 2, origin `[A]`)  
startup measures module loading, migrations, connection, cache warming, configuration and health check. There is no unnecessary business work or sequential connection before accepting traffic; readiness only occurs when essential dependencies are ready; migrations do not run at the startup of every replica.

#### PERF-5.04 · Allocation and GC
**Minor** (weight 1, origin `[M]`)  
heap, temporary allocations, copies, serialization, GC pauses and fragmentation are measured under load. Large objects, unbounded caches, closures and buffers are investigated as a cause of spikes.

#### PERF-5.05 · Hot path
**Minor** (weight 1, origin `[M]`)  
the most expensive functions by CPU and allocation (according to the profiler) are known and optimized: no regex recompiled per request, no repeated serialization, no logging with expensive interpolation at a disabled level, no unnecessary reflection.

#### PERF-5.06 · Pools and resource limits
**Important** (weight 2, origin `[A]`)  
HTTP, Redis, worker, socket, file descriptor and thread pools have limits consistent with the downstream capacity. The system measures wait, use, rejections, timeouts and leaks. *(The database pool is covered in PERF-6.37.)*

#### PERF-5.07 · Idempotency and duplication
**Important** (weight 2, origin `[A]`)  
retries, duplicate messages, refresh, double submit and reprocessing do not generate duplicate work or effects. Idempotency keys have controlled scope, retention and cost.

#### PERF-5.08 · Asynchronous processing
**Important** (weight 2, origin `[A]`)  
long tasks leave the synchronous request; queues have size, age of the oldest message, throughput, concurrency, priority, retry, DLQ and monitored consumers. There is no infinite queue masking saturation; the DLQ has an alert and a reprocessing process.

#### PERF-5.09 · Batching of writes and work
**Minor** (weight 1, origin `[M]`)  
frequent, small writes (counters, events, metrics, audit logs) are grouped (batch, buffer, coalescing) when consistency allows, reducing round-trips and contention.

#### PERF-5.10 · Internal serialization
**Minor** (weight 1, origin `[M]`)  
objects are converted and copied only when necessary; schemas are efficient; internal payloads do not carry fields that no consumer uses. Compression is only applied when the CPU cost pays off in network/disk savings.

#### PERF-5.11 · Noisy-neighbor isolation
**Important** (weight 2, origin `[A]`) · Conditional — *If: multi-tenant*  
one tenant cannot degrade the others: quotas, rate limits, queues and pools per tenant or per tenant class; heavy work from one customer is isolated (own queue, lower priority).

#### PERF-5.12 · Feature flags
**Minor** (weight 1, origin `[M]`)  
flags do not introduce two expensive paths at the same time, duplicate queries or synchronous remote evaluation on the critical path (local evaluation with cache). Old flags are removed with a deadline and rollout allows comparison by cohort, version and metric.

#### PERF-5.13 · Graceful degradation
**Important** (weight 2, origin `[A]`)  
failure of a cache, third party, region or optional feature does not bring down the essential journey. Fallback has a cost, timeout, observability and a test; there is no fallback that does a full scan or causes a request storm.

#### PERF-5.14 · Shutdown and deploy
**Important** (weight 2, origin `[A]`)  
graceful shutdown drains connections and queues, respects the deadline, avoids message loss/duplication and removes instances from the load balancer before stopping. Rolling/blue-green/canary does not concentrate cold starts or reduce headroom below what is necessary.

## PERF-6. Database and modeling

**How to verify:** Read the schema (Prisma/ORM/migrations) and all queries (repositories). For Mongo, the equivalents are `explain('executionStats')`, indexes in `@@index`/`createIndex`, the profiler and `$indexStats`. Look for N+1 (query inside a loop/`Promise.all` per item), `findMany` without `take`, missing `select` (overfetch), deep `skip`, wide transactions, pool/`connection_limit`, destructive migrations. Items that require production data (real plan, query inventory) are only met with versioned evidence.

### 6.1 Modeling

#### PERF-6.01 · Cardinality
**Important** (weight 2, origin `[A]`)  
1:1, 1:N and N:N cardinalities reflect the domain and the real access patterns; estimates of volume, growth, distribution and skew are documented. Queries and indexes are assessed for low and high cardinality, not just a small dataset.

#### PERF-6.02 · Distribution and selectivity
**Important** (weight 2, origin `[A]`)  
filtered columns have a known distribution; histograms/statistics capture skew and popular values; extended statistics (correlation between columns) exist where the planner errs. The planner does not choose a bad plan because of stale statistics, an insufficient sample or a parameter that changes selectivity.

#### PERF-6.03 · Data types
**Minor** (weight 1, origin `[M]`)  
types have the smallest sufficient representation, precision, timezone and correct semantics. There is no text where an integer/enum/date would reduce storage and cost, nor implicit conversions that prevent index use.

#### PERF-6.04 · Keys and identifiers
**Important** (weight 2, origin `[A]`)  
PKs/FKs are appropriate, compact and indexed according to use (FKs used in joins/deletes have an index). ID generation does not create hotspots or fragmentation: random IDs (UUIDv4) in large B-tree indexes are assessed against time-sortable alternatives (UUIDv7, ULID, sequence) — also considering the exposure of predictable IDs (SEC-3.02). Relations require referential integrity without unexpected destructive cascades.

#### PERF-6.05 · Normalization
**Minor** (weight 1, origin `[M]`)  
data repetition, update anomalies and inconsistencies were assessed. Normalization reduces writes and inconsistency without forcing excessive joins on critical journeys; denormalization decisions have a justification and a synchronization mechanism.

#### PERF-6.06 · Controlled denormalization
**Minor** (weight 1, origin `[M]`)  
derived fields, snapshots and aggregate documents have an owner, an update event, accepted consistency, backfill, correction and a strategy to avoid stale data. There are no copies without a contract and no duplication that raises write cost without measured gain.

#### PERF-6.07 · Hot rows and write contention
**Important** (weight 2, origin `[A]`)  
there is no single row updated by many concurrent transactions (global counters, aggregate balance, “last sequence”); partitioned counters, asynchronous aggregation or appropriate structures are used.

#### PERF-6.08 · Soft delete and multi-tenant in indexes
**Minor** (weight 1, origin `[M]`)  
with soft delete, unique indexes and constraints consider the active filter (e.g., partial index `WHERE deleted_at IS NULL`); in multi-tenant with a shared table, the relevant indexes start with `tenant_id` and queries always filter on it.

#### PERF-6.09 · Semi-structured data
**Minor** (weight 1, origin `[M]`) · Conditional — *If: JSON/JSONB/documents*  
frequently queried JSON fields have an adequate index (GIN, expression index) or are promoted to columns; documents do not grow without limit; a partial update does not rewrite huge documents on every change.

#### PERF-6.10 · Partitioning
**Minor** (weight 1, origin `[M]`) · Conditional — *If: large tables*  
large tables are partitioned only when filtering, retention, maintenance or distribution benefits. Pruning occurs in the plans; there are not too many partitions, no default partition growing unchecked and no migrations that lock the whole table.

#### PERF-6.11 · Sharding/distribution
**Minor** (weight 1, origin `[M]`) · Conditional — *If: distributed database*  
the distribution key avoids hotspots, cross-shard joins and unnecessary scatter-gather. Skew, rebalancing, consistency, distributed transactions and the impact of queries without the key are measured.

### 6.2 Plans and indexes

#### PERF-6.12 · EXPLAIN
**Critical** (weight 3, origin `[B]`)  
every critical query has a reviewed plan; `EXPLAIN ANALYZE` (with buffers) or equivalent uses representative data and identifies cost, estimated versus actual rows, loops, scan, join, sort, memory and I/O. The plan is stored per version for comparison.

#### PERF-6.13 · Inventory of real queries
**Important** (weight 2, origin `[A]`)  
production query statistics (e.g., `pg_stat_statements`, Query Store, Performance Schema, slow query log, `auto_explain`) are enabled; the top queries by total time, calls, I/O and variance are reviewed periodically and after every release.

#### PERF-6.14 · Plan regression
**Important** (weight 2, origin `[A]`)  
a change in the plan of critical queries (after a deploy, analyze, version upgrade or data growth) is detected and alerted; a procedure exists to stabilize the plan by fixing the cause.

#### PERF-6.15 · Estimate versus reality
**Important** (weight 2, origin `[A]`)  
relevant divergences between estimated and actual rows are investigated before superficial tuning. Statistics, column correlation, parameters, casts and distribution are fixed; no hint is forced without explaining the cause.

#### PERF-6.16 · Prepared statements and plan cache
**Minor** (weight 1, origin `[M]`)  
queries use prepared statements/parameterization; problems of generic versus specific plans (parameter sniffing) are known and handled; the pooler mode is compatible with prepared statements.

#### PERF-6.17 · Filter indexes
**Critical** (weight 3, origin `[B]`)  
frequent, selective predicates have adequate indexes, considering column order, equality/range, collation, NULL and operator.

#### PERF-6.18 · Composite indexes
**Important** (weight 2, origin `[A]`)  
column order follows filter/sort/join patterns; redundant indexes, covered prefixes and impossible combinations are removed. Write cost, size, cache and maintenance are measured.

#### PERF-6.19 · Partial/functional/specialized indexes
**Minor** (weight 1, origin `[M]`)  
partial, functional, covering (`INCLUDE`), BRIN (time series), GIN/GiST or specialized indexes are used when the predicate and pattern justify them. The query expressions match the index; there is no function/cast on the field that invalidates its use.

#### PERF-6.20 · Unused indexes
**Minor** (weight 1, origin `[M]`)  
indexes never or rarely used are identified, considering seasonality and replicas; excessive indexes do not consume memory, disk and write time without benefit. Removal happens with observation (e.g., making it invisible before removing, where supported) and rollback.

#### PERF-6.21 · Full scan
**Important** (weight 2, origin `[A]`)  
each sequential/full scan on a large table is classified as intentional or a defect. Missing filters, an inadequate index, low selectivity, statistics, casts and dynamic queries are checked; unavoidable scans use a window, partitioning or controlled processing.

### 6.3 Shape of the queries

#### PERF-6.22 · N+1 and overfetching
**Critical** (weight 3, origin `[B]`)  
traces and query logs detect the N+1 pattern per endpoint and collection size (ideally with an automated test that fails if the number of queries per request grows with N). The fix uses a join, batch, selective eager loading, DataLoader or an aggregate query without turning the problem into overfetching. The ORM's default lazy loading is known and controlled.

#### PERF-6.23 · Unnecessary joins
**Minor** (weight 1, origin `[M]`)  
joins that do not filter, project or guarantee existence are removed. The assessor checks for an ORM that adds relations automatically, repeated joins and tables included only for convenience.

#### PERF-6.24 · Redundant joins
**Minor** (weight 1, origin `[M]`)  
the same relationship is not accessed in separate queries or equivalent subqueries. CTEs, views and the ORM do not materialize/re-execute work unnecessarily; the plan confirms elimination or effective sharing.

#### PERF-6.25 · Cartesian joins
**Important** (weight 2, origin `[A]`)  
joins without a predicate, with an incomplete predicate or that multiply rows are tested with high cardinalities. The result does not depend on `DISTINCT` to hide duplication; the cause is fixed and the cost measured.

#### PERF-6.26 · Join order and algorithm
**Minor** (weight 1, origin `[M]`)  
nested loop, hash join, merge join and the chosen order are suited to the volume and selectivity. Hash/sort memory avoids spilling to disk; `work_mem` or equivalent is sized without causing OOM under concurrency.

#### PERF-6.27 · Sorting
**Minor** (weight 1, origin `[M]`)  
`ORDER BY` only occurs when required; a default order is not applied automatically. An index provides the order when worthwhile; sorting of large sets has a limit, cursor/keyset pagination and controlled memory.

#### PERF-6.28 · Pagination
**Important** (weight 2, origin `[A]`)  
deep offsets do not walk through millions of rows without justification. Keyset/cursor, a compatible index, a maximum limit and deterministic ordering (tie-breaking by a unique key) are used; pagination does not allow an unlimited response. Exact `COUNT(*)` on large tables is avoided when an estimate or “there are more pages” solves it.

#### PERF-6.29 · Aggregations
**Minor** (weight 1, origin `[M]`)  
counts, sums, groupings and distinct are analyzed for scan, memory, spill and repetition. Pre-aggregation, materialized views (with a refresh strategy), cache or a time window are used when the pattern justifies it.

#### PERF-6.30 · Subqueries and CTEs
**Minor** (weight 1, origin `[M]`)  
correlated subqueries, materialized CTEs and nested views are examined for re-execution and optimization barriers. The declarative form is compared with join/window/batch using the real plan.

#### PERF-6.31 · SELECT and projection
**Important** (weight 2, origin `[A]`)  
the query returns only the necessary columns; blobs, large JSON, text and sensitive columns are not loaded by default. The persistence layer offers explicit projection, not the full entity on every call. There is no `SELECT *` in production code.

#### PERF-6.32 · Filters and sargability
**Important** (weight 2, origin `[A]`)  
predicates allow index use; functions, casts, `LIKE '%…'`, expressions and comparison of different types do not force a scan. Alternatives via a normalized column, a functional index or specialized search are assessed.

#### PERF-6.33 · Bulk operations
**Minor** (weight 1, origin `[M]`)  
bulk loads and updates use bulk insert/`COPY`/batch with a controlled batch size instead of one operation per row; massive deletes/updates are sliced so they do not produce long locks, replication lag or bloat.

### 6.4 Concurrency, transactions and connections

#### PERF-6.34 · Locks and deadlocks
**Important** (weight 2, origin `[A]`)  
locks acquired, duration, waits, deadlocks and contention are observed. There is deadlock detection, a consistent lock-acquisition order and safe retry for transactions aborted by concurrency/serialization.

#### PERF-6.35 · Database timeouts
**Important** (weight 2, origin `[A]`)  
statement, lock and idle-in-transaction timeouts exist (e.g., `statement_timeout`, `lock_timeout`, `idle_in_transaction_session_timeout`) per connection role; long transactions are alerted, since they block vacuum/compaction and hold locks.

#### PERF-6.36 · Transactions
**Important** (weight 2, origin `[A]`)  
the transactional scope contains only the necessary operations; network calls, user waits and expensive processing stay outside. Isolation is compatible with the case; serializable/global locks are not used by default.

#### PERF-6.37 · Database connection pool
**Critical** (weight 3, origin `[B]`)  
size considers the number of replicas, workers and database capacity (total connections = replicas × pool ≤ the database's safe limit); wait and saturation are alerted; an external pooler (e.g., PgBouncer, managed proxy) is used when the number of instances is elastic. There is no pool per request, leaking connection, transaction returned to the pool open or incompatible multiplexing.

#### PERF-6.38 · Replication and reads
**Minor** (weight 1, origin `[M]`) · Conditional — *If: there are replicas*  
replicas have monitored lag, capacity and consistency. Lag-tolerant reads are routed; reads after writes and critical decisions use an adequate guarantee. Failover does not duplicate writes or cause an avalanche to the primary.

#### PERF-6.39 · Database cache
**Minor** (weight 1, origin `[M]`)  
query/object/result-set cache has a key, TTL, invalidation, size, stampede protection and a hit/miss metric. The cache does not keep incorrect data after a write nor mask database degradation.

### 6.5 Operations and lifecycle

#### PERF-6.40 · Retention and archiving
**Important** (weight 2, origin `[A]`)  
historical data is archived/partitioned so that hot tables stay small. Retention jobs are incremental, bounded, observable and do not block OLTP. *(Align with PRIV-11.)*

#### PERF-6.41 · Migrations
**Critical** (weight 3, origin `[B]`)  
migrations have a lock plan, estimated time at production volume, expand/contract compatibility, incremental backfill, online index creation when possible, a short `lock_timeout`, rollback/forward fix and measured impact. A deploy does not require unexpected downtime nor make a destructive change before all consumers have migrated. Migrations are tested on a copy with realistic volume.

#### PERF-6.42 · Disk and maintenance
**Important** (weight 2, origin `[A]`)  
vacuum/compaction/analyze/reindex/checkpoint/autovacuum equivalents are monitored and tuned per table when needed. Bloat, fragmentation, WAL/redo, risk of transaction ID wraparound, I/O and free space have alerts and capacity; maintenance does not coincide with peaks without planning.

#### PERF-6.43 · Database load per endpoint
**Important** (weight 2, origin `[A]`)  
observability relates duration, rows, bytes, queries, locks and cache hits to route, technical user, release and trace (e.g., SQL comments with `trace_id`/route). It is possible to answer “which endpoint generated this spike?” without manual inference.

#### PERF-6.44 · OLTP/OLAP separation
**Minor** (weight 1, origin `[M]`)  
heavy reports, analytics and exports do not run on the transactional primary; they use a dedicated replica, a data warehouse, CDC or an analytical store, with an agreed data latency.

#### PERF-6.45 · Specialized search
**Minor** (weight 1, origin `[M]`)  
full-text, fuzzy, geospatial, vector or analytics are not forced onto OLTP when a specialized engine reduces cost. Synchronization, consistency, reindexing, cost and fallback are explicitly assessed.

#### PERF-6.46 · Engine upgrade and version
**Minor** (weight 1, origin `[R]`)  
the database version is supported and recent enough not to miss relevant optimizations; upgrades are tested with before/after plan comparison.

## PERF-7. Cache, storage and resources

**How to verify:** Look for cache layers (Redis, `unstable_cache`, `revalidate`, CDN, headers), keys/TTL/invalidation, stampede protection, resource limits (upload quotas, file size), Dockerfile and deploy/autoscaling manifests.

#### PERF-7.01 · Cache strategy per layer
**Important** (weight 2, origin `[A]`)  
browser, CDN, gateway, application, object and database have a documented purpose, TTL, key, invalidation and fallback; there is no duplicate cache without measured gain.

#### PERF-7.02 · Cache stampede and stale-while-revalidate
**Important** (weight 2, origin `[A]`)  
simultaneous expiry, thundering herd, cache penetration and avalanche are tested. There is TTL jitter, single-flight/request coalescing, stale-while-revalidate/stale-if-error, negative cache or pre-warming as the case requires.

#### PERF-7.03 · Consistency
**Important** (weight 2, origin `[A]`)  
stale data, concurrent writes, out-of-order invalidation and partial failure have a defined behavior. The cache does not authorize, does not expose the wrong tenant and does not serve sensitive data outside scope (`Vary` and the key include identity/tenant when the response is personalized). *(See SEC-5.16.)*

#### PERF-7.04 · Health of the distributed cache
**Minor** (weight 1, origin `[M]`) · Conditional — *If: Redis/Memcached or similar*  
memory, eviction policy, big keys, hot keys, command latency and blocking operations (e.g., full key scans) are monitored; O(N) commands over large sets are avoided.

#### PERF-7.05 · Disk and temporary files
**Minor** (weight 1, origin `[M]`)  
uploads, exports, logs, dumps, thumbnails and temporary files have quota, streaming, cleanup, retention and a space alert. Processing does not read a whole file into memory unnecessarily.

#### PERF-7.06 · Object storage/CDN
**Minor** (weight 1, origin `[M]`)  
objects have adequate size, multipart, compression, cache and lifecycle (tiering to cold classes); signed URLs expire; upload/download goes directly to storage (pre-signed) without passing unnecessarily through the application server.

#### PERF-7.07 · Resource limits
**Important** (weight 2, origin `[A]`)  
CPU, memory, disk, sockets, threads, connections, queues, payload and time have tested limits. The service fails in a controlled way and does not grow without limit until it hangs the host.

#### PERF-7.08 · Container and runtime
**Minor** (weight 1, origin `[M]`)  
the final image is minimal, layers/cache are efficient, requests and limits reflect a real measured profile, health/readiness do not run heavy work and shutdown is graceful. The container does not use swap/CPU without observability.

#### PERF-7.09 · Autoscaling
**Important** (weight 2, origin `[A]`)  
scaling uses demand and saturation signals (not just CPU), with cooldown, maximum, minimum and headroom. The metric does not react late nor create a scale-up/scale-down loop; warm-up and load distribution are tested; the database and dependencies support the maximum number of configured replicas.

## PERF-8. Build, CI/CD and delivery

**How to verify:** Read `.github/workflows/*` (or equivalent): dependency cache, `npm ci`, parallelism, path filters, `concurrency`/cancellation, bundle/benchmark gates, multi-stage Dockerfile and `.dockerignore`, pinned versions (`.nvmrc`, `engines`, `packageManager`).

#### PERF-8.01 · Dependency cache
**Minor** (weight 1, origin `[M]`)  
package managers and images use a safe cache, invalidated by lockfile and version; installation is deterministic (`--frozen-lockfile`/`ci`); the cache does not mix incompatible branches nor hide an incomplete installation.

#### PERF-8.02 · Remote build/test cache
**Minor** (weight 1, origin `[R]`)  
incremental build tools with a remote cache and input hashing (e.g., Bazel, Nx, Turborepo, Gradle build cache) avoid recompiling and retesting what has not changed; the cache is protected against poisoning (written only by trusted pipelines).

#### PERF-8.03 · Parallelism
**Minor** (weight 1, origin `[M]`)  
independent lint, unit, integration, build, scan and packaging run in parallel; dependencies between jobs are minimal and explicit; long suites use sharding. The pipeline does not wait for a step that could start earlier.

#### PERF-8.04 · Running only what is needed
**Minor** (weight 1, origin `[M]`)  
path filters avoid running irrelevant jobs (e.g., a docs-only change does not run e2e); runs superseded by a new push to the same branch are canceled automatically; a merge queue avoids revalidating the same content several times.

#### PERF-8.05 · Incremental test selection
**Minor** (weight 1, origin `[M]`)  
tests per package/module/change are used together with a periodic full suite. The dependency graph is correct; no critical test is omitted by excessive selection.

#### PERF-8.06 · Artifacts
**Important** (weight 2, origin `[A]`)  
the build happens once per commit and the same artifact is promoted between environments; there is no diverging rebuild in staging/production. Artifacts have a checksum, metadata and a retention duration.

#### PERF-8.07 · Docker build
**Minor** (weight 1, origin `[M]`)  
the context is small (`.dockerignore`); order preserves the cache; multi-stage separates build/test/runtime; base and dependencies are minimal; cache mounts for package managers; the final image contains only the runtime and necessary artifacts.

#### PERF-8.08 · Reproducibility
**Minor** (weight 1, origin `[M]`)  
runtime version, OS, compiler, package manager, timezone and flags are pinned; two equivalent builds produce an equivalent result. Environment differences are detected before deploy.

#### PERF-8.09 · Pipeline time
**Minor** (weight 1, origin `[M]`)  
each step has duration, variance, cache hit, cost and an owner. Redundant jobs, repeated downloads, recreated environments and flaky tests are eliminated or isolated. There is an explicit target for time from PR to feedback (e.g., required checks < 10–15 min).

#### PERF-8.10 · Flaky tests
**Important** (weight 2, origin `[A]`)  
flaky tests are detected automatically (retries recorded, intermittent failure rate), quarantined with an owner and a deadline, and are not “fixed” by a silent retry that hides a real problem.

#### PERF-8.11 · Ephemeral environments with controlled cost
**Minor** (weight 1, origin `[R]`)  
per-branch preview environments have a TTL, minimum size, synthetic data and automatic destruction.

#### PERF-8.12 · Performance gates
**Important** (weight 2, origin `[A]`)  
CI measures bundle size, query count, benchmark, image size, startup, latency and consumption according to the component; a regression requires explicit approval with justification.

## PERF-9. Load, resilience and diagnostics

**How to verify:** Look for load scripts (`k6`, `artillery`, `locust`, `tests/load`), versioned stress/soak test reports, runbooks and postmortems in `docs/`. A load script with no recorded dataset/result = Partial.

#### PERF-9.01 · Realistic load test
**Critical** (weight 3, origin `[B]`)  
the workload uses a distribution of endpoints, think time, payloads, authentication, cold/warm cache, tenants and representative data (volume close to production, not an empty database). The result includes p95/p99, error, throughput, resources and saturation per component. The load generator is not the bottleneck (verified).

#### PERF-9.02 · Stress and breakpoint
**Important** (weight 2, origin `[A]`)  
load grows until degradation; it identifies queue, timeout, OOM, lock, pool and cascade. The system keeps controlled responses and recovers without destructive intervention.

#### PERF-9.03 · Soak and leaks
**Important** (weight 2, origin `[A]`)  
a prolonged test (hours) detects growth in heap, handles, connections, queues, logs, disk, cache and latency. The variation is compared to the volume processed and the deploy cycle.

#### PERF-9.04 · Spikes and autoscaling
**Important** (weight 2, origin `[A]`)  
bursts, cold start, scale-out, scale-in, rebalancing and instance loss are tested. There is no loss of work, duplication, connection avalanche or SLO drop during the adjustment.

#### PERF-9.05 · Dependency failures
**Important** (weight 2, origin `[A]`)  
timeout, 5xx error, slow response, invalid payload, rate limit, DNS, regional unavailability and partial response are tested. Fallback does not worsen the incident nor produce incorrect data.

#### PERF-9.06 · Performance in failover and DR
**Important** (weight 2, origin `[A]`)  
database failover, region switch and backup restore are measured under load; the real time meets the RTO and the destination environment's capacity supports the traffic. *(See SEC-8.06.)*

#### PERF-9.07 · Regression diagnosis
**Important** (weight 2, origin `[A]`)  
a procedure exists to compare traces, profiles, query plans, metrics, logs, deploys and flags between a good and a bad window. The team can reach the probable cause without depending on a perfect reproduction.

#### PERF-9.08 · Runbooks
**Important** (weight 2, origin `[A]`)  
each performance alert has impact, hypotheses, queries/dashboards, safe commands, reversible mitigation, escalation criteria and a post-incident action. Runbooks are tested in an exercise (game day).

#### PERF-9.09 · Performance postmortem
**Minor** (weight 1, origin `[M]`)  
latency/capacity incidents produce a blameless postmortem, with root cause, a regression test and an update of the budget/SLO/capacity.

## PERF-10. Resource efficiency and cost (FinOps)

**How to verify:** Look for sizing documentation/IaC, storage lifecycle policies, versioned cost reports. A repository without its own infrastructure: assess what is declared in `deploy/`, `infra/`, operations docs.

#### PERF-10.01 · Right-sizing
**Minor** (weight 1, origin `[M]`)  
requests/limits and instance, database and cache sizes are tuned based on measured usage (p95 utilization), reviewed periodically; there are no idle or oversized resources without justification.

#### PERF-10.02 · Orphan resources
**Minor** (weight 1, origin `[M]`)  
unused volumes, snapshots, IPs, load balancers, environments, buckets and queues are detected automatically and removed through a process.

#### PERF-10.03 · Egress and cross-zone traffic
**Minor** (weight 1, origin `[M]`)  
the cost of egress, cross-zone/region traffic and NAT is known; intense communication between services avoids crossing zones unnecessarily; large responses use a CDN.

#### PERF-10.04 · Telemetry volume
**Minor** (weight 1, origin `[M]`)  
the volume and cost of logs, metrics and traces are tracked per service; debug logs are not left on in production; high-cardinality metrics are controlled.

#### PERF-10.05 · Tiered storage
**Minor** (weight 1, origin `[R]`)  
cold data migrates to cheaper storage classes; old backups and logs follow a lifecycle; compression is used where it pays off.

#### PERF-10.06 · Elastic, cheap capacity for batch
**Minor** (weight 1, origin `[R]`)  
workloads that tolerate interruption (batch, CI, asynchronous processing) evaluate preemptible/spot instances and CPU architectures with better price-performance, with a compatibility test.

## PERF-11. AI/LLM workloads *(If: the application calls AI models)*

**How to verify:** Look for calls to AI providers (`@anthropic-ai/sdk`, `openai`, `ai`, LangChain etc.). If there are none, mark the whole section N/A citing the search made. If there are: streaming, `max_tokens`, timeout, retry, fallback, prompt caching, token/cost logging.

#### PERF-11.01 · Perceived latency
**Important** (weight 2, origin `[A]`)  
time to first token (TTFT), tokens per second and total latency are measured per use case; long responses use streaming to the user; there is a progress indicator and the ability to cancel (which stops generation and cost).

#### PERF-11.02 · AI timeouts, limits and fallback
**Important** (weight 2, origin `[A]`)  
model calls have a timeout, `max_tokens`, a context budget, retry with backoff for 429/5xx and a circuit breaker. If the AI is slow, fails, exceeds limits or returns output outside the schema, the application degrades gracefully to a traditional/heuristic flow without interrupting the journey. *(Moved from AI Readiness; see also SEC-10.)*

#### PERF-11.03 · Token economy in production
**Important** (weight 2, origin `[A]`)  
prompts have controlled, versioned size; stable prefixes take advantage of the provider's prompt caching; retrieved context (RAG) is limited to what is necessary; conversation history is summarized/truncated; the model is chosen per task (smaller models for simple tasks, routing by complexity).

#### PERF-11.04 · Response and embedding cache
**Minor** (weight 1, origin `[M]`)  
embeddings are not recomputed for unchanged content (content hash); deterministic or frequent responses are cached when safe, respecting user/tenant scope and personal data.

#### PERF-11.05 · Vector search
**Minor** (weight 1, origin `[M]`) · Conditional — *If: RAG/semantic search*  
the vector index (e.g., HNSW/IVF) has tuned parameters with recall-versus-latency measurement; tenant/permission filters are applied in the index and not after retrieving top-k (which degrades recall and may leak data); reindexing is incremental.

#### PERF-11.06 · Cost per AI request
**Important** (weight 2, origin `[A]`)  
input/output tokens and cost are recorded per feature, user/tenant and prompt version; there is a spending limit and an anomaly alert; per-user quotas prevent abusive consumption.

#### PERF-11.07 · Application data prepared for RAG
**Minor** (weight 1, origin `[M]`) · Conditional — *If: RAG/semantic search over application data*  
the indexed content has a clear semantic schema, clean text (no HTML, navigation or markup noise), chunking suited to the document type, source/date/permission metadata and deduplication; retrieval quality is measured with a set of reference questions. *(Moved from AI Readiness: it concerns the application's data, not the repository.)*
