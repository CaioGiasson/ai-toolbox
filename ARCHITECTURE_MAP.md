# BotPag — Architecture Map

## O que é a BotPag

A BotPag é uma fintech brasileira com foco em serviços financeiros digitais voltados principalmente ao mercado veicular, de importações/impostos, seguros e crédito. Seu portfólio é composto por múltiplas verticais independentes — cada uma endereçando um segmento de mercado específico — integradas por uma camada de serviços compartilhados (identidade, checkout, ordem de serviço, mensageria e monitoramento). A empresa opera com uma arquitetura distribuída em microsserviços, com padrão técnico predominante em Node.js + TypeScript + MongoDB + Prisma no backend e Next.js no frontend, utilizando Prisma ORM, RabbitMQ para filas assíncronas, Datadog para observabilidade e MostQI para biometria/antifraude.

---

## Vertical: Veicular

Conjunto de serviços responsáveis por consulta e pagamento de débitos veiculares (IPVA, multas, licenciamento) junto aos DETRANs estaduais.

### `parcelatudo-2022`
**Legado** — Segunda versão do Parcelatudo. Aplicação full-stack em **Next.js com BFF**, permitindo que o cliente simule e pague débitos veiculares. Substituída pela terceira versão atualmente em construção.

### `parcelatudo-backend-api`
**Ativo (em construção)** — Backend dedicado da terceira versão do Parcelatudo. Construído em **Node.js + TypeScript + MongoDB + Prisma**. Centraliza a lógica de negócio de consulta de débitos, geração de propostas, simulações e processamento de pagamentos. Futuramente integrará área logada com histórico de operações e wallet (gerenciada pelo `id`).

### `parcelatudo-front`
**Ativo (em construção)** — Frontend da terceira versão do Parcelatudo. Construído em **Next.js 15 + TypeScript + Tailwind CSS + shadcn/ui**. Interface mobile-first com autenticação, MFA para operações de wallet e gestão de frota veicular.

### `detran`
**Ativo** — Microsserviço central de consultas ao DETRAN. Concentra **todas as integrações com detrans estaduais e serviços de terceiros** para consulta de débitos veiculares. Opera em modo REST e Webhook, com retry, fallback, cache e histórico de consultas. É o serviço satélite acionado pelo Parcelatudo para obter os débitos de um veículo. API: `https://detran.botpag.ws`.

### `DetranPE`
**Legado/Específico** — Integração específica com o DETRAN do estado de Pernambuco.

### `pre-detran-pr`
**Específico** — Serviço de pré-processamento para integrações com o DETRAN do Paraná.

### `cidadetran`
**Ativo** — Adapter **SOAP → REST** em **Java/Gradle** para o sistema CIDADETRAN. Responsável por traduzir requisições REST em chamadas SOAP de consulta de débitos, gerando o WSDL client e expondo o endpoint `/v1/consulta-debitos/{renavam}/{tipoServico}`.

### `blitz`
**Ativo** — Serviço Blitz, vertical veicular. Documentação interna limitada; integra-se ao ecossistema de consultas veiculares.

### `telegramBot`
**Ativo** — Bot no Telegram com acesso às APIs de consulta de débitos veiculares, capaz de iniciar e gerar operações de pagamento diretamente pelo chat.

### `bot-ia-parcelatudo`
**Ativo** — Chatbot inteligente para o Parcelatudo. Usa **OpenAI GPT-4.1-mini** para interpretar linguagem natural e consultar o MongoDB do Parcelatudo. Permite buscas por placa e RENAVAM, com correção ortográfica automática. Interface via **Telegram**.

### `legacy-parcelatudo`
**Legado** — Versão anterior ao Parcelatudo 2022. Mantida como arquivo histórico.

---

## Vertical: Impostos (antiga Importações)

Serviços para desembaraço aduaneiro, geração e liquidação de impostos federais e estaduais relacionados a importações e transporte nacional.

### `clearance-api`
**Ativo** — API principal do desembaraço aduaneiro. Construída em **Node.js + TypeScript + MongoDB + Prisma**, projetada para alto fluxo com **filas**. Responsável por gerar e enviar para liquidação impostos federais e estaduais (II, ICMS, etc.) de remessas internacionais e transportes nacionais. Também contém a **tesouraria de alto fluxo**: integrações bancárias, filas de liquidação e geração de tickets. API: `https://clearing.botpag.ws`.

### `clearance-admin`
**Ativo** — Dashboard administrativo do Clearance em **Next.js**. Painel de backoffice para operadores acompanharem e gerenciarem os lotes de desembaraço.

### `front-clearance`
**Ativo** — Interface voltada ao cliente do Clearance. Área logada com dashboards de acompanhamento dos status dos lotes, desde a entrada até a finalização. Construído em **Next.js**, com deploy na Vercel.

### `clearance-appsmith-courier`
**Ativo** — Aplicação low-code em **Appsmith** para operações do Clearance voltada a couriers. Permite ao backoffice de couriers acompanhar e gerenciar suas remessas.

### `temp-middleware-smartddu`
**Temporário** — Facade/middleware para o SmartDDU. Gerado com v0.dev em **Next.js**, atua como intermediário para algumas comunicações de banco de dados entre o SmartDDU e a APIv2 legada.

### `logistic-api`
**Em construção** — API de logística responsável por acompanhar envios **China → Brasil**. Gerenciará toda a cadeia desde o first mile (China) até o last mile (Brasil), incluindo geração de etiquetas, pagamento de impostos e comunicação entre as partes envolvidas. Stack: **Node.js + TypeScript + MongoDB + Prisma**.

### `cc-price-engine`
**Ativo** — Motor de cálculo de preços para produtos importados (China). Calcula preços finais considerando câmbio, markups, logística, impostos e comissões. Gerencia entidades como lojas, comissionamentos e aditivos de preço.

### `compra-conforme`
**Em construção** — Frontend do marketplace **Compra Conforme** para vendas China → Brasil. Construído em **Next.js**. Integrará praticamente todos os serviços da empresa.

### `compra-conforme-backend-api`
**Em construção** — Backend do marketplace Compra Conforme. Stack: **Node.js + TypeScript + MongoDB + Prisma**.

### `help-starlink-correios`
**Ativo** — Ferramenta de suporte para integrações com Starlink e serviços dos Correios relacionados a remessas internacionais.

---

## Vertical: Seguros

### `insurance-api`
**Ativo** — API backend para simulação e contratação de seguros. Integra com seguradoras para oficializar apólices. Atualmente suporta **seguros veiculares**; arquitetura preparada para expandir para outros tipos de seguro. Stack: **Node.js + TypeScript + MongoDB + Prisma**.

### `insurance-frontend`
**Ativo** — Frontend da vertical de seguros. Interface para simulação e contratação de seguros. Stack: **Next.js**.

---

## Vertical: Crédito

### `credit-service`
**Em construção** — API de crédito pessoal. Responsável por simulações e gerenciamento de empréstimos, com motores de simulação para verificar limite de crédito disponível. Integra com a **QiTech** como mediadora de contratação. Usa **RabbitMQ** para processamento assíncrono de webhooks. Stack: **Node.js + TypeScript + MongoDB + Prisma** — `credit-api` (TODO: Rename).

### `BarterCred`
**Ativo** — Serviço de crédito por troca/barter. Interface em **Next.js** para operações de BarterCred.

### `whatsbank`
**Ativo** — Integração com o Whatsbank. Interface em **Next.js** para serviços bancários via WhatsApp.

---

## Vertical: Antifraude / Identidade

### `id`
**Ativo** — Serviço central de identidade da BotPag (`ID-BotPag`). Centraliza cadastros de usuários (PF e PJ), múltiplos perfis e filiais vinculados a empresas. Gerencia:
- Sessões de login e autenticação
- Meios de pagamento
- **Wallet completa** (recarga, saldo, débitos e TopUps)
- Chaves PIX e endereços
- Logs de auditoria

Integra com **MostQI** para biometria facial, **DigitalOcean Spaces** para armazenamento e **Comunica** para notificações. API: `https://id.botpag.ws`.

### `assinatura`
**Ativo** — Serviço de assinatura digital com prova de vida e validação antifraude. Processa vídeos com **FFmpeg**, realiza liveness detection e gera contratos em PDF com **pdfmake**. Integra com Firebase e Mongoose.

### `mostLivenessEncoder`
**Ativo** — Encoder de vídeo para liveness detection. Combina **Node.js + .NET (C#)** para processar vídeos em base64 usando a biblioteca de liveness da **MostQI**.

### `contract-service`
**Ativo** — Serviço de geração rápida de contratos baseado em templates. Usa arquitetura **T3 Stack (tRPC)** com Node.js + TypeScript + MongoDB + Prisma.

---

## Vertical: Checkout

### `os-service`
**Ativo** — Módulo centralizador de **Ordens de Serviço (OS)**. Toda operação ou movimentação financeira da empresa está vinculada a uma OS. Responsável pela criação, leitura, atualização e gerenciamento de OS com links de checkout. Stack: **Node.js + TypeScript + Prisma + MySQL**.

### `checkout`
**Ativo** — API backend de cobranças. Processa pagamentos via **PIX e cartão de crédito** com integrações às adquirentes **Cielo**, **PagSeguro** e **GetNet**. Gerencia OS, iniciação de pagamento e processamento de webhooks.

### `checkout-front`
**Em construção** — Novo frontend de checkout. Interface responsável por coletar dados do cliente e se comunicar com a API Checkout para realizar cobranças. Stack: **Next.js**.

### `credit-card-input`
**Ativo** — Componente iframe de coleta de dados de cartão de crédito. Gerador de HTML estático embeddable via iframe. Responsável por **criptografar os dados do cartão** para segurança no transporte, com suporte a 3DS e API postMessage. Produção: `https://card.botpag.ws`.

### `parcela.botpag`
**Legado** — Checkout WEB legado em **PHP**. Microfrontend para cobranças via PIX e cartão de crédito. Produção: `https://parcela.botpag.com.br/[osCode]`.

### `recibo`
**Legado** — Renderizador de recibos em **PHP**. Responsável por gerar o HTML/imagem do recibo (não gera o texto, apenas renderiza). Banco: MySQL.

### `pix_bb`
**Ativo** — Interface de pagamento PIX integrada ao **Banco do Brasil**. Construído em **Next.js** com v0.dev.

### `lp-pix-parcelado`
**Ativo** — Landing page para o produto **PIX parcelado**. Construído em **Next.js** com v0.dev para aquisição de clientes.

### `lp-pix-parcelado-4m`
**Ativo** — Landing page específica para o produto de **PIX parcelado em 4 meses**. Variação da LP acima.

---

## Vertical: Backoffice

### `Painel`
**Legado** — Painel administrativo legado em **PHP/Laravel**. Ferramentas gerais de backoffice: geração de OS individual, listagem de OS pagas, assinaturas, etc. Conecta-se a múltiplos bancos MySQL (OS, BotPag, Telegram). Utilizado principalmente para identificação e registro de pagamentos de operações.

### `front-clearance`
*(Também listado na vertical Impostos)* — Painel de tesouraria do Clearance. Permite ao backoffice autorizar liquidação de lotes e acompanhar valores pendentes.

### `escala-tech`
**Ativo** — Interface para escalação e suporte técnico interno. Stack: **Next.js**.

### `docpag`
**Ativo** — Microfrontend gerador de Ordens de Serviço para despachantes. Stack: **Next.js**.

### `app-pdv`
**Ativo** — Aplicativo PDV (Ponto de Venda) para operações de backoffice e vendas presenciais.

---

## Vertical: Marketplace

### `compra-conforme`
*(Listado também em Impostos)* — Frontend do marketplace para vendas China → Brasil.

### `compra-conforme-backend-api`
*(Listado também em Impostos)* — Backend do marketplace.

### `gift`
**Ativo** — Serviço de **cartão de crédito pré-pago em dólar (USD)** com parcelamento em reais (BRL). Inclui gestão de saldo, recargas e transações em moeda estrangeira.

---

## Core

### `site`
**Ativo** — Website principal da BotPag. Stack: **Next.js + PHP**. Inclui além do site institucional: endpoint interno de extração para bots e callbacks do CBPS.

### `site-grupo`
**Ativo** — Site corporativo do grupo BotPag. Stack: **Next.js**.

### `analytics`
**Ativo** — Serviço de analytics interno para acompanhamento de métricas e dados de uso das verticais.

---

## Tooling

### `comunica`
**Ativo** — Mensageiro centralizado. API hub de comunicação responsável por envio de **e-mail e SMS** para todos os serviços da empresa. Integra com múltiplos provedores de mensageria. Stack: **Node.js + Express**.

### `comunica-module`
**Ativo** — Módulo npm da Comunica para uso como dependência em outros serviços. Abstrai a comunicação com a API do Comunica.

### `crm-backend`
**Ativo** — Backend do CRM. Integra com **RD Station** para rastreamento de leads e conversões do Parcelatudo e seguros. Gerencia hot leads, eventos e conversões. Stack: **Node.js + TypeScript + MongoDB + Prisma**.

### `crm-service`
**Ativo** — CRM Service estendido (nova versão em construção — `crm-api` TODO: Rename). Além de integrar com serviços de mensageria, manterá histórico de interações e conversas dos clientes.

### `crm-module`
**Ativo** — Módulo npm de integração com o RD Station CRM. Biblioteca compartilhada por outros serviços.

### `monitor`
**Ativo** — Dashboard de monitoramento de serviços. Interface **Next.js** para health checks, execução de testes e sinalização de erros nos ambientes da empresa.

### `powerlog`
**Ativo** — Módulo de logging centralizado. Todos os serviços devem usar o PowerLog para enviar logs ao `monitor.botpag.ws`. **Serviços não devem se conectar diretamente ao banco do Monitor.**

### `link`
**Ativo** — Encurtador de links BotPag. Serviço de geração e gerenciamento de URLs curtas.

### `zipcode`
**Ativo** — API de busca de CEP com base interna e fallback para a **BrasilAPI**. Stack: **Node.js + TypeScript + MongoDB + Prisma**.

### `toolbox`
**Ativo** — Ferramentas genéricas para uso interno: intervenções em dados, coletas, exportações e scripts via terminal.

### `tools`
**Ativo** — Biblioteca de ferramentas e utilitários para instalar como módulos em outros repositórios. Inclui: validators (CPF, e-mail, senha), formatters (data, moeda), debounce, throttle e **logger com integração Datadog** (Winston). **Os logs do Datadog estão neste repositório.**

### `tools-ts`
**Ativo** — Versão TypeScript tipada da biblioteca de ferramentas, com utilitários customizados e logger Winston.

### `tools-js`
**Ativo** — Template para importação das ferramentas via git submodules/subtrees em projetos JavaScript.

### `tools-module`
**Ativo** — Módulo npm de utilitários compartilhados para uso como dependência em outros serviços.

### `queue-manager`
**Ativo** — Módulo de gerenciamento de filas. Abstrai a comunicação com **RabbitMQ** para uso pelos demais serviços.

### `bigquery-middleware`
**Ativo** — Middleware de integração com o **Google BigQuery** para análise e processamento de dados. Stack: **NestJS + TypeScript**.

### `data-talk-mcp`
**Ativo** — Serviço MCP (Model Context Protocol) para comunicação de dados entre serviços e modelos de IA.

### `design-system`
**Ativo** — Design System da BotPag (`@bp/design-system`). Biblioteca de componentes UI compartilhada. Stack: **React + TypeScript + Tailwind CSS + Vite**. Exporta componentes como Button, inputs e tokens de design.

### `gh-templates`
**Ativo** — Templates de GitHub para padronização de issues, pull requests e workflows de CI/CD nos repositórios da empresa.

---

## Legado

### `api`
**Legado (APIv2)** — API monolítica onde muitos dos serviços citados acima estavam centralizados. Com o tempo, repositórios e serviços próprios foram criados e ela está sendo cada vez menos utilizada. Mantida em produção para serviços que ainda não foram migrados.

### `parcela.botpag`
*(Listado também em Checkout)* — Checkout WEB legado em PHP.

### `recibo`
*(Listado também em Checkout)* — Geração de recibos legado em PHP.

### `Painel`
*(Listado também em Backoffice)* — Painel administrativo legado em PHP/Laravel.

### `parcelatudo-2022`
*(Listado também em Veicular)* — Segunda versão do Parcelatudo em Next.js (legado).

### `legacy-parcelatudo`
**Legado** — Versão anterior ao Parcelatudo 2022. Mantida como arquivo histórico.

---

## Templates e Ambientes

### `boilerplate-backend`
**Template** — Boilerplate padrão para criação de novos serviços backend. Stack: **Node.js + TypeScript + MongoDB + Prisma + ESLint + Prettier**. Define os padrões de código da empresa: camelCase para variáveis, PascalCase para classes, SNAKE_CASE para constantes, máximo de 3 parâmetros por função, sem uso de `any`.

### `sandbox-bpdev`
**Ambiente** — Sandbox de desenvolvimento para testes e experimentações dos devs.

### `xpto-teste`
**Teste** — Repositório placeholder para testes e demonstrações pontuais.

### `rotinas-backup`
**Utilitário** — Scripts e rotinas de backup de dados e infraestrutura.

### `beeviral-module`
**Módulo** — Integração com o sistema de indicações/referral **Beeviral**.

---

## Diagrama de Dependências Principais

```
[Cliente Web/Mobile]
        │
        ├── parcelatudo-front ──────► parcelatudo-backend-api ──► detran (APIv2 legado)
        │                                                     └──► checkout (pagamento)
        │                                                     └──► id (wallet/auth)
        │
        ├── front-clearance ────────► clearance-api ──────────► queue (liquidação)
        │                         └── clearance-admin            └──► integrações bancárias
        │
        ├── insurance-frontend ─────► insurance-api
        │
        ├── checkout-front ─────────► checkout ───────────────► os-service
        │                                                    └──► adquirentes (Cielo/PagSeguro/GetNet)
        │
        └── compra-conforme ────────► compra-conforme-backend-api
                                  └──► cc-price-engine
                                  └──► logistic-api

[Serviços Compartilhados]
  id              → wallet, auth, cadastros (consumido por todos)
  os-service      → ordens de serviço (consumido por todos)
  comunica        → e-mail/SMS (consumido por todos)
  powerlog/monitor → logs e monitoramento (consumido por todos)
  tools/tools-ts  → utilitários e Datadog (consumido por todos)
  detran          → consultas DETRAN (consumido por Parcelatudo e Telegram)
  contract-service → geração de contratos (consumido por Crédito/Veicular)
  assinatura/id   → antifraude/liveness (consumido por Crédito/Seguros)
```
