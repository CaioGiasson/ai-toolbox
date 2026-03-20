# Contexto do Time — BotPag

> Sincronizado via `claude-sync` para `~/.claude/CONTEXT.md`.

## Sobre a empresa

A BotPag é uma fintech brasileira focada em serviços financeiros digitais nos mercados veicular, de importações/impostos, seguros e crédito. Opera com arquitetura de microsserviços distribuídos.

## Padrões de comunicação

- Issues e PRs em português.
- Commits em inglês (conventional commits: `feat:`, `fix:`, `chore:`, `refactor:`, etc.).
- Branches no padrão `tipo/descricao-curta` (ex: `feat/parcelatudo-wallet`).

## Fluxo de trabalho

1. Branch a partir de `main` ou `develop` (depende do repositório).
2. PR com template definido em `gh-templates`.
3. Review obrigatório de ao menos 1 pessoa do time.
4. Merge via squash sempre que possível para manter histórico limpo.

## Serviços internos relevantes

| Serviço         | Função                                      | URL interna                    |
|-----------------|---------------------------------------------|--------------------------------|
| `id`            | Identidade e autenticação                   | —                              |
| `detran`        | Consultas a DETRANs estaduais               | `https://detran.botpag.ws`     |
| `checkout`      | Processamento de pagamentos                 | —                              |
| `os-service`    | Ordem de serviço                            | —                              |
| `comunica`      | Mensageria (WhatsApp, SMS, e-mail)          | —                              |
| `monitor`       | Monitoramento e alertas                     | —                              |

## Variáveis de ambiente

Sempre utilizar o arquivo `.env.example` como referência. Nunca commitar `.env` real.
