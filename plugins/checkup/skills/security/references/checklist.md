# Criteria catalog — Security

> Derived from the *Senior checklist for application assessment — v3* (October 2026). This file is maintained directly in this repository. Item IDs, severities and criteria are the basis of the score and must stay stable between runs: changing an ID or a severity breaks score comparison across runs, so record any such change in the pull request.

**Severity (fixed per item):** `[B]` Blocking → **Critical** (weight 3) · `[A]` High → **Important** (weight 2) · `[M]` Medium and `[R]` Recommended → **Minor** (weight 1).

**Conditional items** (*If: …*): when the condition does not apply, mark **N/A with justification and evidence** (e.g., a code search with no hits). N/A without evidence counts as Non-compliant.

**Total items:** 153 — Critical: 48 · Important: 89 · Minor: 16. Maximum score (all applicable): 338.

## Pillar goal

> **Pillar goal:** on reaching a high score here, the application must resist known attack techniques (OWASP Top 10:2025, OWASP API Security Top 10, ASVS 5.0 categories), expose the minimum of useful information to an attacker and, where exposure is unavoidable, have an impact that is **contained, localized, detectable and recoverable** — including an explicit, tested Disaster Recovery plan.
>
> **Golden rule:** every control is verified **server-side** and **by a negative test** (the attacker trying and failing), not by the existence of the code. “Hiding the button”, “it isn't documented” and “nobody knows the URL” are not controls.

## SEC-1. Scope, architecture and threat

**How to verify:** Look for an asset inventory, diagrams/flows (`docs/architecture*`), a threat model, security decisions (ASVS), data classification in the schema. Generic documents with no link to real components = Partial.

#### SEC-1.01 · Asset inventory
**Critical** (weight 3, origin `[B]`)  
list applications, APIs, frontends, mobile, workers, cron, consumers, serverless functions, gateways, databases, caches, queues, buckets, registries, CI/CD, domains, subdomains, certificates, environments and versions; compare the declared inventory with active discovery (DNS, Certificate Transparency, port scanning, real gateway routes). Assets without an owner are a finding.

#### SEC-1.02 · Flow map
**Important** (weight 2, origin `[A]`)  
document entries, exits, trust boundaries, identities, data, protocols, third parties, privileges and administrative flows. Each flow has an owner, authentication, authorization, logging and risk. The diagram is updated on every architecture change and versioned with the code.

#### SEC-1.03 · Threat model
**Important** (weight 2, origin `[A]`)  
STRIDE/abuse cases or an equivalent method covers spoofing, tampering, repudiation, disclosure, denial of service and elevation of privilege, plus business-logic abuse; threats are linked to controls, tests and findings. The model is reviewed for every risky feature (payment, auth, upload, integrations, AI).

#### SEC-1.04 · Standard and level of rigor
**Important** (weight 2, origin `[A]`)  
fix **OWASP ASVS 5.0.0** and the applicable level (L1/L2/L3) per component; record the **documented security decisions** that ASVS 5.0 requires for configurable requirements; map requirements to components and exclude items only with justification. Complement with OWASP Top 10:2025, API Security Top 10, MASVS (mobile), LLM/Agentic Top 10 (AI), supply chain and business rules.

#### SEC-1.05 · Security requirements in the development lifecycle
**Minor** (weight 1, origin `[M]`)  
risky stories have security acceptance criteria and abuse cases; a definition of done with security checks exists; practices follow a secure development framework (e.g., NIST SSDF / OWASP SAMM) with measured maturity.

#### SEC-1.06 · Test environment
**Important** (weight 2, origin `[A]`)  
production is not used without authorization; data is synthetic/masked; test accounts cover roles, tenants, states and privileges; origin, window, limits and rules of engagement are documented. The test environment is equivalent to production in security configuration (same headers, WAF, IAM, versions).

#### SEC-1.07 · Impact model
**Important** (weight 2, origin `[A]`)  
classify confidentiality, integrity, availability, privacy, fraud, financial impact, lateral movement and blast radius. Severity considers exploitability and combined impact (chaining of findings).

#### SEC-1.08 · Data classification
**Important** (weight 2, origin `[A]`)  
data is classified (public, internal, confidential, personal, sensitive personal, credential, financial) and the classification is annotated in the schema/data models, guiding encryption, logging, retention and access.

## SEC-2. Identity, authentication and session

**How to verify:** Read the complete auth flow: password hashing (`argon2`/`bcrypt` and parameters), password policy, rate limit/lockout and where the IP comes from (is `x-forwarded-for` trusted?), JWT generation/validation (algorithms, `iss`/`aud`/`exp`, revocation), session cookies, password reset (token, hash, expiry, `Host` header), MFA/WebAuthn, OAuth. Confirm with the existing tests (negative tests count as E3).

#### SEC-2.01 · Account registration
**Important** (weight 2, origin `[A]`)  
e-mail/phone/username do not allow enumeration by response, timing, code, redirect or recovery; duplicates, normalization (Unicode, uppercase, dots/`+` in e-mail, homographs) and takeover of a pre-existing account are handled. Mass automated registration is limited (rate limit, contact verification, adaptive challenge).

#### SEC-2.02 · Password
**Critical** (weight 3, origin `[B]`)  
the password is received only over TLS, never logged, stored with a modern adaptive hash and a unique salt (Argon2id, scrypt, bcrypt or PBKDF2 with current parameters), with parameters reviewed periodically; minimum length per NIST SP 800-63B-4 (15 characters when the password is the sole factor; 8 when part of MFA), a maximum of at least 64, accepts spaces and Unicode; check against leaked/common passwords; **no** arbitrary composition rules and **no** forced periodic change (only on suspected compromise). The hash cost is bounded so it does not become a DoS vector (rate limit before the hash, maximum input size).

#### SEC-2.03 · Phishing-resistant authentication
**Important** (weight 2, origin `[A]`)  
passkeys/WebAuthn (FIDO2) are offered and **required** for administrators and critical operations; SMS OTP is not the only second factor for privileged accounts.

#### SEC-2.04 · Brute force, credential stuffing and rate-limit evasion
**Critical** (weight 3, origin `[B]`)  
login, reset, MFA, OTP, magic link, invite and API key have a rate limit per account, IP, device and context; progressive lockout does not allow simple denial of service against the victim. The system is resilient to evasion by header spoofing (`X-Forwarded-For`, `X-Real-IP`, `True-Client-IP` — the client IP is only read from the trusted proxy), residential proxy rotation, variation in the identifier's capitalization/encoding and parallelism (race on the attempt counter). Credential stuffing detection exists (distributed failure rate, leaked passwords).

#### SEC-2.05 · MFA
**Critical** (weight 3, origin `[B]`)  
enrollment, recovery, factor change, step-up and deactivation resist takeover, SIM swap, replay, predictable phishing, push fatigue (number matching) and endpoint bypass (e.g., reaching a post-login route without completing the second factor). A strong factor is required for critical functions. Recovery codes are single-use and stored hashed.

#### SEC-2.06 · JWT tokens
**Critical** (weight 3, origin `[B]`) · Conditional — *If: JWT*  
validation follows RFC 8725: an explicit algorithm allowlist (blocks `none` and RS256/HS256 confusion), signature, `iss`, `aud`, `exp`, `nbf`, `iat` with a small clock tolerance, `typ` when applicable; the `kid`, `jku`, `x5u` and `jwk` headers do not allow path traversal, key injection or key retrieval from an attacker-controlled URL. Access tokens are short-lived; revocation (denylist, session version or introspection) exists for logout, reset and privilege change. The JWT does not carry sensitive data in clear.

#### SEC-2.07 · Sessions
**Critical** (weight 3, origin `[B]`)  
IDs have ≥ 128 bits of entropy, generated by a CSPRNG, regenerated after login/privilege elevation (anti-fixation), invalidated on the server on logout/reset/password change, and have idle and absolute expiry. Cookies use `Secure`, `HttpOnly`, an adequate `SameSite` and the `__Host-` prefix when possible; the session does not appear in URL/referrer/log. The user sees and ends active sessions.

#### SEC-2.08 · Recovery
**Critical** (weight 3, origin `[B]`)  
reset uses a unique, random (≥ 128 bits), short-lived token, stored hashed, bound to the user, invalidated after use and when another is issued; it does not reveal whether an account exists. The reset link is not built from the `Host` header (host header poisoning). There is no e-mail/phone change without reauthentication; after a reset or change, existing sessions and tokens are invalidated and the owner is notified on the old channel.

#### SEC-2.09 · OAuth/OIDC
**Critical** (weight 3, origin `[B]`) · Conditional — *If: OAuth/OIDC*  
follows the OAuth 2.0 Security BCP (RFC 9700): authorization code + PKCE for all clients, no implicit grant or password grant; `state`, `nonce`, an exact redirect URI allowlist (no wildcards), `iss` validation (mix-up attack), minimal scopes; account linking does not automatically link by unverified e-mail. Tokens do not leak through URL, referrer or log. Sender-constrained tokens (DPoP/mTLS) are evaluated for high-risk APIs.

#### SEC-2.10 · API keys and service accounts
**Important** (weight 2, origin `[A]`)  
they are scoped, expiring/rotated, identifiable (a prefix that enables secret scanning), stored hashed on the server, revocable and never embedded in the client. Use, origin and failures are audited; test keys do not reach production.

#### SEC-2.11 · Federated authentication
**Important** (weight 2, origin `[A]`) · Conditional — *If: SSO/SAML/corporate OIDC*  
claim mapping, groups, domain, signature (SAML: signature validation of the correct element, defense against XML signature wrapping), clock, logout and provisioning/deprovisioning (SCIM) are validated. User-controllable claims do not grant privileges; a user removed from the IdP loses access within a defined period.

#### SEC-2.12 · Reauthentication and step-up
**Important** (weight 2, origin `[A]`)  
sensitive actions (changing e-mail/password/MFA, data export, creating an API key, changing bank details) require recent reauthentication or step-up, regardless of the session being active.

#### SEC-2.13 · Security notifications to the user
**Minor** (weight 1, origin `[M]`)  
the user is notified of login on a new device, password/MFA/e-mail change, credential creation and data export, with a path to react (“it wasn't me”).

## SEC-3. Authorization, tenancy and business logic

**How to verify:** Map all routes and check, per route, authentication and server-side ownership/role checks (middleware/use case). Look for IDs from the path/body used without a check, output DTOs, mass assignment (`...body` in update), operations without a transaction/atomic condition (race). Negative authorization tests are the main evidence.

#### SEC-3.01 · Authorization matrix
**Critical** (weight 3, origin `[B]`)  
an explicit actor × action × resource × property × state × tenant matrix exists; positive and negative automated tests cover each combination. Default deny is applied server-side, in a centralized way (middleware/policy engine), not scattered in `if`s.

#### SEC-3.02 · BOLA/IDOR
**Critical** (weight 3, origin `[B]`)  
IDs of objects, files, messages, orders, reports, jobs and exports are swapped between accounts/tenants; the server prevents reading, changing, deleting and indirect inference (count, timing, different error messages). Non-sequential IDs reduce enumeration but do **not** replace the authorization check.

#### SEC-3.03 · BFLA
**Critical** (weight 3, origin `[B]`)  
admin, debug, internal, bulk, import/export, impersonation and maintenance functions are tested by a regular user, a lower role and a token without scope; changing the HTTP method (GET→DELETE/PUT), an old API version and an alternate route do not bypass the control.

#### SEC-3.04 · Property-level authorization
**Critical** (weight 3, origin `[B]`)  
read-only, internal and financial fields and flags, owner, role, tenant and status cannot be read or changed by mass assignment, JSON merge, GraphQL selection or extra fields; responses are serialized by DTO/allowlist per role.

#### SEC-3.05 · Authorization at every layer
**Important** (weight 2, origin `[A]`)  
gateway, controller, service, repository, job, consumer, websocket and storage do not assume the previous layer authorized. Internal calls are not automatically trusted (zero trust between services with workload identity).

#### SEC-3.06 · Tenant isolation and cross-tenant leakage
**Critical** (weight 3, origin `[B]`) · Conditional — *If: multi-tenant*  
IDs, filters, cache keys, queues, search indexes, vector indexes, exports, logs, backups and observability do not cross tenants. The tenant comes from the authenticated context, never from a client parameter. Tests prove that one tenant's tokens do not access another's subdomains, endpoints or data (including in memory/cache). Database enforcement mechanisms (e.g., row-level security) are considered as defense in depth.

#### SEC-3.07 · States and transitions
**Important** (weight 2, origin `[A]`)  
the workflow validates current state, actor, order, concurrency, expiry and preconditions server-side. There is no jump from draft to approved, duplicate refund, skipping the payment step or cancellation after completion through a race.

#### SEC-3.08 · Sensitive functions
**Important** (weight 2, origin `[A]`)  
payment, withdrawal, account changes, deletion, invites, owner change, export and impersonation require step-up, confirmation, idempotency, an audit trail and limits (amount, frequency). Operations of very high impact have a four-eyes control.

#### SEC-3.09 · Race conditions
**Important** (weight 2, origin `[A]`)  
concurrent requests (including the single-packet attack) test balance, coupon, stock, approval, reset, invite, upload, lock, attempt limit and privilege change. The result is atomically consistent (constraint, lock, transaction or conditional operation) and does not depend only on a prior validation.

#### SEC-3.10 · Integrity of business values
**Important** (weight 2, origin `[A]`)  
price, discount, quantity, currency, shipping, fee and limits are computed or revalidated on the server; negative values, zero, extreme decimals, overflow, rounding and swapped units are tested.

#### SEC-3.11 · Workflow abuse
**Important** (weight 2, origin `[A]`)  
legitimate flows cannot be automated for fraud, spam, scraping, improper purchase, mass creation, referral abuse, enumeration or paid consumption (SMS, e-mail, AI) without compensating controls (limits, bot detection, progressive cost, review).

#### SEC-3.12 · Offline/async decisions
**Important** (weight 2, origin `[A]`)  
authorization is revalidated in the worker at the moment of the effect; an old message, a removed user's job or a reprocessed event does not perform an improper action. Messages carry verifiable identity, not just a trusted `user_id`.

#### SEC-3.13 · Impersonation/support
**Important** (weight 2, origin `[A]`) · Conditional — *If: there is support access*  
support can act only with scope, consent/record, a visible banner, expiry, reason and audit; there is no invisible access or shared session; destructive actions under impersonation are blocked or require approval.

#### SEC-3.14 · Access to stored files and objects
**Critical** (weight 3, origin `[B]`)  
private files are not in a public bucket or at a guessable URL; download goes through authorization or a short-lived signed URL, issued after a permission check, scoped to a single object.

## SEC-4. Input, validation and injections

**How to verify:** Look for schema validation at the boundary (Zod/Joi/class-validator) on ALL routes, raw queries (`$queryRaw`, `$runCommandRaw`, concatenation), Mongo operators coming from input, `child_process`, templates/generated HTML, path manipulation, `fetch` of a user URL (SSRF), deserialization, deep `merge`, regex over input, upload (magic bytes, size, re-encode).

#### SEC-4.01 · Schema validation
**Critical** (weight 3, origin `[B]`)  
body, query, path, header, cookie, multipart, websocket, event and metadata validate type, size, charset, range, depth, unknown fields and encoding at the boundary, with an allowlist; client-side validation is only UX.

#### SEC-4.02 · SQL/ORM
**Critical** (weight 3, origin `[B]`)  
queries are parameterized; dynamic concatenation, optional filters, controllable `ORDER BY`/column names (require an allowlist), `IN`, `LIKE` (wildcard escaping), ORM raw queries, stored procedures and migrations are tested. The ORM is not considered automatic protection. The application's database user has no DDL or administrative privileges.

#### SEC-4.03 · NoSQL and query languages
**Critical** (weight 3, origin `[B]`) · Conditional — *If: NoSQL, search engines, filter languages*  
operators (`$where`, `$ne`, `$regex`, `$gt`), objects where a string is expected, JSON queries, search engine queries and filter expressions are rejected or allowlisted. *(GraphQL controls are consolidated in SEC-5.15.)*

#### SEC-4.04 · Command/OS injection
**Critical** (weight 3, origin `[B]`)  
arguments are passed without a shell (argument array); allowlist of commands/options, `--` before positional arguments, minimal environment, timeout, restricted filesystem and an unprivileged user. Test metacharacters, newlines and argument injection (e.g., options starting with `-`).

#### SEC-4.05 · Template injection
**Critical** (weight 3, origin `[B]`)  
templates, e-mail, PDF, markdown and HTML generation do not evaluate controllable expressions. Test SSTI, stored XSS, contextual escaping and rich content; user templates (if any) run in a logical sandbox with no access to runtime objects.

#### SEC-4.06 · LDAP/XML
**Important** (weight 2, origin `[A]`) · Conditional — *If: LDAP/XML/SAML/SOAP/SVG/Office*  
LDAP filters use correct escaping; XML parsers disable DTD/external entities and limit expansion, size and depth; XXE, SSRF via XML and billion laughs are tested, including in XML-based formats (DOCX, XLSX, SVG).

#### SEC-4.07 · Path traversal
**Critical** (weight 3, origin `[B]`)  
paths, names, zip/tar (zip slip), symlinks and downloads are normalized and confined to a base directory after resolving the real path; `..`, double encoding, null byte, UNC, alternate separators and symbolic links are tested. A user-supplied file name is not used as a storage path.

#### SEC-4.08 · SSRF and cloud metadata
**Critical** (weight 3, origin `[B]`) · Conditional — *If: the server fetches URLs, renders HTML/PDF, imports by link, receives configurable webhooks*  
URLs are allowlisted by scheme, host and port; DNS resolution is validated at connection time (anti DNS rebinding); private IPv4/IPv6, loopback, link-local, alternate IP representations (decimal, octal, IPv6-mapped) and redirects are blocked; `file`, `gopher`, `dict`, `ftp` schemes are disabled. Access to cloud metadata endpoints from user input is blocked in the application **and** in the infrastructure (IMDSv2 with hop limit 1 or equivalent, see SEC-7.05); egress is segmented by an outbound proxy.

#### SEC-4.09 · Deserialization
**Critical** (weight 3, origin `[B]`)  
formats and classes allowed are explicit; arbitrary objects are not deserialized from an untrusted source (Java native serialization, pickle, unsafe YAML, BinaryFormatter etc.); signature/integrity and limits are verified before deserializing.

#### SEC-4.10 · Prototype pollution and mass merge
**Important** (weight 2, origin `[A]`) · Conditional — *If: JavaScript/TypeScript*  
deep merges, query string parsers and object cloning reject `__proto__`, `constructor` and `prototype`; configuration objects are created without a prototype or frozen when appropriate.

#### SEC-4.11 · Regex and parser DoS
**Important** (weight 2, origin `[A]`)  
expressions, JSON, YAML, CSV, image, PDF and multipart have limits on time, size, depth and memory; catastrophic regex (ReDoS) is tested or a linear-time regex engine is used for untrusted input.

#### SEC-4.12 · Headers and protocol smuggling
**Important** (weight 2, origin `[A]`)  
CRLF injection, host header poisoning, forwarded headers, duplicate headers, request desync (CL.TE, TE.CL, TE.TE, H2 downgrade), cache poisoning and divergent normalization between proxy and app are assessed. The `Host` header is validated against an allowlist.

#### SEC-4.13 · Upload
**Critical** (weight 3, origin `[B]`) · Conditional — *If: upload*  
extension (allowlist), real MIME by content (magic bytes), size, decompression bomb, polyglot, macro, SVG with script, file name, quota, antivirus/sandbox and reprocessing (image re-encoding, removal of EXIF metadata) are controlled. Files are served from a separate domain (without the application's cookies) or with `Content-Disposition: attachment` and `X-Content-Type-Options: nosniff`; never executed.

#### SEC-4.14 · Output encoding
**Critical** (weight 3, origin `[B]`)  
HTML, attributes, JS, CSS, URL, JSON, SQL, shell, CSV (formula injection: `=`, `+`, `-`, `@`) and logs (log injection/forging) use context encoding; dangerous DOM sinks and bypass via Unicode/normalization are tested.

#### SEC-4.15 · Canonicalization and Unicode
**Minor** (weight 1, origin `[M]`)  
inputs are normalized (NFC/NFKC as appropriate) before validation and comparison; homographs, control characters and bidi (RTL override) are handled in displayed names, URLs and identifiers.

#### SEC-4.16 · E-mail and notifications
**Important** (weight 2, origin `[A]`) · Conditional — *If: sends e-mail/SMS*  
user-controlled content does not inject e-mail headers, links or HTML into messages sent from the company's domain (abuse for phishing); the sender uses SPF, DKIM and DMARC with a reject policy.

## SEC-5. Web, browser and APIs

**How to verify:** Check CSRF (tokens/`Origin`/`SameSite`), CORS, CSP and headers (`next.config.*`, middleware, `securityHeaders`), use of `dangerouslySetInnerHTML`/`innerHTML`, cookies, `localStorage`, redirects, route inventory vs OpenAPI, rate limit, error format, incoming webhooks.

#### SEC-5.01 · CSRF
**Critical** (weight 3, origin `[B]`) · Conditional — *If: cookie authentication*  
state-changing operations require an anti-CSRF token and/or `Origin`/Fetch Metadata verification (`Sec-Fetch-Site`), with a coherent `SameSite`; state-changing operations never use GET. Login CSRF, JSON CSRF (simple content-type), multipart and alternate endpoints are tested.

#### SEC-5.02 · CORS
**Critical** (weight 3, origin `[B]`)  
origins are not reflected nor validated by a fragile regex (suffix/prefix); the `null` origin is rejected; `Access-Control-Allow-Credentials` only with an exact allowlist; methods, headers and preflight restricted. The API does not expose a sensitive response to an untrusted origin.

#### SEC-5.03 · Subdomain takeover and DNS hygiene
**Important** (weight 2, origin `[A]`)  
DNS records (CNAME, A, NS, MX) pointing to deactivated resources (buckets, PaaS apps, CDNs) are continuously detected and removed; third-party subdomains do not share cookie scope with the application; CAA restricts certificate issuers; DNSSEC is assessed.

#### SEC-5.04 · CSP
**Important** (weight 2, origin `[A]`) · Conditional — *If: web frontend*  
strict CSP based on nonce or hash (with `strict-dynamic`), without `unsafe-inline`/`unsafe-eval`, with `object-src 'none'`, `base-uri 'none'`/`'self'`, `frame-ancestors` and monitored violation reporting. Trusted Types is evaluated to eliminate DOM XSS in rich applications.

#### SEC-5.05 · Security headers
**Important** (weight 2, origin `[A]`)  
HSTS (with `includeSubDomains` and preload when feasible), `X-Content-Type-Options: nosniff`, a restrictive `Referrer-Policy`, a minimal `Permissions-Policy`, `Cross-Origin-Opener-Policy`, `Cross-Origin-Resource-Policy` and, when necessary, `Cross-Origin-Embedder-Policy`; `Cache-Control: no-store` on sensitive responses. Verified on **all** relevant responses, including errors, redirects and assets.

#### SEC-5.06 · XSS
**Critical** (weight 3, origin `[B]`)  
reflected, stored, DOM, template, markdown, SVG, e-mail, preview, generated PDF and imported data are tested in all contexts, including the admin panel (where the impact is greater). Use of the framework's escape-bypass APIs (`dangerouslySetInnerHTML`, `v-html`, `innerHTML`, `bypassSecurityTrust*`) is inventoried and justified, with a maintained sanitizer (e.g., DOMPurify).

#### SEC-5.07 · Cookies
**Important** (weight 2, origin `[A]`)  
minimal domain and path scope, correct flags, `__Host-`/`__Secure-` prefixes; sensitive cookies are not accessible to less trusted subdomains; logout clears cookies and invalidates the session on the server.

#### SEC-5.08 · Client-side storage
**Important** (weight 2, origin `[A]`)  
tokens and sensitive data are not kept in `localStorage`, `sessionStorage`, IndexedDB, URL, analytics, crash reports or service worker cache without documented justification; local data is cleared on logout; authenticated responses are not kept in a shared cache.

#### SEC-5.09 · Clickjacking and cross-window communication
**Important** (weight 2, origin `[A]`)  
sensitive pages block framing (`frame-ancestors`); `postMessage` validates `origin`, `source` and schema; `window.opener` is neutralized (`noopener`/COOP); cross-window communication does not accept arbitrary commands.

#### SEC-5.10 · Open redirect
**Important** (weight 2, origin `[A]`)  
redirects accept only permitted destinations (allowlist or validated relative paths), with no bypass by encoding, userinfo (`@`), backslash, `//`, an alternate scheme (`javascript:`, `data:`) or a look-alike domain.

#### SEC-5.11 · API inventory
**Important** (weight 2, origin `[A]`)  
specifications (OpenAPI/GraphQL schema), real routes, subdomains, old versions, debug, health, metrics, GraphQL, websocket and documentation endpoints are compared; forgotten assets (shadow/zombie APIs) are removed or protected; old versions have a shutdown date.

#### SEC-5.12 · Mass assignment
**Critical** (weight 3, origin `[B]`)  
unknown and privileged fields are rejected or allowlisted; the response does not leak internal fields. Test POST/PUT/PATCH/merge, nested objects and arrays.

#### SEC-5.13 · Rate limit and quotas
**Important** (weight 2, origin `[A]`)  
limits exist per identity, IP, tenant, endpoint, cost and operation; headers report the limit and retry; a distributed and multi-region implementation does not allow simple bypass (changing region, IPv6 with a whole prefix, path/case/trailing slash variation).

#### SEC-5.14 · Expensive resources
**Important** (weight 2, origin `[A]`)  
pagination, regex, export, report, search, upload, SMS/e-mail sending, biometrics, paid calls and AI have a maximum cost, timeout, quota and authorization (OWASP API4: unrestricted resource consumption).

#### SEC-5.15 · GraphQL
**Important** (weight 2, origin `[A]`) · Conditional — *If: GraphQL*  
limits on depth, complexity/cost, aliases, fragments and batching; per-field/resolver authorization; persisted queries/allowlist for first-party clients; introspection **disabled** in production for private APIs (for public APIs, allowed only as a documented decision, with the other limits active); field suggestions (“did you mean”) turned off; error messages without internal details.

#### SEC-5.16 · Web cache poisoning and web cache deception
**Important** (weight 2, origin `[A]`) · Conditional — *If: CDN/reverse cache*  
the cache key includes every input that changes the response (unkeyed headers are tested); authenticated/personalized responses are not publicly cached; path tricks (`/account/profile.css`, delimiters, normalization) do not make the CDN cache a private page.

#### SEC-5.17 · WebSocket/SSE
**Important** (weight 2, origin `[A]`) · Conditional — *If: real time*  
the handshake authenticates, `Origin` is validated (anti cross-site WebSocket hijacking), per-message/channel authorization, tokens expire and the connection is closed when the session is revoked; messages have a schema/size and the connection has a quota/timeout.

#### SEC-5.18 · API errors
**Important** (weight 2, origin `[A]`)  
status, headers, messages, timing and pagination do not reveal the existence of others' resources, stack, version, internal IDs, query or other users' data. A standardized error format (e.g., Problem Details) with no debug fields in production.

#### SEC-5.19 · Subresource Integrity and third parties in the browser
**Minor** (weight 1, origin `[M]`)  
third-party CDN scripts/CSS use SRI or are served from the own domain; an inventory of third-party scripts per page exists, with change monitoring (protection against skimming/Magecart on payment pages).

#### SEC-5.20 · Incoming webhooks
**Important** (weight 2, origin `[A]`) · Conditional — *If: receives webhooks*  
HMAC/mTLS signature verified with constant-time comparison, a short-window timestamp and replay protection (unique event ID), payload validated by schema, idempotent processing; webhook content is treated as untrusted.

#### SEC-5.21 · Methods and content types
**Minor** (weight 1, origin `[M]`)  
only the necessary HTTP methods are accepted per route (TRACE disabled; method override via header/parameter controlled); the content type is validated and the server does not interpret a body in a format different from the declared one (e.g., accepting XML where JSON is expected).

## SEC-6. Cryptography, secrets and data

**How to verify:** Look for disabled TLS (`rejectUnauthorized: false`, `NODE_TLS_REJECT_UNAUTHORIZED`), secrets in the code and history (`git log -p`, key patterns), versioned `.env`, masking in the logger, use of `Math.random` for tokens, weak algorithms (`md5`, `sha1`, `createCipher`), secret comparison without constant time, app→database TLS.

#### SEC-6.01 · External TLS
**Critical** (weight 3, origin `[B]`)  
TLS 1.2+ (preferably 1.3), cipher suites with forward secrecy and AEAD, valid certificates with the full chain, automatic renewal and expiry alerting, HTTP→HTTPS redirect, HSTS; certificate validation is not disabled in any HTTP client in the code (verified by code search).

#### SEC-6.02 · Internal communication
**Important** (weight 2, origin `[A]`)  
traffic between services, database, cache and queues is encrypted (TLS/mTLS or a service mesh) when it crosses a shared network; internal services authenticate each other with workload identity.

#### SEC-6.03 · Encryption at rest
**Important** (weight 2, origin `[A]`)  
database, volumes, objects, queues, backups, logs and devices use proportionate protection; key and data are not under the same control without separation and audit.

#### SEC-6.04 · Field-level encryption
**Important** (weight 2, origin `[A]`) · Conditional — *If: sensitive personal data, documents, financial data*  
higher-risk fields (document, health, bank data, biometrics) are encrypted in the application or tokenized, so that a database dump or improper DBA access does not expose the clear value; search uses a keyed hash (blind index) when needed.

#### SEC-6.05 · Key management
**Important** (weight 2, origin `[A]`)  
generation, storage, access, use, rotation, revocation, destruction, backup and recovery are documented; KMS/HSM and envelope encryption are used where applicable; keys have a single purpose; key access is audited.

#### SEC-6.06 · Secrets
**Critical** (weight 3, origin `[B]`)  
a scanner covers Git history, branches, container images, logs, CI, IaC, notebooks, fixtures, frontend bundles and source maps; **push protection** blocks new secrets; the secret manager applies least privilege, expiry, rotation and audit; a leaked secret has an immediate rotation procedure (removing it from history is not enough).

#### SEC-6.07 · Hardcoded/config
**Critical** (weight 3, origin `[B]`)  
tokens, passwords, connection strings, private keys and third-party credentials do not appear in versioned code or configuration. `.env`, dumps and backup files are neither versioned nor served; long-lived cloud credentials are replaced by identity federation (OIDC/workload identity).

#### SEC-6.08 · Data in logs/telemetry
**Important** (weight 2, origin `[A]`)  
PII, credentials, `Authorization` headers, cookies, tokens, payloads and payment data are masked **before** logging/export (redaction in the logging library, not by convention). Errors, traces, crash reports and support do not become a leak channel. *(See PERF-2.14 and PRIV-12.)*

#### SEC-6.09 · Hash, tokens and randomness
**Important** (weight 2, origin `[A]`)  
passwords, reset tokens, API keys and secret identifiers use a CSPRNG and adequate hashing; secret comparisons are constant-time; tokens are neither predictable nor reusable. There is no use of `Math.random`, `rand()` or an equivalent for security.

#### SEC-6.10 · Algorithms and implementations
**Important** (weight 2, origin `[A]`)  
only current algorithms and mature libraries (no home-made cryptography); no MD5/SHA-1 for security, no ECB, no reused IV/nonce, no RSA < 2048 bits; authenticated modes (AES-GCM, ChaCha20-Poly1305).

#### SEC-6.11 · Cryptographic inventory and post-quantum readiness
**Minor** (weight 1, origin `[R]`)  
an inventory exists of where and how cryptography is used (TLS, signatures, tokens, data at rest, integrations), allowing algorithms to be swapped without a rewrite (crypto-agility); there is a migration plan to NIST-standardized post-quantum algorithms and an evaluation of hybrid TLS for data with a long confidentiality lifetime (“harvest now, decrypt later” risk).

#### SEC-6.12 · Minimizing exposure
**Important** (weight 2, origin `[A]`)  
responses, exports, debug, documentation, directories, source maps, banners and metadata publish only what is necessary. An attacker does not obtain version/stack/topology without need. *(Detailed in section 9.)*

## SEC-7. Configuration, infrastructure and supply chain

**How to verify:** Read CI (`permissions:`, actions pinned by SHA, `pull_request_target`, interpolation of `${{ github.event.* }}` in `run:`), lockfiles, SCA/Dependabot/Renovate, SBOM, Dockerfile (non-root user, minimal base), IaC, CODEOWNERS and branch protection (via `gh api` when available), production settings (debug, CORS, sample endpoints).

#### SEC-7.01 · Secure defaults
**Critical** (weight 3, origin `[B]`)  
debug, verbose errors, directory listing, admin seed, sample credentials, broad CORS, extra HTTP methods, administrative consoles (actuator, profiler, framework admin, phpMyAdmin etc.) and test endpoints are disabled or protected in production — verified by scanning, not just by configuration.

#### SEC-7.02 · Environment segregation
**Important** (weight 2, origin `[A]`)  
cloud accounts/projects, networks, databases, buckets, secrets, pipelines and observability for dev/stage/prod are separate; a lower environment's credential does not reach production; production data is not copied to lower environments without anonymization.

#### SEC-7.03 · IAM
**Critical** (weight 3, origin `[B]`)  
users, roles, workloads and services have minimal permissions, per-resource scope, temporary (just-in-time) access for elevated privileges, MFA for humans, periodic review and revocation on offboarding; there is no administrative wildcard for convenience nor a root/owner account used day to day. Break-glass accounts exist, are monitored and tested.

#### SEC-7.04 · Network and egress
**Important** (weight 2, origin `[A]`)  
subnets, security groups, firewall, egress, DNS, metadata and administration are restricted; databases, caches and queues are not reachable from the internet; administrative access goes through a bastion/zero-trust with MFA; segmentation limits lateral movement; egress is allowlisted for services that do not need the internet.

#### SEC-7.05 · Cloud posture (CSPM)
**Important** (weight 2, origin `[A]`) · Conditional — *If: public cloud*  
cloud configuration is continuously assessed against a benchmark (e.g., CIS) by a CSPM tool: buckets without public access (account-level block), a hardened metadata service (e.g., IMDSv2 required with hop limit 1 on AWS or equivalent), cloud audit logs enabled and protected, old access keys, public snapshots, open security groups. Deviations raise an alert with an owner.

#### SEC-7.06 · Containers/Kubernetes
**Important** (weight 2, origin `[A]`) · Conditional — *If: containers*  
non-root, `readOnlyRootFilesystem`, minimal capabilities (`drop: ALL`), no privileged/hostPath/hostNetwork, seccomp/AppArmor, Pod Security Standards at the *restricted* level, images verified by signature through an admission policy, namespaces, default-deny network policies, secrets not mounted in pods that do not need them, service accounts without an automatic token, API server not publicly exposed, minimal RBAC.

#### SEC-7.07 · Base images and runtime
**Important** (weight 2, origin `[A]`)  
minimal base images (distroless/slim), updated at a defined frequency, scanned at build and continuously in the registry; no shell tools/compilers unnecessary in the final image.

#### SEC-7.08 · IaC
**Important** (weight 2, origin `[A]`) · Conditional — *If: IaC*  
Terraform/Helm/CloudFormation/Pulumi has a security scan, review, protected and encrypted state (it contains secrets), drift detection, no secrets, destructive changes flagged and an auditable plan.

#### SEC-7.09 · Dependencies (SCA)
**Critical** (weight 3, origin `[B]`)  
versioned lockfiles, an SBOM generated per build (CycloneDX/SPDX), SCA with CVE/OSV in CI and continuously, transitive dependencies included, prioritization by exploitability (CISA KEV, EPSS, reachability), licenses assessed, out-of-support (EOL) components identified, automated updates with an SLA.

#### SEC-7.10 · Package supply chain attacks
**Important** (weight 2, origin `[A]`)  
protection against dependency confusion (reserved private scopes/namespaces and a registry configured to resolve internal packages only from the internal registry), typosquatting, compromised packages and maintainer takeover: install scripts disabled by default when possible, a **quarantine period** for newly published versions before automatic adoption, provenance verification when available, review of new dependencies (popularity, maintainer, permissions).

#### SEC-7.11 · Artifacts
**Important** (weight 2, origin `[A]`)  
images/packages/releases have provenance (SLSA), checksum, signature and verification before deploy (e.g., Sigstore/cosign); the registry prevents tag overwriting (immutability) and promotion of an unapproved artifact; deploy references a digest, not a mutable tag.

#### SEC-7.12 · CI/CD
**Critical** (weight 3, origin `[B]`)  
minimal token permissions per job (explicit `permissions:`); third-party actions/workflows pinned by SHA; fork PRs do not run with secrets or write permission (beware `pull_request_target` and `workflow_run`); untrusted inputs (PR title, branch name, issue body) are not interpolated into shell; cloud deploy uses OIDC instead of static keys; self-hosted runners are ephemeral and isolated; CI logs do not print secrets.

#### SEC-7.13 · Branch and review
**Important** (weight 2, origin `[A]`)  
protection requires independent review, required checks, an up-to-date branch, CODEOWNERS for sensitive areas (auth, crypto, CI, IaC, dependencies), blocked force push and deletion, signed commits assessed and an audit of administrator bypass.

#### SEC-7.14 · SAST/DAST/fuzz
**Important** (weight 2, origin `[A]`)  
SAST and secret scan run on every PR; authenticated DAST runs periodically and before major releases; findings are triaged with an SLA (not merely suppressed — suppressions have justification and expiry); fuzzing covers parsers, authentication, authorization and critical properties.

#### SEC-7.15 · Third-party dependency (SaaS/APIs)
**Important** (weight 2, origin `[A]`)  
versions, scopes, endpoints, data sent, SLA, fallback, sub-processors and supply chain risk are inventoried; external responses are validated as untrusted; integration credentials have minimal scope and rotation.

#### SEC-7.16 · OpenSSF Scorecard
**Minor** (weight 1, origin `[M]`)  
checks for vulnerabilities, updates, security policy, tests, SAST, branch protection, review, dangerous workflows, pinned dependencies, token permissions and signed releases are run and tracked, with a score target.

#### SEC-7.17 · Edge protection
**Minor** (weight 1, origin `[M]`)  
WAF/edge rules and DDoS protection are active for public endpoints, with tuned rules (blocking mode, not just monitoring), without replacing a fix in the code; the origin is not reachable bypassing the CDN/WAF (edge IP allowlist or origin authentication).

#### SEC-7.18 · Host and managed-service hardening
**Minor** (weight 1, origin `[M]`)  
operating systems and managed services follow a baseline (CIS or equivalent), with automated patching and SSH access disabled or through an audited mechanism.

## SEC-8. Logs, detection, response and recovery

**How to verify:** Look for audit events in the code (login, failures, role changes, exports), log destination and immutability, detection rules, incident playbook, DRP with RPO/RTO and a record of exercises, backup policy and restore test.

#### SEC-8.01 · Auditable events
**Critical** (weight 3, origin `[B]`)  
login (success/failure), MFA, reset, role change, authorization denied, export, reading of sensitive data, use of a secret, configuration change, deploy, destructive operation, administrative access and impersonation generate an event sufficient for investigation.

#### SEC-8.02 · Minimum event content
**Important** (weight 2, origin `[A]`)  
each event records who (identity and actor type), what, on which resource, when (synchronized UTC), from where (trusted IP, user agent, session), the result and correlation (`trace_id`), without recording a secret or sensitive data in clear.

#### SEC-8.03 · Log integrity and access
**Important** (weight 2, origin `[A]`)  
logs are sent to storage out of reach of the service that generates them (separate account/project), append-only/immutable (WORM), with a trusted timestamp, defined retention, role-based control and an alert for deletion, alteration or ingestion drop.

#### SEC-8.04 · Detection
**Important** (weight 2, origin `[A]`)  
rules correlate brute force, credential stuffing, impossible travel, token reuse, privilege escalation, scraping, exfiltration (anomalous export/download volume), SSRF, API abuse, pipeline/IAM changes and credential creation; alerts have an owner, severity, runbook and periodic testing (attack simulation).

#### SEC-8.05 · Incident response
**Critical** (weight 3, origin `[B]`)  
a playbook aligned with a current reference (e.g., NIST SP 800-61r3) covers triage, severity, containment, token and session revocation, secret rotation, isolation, evidence preservation (chain of custody), communication, eradication, recovery and postmortem; 24×7 roles and contacts are defined.

#### SEC-8.06 · Disaster Recovery Plan
**Critical** (weight 3, origin `[B]`)  
an **explicit, versioned DRP** exists, with: RPO/RTO approved per service and per data set; scenarios covered (region loss, logical corruption, accidental deletion, ransomware, cloud account compromise, critical vendor outage); restoration order and dependencies; a step-by-step runbook executable by someone who did not write it; owner and deputy; criteria for declaring a disaster and for returning. The plan is **exercised** (at least annually and after relevant changes) with real time measured against RTO/RPO and lessons recorded.

#### SEC-8.07 · Attack-resilient backups
**Critical** (weight 3, origin `[B]`)  
backups follow 3-2-1 with at least one immutable/isolated copy (another account or a vault with locked retention), encrypted, with credentials separate from production's (compromising production does not allow deleting backups); restore is tested periodically with integrity verification (a real restore, not just “job completed”); backups of personal data respect retention and deletion (see PRIV-11).

#### SEC-8.08 · Blast radius
**Important** (weight 2, origin `[A]`)  
the compromise of an account, pod, action, vendor, tenant or key does not grant global access; segmentation, quotas, scopes, kill switches (quickly disabling a feature/integration/key) and mass revocation limit damage. A tested ability exists to revoke all sessions and rotate all secrets.

#### SEC-8.09 · Logging privacy
**Important** (weight 2, origin `[A]`)  
retention and content obey minimization; access to logs is audited; investigation can work with pseudonyms and reveal identity only under authorization. *(See PRIV-12.)*

#### SEC-8.10 · Incident communication
**Important** (weight 2, origin `[A]`)  
contacts, escalation, legal, privacy, customers, vendors and authorities are defined; decisions and timestamps are recorded. Incidents involving personal data integrate with the LGPD procedure (see PRIV-17) and applicable sectoral rules.

#### SEC-8.11 · Lessons learned
**Minor** (weight 1, origin `[M]`)  
post-incident produces root causes, missing controls, regression tests, an owner and a deadline; repeated findings or expired acceptances are escalated.

#### SEC-8.12 · Exercises
**Minor** (weight 1, origin `[M]`)  
incident and DR tabletops are held periodically with technical, legal and business participation, including a ransomware and a data leak scenario.

## SEC-9. Exposed surface and reconnaissance

**How to verify:** Check what is served publicly: `public/`, source maps (`productionBrowserSourceMaps`), `X-Powered-By` headers, exposed Swagger/health/metrics, `robots.txt`, `security.txt`, error pages.

> Goal: reduce what an attacker learns **before** attacking. Every piece of information exposed speeds up exploitation.

#### SEC-9.01 · Sensitive files and directories
**Critical** (weight 3, origin `[B]`)  
the following are not publicly accessible: `.git/`, `.env`, `.DS_Store`, backups (`*.bak`, `*.old`, `*.zip`, `*.sql`), dumps, IDE files, `docker-compose.yml`, a server's `package.json`, logs, `phpinfo`, status panels. Verified by scanning with a wordlist.

#### SEC-9.02 · Source maps and client code
**Important** (weight 2, origin `[A]`)  
source maps are not published in production (or only to an error tool, with authenticated access); bundles do not contain internal comments, URLs of internal environments, keys, sensitive hidden feature flags or authorization logic that depends on a secret.

#### SEC-9.03 · Fingerprinting
**Minor** (weight 1, origin `[M]`)  
`Server`, `X-Powered-By` headers, versions on default error pages, service banners and characteristic paths are removed or neutralized; error pages are customized and uniform.

#### SEC-9.04 · Documentation and operational endpoints
**Important** (weight 2, origin `[A]`)  
Swagger/OpenAPI UI, GraphQL playground, metrics endpoints (`/metrics`), detailed health, debug and profiling are not public in production (or require authentication); a public health check returns only a minimal status.

#### SEC-9.05 · Leakage through metadata
**Minor** (weight 1, origin `[M]`)  
published documents and images carry no internal metadata (author, path, software, geolocation); `robots.txt` and `sitemap` do not list sensitive areas.

#### SEC-9.06 · Exposure in public sources
**Important** (weight 2, origin `[A]`)  
monitoring for leaks of the organization's credentials and code in public repositories, pastes and leaked databases; the organization's public repositories and buckets are inventoried and reviewed.

#### SEC-9.07 · Responsible disclosure channel
**Minor** (weight 1, origin `[M]`)  
`/.well-known/security.txt` (RFC 9116) is published with a contact and a disclosure policy; a process exists to receive, triage and answer external reports within a defined time.

## SEC-10. Applications with LLMs and agents *(If: the application uses AI models, RAG or agents)*

**How to verify:** Look for use of LLMs/agents in the application. If there is none, mark the section N/A citing the search. If there is: separation of instructions and data, output validation, tools scoped to the user, RAG filters by permission, token/cost limits, execution sandbox.

> References: OWASP Top 10 for LLM Applications 2025 and OWASP Top 10 for Agentic Applications 2026.

#### SEC-10.01 · Direct and indirect prompt injection
**Critical** (weight 3, origin `[B]`)  
the system assumes that **all** content reaching the model (user input, documents, web pages, e-mails, tool results, data retrieved by RAG) may contain malicious instructions. Mitigation is layered: a clear separation between instructions and data, input and output classifiers/guardrails, least privilege for tools, human confirmation for impactful actions and adversarial testing with a corpus of known attacks. **Text sanitization alone is not considered a sufficient control.**

#### SEC-10.02 · Model output as untrusted input
**Critical** (weight 3, origin `[B]`)  
model output is validated by schema and context-encoded before being rendered (XSS), executed (code, SQL, shell), used in URLs (SSRF, exfiltration via image/markdown) or passed to another tool. Rendering of links and images generated by the model is restricted to allowed domains.

#### SEC-10.03 · Excessive agency and tool privilege
**Critical** (weight 3, origin `[B]`)  
tools exposed to the model/agent are minimal, with the scope and permissions of the **end user** (not of an all-powerful service account); destructive, financial, external-sending or irreversible actions require explicit human confirmation; there are limits on steps, spend and rate per agent session.

#### SEC-10.04 · Leakage of sensitive information
**Important** (weight 2, origin `[A]`)  
the model has no access to data the user could not see; system prompts contain no secrets (assume they will be extracted); responses are filtered for personal data and secrets; prompt/response logs follow the same sensitive-data policy.

#### SEC-10.05 · RAG and vector databases
**Important** (weight 2, origin `[A]`)  
indexed documents carry permission and tenant metadata; retrieval filters by authorization **before** sending to the model; ingestion validates the origin of the content (database poisoning); deleting a document also removes embeddings and caches.

#### SEC-10.06 · Agent memory and state
**Important** (weight 2, origin `[A]`) · Conditional — *If: agents with memory*  
persistent memory is isolated per user/tenant, validated before being written, expirable and auditable; untrusted content does not become permanent instruction (memory poisoning).

#### SEC-10.07 · Unbounded consumption and cost abuse
**Important** (weight 2, origin `[A]`)  
token limits per request, per user and per period; protection against prompts that force long outputs or tool loops; alerting on anomalous spend. *(See PERF-11.06.)*

#### SEC-10.08 · AI supply chain
**Important** (weight 2, origin `[A]`)  
models, providers, SDKs, MCP servers/plugins and datasets are inventoried, versioned, from trusted sources and reviewed; third-party MCP servers are treated as untrusted code (pinned, reviewed, with minimal permissions).

#### SEC-10.09 · Execution of generated code
**Critical** (weight 3, origin `[B]`) · Conditional — *If: the agent executes code*  
execution takes place in an isolated sandbox (no network by default, no credentials, with CPU/memory/time limits, ephemeral filesystem), never on the application host.

#### SEC-10.10 · AI adversarial testing
**Important** (weight 2, origin `[A]`)  
a red-teaming suite (jailbreak, indirect injection, exfiltration, tool abuse, system prompt extraction) is run in CI or before each prompt/model change, with attack success rate metrics.

## SEC-11. Exception handling and anomalous conditions

**How to verify:** Look for a global error handler and `unhandledRejection`, behavior on authorization/validation failure (fail-closed), rollback/compensation in multi-step operations, `finally` to release resources, rate limit/log behavior when the dependency goes down.

> Reference: OWASP Top 10:2025 category A10:2025 “Mishandling of Exceptional Conditions”.

#### SEC-11.01 · Fail closed
**Critical** (weight 3, origin `[B]`)  
an error in an authorization check, token validation, signature verification, permission service lookup or security feature flag results in **denial**, never in release.

#### SEC-11.02 · Unhandled exceptions
**Important** (weight 2, origin `[A]`)  
a global handler exists that captures exceptions, logs them with context and responds with a generic error; promise rejections/exceptions in threads neither silently bring down the process nor leave inconsistent state.

#### SEC-11.03 · Consistency after failure
**Important** (weight 2, origin `[A]`)  
a failure in the middle of a multi-step operation rolls back or compensates (saga), without leaving a resource created without an owner, a payment without an order or a partially applied permission; resources (files, locks, connections) are released in `finally`/equivalent.

#### SEC-11.04 · Boundary conditions
**Minor** (weight 1, origin `[M]`)  
numeric overflow/underflow, division by zero, invalid dates, timezones, leap years, null values and empty collections are tested on security and business paths.

#### SEC-11.05 · Behavior under exhaustion
**Important** (weight 2, origin `[A]`)  
a full disk, exhausted memory, exhausted pool or unavailable dependency does not disable security controls (e.g., the audit log failing silently, the rate limit turned off when Redis goes down). The failure behavior of each control is decided and documented (fail-open vs. fail-closed).

## SEC-12. Vulnerability management

**How to verify:** Look for a vulnerability SLA policy, triage reports, an EOL register of runtimes/frameworks (`engines`, versions), records of earlier pentests.

#### SEC-12.01 · Remediation SLA
**Critical** (weight 3, origin `[B]`)  
remediation deadlines by severity are defined and measured (common reference: critical ≤ 7 days, high ≤ 30, medium ≤ 90), with acceleration for vulnerabilities under active exploitation (CISA KEV) or high exploitation probability (EPSS); the age of open findings is reported.

#### SEC-12.02 · Prioritization by context
**Important** (weight 2, origin `[A]`)  
prioritization considers reachability of the vulnerable code, asset exposure, the data involved and compensating controls, besides the base score (CVSS v4.0).

#### SEC-12.03 · End of life
**Important** (weight 2, origin `[A]`)  
out-of-support runtimes, frameworks, databases, operating systems and libraries are identified with a dated migration plan.

#### SEC-12.04 · Recurring external tests
**Minor** (weight 1, origin `[M]`)  
periodic independent pentest (at least annually and after significant changes) and, when mature, a bug bounty; findings return to the backlog with an SLA.

## SEC-13. Mobile apps *(If: there is an iOS/Android app)*

**How to verify:** Look for mobile app code (iOS/Android/React Native/Flutter). If there is none, mark the section N/A.

#### SEC-13.01 · MASVS standard
**Important** (weight 2, origin `[A]`)  
the app is assessed against OWASP MASVS v2 (storage, cryptography, authentication, network, platform, code, resilience, privacy).

#### SEC-13.02 · Secure storage
**Important** (weight 2, origin `[A]`)  
tokens and secrets live in the Keychain/Keystore; sensitive data does not go to backups, logs, app-switcher screenshots or the clipboard.

#### SEC-13.03 · Communication
**Important** (weight 2, origin `[A]`)  
TLS only, no cleartext exceptions; pinning assessed for high-risk operations, with a rotation strategy.

#### SEC-13.04 · The backend does not trust the app
**Critical** (weight 3, origin `[B]`)  
every authorization and business rule is on the server; the app is considered reverse-engineerable; embedded keys are treated as public; app/device attestation is used as an additional signal, not as the only control.

#### SEC-13.05 · Deep links and exported components
**Important** (weight 2, origin `[A]`)  
deep links/app links validate parameters and origin; exported activities, services, content providers and URL schemes are minimal and protected.

## SEC-14. Execution and reporting of the whitebox pentest

**How to verify:** Assess the existence and quality of earlier pentest/assessment reports and of security regression tests (e.g., `tests/security/`), documented severity methodology and approval criterion.

#### SEC-14.01 · Risk-oriented code review
**Important** (weight 2, origin `[A]`)  
prioritize auth, authorization, parsing, crypto, secrets, SSRF, uploads, payments, admin, exports, webhooks, jobs, migrations, integrations and AI; record files, lines and call paths (source → sink).

#### SEC-14.02 · Authenticated dynamic testing
**Important** (weight 2, origin `[A]`)  
run with each role, tenant and state; compare responses, timing, side effects and logs. Test endpoints discovered outside the documentation and old versions.

#### SEC-14.03 · Negative testing
**Important** (weight 2, origin `[A]`)  
validate malformed inputs, limits, Unicode, double encoding, concurrency, out-of-order requests, replay, timeout, third-party failure and duplicate messages.

#### SEC-14.04 · Security tests as regression
**Important** (weight 2, origin `[A]`)  
each fixed vulnerability gets an automated test that would fail if it returned; authorization tests (matrix SEC-3.01) run in CI.

#### SEC-14.05 · Evidence of exploitation
**Important** (weight 2, origin `[A]`)  
each finding has a request/response or automated test, preconditions, demonstrated impact, reach, likelihood, sanitized screenshots/logs and reproduction instructions.

#### SEC-14.06 · Severity
**Important** (weight 2, origin `[A]`)  
the score uses a declared methodology (e.g., CVSS v4.0 with environmental metrics) and considers remote exploitation, required authentication, complexity, interaction, confidentiality, integrity, availability, privacy, multi-tenancy and business impact; residual risk is separated from technical severity; chainable findings are assessed together.

#### SEC-14.07 · Verifiable remediation
**Important** (weight 2, origin `[A]`)  
the recommendation points to the fix at the right boundary, not just a workaround; retest confirms the exploit is blocked, no bypass exists and legitimate functionality is kept.

#### SEC-14.08 · Approval criterion
**Critical** (weight 3, origin `[B]`)  
there is no open critical/high without formal acceptance; mediums have a deadline and compensation; exceptions have an owner, justification, expiry, monitoring and a remediation plan.
