# Catálogo de critérios — Security

> Gerado a partir do *Checklist sênior para assessment de aplicações — v3* (outubro/2026). Não edite à mão: regenere com `python -X utf8 scripts/gen-assessment-catalog.py` no ai-toolbox (fonte: `docs/application-assessment-v3.md`). IDs, severidades e critérios são a base do score e precisam ser estáveis entre execuções.

**Severidade (fixa por item):** `[B]` Bloqueante → **Crítico** (peso 3) · `[A]` Alto → **Importante** (peso 2) · `[M]` Médio e `[R]` Recomendado → **Menor** (peso 1).

**Itens condicionais** (*Se: …*): quando a condição não se aplica, marque **N/A com justificativa e evidência** (ex.: busca no código sem ocorrências). N/A sem evidência conta como Não compliant.

**Total de itens:** 153 — Crítico: 48 · Importante: 89 · Menor: 16. Pontuação máxima (todos aplicáveis): 338.

## Objetivo do pilar

> **Objetivo do pilar:** ao atingir score alto aqui, a aplicação deve resistir às técnicas conhecidas de ataque (OWASP Top 10:2025, OWASP API Security Top 10, categorias da ASVS 5.0), expor o mínimo de informação útil a um atacante e, onde a exposição é inevitável, ter impacto **contido, localizado, detectável e recuperável** — incluindo um plano de Disaster Recovery explícito e testado.
>
> **Regra de ouro:** todo controle é verificado **server-side** e **por teste negativo** (o atacante tentando e falhando), não pela existência do código. “Esconder botão”, “não está documentado” e “ninguém sabe a URL” não são controles.

## SEC-1. Escopo, arquitetura e ameaça

**Como verificar:** Procure inventário de ativos, diagramas/fluxos (`docs/architecture*`), threat model, decisões de segurança (ASVS), classificação de dados no schema. Documentos genéricos sem vínculo a componentes reais = Parcial.

#### SEC-1.01 · Inventário de ativos
**Crítico** (peso 3, origem `[B]`)  
listar aplicações, APIs, frontends, mobile, workers, cron, consumers, funções serverless, gateways, bancos, caches, filas, buckets, registries, CI/CD, domínios, subdomínios, certificados, ambientes e versões; comparar o inventário declarado com descoberta ativa (DNS, Certificate Transparency, varredura de portas, rotas reais do gateway). Ativos sem owner são achado.

#### SEC-1.02 · Mapa de fluxos
**Importante** (peso 2, origem `[A]`)  
documentar entradas, saídas, trust boundaries, identidades, dados, protocolos, terceiros, privilégios e fluxos administrativos. Cada fluxo possui owner, autenticação, autorização, logging e risco. O diagrama é atualizado a cada mudança arquitetural e versionado com o código.

#### SEC-1.03 · Threat model
**Importante** (peso 2, origem `[A]`)  
STRIDE/abuse cases ou método equivalente cobre spoofing, tampering, repudiation, disclosure, denial of service e elevation of privilege, além de abuso de lógica de negócio; ameaças são ligadas a controles, testes e achados. O modelo é revisado em toda feature de risco (pagamento, auth, upload, integrações, IA).

#### SEC-1.04 · Padrão e nível de rigor
**Importante** (peso 2, origem `[A]`)  
fixar **OWASP ASVS 5.0.0** e o nível aplicável (L1/L2/L3) por componente; registrar as **decisões de segurança documentadas** que a ASVS 5.0 exige para requisitos configuráveis; mapear requisitos a componentes e excluir apenas itens com justificativa. Complementar com OWASP Top 10:2025, API Security Top 10, MASVS (mobile), LLM/Agentic Top 10 (IA), supply chain e regras de negócio.

#### SEC-1.05 · Requisitos de segurança no ciclo de desenvolvimento
**Menor** (peso 1, origem `[M]`)  
histórias de risco têm critérios de aceite de segurança e casos de abuso; existe definição de pronto com checagens de segurança; práticas seguem um framework de desenvolvimento seguro (ex.: NIST SSDF / OWASP SAMM) com maturidade medida.

#### SEC-1.06 · Ambiente do teste
**Importante** (peso 2, origem `[A]`)  
produção não é usada sem autorização; dados são sintéticos/mascarados; contas de teste cobrem papéis, tenants, estados e privilégios; origem, janela, limites e regras de engajamento estão documentados. O ambiente de teste é equivalente a produção em configuração de segurança (mesmos headers, WAF, IAM, versões).

#### SEC-1.07 · Modelo de impacto
**Importante** (peso 2, origem `[A]`)  
classificar confidencialidade, integridade, disponibilidade, privacidade, fraude, impacto financeiro, lateral movement e blast radius. A severidade considera explorabilidade e impacto combinado (encadeamento de achados).

#### SEC-1.08 · Classificação de dados
**Importante** (peso 2, origem `[A]`)  
dados são classificados (público, interno, confidencial, pessoal, pessoal sensível, credencial, financeiro) e a classificação está anotada no schema/modelos de dados, orientando criptografia, logging, retenção e acesso.

## SEC-2. Identidade, autenticação e sessão

**Como verificar:** Leia o fluxo completo de auth: hash de senha (`argon2`/`bcrypt` e parâmetros), política de senha, rate limit/lockout e de onde vem o IP (`x-forwarded-for` confiável?), geração/validação de JWT (algoritmos, `iss`/`aud`/`exp`, revogação), cookies de sessão, reset de senha (token, hash, expiração, `Host` header), MFA/WebAuthn, OAuth. Confirme com os testes existentes (testes negativos contam como E3).

#### SEC-2.01 · Registro de contas
**Importante** (peso 2, origem `[A]`)  
e-mail/telefone/username não permitem enumeração por resposta, tempo, código, redirect ou recuperação; duplicidade, normalização (Unicode, maiúsculas, pontos/`+` em e-mail, homógrafos) e takeover de conta pré-existente são tratados. Registro automatizado em massa é limitado (rate limit, verificação de contato, desafio adaptativo).

#### SEC-2.02 · Senha
**Crítico** (peso 3, origem `[B]`)  
senha é recebida apenas por TLS, nunca logada, armazenada com hash adaptativo moderno e salt único (Argon2id, scrypt, bcrypt ou PBKDF2 com parâmetros atuais), com parâmetros revisados periodicamente; comprimento mínimo conforme NIST SP 800-63B-4 (15 caracteres quando a senha é fator único; 8 quando faz parte de MFA), máximo de pelo menos 64, aceita espaços e Unicode; checagem contra senhas vazadas/comuns; **sem** regras de composição arbitrárias e **sem** troca periódica forçada (apenas por suspeita de comprometimento). Custo do hash é limitado para não virar vetor de DoS (rate limit antes do hash, tamanho máximo de entrada).

#### SEC-2.03 · Autenticação resistente a phishing
**Importante** (peso 2, origem `[A]`)  
passkeys/WebAuthn (FIDO2) são oferecidos e **exigidos** para administradores e operações críticas; OTP por SMS não é o único segundo fator para contas privilegiadas.

#### SEC-2.04 · Brute force, credential stuffing e evasão de rate limit
**Crítico** (peso 3, origem `[B]`)  
login, reset, MFA, OTP, magic link, convite e API key têm rate limit por conta, IP, dispositivo e contexto; lockout progressivo não permite negação de serviço simples contra a vítima. O sistema é resiliente a evasão por spoofing de headers (`X-Forwarded-For`, `X-Real-IP`, `True-Client-IP` — o IP do cliente só é lido do proxy confiável), rotação de proxies residenciais, variação de capitalização/encoding do identificador e paralelismo (race em contador de tentativas). Há detecção de credential stuffing (taxa de falhas distribuída, senhas vazadas).

#### SEC-2.05 · MFA
**Crítico** (peso 3, origem `[B]`)  
enrollment, recovery, troca de fator, step-up e desativação resistem a takeover, SIM swap, replay, phishing previsível, fadiga de push (number matching) e bypass de endpoint (ex.: acessar rota pós-login sem completar o segundo fator). Fator forte é exigido para funções críticas. Códigos de recuperação são de uso único, armazenados com hash.

#### SEC-2.06 · Tokens JWT
**Crítico** (peso 3, origem `[B]`) · Condicional — *Se: JWT*  
validação segue RFC 8725: allowlist explícita de algoritmo (bloqueia `none` e confusão RS256/HS256), assinatura, `iss`, `aud`, `exp`, `nbf`, `iat` com tolerância de relógio pequena, `typ` quando aplicável; os cabeçalhos `kid`, `jku`, `x5u` e `jwk` não permitem path traversal, injeção de chave ou busca de chave em URL controlada pelo atacante. Tokens de acesso são de vida curta; revogação (lista de negação, versão de sessão ou introspecção) existe para logout, reset e troca de privilégio. JWT não carrega dados sensíveis em claro.

#### SEC-2.07 · Sessões
**Crítico** (peso 3, origem `[B]`)  
IDs têm ≥ 128 bits de entropia, gerados por CSPRNG, regenerados após login/elevação de privilégio (anti-fixation), invalidados no servidor em logout/reset/troca de senha e possuem expiração idle e absoluta. Cookies usam `Secure`, `HttpOnly`, `SameSite` adequado e prefixo `__Host-` quando possível; sessão não aparece em URL/referrer/log. Usuário vê e encerra sessões ativas.

#### SEC-2.08 · Recovery
**Crítico** (peso 3, origem `[B]`)  
reset usa token único, aleatório (≥ 128 bits), de vida curta, armazenado com hash, vinculado ao usuário, invalidado após uso e quando outro é emitido; não revela existência de conta. Link de reset não é construído a partir do header `Host` (host header poisoning). Não há troca de e-mail/telefone sem reautenticação; após reset ou troca, sessões e tokens existentes são invalidados e o titular é notificado no canal antigo.

#### SEC-2.09 · OAuth/OIDC
**Crítico** (peso 3, origem `[B]`) · Condicional — *Se: OAuth/OIDC*  
segue o OAuth 2.0 Security BCP (RFC 9700): authorization code + PKCE para todos os clientes, sem implicit grant nem password grant; `state`, `nonce`, allowlist exata de redirect URI (sem curingas), validação de `iss` (mix-up attack), escopos mínimos; account linking não vincula automaticamente por e-mail não verificado. Tokens não vazam por URL, referrer ou log. Tokens sender-constrained (DPoP/mTLS) avaliados para APIs de alto risco.

#### SEC-2.10 · API keys e service accounts
**Importante** (peso 2, origem `[A]`)  
são escopadas, expiradas/rotacionadas, identificáveis (prefixo que permite secret scanning), armazenadas com hash no servidor, revogáveis e nunca embutidas no cliente. Uso, origem e falhas são auditados; chaves de teste não alcançam produção.

#### SEC-2.11 · Autenticação federada
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: SSO/SAML/OIDC corporativo*  
mapeamento de claims, grupos, domínio, assinatura (SAML: validação de assinatura do elemento correto, defesa contra XML signature wrapping), relógio, logout e provisionamento/desprovisionamento (SCIM) são validados. Claims controláveis pelo usuário não concedem privilégios; usuário removido no IdP perde acesso em prazo definido.

#### SEC-2.12 · Reautenticação e step-up
**Importante** (peso 2, origem `[A]`)  
ações sensíveis (troca de e-mail/senha/MFA, exportação de dados, criação de API key, alteração de dados bancários) exigem reautenticação recente ou step-up, independentemente da sessão estar ativa.

#### SEC-2.13 · Notificações de segurança ao usuário
**Menor** (peso 1, origem `[M]`)  
o usuário é notificado de login em novo dispositivo, troca de senha/MFA/e-mail, criação de credenciais e exportação de dados, com caminho para reagir (“não fui eu”).

## SEC-3. Autorização, tenancy e lógica de negócio

**Como verificar:** Mapeie todas as rotas e verifique, por rota, autenticação e checagem de ownership/papel no servidor (middleware/use case). Procure IDs vindos do path/body usados sem checagem, DTOs de saída, mass assignment (`...body` em update), operações sem transação/condição atômica (race). Testes de autorização negativa são a evidência principal.

#### SEC-3.01 · Matriz de autorização
**Crítico** (peso 3, origem `[B]`)  
existe matriz explícita de ator × ação × recurso × propriedade × estado × tenant; testes automatizados positivos e negativos cobrem cada combinação. Default deny é aplicado server-side, de forma centralizada (middleware/policy engine), não espalhado em `if`s.

#### SEC-3.02 · BOLA/IDOR
**Crítico** (peso 3, origem `[B]`)  
IDs de objetos, arquivos, mensagens, pedidos, relatórios, jobs e exports são trocados entre contas/tenants; servidor impede leitura, alteração, exclusão e inferência indireta (contagem, timing, mensagens de erro diferentes). IDs não sequenciais reduzem enumeração, mas **não** substituem a checagem de autorização.

#### SEC-3.03 · BFLA
**Crítico** (peso 3, origem `[B]`)  
funções admin, debug, internal, bulk, import/export, impersonation e maintenance são testadas por usuário comum, papel inferior e token sem escopo; troca de método HTTP (GET→DELETE/PUT), versão de API antiga e rota alternativa não contornam o controle.

#### SEC-3.04 · Property-level authorization
**Crítico** (peso 3, origem `[B]`)  
campos read-only, internos, financeiros, flags, owner, role, tenant e status não podem ser lidos ou alterados por mass assignment, JSON merge, GraphQL selection ou campos extras; respostas são serializadas por DTO/allowlist por papel.

#### SEC-3.05 · Autorização em cada camada
**Importante** (peso 2, origem `[A]`)  
gateway, controller, service, repository, job, consumer, websocket e storage não assumem que camada anterior autorizou. Chamadas internas não são automaticamente confiáveis (zero trust entre serviços com identidade de workload).

#### SEC-3.06 · Tenant isolation e vazamento entre tenants
**Crítico** (peso 3, origem `[B]`) · Condicional — *Se: multi-tenant*  
IDs, filtros, cache keys, filas, índices de busca, índices vetoriais, exports, logs, backups e observabilidade não cruzam tenants. O tenant vem do contexto autenticado, nunca de parâmetro do cliente. Testes provam que tokens de um tenant não acessam subdomínios, endpoints ou dados (inclusive em memória/cache) de outro. Mecanismos de reforço no banco (ex.: row-level security) são considerados como defesa em profundidade.

#### SEC-3.07 · Estados e transições
**Importante** (peso 2, origem `[A]`)  
workflow valida estado atual, ator, ordem, concorrência, expiração e pré-condições server-side. Não há salto de draft para approved, refund duplicado, pular etapa de pagamento ou cancelamento após finalização por race.

#### SEC-3.08 · Funções sensíveis
**Importante** (peso 2, origem `[A]`)  
pagamento, saque, alteração de conta, exclusão, convite, mudança de owner, exportação e impersonation exigem step-up, confirmação, idempotência, trilha de auditoria e limites (valor, frequência). Operações de altíssimo impacto têm controle de quatro olhos.

#### SEC-3.09 · Race conditions
**Importante** (peso 2, origem `[A]`)  
requests concorrentes (incluindo ataque de pacote único/single-packet) testam saldo, cupom, estoque, aprovação, reset, convite, upload, lock, limite de tentativas e mudança de privilégio. Resultado é atomicamente consistente (constraint, lock, transação ou operação condicional) e não depende apenas de validação anterior.

#### SEC-3.10 · Integridade de valores de negócio
**Importante** (peso 2, origem `[A]`)  
preço, desconto, quantidade, moeda, frete, taxa e limites são calculados ou revalidados no servidor; valores negativos, zero, decimais extremos, overflow, arredondamento e unidades trocadas são testados.

#### SEC-3.11 · Workflow abuse
**Importante** (peso 2, origem `[A]`)  
fluxos legítimos não podem ser automatizados para fraude, spam, scraping, compra indevida, criação massiva, abuso de referral, enumeração ou consumo pago (SMS, e-mail, IA) sem controles compensatórios (limites, detecção de bot, custo progressivo, revisão).

#### SEC-3.12 · Decisões offline/async
**Importante** (peso 2, origem `[A]`)  
autorização é revalidada no worker no momento do efeito; mensagem antiga, job de usuário removido ou evento reprocessado não executa ação indevida. Mensagens carregam identidade verificável, não apenas um `user_id` confiado.

#### SEC-3.13 · Impersonation/support
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: há acesso de suporte*  
suporte pode atuar somente com escopo, consentimento/registro, banner visível, expiração, motivo e auditoria; não há acesso invisível nem sessão compartilhada; ações destrutivas sob impersonation são bloqueadas ou exigem aprovação.

#### SEC-3.14 · Acesso a arquivos e objetos armazenados
**Crítico** (peso 3, origem `[B]`)  
arquivos privados não ficam em bucket público nem em URL adivinhável; download passa por autorização ou URL assinada de vida curta, emitida após checagem de permissão, com escopo de um objeto.

## SEC-4. Entrada, validação e injeções

**Como verificar:** Procure validação de schema na borda (Zod/Joi/class-validator) em TODAS as rotas, queries raw (`$queryRaw`, `$runCommandRaw`, concatenação), operadores Mongo vindos do input, `child_process`, templates/HTML gerado, manipulação de caminhos, `fetch` de URL do usuário (SSRF), desserialização, `merge` profundo, regex sobre input, upload (magic bytes, tamanho, re-encode).

#### SEC-4.01 · Validação de esquema
**Crítico** (peso 3, origem `[B]`)  
body, query, path, header, cookie, multipart, websocket, evento e metadata validam tipo, tamanho, charset, range, profundidade, campos desconhecidos e encoding na fronteira, com allowlist; validação no cliente é apenas UX.

#### SEC-4.02 · SQL/ORM
**Crítico** (peso 3, origem `[B]`)  
queries são parametrizadas; concatenação dinâmica, filtros opcionais, `ORDER BY`/nome de coluna controlável (exige allowlist), `IN`, `LIKE` (escape de curingas), raw queries do ORM, stored procedures e migrations são testados. ORM não é considerado proteção automática. Usuário de banco da aplicação não tem DDL nem privilégios administrativos.

#### SEC-4.03 · NoSQL e linguagens de consulta
**Crítico** (peso 3, origem `[B]`) · Condicional — *Se: NoSQL, motores de busca, linguagens de filtro*  
operadores (`$where`, `$ne`, `$regex`, `$gt`), objetos onde se espera string, JSON query, consultas de motores de busca e expressões de filtro são rejeitados ou allowlistados. *(Controles de GraphQL consolidados em SEC-5.15.)*

#### SEC-4.04 · Command/OS injection
**Crítico** (peso 3, origem `[B]`)  
argumentos são passados sem shell (array de argumentos); allowlist de comandos/opções, `--` antes de argumentos posicionais, ambiente mínimo, timeout, filesystem restrito e usuário não privilegiado. Testar metacaracteres, newline e injeção de argumentos (ex.: opções iniciadas por `-`).

#### SEC-4.05 · Template injection
**Crítico** (peso 3, origem `[B]`)  
templates, e-mail, PDF, markdown e geração de HTML não avaliam expressão controlável. Testar SSTI, XSS armazenado, escaping contextual e conteúdo rico; templates de usuário (se existirem) rodam em sandbox lógico sem acesso a objetos do runtime.

#### SEC-4.06 · LDAP/XML
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: LDAP/XML/SAML/SOAP/SVG/Office*  
filtros LDAP usam escape correto; parsers XML desabilitam DTD/entidades externas e limitam expansão, tamanho e profundidade; XXE, SSRF via XML e billion laughs são testados, inclusive em formatos baseados em XML (DOCX, XLSX, SVG).

#### SEC-4.07 · Path traversal
**Crítico** (peso 3, origem `[B]`)  
caminhos, nomes, zip/tar (zip slip), symlink e downloads são normalizados e confinados a um diretório base após resolução do caminho real; `..`, encoding duplo, null byte, UNC, separadores alternativos e links simbólicos são testados. Nome de arquivo do usuário não é usado como caminho de armazenamento.

#### SEC-4.08 · SSRF e metadados de nuvem
**Crítico** (peso 3, origem `[B]`) · Condicional — *Se: o servidor busca URLs, renderiza HTML/PDF, importa por link, recebe webhooks configuráveis*  
URLs são allowlistadas por esquema, host e porta; resolução DNS é validada no momento da conexão (anti DNS rebinding); IPv4/IPv6 privados, loopback, link-local, representações alternativas de IP (decimal, octal, IPv6-mapped) e redirects são bloqueados; esquemas `file`, `gopher`, `dict`, `ftp` desabilitados. Acesso a endpoints de metadados de nuvem a partir de input do usuário é bloqueado na aplicação **e** na infraestrutura (IMDSv2 com hop limit 1 ou equivalente, ver SEC-7.05); egress é segmentado por proxy de saída.

#### SEC-4.09 · Deserialização
**Crítico** (peso 3, origem `[B]`)  
formatos e classes permitidos são explícitos; não se desserializa objeto arbitrário de fonte não confiável (Java native serialization, pickle, YAML inseguro, BinaryFormatter etc.); assinatura/integridade e limites são verificados antes de desserializar.

#### SEC-4.10 · Prototype pollution e mass merge
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: JavaScript/TypeScript*  
merges profundos, parsers de query string e clonagem de objetos rejeitam `__proto__`, `constructor` e `prototype`; objetos de configuração são criados sem protótipo ou congelados quando apropriado.

#### SEC-4.11 · Regex e parser DoS
**Importante** (peso 2, origem `[A]`)  
expressões, JSON, YAML, CSV, imagem, PDF e multipart têm limites de tempo, tamanho, profundidade e memória; regex catastrófica (ReDoS) é testada ou motor de regex de tempo linear é usado para entrada não confiável.

#### SEC-4.12 · Headers e protocol smuggling
**Importante** (peso 2, origem `[A]`)  
CRLF injection, host header poisoning, forwarded headers, headers duplicados, request desync (CL.TE, TE.CL, TE.TE, H2 downgrade), cache poisoning e normalização divergente entre proxy e app são avaliados. O header `Host` é validado contra allowlist.

#### SEC-4.13 · Upload
**Crítico** (peso 3, origem `[B]`) · Condicional — *Se: upload*  
extensão (allowlist), MIME real por conteúdo (magic bytes), tamanho, decompression bomb, polyglot, macro, SVG com script, nome de arquivo, quota, antivírus/sandbox e reprocessamento (re-encode de imagens, remoção de metadados EXIF) são controlados. Arquivos são servidos de domínio separado (sem cookies da aplicação) ou com `Content-Disposition: attachment` e `X-Content-Type-Options: nosniff`; nunca executados.

#### SEC-4.14 · Output encoding
**Crítico** (peso 3, origem `[B]`)  
HTML, atributos, JS, CSS, URL, JSON, SQL, shell, CSV (formula injection: `=`, `+`, `-`, `@`) e logs (log injection/forging) usam encoding de contexto; DOM sinks perigosos e bypass por Unicode/normalização são testados.

#### SEC-4.15 · Canonicalização e Unicode
**Menor** (peso 1, origem `[M]`)  
entradas são normalizadas (NFC/NFKC conforme o caso) antes de validação e comparação; homógrafos, caracteres de controle e bidi (RTL override) são tratados em nomes, URLs e identificadores exibidos.

#### SEC-4.16 · E-mail e notificações
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: envia e-mail/SMS*  
conteúdo controlado pelo usuário não injeta headers de e-mail, links ou HTML em mensagens enviadas pelo domínio da empresa (abuso para phishing); remetente usa SPF, DKIM e DMARC com política de rejeição.

## SEC-5. Web, browser e APIs

**Como verificar:** Verifique CSRF (tokens/`Origin`/`SameSite`), CORS, CSP e headers (`next.config.*`, middleware, `securityHeaders`), uso de `dangerouslySetInnerHTML`/`innerHTML`, cookies, `localStorage`, redirects, inventário de rotas vs OpenAPI, rate limit, formato de erro, webhooks recebidos.

#### SEC-5.01 · CSRF
**Crítico** (peso 3, origem `[B]`) · Condicional — *Se: autenticação por cookie*  
operações state-changing exigem token anti-CSRF e/ou verificação de `Origin`/Fetch Metadata (`Sec-Fetch-Site`), com `SameSite` coerente; operações de mudança de estado nunca usam GET. Login CSRF, JSON CSRF (content-type simples), multipart e endpoints alternativos são testados.

#### SEC-5.02 · CORS
**Crítico** (peso 3, origem `[B]`)  
origens não são refletidas nem validadas por regex frágil (sufixo/prefixo); `null` origin é rejeitada; `Access-Control-Allow-Credentials` só com allowlist exata; métodos, headers e preflight restritos. API não expõe resposta sensível a origem não confiável.

#### SEC-5.03 · Subdomain takeover e higiene de DNS
**Importante** (peso 2, origem `[A]`)  
registros DNS (CNAME, A, NS, MX) apontando para recursos desativados (buckets, apps de PaaS, CDNs) são detectados continuamente e removidos; subdomínios de terceiros não compartilham escopo de cookie com a aplicação; CAA restringe emissores de certificado; DNSSEC avaliado.

#### SEC-5.04 · CSP
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: frontend web*  
CSP estrita baseada em nonce ou hash (com `strict-dynamic`), sem `unsafe-inline`/`unsafe-eval`, com `object-src 'none'`, `base-uri 'none'`/`'self'`, `frame-ancestors` e relatório de violações monitorado. Trusted Types é avaliado para eliminar DOM XSS em aplicações ricas.

#### SEC-5.05 · Headers de segurança
**Importante** (peso 2, origem `[A]`)  
HSTS (com `includeSubDomains` e preload quando viável), `X-Content-Type-Options: nosniff`, `Referrer-Policy` restritiva, `Permissions-Policy` mínima, `Cross-Origin-Opener-Policy`, `Cross-Origin-Resource-Policy` e, quando necessário, `Cross-Origin-Embedder-Policy`; `Cache-Control: no-store` em respostas sensíveis. Verificados em **todas** as respostas relevantes, inclusive erros, redirects e assets.

#### SEC-5.06 · XSS
**Crítico** (peso 3, origem `[B]`)  
refletido, armazenado, DOM, template, markdown, SVG, e-mail, preview, PDF gerado e dados importados são testados em todos os contextos, inclusive painel admin (onde o impacto é maior). Uso de APIs de escape bypass do framework (`dangerouslySetInnerHTML`, `v-html`, `innerHTML`, `bypassSecurityTrust*`) é inventariado e justificado, com sanitizador mantido (ex.: DOMPurify).

#### SEC-5.07 · Cookies
**Importante** (peso 2, origem `[A]`)  
escopo de domínio e path mínimo, flags corretas, prefixos `__Host-`/`__Secure-`; cookies sensíveis não são acessíveis a subdomínios menos confiáveis; logout limpa cookies e invalida a sessão no servidor.

#### SEC-5.08 · Armazenamento no cliente
**Importante** (peso 2, origem `[A]`)  
tokens e dados sensíveis não ficam em `localStorage`, `sessionStorage`, IndexedDB, URL, analytics, crash report ou cache de service worker sem justificativa documentada; dados locais são limpos no logout; respostas autenticadas não ficam em cache compartilhado.

#### SEC-5.09 · Clickjacking e comunicação entre janelas
**Importante** (peso 2, origem `[A]`)  
páginas sensíveis bloqueiam framing (`frame-ancestors`); `postMessage` valida `origin`, `source` e schema; `window.opener` é neutralizado (`noopener`/COOP); comunicação entre janelas não aceita comandos arbitrários.

#### SEC-5.10 · Open redirect
**Importante** (peso 2, origem `[A]`)  
redirects aceitam apenas destinos permitidos (allowlist ou caminhos relativos validados), sem bypass por encoding, userinfo (`@`), backslash, `//`, esquema alternativo (`javascript:`, `data:`) ou domínio parecido.

#### SEC-5.11 · Inventário de API
**Importante** (peso 2, origem `[A]`)  
especificações (OpenAPI/GraphQL schema), rotas reais, subdomínios, versões antigas, debug, health, métricas, GraphQL, websocket e endpoints de documentação são comparados; ativos esquecidos (shadow/zombie APIs) são removidos ou protegidos; versões antigas têm data de desligamento.

#### SEC-5.12 · Mass assignment
**Crítico** (peso 3, origem `[B]`)  
campos desconhecidos e privilegiados são rejeitados ou allowlistados; resposta não vaza campos internos. Testar POST/PUT/PATCH/merge, objetos aninhados e arrays.

#### SEC-5.13 · Rate limit e quotas
**Importante** (peso 2, origem `[A]`)  
limites existem por identidade, IP, tenant, endpoint, custo e operação; headers informam limite e retry; implementação distribuída e multirregional não permite bypass simples (troca de região, IPv6 com prefixo inteiro, variação de path/case/trailing slash).

#### SEC-5.14 · Recursos caros
**Importante** (peso 2, origem `[A]`)  
paginação, regex, export, relatório, busca, upload, envio de SMS/e-mail, biometria, chamadas pagas e IA têm custo máximo, timeout, quota e autorização (OWASP API4: consumo irrestrito de recursos).

#### SEC-5.15 · GraphQL
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: GraphQL*  
limites de profundidade, complexidade/custo, aliases, fragments e batching; autorização por campo/resolver; persisted queries/allowlist para clientes próprios; introspection **desabilitada** em produção para APIs privadas (para APIs públicas, permitida apenas se for decisão documentada, com os demais limites ativos); sugestões de campo (“did you mean”) desligadas; mensagens de erro sem detalhes internos.

#### SEC-5.16 · Web cache poisoning e web cache deception
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: CDN/cache reverso*  
chave de cache inclui todos os inputs que alteram a resposta (headers não chaveados são testados); respostas autenticadas/personalizadas não são cacheadas publicamente; truques de path (`/conta/perfil.css`, delimitadores, normalização) não fazem a CDN cachear página privada.

#### SEC-5.17 · WebSocket/SSE
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: tempo real*  
handshake autentica, `Origin` é validada (anti cross-site WebSocket hijacking), autorização por mensagem/canal, tokens expiram e a conexão é encerrada quando a sessão é revogada; mensagens têm schema/tamanho e conexão possui quota/timeout.

#### SEC-5.18 · Erros da API
**Importante** (peso 2, origem `[A]`)  
status, headers, mensagens, timing e paginação não revelam existência de recursos alheios, stack, versão, IDs internos, query ou dados de outros usuários. Formato de erro padronizado (ex.: Problem Details) sem campos de debug em produção.

#### SEC-5.19 · Subresource Integrity e terceiros no browser
**Menor** (peso 1, origem `[M]`)  
scripts/CSS de CDN de terceiros usam SRI ou são servidos do próprio domínio; inventário de scripts de terceiros por página existe, com monitoramento de mudança (proteção contra skimming/Magecart em páginas de pagamento).

#### SEC-5.20 · Webhooks recebidos
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: recebe webhooks*  
assinatura HMAC/mTLS verificada com comparação em tempo constante, timestamp com janela curta e proteção contra replay (ID de evento único), payload validado por schema, processamento idempotente; o conteúdo do webhook é tratado como não confiável.

#### SEC-5.21 · Métodos e content-types
**Menor** (peso 1, origem `[M]`)  
apenas métodos HTTP necessários são aceitos por rota (TRACE desabilitado; override de método via header/parâmetro controlado); content-type é validado e o servidor não interpreta corpo em formato diferente do declarado (ex.: aceitar XML onde se espera JSON).

## SEC-6. Criptografia, segredos e dados

**Como verificar:** Procure TLS desabilitado (`rejectUnauthorized: false`, `NODE_TLS_REJECT_UNAUTHORIZED`), segredos no código e no histórico (`git log -p`, padrões de chave), `.env` versionado, mascaramento no logger, uso de `Math.random` para tokens, algoritmos fracos (`md5`, `sha1`, `createCipher`), comparação de segredos sem tempo constante, TLS app→banco.

#### SEC-6.01 · TLS externo
**Crítico** (peso 3, origem `[B]`)  
TLS 1.2+ (preferencialmente 1.3), cipher suites com forward secrecy e AEAD, certificados válidos com cadeia completa, renovação automática e alerta de expiração, redirect HTTP→HTTPS, HSTS; não há validação de certificado desabilitada em nenhum cliente HTTP do código (verificado por busca no código).

#### SEC-6.02 · Comunicação interna
**Importante** (peso 2, origem `[A]`)  
tráfego entre serviços, banco, cache e filas é cifrado (TLS/mTLS ou malha de serviço) quando atravessa rede compartilhada; serviços internos autenticam-se mutuamente com identidade de workload.

#### SEC-6.03 · Criptografia em repouso
**Importante** (peso 2, origem `[A]`)  
banco, volumes, objetos, filas, backups, logs e dispositivos usam proteção proporcional; chave e dado não ficam no mesmo controle sem separação e auditoria.

#### SEC-6.04 · Criptografia em nível de campo
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: dados pessoais sensíveis, documentos, dados financeiros*  
campos de maior risco (documento, saúde, dados bancários, biometria) são cifrados na aplicação ou tokenizados, de forma que um dump do banco ou acesso indevido de DBA não exponha o valor em claro; busca usa hash com chave (blind index) quando necessário.

#### SEC-6.05 · Gestão de chaves
**Importante** (peso 2, origem `[A]`)  
geração, armazenamento, acesso, uso, rotação, revogação, destruição, backup e recuperação são documentados; KMS/HSM e envelope encryption são usados quando aplicável; chaves têm finalidade única; acesso a chaves é auditado.

#### SEC-6.06 · Segredos
**Crítico** (peso 3, origem `[B]`)  
scanner cobre histórico Git, branches, imagens de container, logs, CI, IaC, notebooks, fixtures, bundles do frontend e source maps; **push protection** bloqueia novos segredos; secret manager aplica least privilege, expiração, rotação e auditoria; segredo vazado tem procedimento de rotação imediata (remover do histórico não basta).

#### SEC-6.07 · Hardcoded/config
**Crítico** (peso 3, origem `[B]`)  
tokens, passwords, connection strings, private keys e credenciais de terceiros não aparecem em código ou configuração versionada. `.env`, dumps e arquivos de backup não são versionados nem servidos; credenciais de nuvem de longa duração são substituídas por federação de identidade (OIDC/workload identity).

#### SEC-6.08 · Dados em logs/telemetria
**Importante** (peso 2, origem `[A]`)  
PII, credenciais, headers `Authorization`, cookies, tokens, payloads e dados de pagamento são mascarados **antes** de log/export (redação na biblioteca de logging, não por convenção). Erro, trace, crash report e suporte não viram canal de vazamento. *(Ver PERF-2.14 e PRIV-12.)*

#### SEC-6.09 · Hash, tokens e aleatoriedade
**Importante** (peso 2, origem `[A]`)  
senhas, tokens de reset, API keys e identificadores secretos usam CSPRNG e hash adequados; comparações de segredos são em tempo constante; tokens não são previsíveis nem reutilizáveis. Não há uso de `Math.random`, `rand()` ou equivalente para segurança.

#### SEC-6.10 · Algoritmos e implementações
**Importante** (peso 2, origem `[A]`)  
apenas algoritmos atuais e bibliotecas maduras (sem criptografia própria); sem MD5/SHA-1 para segurança, sem ECB, sem IV/nonce reutilizado, sem RSA < 2048 bits; modos autenticados (AES-GCM, ChaCha20-Poly1305).

#### SEC-6.11 · Inventário criptográfico e preparação pós-quântica
**Menor** (peso 1, origem `[R]`)  
existe inventário de onde e como criptografia é usada (TLS, assinaturas, tokens, dados em repouso, integrações), permitindo trocar algoritmos sem reescrita (criptoagilidade); há plano de migração para algoritmos pós-quânticos padronizados pelo NIST e avaliação de TLS híbrido para dados com longa vida de confidencialidade (risco de “coletar agora, decifrar depois”).

#### SEC-6.12 · Minimização de exposição
**Importante** (peso 2, origem `[A]`)  
respostas, exports, debug, documentação, diretórios, source maps, banners e metadata publicam somente o necessário. Atacante não obtém versão/stack/topologia sem necessidade. *(Detalhado na seção 9.)*

## SEC-7. Configuração, infraestrutura e supply chain

**Como verificar:** Leia CI (`permissions:`, actions pinadas por SHA, `pull_request_target`, interpolação de `${{ github.event.* }}` em `run:`), lockfiles, SCA/Dependabot/Renovate, SBOM, Dockerfile (usuário não-root, base mínima), IaC, CODEOWNERS e proteção de branch (via `gh api` quando disponível), configurações de produção (debug, CORS, endpoints de exemplo).

#### SEC-7.01 · Defaults seguros
**Crítico** (peso 3, origem `[B]`)  
debug, verbose error, directory listing, admin seed, credenciais de exemplo, CORS amplo, métodos HTTP extras, consoles administrativos (actuator, profiler, admin de framework, phpMyAdmin etc.) e endpoints de teste estão desativados ou protegidos em produção — verificado por varredura, não só por configuração.

#### SEC-7.02 · Segregação de ambientes
**Importante** (peso 2, origem `[A]`)  
contas/projetos de nuvem, redes, bancos, buckets, secrets, pipelines e observabilidade de dev/stage/prod são separados; credencial de ambiente inferior não alcança produção; dados de produção não são copiados para ambientes inferiores sem anonimização.

#### SEC-7.03 · IAM
**Crítico** (peso 3, origem `[B]`)  
usuários, roles, workloads e serviços têm permissões mínimas, escopo por recurso, acesso temporário (just-in-time) para privilégios elevados, MFA para humanos, revisão periódica e revogação no desligamento; não há wildcard administrativo por conveniência nem conta root/owner usada no dia a dia. Contas de break-glass existem, são monitoradas e testadas.

#### SEC-7.04 · Rede e egress
**Importante** (peso 2, origem `[A]`)  
subnets, security groups, firewall, egress, DNS, metadata e administração são restritos; bancos, caches e filas não são acessíveis pela internet; acesso administrativo passa por bastion/zero-trust com MFA; segmentação limita movimento lateral; egress é allowlistado para serviços que não precisam de internet.

#### SEC-7.05 · Postura de nuvem (CSPM)
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: nuvem pública*  
configuração de nuvem é avaliada continuamente contra benchmark (ex.: CIS) por ferramenta de CSPM: buckets sem acesso público (bloqueio no nível da conta), serviço de metadados endurecido (ex.: IMDSv2 obrigatório com hop limit 1 na AWS ou equivalente), logs de auditoria da nuvem habilitados e protegidos, chaves de acesso antigas, snapshots públicos, security groups abertos. Desvios geram alerta com owner.

#### SEC-7.06 · Containers/Kubernetes
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: containers*  
não-root, `readOnlyRootFilesystem`, capabilities mínimas (`drop: ALL`), sem privileged/hostPath/hostNetwork, seccomp/AppArmor, Pod Security Standards em nível *restricted*, imagens verificadas por assinatura via admission policy, namespaces, network policies default deny, secrets não montados em pods que não precisam, service accounts sem token automático, API server não exposto publicamente, RBAC mínimo.

#### SEC-7.07 · Imagens base e runtime
**Importante** (peso 2, origem `[A]`)  
imagens base mínimas (distroless/slim), atualizadas com frequência definida, escaneadas no build e continuamente no registry; sem ferramentas de shell/compiladores desnecessários na imagem final.

#### SEC-7.08 · IaC
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: IaC*  
Terraform/Helm/CloudFormation/Pulumi tem scan de segurança, review, state protegido e cifrado (contém segredos), drift detection, ausência de secrets, mudanças destrutivas sinalizadas e plano auditável.

#### SEC-7.09 · Dependências (SCA)
**Crítico** (peso 3, origem `[B]`)  
lockfiles versionados, SBOM gerado por build (CycloneDX/SPDX), SCA com CVE/OSV em CI e contínuo, dependências transitivas incluídas, priorização por explorabilidade (CISA KEV, EPSS, alcançabilidade), licenças avaliadas, componentes fora de suporte (EOL) identificados, atualização automatizada com SLA.

#### SEC-7.10 · Ataques à cadeia de pacotes
**Importante** (peso 2, origem `[A]`)  
proteção contra dependency confusion (escopos/namespaces privados reservados e registry configurado para resolver pacotes internos apenas do repositório interno), typosquatting, pacotes comprometidos e maintainer takeover: scripts de instalação desabilitados por padrão quando possível, **período de quarentena** para versões recém-publicadas antes de adoção automática, verificação de proveniência quando disponível, revisão de dependências novas (popularidade, mantenedor, permissões).

#### SEC-7.11 · Artefatos
**Importante** (peso 2, origem `[A]`)  
imagens/pacotes/releases têm proveniência (SLSA), checksum, assinatura e verificação antes do deploy (ex.: Sigstore/cosign); registry impede sobrescrita de tags (imutabilidade) e promoção de artefato não aprovado; deploy referencia digest, não tag mutável.

#### SEC-7.12 · CI/CD
**Crítico** (peso 3, origem `[B]`)  
permissões de token mínimas por job (`permissions:` explícito); actions/workflows de terceiros pinados por SHA; PR de fork não executa com secrets nem com permissão de escrita (cuidado com `pull_request_target` e `workflow_run`); entradas não confiáveis (título de PR, nome de branch, corpo de issue) não são interpoladas em shell; deploy para nuvem usa OIDC em vez de chaves estáticas; runners self-hosted são efêmeros e isolados; logs de CI não imprimem segredos.

#### SEC-7.13 · Branch e revisão
**Importante** (peso 2, origem `[A]`)  
proteção exige revisão independente, checks obrigatórios, branch atualizado, CODEOWNERS para áreas sensíveis (auth, crypto, CI, IaC, dependências), bloqueio de force push e de exclusão, commits assinados avaliados e auditoria de bypass de administrador.

#### SEC-7.14 · SAST/DAST/fuzz
**Importante** (peso 2, origem `[A]`)  
SAST e secret scan rodam em todo PR; DAST autenticado roda periodicamente e antes de releases maiores; findings são triados com SLA (não apenas suprimidos — supressões têm justificativa e expiração); fuzzing cobre parsers, autenticação, autorização e propriedades críticas.

#### SEC-7.15 · Dependência de terceiros (SaaS/APIs)
**Importante** (peso 2, origem `[A]`)  
versões, escopos, endpoints, dados enviados, SLA, fallback, suboperadores e risco de supply chain estão inventariados; respostas externas são validadas como não confiáveis; credenciais de integração têm escopo mínimo e rotação.

#### SEC-7.16 · OpenSSF Scorecard
**Menor** (peso 1, origem `[M]`)  
checks de vulnerabilidades, updates, security policy, testes, SAST, branch protection, review, workflows perigosos, dependências pinadas, permissões de token e releases assinadas são executados e acompanhados, com meta de score.

#### SEC-7.17 · Proteção de borda
**Menor** (peso 1, origem `[M]`)  
WAF/regras de borda e proteção DDoS estão ativas para endpoints públicos, com regras ajustadas (modo bloqueio, não só monitoramento), sem substituir correção no código; origem não é acessível contornando a CDN/WAF (allowlist de IPs da borda ou autenticação de origem).

#### SEC-7.18 · Hardening de host e serviços gerenciados
**Menor** (peso 1, origem `[M]`)  
sistemas operacionais e serviços gerenciados seguem baseline (CIS ou equivalente), com patching automatizado e acesso SSH desabilitado ou via mecanismo auditado.

## SEC-8. Logs, detecção, resposta e recuperação

**Como verificar:** Procure eventos de auditoria no código (login, falhas, mudanças de papel, exports), destino e imutabilidade dos logs, regras de detecção, playbook de incidente, DRP com RPO/RTO e registro de exercícios, política e teste de restore de backup.

#### SEC-8.01 · Eventos auditáveis
**Crítico** (peso 3, origem `[B]`)  
login (sucesso/falha), MFA, reset, alteração de role, autorização negada, export, leitura de dado sensível, uso de segredo, mudança de config, deploy, operação destrutiva, acesso administrativo e impersonation geram evento suficiente para investigação.

#### SEC-8.02 · Conteúdo mínimo do evento
**Importante** (peso 2, origem `[A]`)  
cada evento registra quem (identidade e tipo de ator), o quê, sobre qual recurso, quando (UTC sincronizado), de onde (IP confiável, user agent, sessão), resultado e correlação (`trace_id`), sem registrar segredo ou dado sensível em claro.

#### SEC-8.03 · Integridade e acesso aos logs
**Importante** (peso 2, origem `[A]`)  
logs são enviados para armazenamento fora do alcance do serviço que os gera (conta/projeto separado), append-only/imutáveis (WORM), com timestamp confiável, retenção definida, controle por função e alerta para exclusão, alteração ou queda de ingestão.

#### SEC-8.04 · Detecção
**Importante** (peso 2, origem `[A]`)  
regras correlacionam brute force, credential stuffing, impossible travel, reuso de token, escalada de privilégio, scraping, exfiltração (volume anômalo de export/download), SSRF, abuso de API, mudança de pipeline/IAM e criação de credenciais; alertas têm owner, severidade, runbook e teste periódico (simulação de ataque).

#### SEC-8.05 · Incident response
**Crítico** (peso 3, origem `[B]`)  
playbook alinhado a referência atual (ex.: NIST SP 800-61r3) cobre triagem, severidade, contenção, revogação de tokens e sessões, rotação de segredos, isolamento, preservação de evidência (cadeia de custódia), comunicação, erradicação, recuperação e postmortem; papéis e contatos 24×7 definidos.

#### SEC-8.06 · Disaster Recovery Plan
**Crítico** (peso 3, origem `[B]`)  
existe **DRP explícito e versionado**, com: RPO/RTO aprovados por serviço e por dado; cenários cobertos (perda de região, corrupção lógica, exclusão acidental, ransomware, comprometimento da conta de nuvem, indisponibilidade de fornecedor crítico); ordem de restauração e dependências; runbook passo a passo executável por quem não escreveu; owner e substituto; critérios de declaração de desastre e de retorno. O plano é **exercitado** (no mínimo anualmente e após mudanças relevantes) com tempo real medido contra RTO/RPO e lições registradas.

#### SEC-8.07 · Backups resilientes a ataque
**Crítico** (peso 3, origem `[B]`)  
backups seguem 3-2-1 com pelo menos uma cópia imutável/isolada (outra conta ou cofre com retenção bloqueada), cifrada, com credenciais separadas das de produção (comprometer produção não permite apagar backups); restauração é testada periodicamente com verificação de integridade (restore real, não só “job concluído”); backups de dados pessoais respeitam retenção e eliminação (ver PRIV-11).

#### SEC-8.08 · Blast radius
**Importante** (peso 2, origem `[A]`)  
comprometimento de uma conta, pod, action, fornecedor, tenant ou chave não concede acesso global; segmentação, quotas, escopos, kill switches (desabilitar feature/integração/chave rapidamente) e revogação em massa limitam dano. Existe capacidade testada de revogar todas as sessões e rotacionar todos os segredos.

#### SEC-8.09 · Privacidade do logging
**Importante** (peso 2, origem `[A]`)  
retenção e conteúdo obedecem minimização; acesso a logs é auditado; investigação consegue trabalhar com pseudônimos e revelar identidade apenas sob autorização. *(Ver PRIV-12.)*

#### SEC-8.10 · Comunicação em incidentes
**Importante** (peso 2, origem `[A]`)  
contatos, escalonamento, jurídico, privacidade, clientes, fornecedores e autoridades são definidos; decisões e timestamps são registrados. Incidentes com dados pessoais integram o procedimento LGPD (ver PRIV-17) e normas setoriais aplicáveis.

#### SEC-8.11 · Lições aprendidas
**Menor** (peso 1, origem `[M]`)  
pós-incidente gera causas raiz, controles faltantes, testes de regressão, owner e prazo; findings repetidos ou aceites vencidos são escalados.

#### SEC-8.12 · Exercícios
**Menor** (peso 1, origem `[M]`)  
tabletop de incidente e de DR é realizado periodicamente com participação técnica, jurídica e de negócio, incluindo cenário de ransomware e de vazamento de dados.

## SEC-9. Superfície exposta e reconhecimento

**Como verificar:** Verifique o que é servido publicamente: `public/`, source maps (`productionBrowserSourceMaps`), headers `X-Powered-By`, Swagger/health/metrics expostos, `robots.txt`, `security.txt`, páginas de erro.

> Objetivo: reduzir o que um atacante aprende **antes** de atacar. Cada informação exposta acelera a exploração.

#### SEC-9.01 · Arquivos e diretórios sensíveis
**Crítico** (peso 3, origem `[B]`)  
não são acessíveis publicamente: `.git/`, `.env`, `.DS_Store`, backups (`*.bak`, `*.old`, `*.zip`, `*.sql`), dumps, arquivos de IDE, `docker-compose.yml`, `package.json` de servidor, logs, `phpinfo`, painéis de status. Verificado por varredura com wordlist.

#### SEC-9.02 · Source maps e código do cliente
**Importante** (peso 2, origem `[A]`)  
source maps não são publicados em produção (ou só para ferramenta de erro, com acesso autenticado); bundles não contêm comentários internos, URLs de ambientes internos, chaves, flags de features ocultas sensíveis ou lógica de autorização que dependa de segredo.

#### SEC-9.03 · Fingerprinting
**Menor** (peso 1, origem `[M]`)  
headers `Server`, `X-Powered-By`, versões em páginas de erro padrão, banners de serviço e caminhos característicos são removidos ou neutralizados; páginas de erro são customizadas e uniformes.

#### SEC-9.04 · Documentação e endpoints operacionais
**Importante** (peso 2, origem `[A]`)  
Swagger/OpenAPI UI, GraphQL playground, endpoints de métricas (`/metrics`), health detalhado, debug e profiling não são públicos em produção (ou exigem autenticação); health check público retorna apenas status mínimo.

#### SEC-9.05 · Vazamento por metadados
**Menor** (peso 1, origem `[M]`)  
documentos e imagens publicados não carregam metadados internos (autor, caminho, software, geolocalização); `robots.txt` e `sitemap` não listam áreas sensíveis.

#### SEC-9.06 · Exposição em fontes públicas
**Importante** (peso 2, origem `[A]`)  
monitoramento de vazamento de credenciais e código da organização em repositórios públicos, pastes e bases vazadas; repositórios e buckets públicos da organização são inventariados e revisados.

#### SEC-9.07 · Canal de divulgação responsável
**Menor** (peso 1, origem `[M]`)  
`/.well-known/security.txt` (RFC 9116) publicado com contato e política de divulgação; existe processo para receber, triar e responder relatos externos em prazo definido.

## SEC-10. Aplicações com LLM e agentes *(Se: a aplicação usa modelos de IA, RAG ou agentes)*

**Como verificar:** Procure uso de LLM/agentes na aplicação. Se não houver, marque a seção N/A citando a busca. Se houver: separação instrução/dados, validação da saída, ferramentas com escopo do usuário, filtros de RAG por permissão, limites de tokens/custo, sandbox de execução.

> Referências: OWASP Top 10 for LLM Applications 2025 e OWASP Top 10 for Agentic Applications 2026.

#### SEC-10.01 · Prompt injection direta e indireta
**Crítico** (peso 3, origem `[B]`)  
o sistema assume que **todo** conteúdo que chega ao modelo (input do usuário, documentos, páginas web, e-mails, resultados de ferramentas, dados recuperados por RAG) pode conter instruções maliciosas. Mitigação é em camadas: separação clara entre instruções e dados, classificadores/guardrails de entrada e saída, privilégio mínimo das ferramentas, confirmação humana para ações de impacto e testes adversariais com corpus de ataques conhecidos. **Sanitização de texto isolada não é considerada controle suficiente.**

#### SEC-10.02 · Saída do modelo como entrada não confiável
**Crítico** (peso 3, origem `[B]`)  
a saída do modelo é validada por schema e codificada por contexto antes de ser renderizada (XSS), executada (código, SQL, shell), usada em URLs (SSRF, exfiltração por imagem/markdown) ou passada a outra ferramenta. Renderização de links e imagens gerados pelo modelo é restrita a domínios permitidos.

#### SEC-10.03 · Agência excessiva e privilégio de ferramentas
**Crítico** (peso 3, origem `[B]`)  
ferramentas expostas ao modelo/agente são mínimas, com escopo e permissões do **usuário final** (não de uma conta de serviço onipotente); ações destrutivas, financeiras, de envio externo ou irreversíveis exigem confirmação humana explícita; há limites de passos, de gasto e de taxa por sessão de agente.

#### SEC-10.04 · Vazamento de informação sensível
**Importante** (peso 2, origem `[A]`)  
o modelo não tem acesso a dados que o usuário não poderia ver; system prompts não contêm segredos (considerar que serão extraídos); respostas são filtradas para dados pessoais e segredos; logs de prompts/respostas seguem a mesma política de dados sensíveis.

#### SEC-10.05 · RAG e bancos vetoriais
**Importante** (peso 2, origem `[A]`)  
documentos indexados carregam metadados de permissão e tenant; a recuperação filtra por autorização **antes** de enviar ao modelo; ingestão valida a origem do conteúdo (envenenamento de base); exclusão de documento remove também embeddings e caches.

#### SEC-10.06 · Memória e estado de agentes
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: agentes com memória*  
memória persistente é isolada por usuário/tenant, validada antes de ser gravada, expirável e auditável; conteúdo não confiável não se torna instrução permanente (memory poisoning).

#### SEC-10.07 · Consumo ilimitado e abuso de custo
**Importante** (peso 2, origem `[A]`)  
limites de tokens por requisição, por usuário e por período; proteção contra prompts que forçam saídas longas ou loops de ferramentas; alerta de gasto anômalo. *(Ver PERF-11.06.)*

#### SEC-10.08 · Cadeia de suprimento de IA
**Importante** (peso 2, origem `[A]`)  
modelos, provedores, SDKs, servidores MCP/plugins e datasets são inventariados, versionados, de fontes confiáveis e revisados; servidores MCP de terceiros são tratados como código não confiável (pinados, revisados, com permissões mínimas).

#### SEC-10.09 · Execução de código gerado
**Crítico** (peso 3, origem `[B]`) · Condicional — *Se: o agente executa código*  
execução ocorre em sandbox isolado (sem rede por padrão, sem credenciais, com limites de CPU/memória/tempo, filesystem efêmero), nunca no host da aplicação.

#### SEC-10.10 · Testes adversariais de IA
**Importante** (peso 2, origem `[A]`)  
existe suíte de red teaming (jailbreak, injeção indireta, exfiltração, abuso de ferramenta, extração de system prompt) executada em CI ou antes de cada mudança de prompt/modelo, com métricas de taxa de sucesso de ataque.

## SEC-11. Tratamento de exceções e condições anômalas

**Como verificar:** Procure handler global de erros e de `unhandledRejection`, comportamento em falha de autorização/validação (fail-closed), rollback/compensação em operações multi-etapa, `finally` para liberar recursos, comportamento do rate limit/log quando a dependência cai.

> Referência: categoria A10:2025 “Mishandling of Exceptional Conditions” do OWASP Top 10:2025.

#### SEC-11.01 · Falha fechada
**Crítico** (peso 3, origem `[B]`)  
erro em checagem de autorização, validação de token, verificação de assinatura, consulta a serviço de permissões ou feature flag de segurança resulta em **negação**, nunca em liberação.

#### SEC-11.02 · Exceções não tratadas
**Importante** (peso 2, origem `[A]`)  
existe handler global que captura exceções, registra com contexto e responde com erro genérico; rejeições de promises/exceções em threads não derrubam o processo de forma silenciosa nem deixam estado inconsistente.

#### SEC-11.03 · Consistência após falha
**Importante** (peso 2, origem `[A]`)  
falha no meio de operação multi-etapa faz rollback ou compensação (saga), sem deixar recurso criado sem dono, pagamento sem pedido ou permissão parcialmente aplicada; recursos (arquivos, locks, conexões) são liberados em `finally`/equivalente.

#### SEC-11.04 · Condições de limite
**Menor** (peso 1, origem `[M]`)  
overflow/underflow numérico, divisão por zero, datas inválidas, fuso horário, ano bissexto, valores nulos e coleções vazias são testados nos caminhos de segurança e de negócio.

#### SEC-11.05 · Comportamento sob esgotamento
**Importante** (peso 2, origem `[A]`)  
disco cheio, memória esgotada, pool esgotado ou dependência indisponível não desativam controles de segurança (ex.: log de auditoria falhando silenciosamente, rate limit desligado quando o Redis cai). O comportamento em falha de cada controle é decidido e documentado (fail-open vs. fail-closed).

## SEC-12. Gestão de vulnerabilidades

**Como verificar:** Procure política de SLA de vulnerabilidades, relatórios de triagem, registro de EOL de runtime/frameworks (`engines`, versões), registros de pentest anteriores.

#### SEC-12.01 · SLA de correção
**Crítico** (peso 3, origem `[B]`)  
prazos de correção por severidade definidos e medidos (referência comum: crítico ≤ 7 dias, alto ≤ 30, médio ≤ 90), com aceleração para vulnerabilidades em exploração ativa (CISA KEV) ou alta probabilidade de exploração (EPSS); idade dos findings abertos é reportada.

#### SEC-12.02 · Priorização por contexto
**Importante** (peso 2, origem `[A]`)  
a priorização considera alcançabilidade do código vulnerável, exposição do ativo, dados envolvidos e controles compensatórios, além do score base (CVSS v4.0).

#### SEC-12.03 · Fim de vida
**Importante** (peso 2, origem `[A]`)  
runtimes, frameworks, bancos, sistemas operacionais e bibliotecas fora de suporte são identificados com plano de migração datado.

#### SEC-12.04 · Testes externos recorrentes
**Menor** (peso 1, origem `[M]`)  
pentest independente periódico (no mínimo anual e após mudanças significativas) e, quando maduro, bug bounty; achados retornam ao backlog com SLA.

## SEC-13. Aplicativos mobile *(Se: há app iOS/Android)*

**Como verificar:** Procure código de app mobile (iOS/Android/React Native/Flutter). Se não houver, marque a seção N/A.

#### SEC-13.01 · Padrão MASVS
**Importante** (peso 2, origem `[A]`)  
o app é avaliado contra OWASP MASVS v2 (armazenamento, criptografia, autenticação, rede, plataforma, código, resiliência, privacidade).

#### SEC-13.02 · Armazenamento seguro
**Importante** (peso 2, origem `[A]`)  
tokens e segredos ficam no Keychain/Keystore; dados sensíveis não vão para backup, logs, screenshots do app switcher ou área de transferência.

#### SEC-13.03 · Comunicação
**Importante** (peso 2, origem `[A]`)  
apenas TLS, sem exceções de cleartext; pinning avaliado para operações de alto risco, com estratégia de rotação.

#### SEC-13.04 · Backend não confia no app
**Crítico** (peso 3, origem `[B]`)  
toda regra de autorização e de negócio está no servidor; o app é considerado engenharia-reversível; chaves embutidas são tratadas como públicas; atestação de app/dispositivo é usada como sinal adicional, não como controle único.

#### SEC-13.05 · Deep links e componentes exportados
**Importante** (peso 2, origem `[A]`)  
deep links/app links validam parâmetros e origem; activities, services, content providers e URL schemes exportados são mínimos e protegidos.

## SEC-14. Execução e relatório do pentest whitebox

**Como verificar:** Avalie a existência e a qualidade de relatórios de pentest/assessment anteriores e de testes de regressão de segurança (ex.: `tests/security/`), metodologia de severidade e critério de aprovação documentados.

#### SEC-14.01 · Revisão de código orientada a risco
**Importante** (peso 2, origem `[A]`)  
priorizar auth, autorização, parsing, crypto, secrets, SSRF, uploads, pagamentos, admin, exports, webhooks, jobs, migrations, integrações e IA; registrar arquivos, linhas e call paths (source → sink).

#### SEC-14.02 · Teste dinâmico autenticado
**Importante** (peso 2, origem `[A]`)  
executar com cada papel, tenant e estado; comparar respostas, timing, side effects e logs. Testar endpoints descobertos fora da documentação e versões antigas.

#### SEC-14.03 · Teste negativo
**Importante** (peso 2, origem `[A]`)  
validar entradas malformadas, limites, Unicode, encoding duplo, concorrência, requests fora de ordem, replay, timeout, falha de terceiro e mensagens duplicadas.

#### SEC-14.04 · Testes de segurança como regressão
**Importante** (peso 2, origem `[A]`)  
cada vulnerabilidade corrigida ganha teste automatizado que falharia se ela voltasse; testes de autorização (matriz SEC-3.01) rodam em CI.

#### SEC-14.05 · Evidência de exploração
**Importante** (peso 2, origem `[A]`)  
cada finding tem request/response ou teste automatizado, pré-condições, impacto demonstrado, alcance, probabilidade, screenshots/logs sanitizados e instrução de reprodução.

#### SEC-14.06 · Severidade
**Importante** (peso 2, origem `[A]`)  
score usa metodologia declarada (ex.: CVSS v4.0 com métricas de ambiente) e considera exploração remota, autenticação necessária, complexidade, interação, confidencialidade, integridade, disponibilidade, privacidade, multi-tenancy e impacto de negócio; risco residual é separado da severidade técnica; achados encadeáveis são avaliados em conjunto.

#### SEC-14.07 · Remediação verificável
**Importante** (peso 2, origem `[A]`)  
recomendação aponta correção no boundary correto, não só workaround; reteste confirma exploit bloqueado, ausência de bypass e manutenção de funcionalidade legítima.

#### SEC-14.08 · Critério de aprovação
**Crítico** (peso 3, origem `[B]`)  
não há crítico/alto aberto sem aceite formal; médios têm prazo e compensação; exceções possuem owner, justificativa, expiração, monitoramento e plano de correção.
