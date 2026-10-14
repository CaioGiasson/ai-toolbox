"""Gera os catálogos de critérios das skills eval-* a partir do application-assessment v3.

Uso (na raiz do ai-toolbox):
    python -X utf8 scripts/gen-assessment-catalog.py [fonte.md] [pasta-skills]

Padrões: docs/application-assessment-v3.md e skills/. Gera skills/eval-*/references/checklist.md.
Ao atualizar o checklist-fonte, rode o script e revise o diff: mudar IDs ou severidades altera
a comparabilidade do score entre execuções.
"""
import re, sys, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'docs', 'application-assessment-v3.md')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'skills')

SEV = {'B': ('Crítico', 3), 'A': ('Importante', 2), 'M': ('Menor', 1), 'R': ('Menor', 1)}

PILLARS = [
    ('## Performance', 'eval-performance', 'Performance', 'PERF'),
    ('## Security', 'eval-security', 'Security', 'SEC'),
    ('## Privacy', 'eval-privacy', 'Privacy (LGPD)', 'PRIV'),
    ('## AI Readiness', 'eval-ai-readiness', 'AI Readiness', 'AIR'),
]

# Guia de verificação por seção: onde procurar e o que conta como evidência no repositório.
GUIDE = {
 'PERF-1': "Procure `docs/` (SLO, budgets, capacidade, baseline), arquivos de config de budget (`.size-limit*`, `lighthouserc*`, `budget.json`), steps de CI que comparam métricas. SLO/budget só em texto sem fonte de dados ou gate = Parcial no máximo.",
 'PERF-2': "Procure instrumentação (`@opentelemetry/*`, `instrumentation.ts`, exporters, `prom-client`), logger estruturado e seus campos, dashboards/alertas como código (`*.json` Grafana, regras Prometheus, monitores Datadog/Terraform), RUM (`web-vitals`). Ausência de qualquer telemetria além de logs = Não atende na maioria dos itens.",
 'PERF-3': "Inspecione o frontend: estratégia de render por rota (RSC/SSR/CSR), `next/image`/`srcset`, `loading=\"lazy\"`, `fetchpriority`, fontes (`next/font`, WOFF2), `next.config.*` (headers de cache, compressão), bundle analyzer, virtualização de listas, uso de `useEffect` para buscar dados iniciais. Se não há frontend web, marque N/A com o inventário como justificativa.",
 'PERF-4': "Procure clientes HTTP (`fetch`, `axios`, `undici`, SDKs) e verifique timeout/`AbortSignal`, retry com backoff+jitter, circuit breaker, limites de payload, paginação/projeção nas respostas, compressão e `Cache-Control`. Toda chamada de rede sem timeout explícito torna PERF-4.07 Não atende.",
 'PERF-5': "Verifique código síncrono pesado no request (`fs.*Sync`, crypto síncrono, parsing grande), uso de workers/filas, idempotência de mutações, graceful shutdown (`SIGTERM` + fechamento de conexões), configuração de container (limites, número de workers), feature flags.",
 'PERF-6': "Leia o schema (Prisma/ORM/migrations) e todas as queries (repositories). Para Mongo, os equivalentes são `explain('executionStats')`, índices em `@@index`/`createIndex`, profiler e `$indexStats`. Procure N+1 (query dentro de loop/`Promise.all` por item), `findMany` sem `take`, `select` ausente (overfetch), `skip` profundo, transações amplas, pool/`connection_limit`, migrations destrutivas. Itens que exigem dados de produção (plano real, inventário de consultas) só atendem com evidência versionada.",
 'PERF-7': "Procure camadas de cache (Redis, `unstable_cache`, `revalidate`, CDN, headers), chaves/TTL/invalidação, proteção contra stampede, limites de recursos (quotas de upload, tamanho de arquivo), Dockerfile e manifestos de deploy/autoscaling.",
 'PERF-8': "Leia `.github/workflows/*` (ou equivalente): cache de dependências, `npm ci`, paralelismo, filtros por caminho, `concurrency`/cancelamento, gates de bundle/benchmark, Dockerfile multi-stage e `.dockerignore`, versões fixadas (`.nvmrc`, `engines`, `packageManager`).",
 'PERF-9': "Procure scripts de carga (`k6`, `artillery`, `locust`, `tests/load`), relatórios de testes de stress/soak versionados, runbooks e postmortems em `docs/`. Script de carga sem dataset/resultado registrado = Parcial.",
 'PERF-10': "Procure documentação/IaC de dimensionamento, políticas de lifecycle de storage, relatórios de custo versionados. Repositório sem infraestrutura própria: avalie o que está declarado em `deploy/`, `infra/`, docs de operação.",
 'PERF-11': "Procure chamadas a provedores de IA (`@anthropic-ai/sdk`, `openai`, `ai`, LangChain etc.). Se não houver, marque toda a seção N/A citando a busca feita. Se houver: streaming, `max_tokens`, timeout, retry, fallback, prompt caching, registro de tokens/custo.",
 'SEC-1': "Procure inventário de ativos, diagramas/fluxos (`docs/architecture*`), threat model, decisões de segurança (ASVS), classificação de dados no schema. Documentos genéricos sem vínculo a componentes reais = Parcial.",
 'SEC-2': "Leia o fluxo completo de auth: hash de senha (`argon2`/`bcrypt` e parâmetros), política de senha, rate limit/lockout e de onde vem o IP (`x-forwarded-for` confiável?), geração/validação de JWT (algoritmos, `iss`/`aud`/`exp`, revogação), cookies de sessão, reset de senha (token, hash, expiração, `Host` header), MFA/WebAuthn, OAuth. Confirme com os testes existentes (testes negativos contam como E3).",
 'SEC-3': "Mapeie todas as rotas e verifique, por rota, autenticação e checagem de ownership/papel no servidor (middleware/use case). Procure IDs vindos do path/body usados sem checagem, DTOs de saída, mass assignment (`...body` em update), operações sem transação/condição atômica (race). Testes de autorização negativa são a evidência principal.",
 'SEC-4': "Procure validação de schema na borda (Zod/Joi/class-validator) em TODAS as rotas, queries raw (`$queryRaw`, `$runCommandRaw`, concatenação), operadores Mongo vindos do input, `child_process`, templates/HTML gerado, manipulação de caminhos, `fetch` de URL do usuário (SSRF), desserialização, `merge` profundo, regex sobre input, upload (magic bytes, tamanho, re-encode).",
 'SEC-5': "Verifique CSRF (tokens/`Origin`/`SameSite`), CORS, CSP e headers (`next.config.*`, middleware, `securityHeaders`), uso de `dangerouslySetInnerHTML`/`innerHTML`, cookies, `localStorage`, redirects, inventário de rotas vs OpenAPI, rate limit, formato de erro, webhooks recebidos.",
 'SEC-6': "Procure TLS desabilitado (`rejectUnauthorized: false`, `NODE_TLS_REJECT_UNAUTHORIZED`), segredos no código e no histórico (`git log -p`, padrões de chave), `.env` versionado, mascaramento no logger, uso de `Math.random` para tokens, algoritmos fracos (`md5`, `sha1`, `createCipher`), comparação de segredos sem tempo constante, TLS app→banco.",
 'SEC-7': "Leia CI (`permissions:`, actions pinadas por SHA, `pull_request_target`, interpolação de `${{ github.event.* }}` em `run:`), lockfiles, SCA/Dependabot/Renovate, SBOM, Dockerfile (usuário não-root, base mínima), IaC, CODEOWNERS e proteção de branch (via `gh api` quando disponível), configurações de produção (debug, CORS, endpoints de exemplo).",
 'SEC-8': "Procure eventos de auditoria no código (login, falhas, mudanças de papel, exports), destino e imutabilidade dos logs, regras de detecção, playbook de incidente, DRP com RPO/RTO e registro de exercícios, política e teste de restore de backup.",
 'SEC-9': "Verifique o que é servido publicamente: `public/`, source maps (`productionBrowserSourceMaps`), headers `X-Powered-By`, Swagger/health/metrics expostos, `robots.txt`, `security.txt`, páginas de erro.",
 'SEC-10': "Procure uso de LLM/agentes na aplicação. Se não houver, marque a seção N/A citando a busca. Se houver: separação instrução/dados, validação da saída, ferramentas com escopo do usuário, filtros de RAG por permissão, limites de tokens/custo, sandbox de execução.",
 'SEC-11': "Procure handler global de erros e de `unhandledRejection`, comportamento em falha de autorização/validação (fail-closed), rollback/compensação em operações multi-etapa, `finally` para liberar recursos, comportamento do rate limit/log quando a dependência cai.",
 'SEC-12': "Procure política de SLA de vulnerabilidades, relatórios de triagem, registro de EOL de runtime/frameworks (`engines`, versões), registros de pentest anteriores.",
 'SEC-13': "Procure código de app mobile (iOS/Android/React Native/Flutter). Se não houver, marque a seção N/A.",
 'SEC-14': "Avalie a existência e a qualidade de relatórios de pentest/assessment anteriores e de testes de regressão de segurança (ex.: `tests/security/`), metodologia de severidade e critério de aprovação documentados.",
 'PRIV-1': "Procure política de privacidade, termos, ROPA, documentação de papéis (controlador/operador), público-alvo do produto. Sem documentação de aplicabilidade e papéis = Não atende.",
 'PRIV-2': "Compare o inventário de dados (ROPA/docs) com o schema real (modelos e campos com dados pessoais) e com os terceiros chamados no código e no frontend (SDKs, pixels, APIs). Campo pessoal ou terceiro não inventariado = Parcial ou Não atende.",
 'PRIV-3': "Avalie campo a campo os formulários/APIs de cadastro e eventos: necessidade de cada dado, finalidades declaradas, acesso do titular aos próprios dados, mecanismos de correção. Use o aviso de privacidade como referência do declarado.",
 'PRIV-4': "Procure as bases legais por finalidade no aviso/ROPA e verifique coerência com o comportamento (ex.: marketing não pode estar sob \"execução de contrato\").",
 'PRIV-5': "Procure registro de consentimento (modelo/tabela com versão, data, canal), opções granulares, fluxo de revogação e se o código consulta o consentimento antes de usar o dado. Se nenhuma finalidade usa consentimento, marque a seção N/A justificando.",
 'PRIV-6': "Procure testes de balanceamento (LIA) documentados para cada finalidade baseada em legítimo interesse e o canal de oposição. Sem uso de legítimo interesse, marque N/A justificando.",
 'PRIV-7': "Procure dados sensíveis no schema e nos fluxos (saúde, biometria, origem, religião etc., inclusive inferidos de fotos/compras) e a base do art. 11. Se não houver dado sensível, registre a busca como evidência do N/A.",
 'PRIV-8': "Verifique público-alvo, age gate, verificação de idade, configurações protetivas por padrão e obrigações do ECA Digital. Conclusão \"não se aplica\" exige justificativa documentada no repositório.",
 'PRIV-9': "Leia o aviso de privacidade e compare com o comportamento real (terceiros no código/HTML, cookies setados, storage). Verifique banner de cookies (recusar tão fácil quanto aceitar), avisos contextuais e versionamento do aviso.",
 'PRIV-10': "Procure endpoints/fluxos de acesso/export, correção, eliminação, revogação e oposição; registro de pedidos (protocolo, prazos); testes ponta a ponta desses fluxos.",
 'PRIV-11': "Procure tabela/política de retenção, jobs de expurgo (cron) e seus testes, cobertura da eliminação (storage, caches, logs, backups, terceiros), política de contas inativas.",
 'PRIV-12': "Use o resultado do pilar Security para PRIV-12.01. Verifique template de PR com perguntas de privacidade, defaults protetivos (visibilidade, opt-ins), uso de dados reais em seeds/fixtures, mascaramento em logs.",
 'PRIV-13': "Procure onde dados são declarados \"anonimizados\" (ex.: exclusão de conta) e avalie se quase-identificadores permanecem; pseudônimos tratados como dados pessoais; documentação da técnica.",
 'PRIV-14': "Procure decisões automatizadas (moderação, bloqueio, antifraude, score) e uso de dados pessoais com IA. Sem decisões automatizadas relevantes, registre a busca como justificativa do N/A.",
 'PRIV-15': "Liste os terceiros que recebem dados (código, SDKs, integrações) e verifique DPA/registro de suboperadores e os campos efetivamente enviados nos payloads.",
 'PRIV-16': "Identifique regiões de hospedagem (DB, storage, app, e-mail, IA) e o mecanismo de transferência documentado para cada destino fora do Brasil.",
 'PRIV-17': "Procure playbook de incidente com dados pessoais, critérios de risco relevante, prazo de 3 dias úteis, registro de incidentes (5 anos), capacidade de dimensionar titulares afetados via logs.",
 'PRIV-18': "Verifique designação do encarregado, divulgação pública (nome e contato) no site/app e na política.",
 'PRIV-19': "Procure RIPD/DPIA, critérios de quando elaborar e a triagem de privacidade no processo de produto.",
 'PRIV-20': "Procure programa de governança, políticas internas, indicadores e auditorias periódicas registradas (inclusive execuções anteriores deste assessment).",
 'PRIV-21': "Aplica-se apenas a órgão público ou tratamento em nome do poder público; caso contrário, N/A com justificativa.",
 'PRIV-22': "Verifique guarda de registros do Marco Civil, relação de consumo (CDC) e normas setoriais aplicáveis ao produto.",
 'PRIV-23': "Avalie se as evidências exigidas pela ANPD estão reunidas e recuperáveis (ROPA, avisos, consentimentos, contratos, incidentes, RIPDs).",
 'PRIV-24': "Procure repositório de evidências versionado e matriz requisito → evidência (este relatório versionado conta como parte da evidência).",
 'AIR-1': "Leia `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, `.github/copilot-instructions.md`, `GEMINI.md`: tamanho, conteúdo (mapa, stack, comandos, restrições), duplicação/contradição, CODEOWNERS sobre esses arquivos, verificação automática em CI.",
 'AIR-2': "Procure skills (`.claude/skills`, `skills/`), geradores (`plop`, scripts de scaffold), config de MCP (`.mcp.json`), hooks (`.claude/settings.json`, Husky/lint-staged) e documentação de dependências na versão usada.",
 'AIR-3': "Procure README, arquitetura, ADRs, glossário, contexto de negócio, matriz de autorização e requisitos não funcionais documentados e encontráveis.",
 'AIR-4': "Avalie estrutura de pastas, regras de import/arquitetura (`eslint-plugin-boundaries`, `dependency-cruiser`), tamanho de arquivos (liste os maiores), código gerado isolado, código morto, exemplos canônicos citados nas instruções.",
 'AIR-5': "Verifique `strict` no `tsconfig`, typecheck em CI, regras contra `any`/`@ts-ignore`, validação de borda e sincronização de contratos (OpenAPI gerado/verificado), testes de contrato.",
 'AIR-6': "Execute (quando seguro) os comandos documentados: install, lint, typecheck, test, build. Verifique se existe um comando único de verificação, execução por arquivo/pacote, ambiente reproduzível (Docker Compose/dev container) e versões fixadas.",
 'AIR-7': "Avalie a suíte de testes: tipos de teste presentes, espelhamento, factories/fixtures, determinismo (datas, rede), mutation testing, regra de \"teste antes de corrigir\" nas instruções.",
 'AIR-8': "Leia o CI e as configs de lint: SAST, secret scanning, SCA, testes de arquitetura, budgets, regras específicas para erros típicos de agentes, política de dependências novas, áreas protegidas no CODEOWNERS.",
 'AIR-9': "Verifique arquivos de ignore para agentes (`.cursorignore`, `.claudeignore`, `.aiexclude`, permissões em `.claude/settings.json`), tamanho somado dos arquivos de contexto, divisão de docs por domínio.",
 'AIR-10': "Verifique permissões configuradas para agentes (allowlist de comandos), bloqueio de leitura de `.env`, guardrails documentados (sem push em main, sem prod), revisão de plugins/MCP, rastreabilidade de commits gerados (trailer `Co-Authored-By`), política de uso de IA.",
 'AIR-11': "Verifique se a app sobe isolada por worktree (portas/bancos configuráveis), comandos de diagnóstico documentados e verificação de UI automatizada (e2e/browser).",
 'AIR-12': "Procure planos/specs versionados, ADRs, `tasks/lessons.md` ou equivalente e o fluxo de especificação antes do código.",
 'AIR-13': "Verifique templates de PR/issue, tamanho típico das PRs (`gh pr list`), revisão humana + automatizada documentada e checkpoints/rollback.",
 'AIR-14': "Procure métricas de efetividade de agentes, registro de melhorias sistêmicas após erros recorrentes e tarefas de referência para avaliação.",
 'AIR-15': "Verifique diretamente os arquivos citados em cada item (`CONTRIBUTING.md`, `.env.example` × `process.env.*` no código, índice de scripts, catálogos de i18n, `.github/ISSUE_TEMPLATE`, `docs/assessments/`, estrutura de pastas).",
}

ITEM_RE = re.compile(r'^- \[ \] (?:🆕 |✎ )*\*\*(?P<id>[A-Z]+-\d+\.\d+) · (?P<title>.+?)\*\* `\[(?P<sev>[BAMR])\]`(?P<rest>.*)$')
COND_RE = re.compile(r'\*\(Se: (.+?)\)\*')
LEGAL_RE = re.compile(r'^\s*\[([^\]]+)\]')


def clean(s):
    return s.replace('🆕 ', '').replace('🆕', '').replace('✎ ', '').strip()


def parse(lines):
    pillars = {}
    current = None
    section = None
    for line in lines:
        if line.startswith('## Anexo'):
            break
        hit = [p for p in PILLARS if line.startswith(p[0])]
        if hit:
            current = hit[0]
            pillars[current[3]] = {'meta': current, 'intro': [], 'sections': []}
            section = None
            continue
        if current is None:
            continue
        P = pillars[current[3]]
        m = re.match(r'^### (\d+)\. (.+)$', line)
        if m:
            section = {'num': m.group(1), 'title': clean(m.group(2)), 'notes': [], 'items': [], 'sub': None}
            P['sections'].append(section)
            continue
        m = re.match(r'^#### (\d+\.\d+) (.+)$', line)
        if m and section:
            section['items'].append(('SUB', f"{m.group(1)} {clean(m.group(2))}"))
            continue
        if line.startswith('#### '):
            section = None  # matriz de cobertura etc. fica fora
            continue
        m = ITEM_RE.match(line)
        if m and section:
            rest = m.group('rest')
            cond = COND_RE.search(rest)
            head, _, text = rest.partition(' — ')
            legal = LEGAL_RE.search(COND_RE.sub('', head))
            section['items'].append({
                'id': m.group('id'), 'title': m.group('title'), 'sev': m.group('sev'),
                'cond': cond.group(1) if cond else None,
                'legal': legal.group(1) if legal else None,
                'text': text.strip(),
            })
            continue
        if section is None and line.startswith('>'):
            P['intro'].append(line)
        elif section is not None and not section['items'] and line.strip() and not line.startswith('- ['):
            section['notes'].append(line.strip())
    return pillars


def render(code, P):
    _, skill, name, prefix = P['meta']
    out = []
    counts = Counter()
    out.append(f"# Catálogo de critérios — {name}\n")
    out.append("> Gerado a partir do *Checklist sênior para assessment de aplicações — v3* (outubro/2026). "
               "Não edite à mão: regenere com `python -X utf8 scripts/gen-assessment-catalog.py` no ai-toolbox "
               "(fonte: `docs/application-assessment-v3.md`). IDs, severidades e critérios são a base do score "
               "e precisam ser estáveis entre execuções.\n")
    out.append("**Severidade (fixa por item):** `[B]` Bloqueante → **Crítico** (peso 3) · `[A]` Alto → **Importante** (peso 2) · "
               "`[M]` Médio e `[R]` Recomendado → **Menor** (peso 1).\n")
    out.append("**Itens condicionais** (*Se: …*): quando a condição não se aplica, marque **N/A com justificativa e evidência** "
               "(ex.: busca no código sem ocorrências). N/A sem evidência conta como Não compliant.\n")
    if P['intro']:
        out.append("## Objetivo do pilar\n")
        out.extend(P['intro'])
        out.append('')
    secs = list(P['sections'])
    for s in secs:
        key = f"{prefix}-{s['num']}"
        out.append(f"## {prefix}-{s['num']}. {s['title']}\n")
        if key in GUIDE:
            out.append(f"**Como verificar:** {GUIDE[key]}\n")
        for n in s['notes']:
            out.append(n)
        if s['notes']:
            out.append('')
        for it in s['items']:
            if isinstance(it, tuple) and it[0] == 'SUB':
                out.append(f"### {it[1]}\n")
                continue
            label, w = SEV[it['sev']]
            counts[label] += 1
            meta = [f"**{label}** (peso {w}, origem `[{it['sev']}]`)"]
            if it['cond']:
                meta.append(f"Condicional — *Se: {it['cond']}*")
            if it['legal']:
                meta.append(f"Fundamento: {it['legal']}")
            out.append(f"#### {it['id']} · {it['title']}")
            out.append(' · '.join(meta) + '  ')
            out.append(it['text'] + '\n')
    total = sum(counts.values())
    summary = (f"**Total de itens:** {total} — Crítico: {counts['Crítico']} · Importante: {counts['Importante']} · Menor: {counts['Menor']}. "
               f"Pontuação máxima (todos aplicáveis): {counts['Crítico']*3 + counts['Importante']*2 + counts['Menor']}.\n")
    out.insert(4, summary)
    path = os.path.join(OUT, skill, 'references')
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'checklist.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(out).rstrip() + '\n')
    return total, counts


lines = open(SRC, encoding='utf-8').read().splitlines()
pillars = parse(lines)
grand = 0
for code, P in pillars.items():
    total, counts = render(code, P)
    grand += total
    print(code, total, dict(counts))
print('itens no fonte:', sum(1 for l in lines if l.startswith('- [ ]')), '| gerados:', grand)
