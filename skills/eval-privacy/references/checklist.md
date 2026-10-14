# Catálogo de critérios — Privacy (LGPD)

> Gerado a partir do *Checklist sênior para assessment de aplicações — v3* (outubro/2026). Não edite à mão: regenere com `python -X utf8 scripts/gen-assessment-catalog.py` no ai-toolbox (fonte: `docs/application-assessment-v3.md`). IDs, severidades e critérios são a base do score e precisam ser estáveis entre execuções.

**Severidade (fixa por item):** `[B]` Bloqueante → **Crítico** (peso 3) · `[A]` Alto → **Importante** (peso 2) · `[M]` Médio e `[R]` Recomendado → **Menor** (peso 1).

**Itens condicionais** (*Se: …*): quando a condição não se aplica, marque **N/A com justificativa e evidência** (ex.: busca no código sem ocorrências). N/A sem evidência conta como Não compliant.

**Total de itens:** 126 — Crítico: 37 · Importante: 66 · Menor: 23. Pontuação máxima (todos aplicáveis): 266.

## Objetivo do pilar

> **Objetivo do pilar:** identificar **toda** lacuna que impeça a aplicação (e a operação que a sustenta) de estar em conformidade com a LGPD e normas conexas, de forma rastreável a artigo de lei ou resolução da ANPD. A conformidade é avaliada no **comportamento real do sistema** (o que é coletado, enviado, armazenado e apagado de fato), não apenas na política publicada.
>
> **Regras de avaliação deste pilar:**
> - Cada item indica o fundamento legal entre colchetes. Ao registrar um achado, citar o artigo.
> - Divergência entre o aviso de privacidade e o comportamento observado (captura de rede, banco, logs) é sempre achado `[A]` ou superior.
> - Quando a ANPD ainda não regulamentou um tema (ex.: RIPD, portabilidade), aplica-se a lei, os guias orientativos vigentes e a melhor prática; o item registra essa condição.
> - Agentes de pequeno porte (Res. CD/ANPD nº 2/2022) podem ter regime simplificado — marcar quando aplicável e verificar se o tratamento é de alto risco (o que afasta parte dos benefícios).
> - Verificar sempre a versão vigente das resoluções; a ANPD tornou-se agência reguladora (Lei 15.352/2026), tem agenda regulatória ativa e mapa de temas prioritários de fiscalização para 2026–2027 (Res. 30/2025), com foco declarado em direitos dos titulares, dados sensíveis, crianças e adolescentes e poder público.

## PRIV-1. Aplicabilidade, papéis e escopo

**Como verificar:** Procure política de privacidade, termos, ROPA, documentação de papéis (controlador/operador), público-alvo do produto. Sem documentação de aplicabilidade e papéis = Não atende.

#### PRIV-1.01 · Aplicabilidade territorial e material
**Crítico** (peso 3, origem `[B]`) · Fundamento: arts. 3º e 4º  
está documentado por que a LGPD se aplica (tratamento no Brasil, oferta de bens/serviços a pessoas no Brasil ou dados coletados no Brasil) e quais tratamentos estão fora do escopo (art. 4º), com justificativa. Outras jurisdições aplicáveis (ex.: GDPR para titulares na UE) são identificadas.

#### PRIV-1.02 · Papéis por operação
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 5º, VI–IX; arts. 37–40  
para **cada operação de tratamento** está definido quem é controlador, cocontrolador, operador e suboperador, com base em quem decide finalidade e elementos essenciais (não no que diz o contrato). Situações em que a empresa atua como operadora de clientes (SaaS B2B) são separadas das em que é controladora.

#### PRIV-1.03 · Porte do agente
**Menor** (peso 1, origem `[M]`) · Fundamento: Res. 2/2022  
está avaliado se a organização se enquadra como agente de pequeno porte e, em caso positivo, se realiza tratamento de alto risco (larga escala ou impacto significativo **e** uso de tecnologia inovadora, vigilância, decisão automatizada ou dados sensíveis/de crianças/de idosos), o que limita as flexibilizações.

#### PRIV-1.04 · Categorias de titulares
**Importante** (peso 2, origem `[A]`)  
estão identificadas todas as categorias de titulares (clientes, usuários finais de clientes, visitantes, leads, colaboradores, candidatos, representantes de PJ, dependentes, terceiros mencionados em conteúdo), inclusive titulares indiretos.

## PRIV-2. Inventário e registro das operações (ROPA)

**Como verificar:** Compare o inventário de dados (ROPA/docs) com o schema real (modelos e campos com dados pessoais) e com os terceiros chamados no código e no frontend (SDKs, pixels, APIs). Campo pessoal ou terceiro não inventariado = Parcial ou Não atende.

#### PRIV-2.01 · Inventário de dados ponta a ponta
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 37; art. 6º, X  
o inventário mapeia cada fluxo desde a coleta até a eliminação: sistemas, tabelas/campos, integrações, regiões, categorias de titulares, volume, dados pessoais e sensíveis, finalidade, base legal, compartilhamentos, retenção e controles. Inclui coleta direta e indireta, cookies, SDKs, pixels, logs, analytics, gravação de sessão, suporte/CRM, backups, ambientes não produtivos, planilhas exportadas, treinamento/avaliação de modelos e dados enviados a provedores de IA.

#### PRIV-2.02 · Inventário verificado contra o sistema real
**Importante** (peso 2, origem `[A]`)  
o inventário é conferido por evidência técnica: varredura de schemas/bancos por dados pessoais (data discovery), captura de tráfego do frontend e app (quais terceiros recebem o quê), revisão de payloads de logs e eventos. Campos pessoais não inventariados são achado.

#### PRIV-2.03 · Classificação no código
**Menor** (peso 1, origem `[M]`)  
campos com dados pessoais e sensíveis são anotados no schema/modelos (tags, comentários estruturados ou catálogo de dados), permitindo que testes, linters, mascaramento e pipelines de eliminação os localizem automaticamente.

#### PRIV-2.04 · Registro das operações
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 37; Res. 2/2022  
existe registro das operações de tratamento atualizado, com owner por finalidade, especialmente para tratamentos baseados em legítimo interesse; formato simplificado apenas para agentes de pequeno porte elegíveis. Mudanças de produto disparam atualização (gatilho no processo de desenvolvimento).

## PRIV-3. Princípios (art. 6º)

**Como verificar:** Avalie campo a campo os formulários/APIs de cadastro e eventos: necessidade de cada dado, finalidades declaradas, acesso do titular aos próprios dados, mecanismos de correção. Use o aviso de privacidade como referência do declarado.

#### PRIV-3.01 · Boa-fé e finalidade
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 6º, caput e I  
cada tratamento tem propósito legítimo, específico, explícito e informado; não há tratamento posterior incompatível (ex.: dados de suporte usados para marketing, dados de cadastro usados para treinar modelo sem avaliação).

#### PRIV-3.02 · Adequação
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 6º, II  
o tratamento é compatível com o contexto e a expectativa do titular (avaliado pelo que o titular razoavelmente espera ao usar a funcionalidade).

#### PRIV-3.03 · Necessidade e minimização
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 6º, III  
cada campo coletado tem justificativa vinculada à finalidade; campos opcionais são realmente opcionais; não há coleta “por precaução”; dados são truncados/agregados quando a precisão total não é necessária (ex.: data de nascimento → faixa etária; geolocalização precisa → cidade). Formulários, APIs e eventos de analytics são revisados campo a campo.

#### PRIV-3.04 · Livre acesso
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 6º, IV; art. 9º  
o titular consegue consultar, de forma facilitada e gratuita, a forma e duração do tratamento e a integralidade dos seus dados.

#### PRIV-3.05 · Qualidade dos dados
**Menor** (peso 1, origem `[M]`) · Fundamento: art. 6º, V  
há mecanismos de correção e atualização (pelo titular e por processo interno); dados desatualizados que geram decisões sobre o titular são revisados.

#### PRIV-3.06 · Transparência
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 6º, VI  
informações claras, precisas e acessíveis sobre o tratamento e os agentes, respeitados segredos comercial e industrial (detalhado na seção 9).

#### PRIV-3.07 · Segurança e prevenção
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 6º, VII e VIII  
medidas técnicas e administrativas protegem contra acessos não autorizados e situações acidentais ou ilícitas, e previnem danos (detalhado na seção 12 e no pilar Security).

#### PRIV-3.08 · Não discriminação
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 6º, IX  
não há tratamento para fins discriminatórios ilícitos ou abusivos; modelos, regras de score, precificação e segmentações são avaliados quanto a efeitos discriminatórios (inclusive por variáveis proxy).

#### PRIV-3.09 · Responsabilização e prestação de contas
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 6º, X  
o controlador consegue **demonstrar**, com evidência, a adoção de medidas eficazes e a eficácia delas (ver seção 24).

## PRIV-4. Bases legais

**Como verificar:** Procure as bases legais por finalidade no aviso/ROPA e verifique coerência com o comportamento (ex.: marketing não pode estar sob "execução de contrato").

#### PRIV-4.01 · Base legal por finalidade
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 7º  
cada finalidade tem **uma** base legal documentada e coerente entre as dez hipóteses do art. 7º (consentimento; obrigação legal/regulatória; políticas públicas; pesquisa; execução de contrato ou procedimentos preliminares; exercício regular de direitos; proteção da vida; tutela da saúde; legítimo interesse; proteção do crédito). Não se usa consentimento quando o tratamento ocorreria de qualquer forma (base incorreta gera expectativa falsa de revogação).

#### PRIV-4.02 · Execução de contrato aplicada com rigor
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 7º, V  
a base “contrato” cobre apenas o estritamente necessário para entregar o serviço contratado; marketing, analytics não essenciais, perfilamento e compartilhamento com parceiros não são justificados por ela.

#### PRIV-4.03 · Obrigação legal identificada
**Menor** (peso 1, origem `[M]`) · Fundamento: art. 7º, II  
quando a base é obrigação legal/regulatória, a norma específica e o prazo exigido estão citados (ex.: registros fiscais, guarda de registros de acesso do Marco Civil).

#### PRIV-4.04 · Dados públicos e manifestamente públicos
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 7º, §§ 3º, 4º e 7º  
dados obtidos de fontes públicas ou tornados públicos pelo titular são tratados considerando a finalidade, a boa-fé e o interesse público que justificaram sua disponibilização; scraping e enriquecimento de dados têm base legal e avaliação própria.

#### PRIV-4.05 · Mudança de base ou finalidade
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 9º, § 2º  
alteração de finalidade incompatível com o consentimento original é informada **previamente**, com possibilidade de revogação; a troca de base legal não é usada para contornar revogação de consentimento.

## PRIV-5. Consentimento

**Como verificar:** Procure registro de consentimento (modelo/tabela com versão, data, canal), opções granulares, fluxo de revogação e se o código consulta o consentimento antes de usar o dado. Se nenhuma finalidade usa consentimento, marque a seção N/A justificando.

*(Se: alguma finalidade usa consentimento.)*

#### PRIV-5.01 · Requisitos de validade
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 5º, XII; art. 8º  
consentimento é livre, informado e inequívoco, para finalidades determinadas (autorizações genéricas são nulas), fornecido por escrito ou meio que demonstre a manifestação de vontade; cláusula destacada das demais quando em contrato; não é condição para serviço que não depende daquele tratamento.

#### PRIV-5.02 · Granularidade
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 8º, § 4º  
finalidades distintas têm opções distintas (ex.: newsletter, ofertas de parceiros, personalização, analytics); não há “aceito tudo” como única opção.

#### PRIV-5.03 · Prova do consentimento
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 8º, § 2º  
o ônus da prova é do controlador: cada consentimento é registrado com titular, finalidade, versão do texto apresentado, data/hora, canal, interface/versão do app e evidência da ação afirmativa; o registro é íntegro e recuperável.

#### PRIV-5.04 · Revogação
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 8º, § 5º; art. 18, IX  
revogação é gratuita, facilitada, pelo mesmo canal ou mais simples que a concessão, e **efetiva tecnicamente**: o sistema para de tratar (eventos deixam de ser enviados, listas são atualizadas, terceiros são notificados) em prazo definido e verificado por teste.

#### PRIV-5.05 · Aplicação do consentimento no código
**Importante** (peso 2, origem `[A]`)  
o estado de consentimento é consultado no ponto de uso (envio de e-mail marketing, disparo de pixel, uso para personalização), não apenas na coleta; existe teste automatizado que garante que nenhum tracker/evento opcional dispara sem consentimento (verificação por captura de rede).

#### PRIV-5.06 · Vícios de consentimento
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 8º, § 3º  
não há consentimento obtido mediante erro, dolo, coação ou interface enganosa (ver PRIV-9.04 sobre dark patterns).

## PRIV-6. Legítimo interesse

**Como verificar:** Procure testes de balanceamento (LIA) documentados para cada finalidade baseada em legítimo interesse e o canal de oposição. Sem uso de legítimo interesse, marque N/A justificando.

*(Se: alguma finalidade usa legítimo interesse.)*

#### PRIV-6.01 · Teste de balanceamento documentado
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 10; art. 7º, IX; guia orientativo da ANPD sobre legítimo interesse  
para cada finalidade há avaliação registrada de: (i) finalidade legítima e situação concreta; (ii) necessidade (apenas dados estritamente necessários, sem alternativa menos invasiva); (iii) balanceamento com expectativas legítimas e direitos do titular; (iv) salvaguardas (transparência, opt-out, minimização, segurança).

#### PRIV-6.02 · Vedação para dados sensíveis
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 11  
legítimo interesse **não** é usado como base para dados pessoais sensíveis.

#### PRIV-6.03 · Transparência e oposição
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 10, § 2º; art. 18, § 2º  
o titular é informado sobre o tratamento por legítimo interesse e pode se opor por canal simples; a oposição é avaliada e, quando procedente, efetivada tecnicamente.

#### PRIV-6.04 · Disponibilidade para a ANPD
**Menor** (peso 1, origem `[M]`) · Fundamento: art. 10, § 3º; art. 37  
o teste de balanceamento e o registro das operações estão prontos para entrega à ANPD; a ANPD pode exigir RIPD nesses casos.

## PRIV-7. Dados pessoais sensíveis

**Como verificar:** Procure dados sensíveis no schema e nos fluxos (saúde, biometria, origem, religião etc., inclusive inferidos de fotos/compras) e a base do art. 11. Se não houver dado sensível, registre a busca como evidência do N/A.

#### PRIV-7.01 · Identificação de dados sensíveis
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 5º, II  
estão mapeados todos os dados sobre origem racial ou étnica, convicção religiosa, opinião política, filiação sindical ou a organização religiosa/filosófica/política, saúde, vida sexual, genéticos e **biométricos** — inclusive dados **inferidos** (ex.: compras que revelam condição de saúde, foto usada para reconhecimento facial).

#### PRIV-7.02 · Base legal do art. 11
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 11  
cada tratamento sensível usa uma hipótese do art. 11 (consentimento específico e destacado para finalidades específicas, ou as hipóteses sem consentimento, como obrigação legal, exercício regular de direitos inclusive em contrato, proteção da vida, tutela da saúde e prevenção à fraude e segurança do titular em processos de identificação e autenticação de cadastro). Biometria para login/antifraude cita expressamente a hipótese usada.

#### PRIV-7.03 · Vedações específicas
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 11, §§ 4º e 5º  
não há comunicação ou uso compartilhado de dados de saúde para vantagem econômica fora das exceções legais; operadoras de planos de saúde não tratam dados para seleção de riscos.

#### PRIV-7.04 · Proteção reforçada
**Importante** (peso 2, origem `[A]`) · Fundamento: arts. 11, 46  
dados sensíveis têm controles adicionais: criptografia em nível de campo, acesso restrito e auditado por pessoa, exclusão de logs/analytics, segregação, retenção mínima e RIPD (ver SEC-6.04 e seção 19).

#### PRIV-7.05 · Uso em publicidade e perfilamento
**Importante** (peso 2, origem `[A]`) · Fundamento: arts. 6º, IX; 11; Res. 30/2025  
dados sensíveis (inclusive inferidos) não alimentam segmentação publicitária nem públicos de plataformas de anúncios sem base legal adequada; esse ponto é tema prioritário de fiscalização da ANPD.

## PRIV-8. Crianças, adolescentes e outros vulneráveis

**Como verificar:** Verifique público-alvo, age gate, verificação de idade, configurações protetivas por padrão e obrigações do ECA Digital. Conclusão "não se aplica" exige justificativa documentada no repositório.

#### PRIV-8.01 · Determinação de público e de acesso provável
**Crítico** (peso 3, origem `[B]`)  
ECA Digital] — está avaliado se o produto é direcionado a crianças/adolescentes **ou de acesso provável** por eles (conceito do ECA Digital, vigente desde 17/03/2026), com evidência (natureza do serviço, analytics, público de marketing). A conclusão “não se aplica” é documentada.

#### PRIV-8.02 · Melhor interesse e base legal
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 14, caput; Enunciado CD/ANPD nº 1/2023  
o tratamento de dados de crianças e adolescentes observa o melhor interesse e usa as hipóteses legais dos arts. 7º ou 11, com consentimento específico e em destaque de um dos pais ou responsável quando o consentimento for a base para crianças (art. 14, § 1º), e esforços razoáveis para verificar que o consentimento foi dado pelo responsável (§ 5º).

#### PRIV-8.03 · Minimização em jogos e aplicações
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 14, § 4º  
a participação em jogos, aplicações e atividades não é condicionada ao fornecimento de dados além do estritamente necessário.

#### PRIV-8.04 · Transparência adequada à idade
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 14, §§ 2º e 6º  
são públicos os tipos de dados coletados, a forma de utilização e o procedimento para exercício de direitos; as informações são simples, claras, acessíveis e adequadas ao entendimento da criança, com recursos audiovisuais quando apropriado.

#### PRIV-8.05 · Obrigações do ECA Digital
**Crítico** (peso 3, origem `[B]`) · Condicional — *Se: direcionado ou de acesso provável por menores* · Fundamento: Lei 15.211/2025 e decretos regulamentadores de 18/03/2026  
verificar, por tipo de serviço: mecanismo **confiável** de verificação de idade (autodeclaração isolada não é suficiente); configurações protetivas por padrão (*safety by default*); ferramentas de supervisão parental; vedação de perfilamento para publicidade direcionada a crianças e adolescentes; vedação de caixas de recompensa (loot boxes) em jogos; canais de denúncia e remoção; e demais obrigações específicas por categoria (redes sociais, jogos, lojas de aplicativos, plataformas de vídeo). A ANPD é a autoridade fiscalizadora.

#### PRIV-8.06 · Verificação de idade proporcional e com privacidade
**Importante** (peso 2, origem `[A]`)  
o método de verificação de idade coleta o mínimo necessário (preferência por estimativa/atestação que não retenha documento ou imagem), elimina dados de verificação após uso e não cria nova base de dados biométricos desnecessária.

#### PRIV-8.07 · Idosos e outros vulneráveis
**Menor** (peso 1, origem `[M]`) · Fundamento: art. 6º; Res. 2/2022  
idosos, pessoas com deficiência e outros grupos vulneráveis são considerados na avaliação de risco, no desenho do consentimento, na acessibilidade das interfaces (WCAG) e na comunicação.

## PRIV-9. Transparência, aviso de privacidade e cookies

**Como verificar:** Leia o aviso de privacidade e compare com o comportamento real (terceiros no código/HTML, cookies setados, storage). Verifique banner de cookies (recusar tão fácil quanto aceitar), avisos contextuais e versionamento do aviso.

#### PRIV-9.01 · Conteúdo mínimo do aviso
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 9º; art. 18  
o aviso informa: finalidade específica; forma e duração do tratamento; identificação e contato do controlador; identidade e contato do encarregado; uso compartilhado e sua finalidade; responsabilidades dos agentes; direitos do titular e como exercê-los; transferência internacional; base legal por finalidade; critérios de retenção; e, quando o tratamento for condição para o serviço, esse fato e os meios de exercer direitos (art. 9º, § 3º).

#### PRIV-9.02 · Aviso consistente com o comportamento real
**Crítico** (peso 3, origem `[B]`)  
cada terceiro que recebe dados (detectado em captura de rede, integrações e contratos) está no aviso; cada dado coletado está no aviso; não há coleta não declarada. Diferenças são achado.

#### PRIV-9.03 · Aviso contextual e versionado
**Menor** (peso 1, origem `[M]`) · Fundamento: art. 8º, § 6º; art. 9º  
além da política geral, há avisos no momento da coleta (just-in-time) para dados não óbvios (localização, contatos, câmera, biometria); versões do aviso são datadas e arquivadas; alterações relevantes são comunicadas ao titular.

#### PRIV-9.04 · Ausência de dark patterns
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 6º, I e VI; art. 8º; guia orientativo da ANPD sobre cookies  
o banner/fluxo de consentimento não usa padrões enganosos: recusar é tão fácil e visível quanto aceitar (mesma camada, mesmo destaque), não há caixas pré-marcadas, contraste ou linguagem enganosa, cansaço por repetição (re-perguntar após recusa em curto intervalo), “cookie wall” injustificado ou interpretação de rolagem/navegação como consentimento.

#### PRIV-9.05 · Cookies e tecnologias de rastreamento
**Importante** (peso 2, origem `[A]`) · Fundamento: guia orientativo da ANPD sobre cookies  
cookies, local storage, pixels, SDKs, fingerprinting e server-side tagging são inventariados por categoria (necessários, desempenho, funcionais, publicidade); apenas os estritamente necessários operam antes da escolha; a escolha é registrada, pode ser alterada a qualquer momento por link sempre acessível e é respeitada também no tagueamento server-side e em integrações de conversão (ex.: envio de e-mail/telefone com hash a plataformas de anúncio continua sendo dado pessoal).

#### PRIV-9.06 · Gravação de sessão e ferramentas de comportamento
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: session replay, heatmaps*  
campos de entrada, dados pessoais exibidos e telas sensíveis são mascarados por padrão; a ferramenta está no aviso, tem base legal e retenção curta.

#### PRIV-9.07 · Acessibilidade da informação
**Menor** (peso 1, origem `[M]`)  
aviso e central de privacidade são acessíveis (leitores de tela, linguagem simples, português), encontráveis a partir de qualquer página e no app.

## PRIV-10. Direitos dos titulares

**Como verificar:** Procure endpoints/fluxos de acesso/export, correção, eliminação, revogação e oposição; registro de pedidos (protocolo, prazos); testes ponta a ponta desses fluxos.

#### PRIV-10.01 · Canal e verificação de identidade
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 18, caput e §§ 3º e 5º  
há canal gratuito, acessível e divulgado (autosserviço na conta e canal alternativo para quem não tem conta); a verificação de identidade é proporcional ao risco (não exige mais dados do que o necessário nem vira barreira); pedidos por representante legal são tratados.

#### PRIV-10.02 · Cobertura de todos os direitos do art. 18
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 18, I–IX e § 2º  
o processo e o sistema atendem: (I) confirmação da existência de tratamento; (II) acesso; (III) correção de dados incompletos, inexatos ou desatualizados; (IV) anonimização, bloqueio ou eliminação de dados desnecessários, excessivos ou tratados em desconformidade; (V) portabilidade; (VI) eliminação dos dados tratados com consentimento (ressalvado o art. 16); (VII) informação sobre entidades com as quais houve uso compartilhado; (VIII) informação sobre a possibilidade de não consentir e suas consequências; (IX) revogação do consentimento; e oposição (§ 2º).

#### PRIV-10.03 · Prazos do art. 19
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 19  
confirmação de existência ou acesso: **imediatamente**, em formato simplificado, ou em até **15 dias** por declaração clara e completa (origem, inexistência de registro, critérios e finalidade). Prazos são medidos por pedido, com alerta antes do vencimento. Quando a providência não puder ser imediata, o titular recebe resposta com as razões (art. 18, § 4º). Agentes de pequeno porte: verificar regra de prazo diferenciado da Res. 2/2022.

#### PRIV-10.04 · Formato da resposta e cópia integral
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 19, §§ 1º a 3º  
dados são armazenados de forma que favoreça o exercício do acesso; a resposta pode ser eletrônica ou impressa; quando o tratamento se basear em consentimento ou contrato, o titular pode obter cópia eletrônica integral em formato que permita uso subsequente.

#### PRIV-10.05 · Compilação automatizada (DSAR)
**Importante** (peso 2, origem `[A]`)  
o sistema gera a exportação de dados de um titular a partir de **todas** as fontes do inventário (banco principal, serviços satélites, data warehouse, ferramentas de suporte/CRM, logs relevantes, terceiros), por processo automatizado e testado; o pacote não inclui dados de outros titulares.

#### PRIV-10.06 · Portabilidade
**Menor** (peso 1, origem `[M]`) · Fundamento: art. 18, V; art. 40  
a exportação é estruturada e em formato interoperável (ex.: JSON/CSV documentado); a regulamentação específica da ANPD sobre portabilidade é acompanhada (tema de agenda regulatória).

#### PRIV-10.07 · Correção propagada
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 18, § 6º  
correção, eliminação, anonimização e bloqueio são comunicados **de imediato** aos agentes com quem houve uso compartilhado, para que repitam o procedimento (exceto quando comprovadamente impossível ou desproporcional, com registro).

#### PRIV-10.08 · Registro e auditoria de pedidos
**Importante** (peso 2, origem `[A]`)  
cada pedido tem protocolo, data de recebimento, verificação, ações executadas por sistema, data de resposta, conteúdo enviado e evidência de cumprimento; métricas (volume, prazo médio, atrasos) são reportadas ao encarregado.

#### PRIV-10.09 · Teste ponta a ponta de direitos
**Importante** (peso 2, origem `[A]`)  
existe teste (automatizado ou roteiro periódico) que cria um titular sintético, gera dados em todas as funcionalidades, executa acesso, correção, eliminação e revogação, e verifica o resultado em cada sistema e terceiro.

## PRIV-11. Término do tratamento, retenção e eliminação

**Como verificar:** Procure tabela/política de retenção, jobs de expurgo (cron) e seus testes, cobertura da eliminação (storage, caches, logs, backups, terceiros), política de contas inativas.

#### PRIV-11.01 · Tabela de retenção
**Crítico** (peso 3, origem `[B]`) · Fundamento: arts. 15 e 16; art. 6º, III  
cada dado/categoria tem prazo, justificativa (finalidade, obrigação legal, exercício de direitos), evento que inicia a contagem, ação no fim (eliminar, anonimizar, bloquear), exceções legais e owner. Dados não são mantidos indefinidamente “por via das dúvidas”.

#### PRIV-11.02 · Hipóteses de término
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 15  
o sistema reconhece o término do tratamento quando a finalidade é alcançada ou os dados deixam de ser necessários, quando o período acaba, quando o titular revoga/solicita (respeitado o interesse público) ou por determinação da ANPD.

#### PRIV-11.03 · Conservação autorizada
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 16  
dados mantidos após o término se enquadram em: obrigação legal/regulatória; estudo por órgão de pesquisa (com anonimização sempre que possível); transferência a terceiro respeitados os requisitos; ou uso exclusivo do controlador com dados anonimizados e vedado o acesso por terceiro. Cada exceção está registrada.

#### PRIV-11.04 · Guarda mínima obrigatória do Marco Civil
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: provedor de aplicação constituído como pessoa jurídica com fins econômicos* · Fundamento: Lei 12.965/2014, art. 15  
registros de acesso a aplicações (data, hora, IP) são guardados por 6 meses, em ambiente controlado e seguro, com sigilo — e **não** são estendidos sem justificativa; o conflito aparente entre “guardar” e “minimizar” está resolvido na tabela de retenção.

#### PRIV-11.05 · Eliminação efetiva e completa
**Crítico** (peso 3, origem `[B]`)  
eliminação, anonimização ou bloqueio alcançam produção, réplicas, caches, índices de busca, índices vetoriais/embeddings, filas e DLQs, data warehouse, logs, exports, arquivos em storage, ambientes não produtivos, backups (eliminação na expiração ou mecanismo de “não restaurar” documentado, ex.: lista de exclusões reaplicada após restore) e suboperadores.

#### PRIV-11.06 · Propagação a terceiros
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 18, § 6º  
pedidos de exclusão são propagados por API/webhook aos SaaS integrados (CRM, e-mail marketing, analytics, suporte, plataformas de anúncio), com confirmação e registro.

#### PRIV-11.07 · Jobs de retenção testados
**Importante** (peso 2, origem `[A]`)  
rotinas de expurgo são automatizadas, idempotentes, observáveis (quantos registros removidos), alertam em falha e são testadas; não dependem de execução manual.

#### PRIV-11.08 · Contas inativas
**Menor** (peso 1, origem `[M]`)  
há política para contas e dados de usuários inativos (aviso e eliminação/anonimização após período definido).

## PRIV-12. Segurança, privacy by design e privacy by default

**Como verificar:** Use o resultado do pilar Security para PRIV-12.01. Verifique template de PR com perguntas de privacidade, defaults protetivos (visibilidade, opt-ins), uso de dados reais em seeds/fixtures, mascaramento em logs.

#### PRIV-12.01 · Medidas de segurança proporcionais
**Crítico** (peso 3, origem `[B]`) · Fundamento: arts. 46, 47 e 49  
medidas técnicas e administrativas aptas a proteger dados de acessos não autorizados e de situações acidentais ou ilícitas, proporcionais ao risco — verificadas pelo pilar Security (mínimo: score de Security sem `[B]` aberto nos itens que tocam dados pessoais). Todos que intervêm no tratamento mantêm a segurança mesmo após o término (art. 47).

#### PRIV-12.02 · Privacy by design
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 46, § 2º  
privacidade é considerada desde a concepção: template de design/PR inclui perguntas de privacidade (novos dados? nova finalidade? novo terceiro? retenção?); revisão de privacidade é obrigatória para mudanças que alteram o inventário.

#### PRIV-12.03 · Privacy by default
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 6º, III; art. 46, § 2º  
configurações padrão são as mais protetivas: perfis não públicos por padrão, compartilhamentos opcionais desligados, rastreamentos opcionais desligados, retenção mínima.

#### PRIV-12.04 · Acesso interno
**Importante** (peso 2, origem `[A]`)  
acesso de colaboradores a dados pessoais é baseado em função e necessidade, com justificativa, aprovação, revisão periódica e trilha de auditoria por consulta a dados de titular identificado; acesso direto a produção é excepcional e registrado.

#### PRIV-12.05 · Ambientes não produtivos
**Importante** (peso 2, origem `[A]`)  
dev, teste, staging, demos e análises não usam dados pessoais reais, ou usam dados anonimizados/sintéticos; cópias de produção para esses ambientes passam por mascaramento irreversível automatizado.

#### PRIV-12.06 · Logs e telemetria
**Importante** (peso 2, origem `[A]`)  
logs, traces, métricas, crash reports e ferramentas de erro não contêm dados pessoais além do necessário, com mascaramento automático e retenção definida (ver SEC-6.08, PERF-2.14).

#### PRIV-12.07 · Exportações e planilhas
**Menor** (peso 1, origem `[M]`)  
exports de dados pessoais são limitados por permissão, registrados, com expiração de link e marca d'água/identificação quando apropriado; dados não circulam em planilhas e e-mails fora de sistemas controlados.

#### PRIV-12.08 · Treinamento e conscientização
**Menor** (peso 1, origem `[M]`)  
colaboradores com acesso a dados pessoais recebem treinamento periódico e registrado sobre LGPD, segurança e procedimentos internos.

## PRIV-13. Anonimização e pseudonimização

**Como verificar:** Procure onde dados são declarados "anonimizados" (ex.: exclusão de conta) e avalie se quase-identificadores permanecem; pseudônimos tratados como dados pessoais; documentação da técnica.

#### PRIV-13.01 · Critério de anonimização
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 5º, III e XI; art. 12  
dados declarados como “anonimizados” resistem à reidentificação com meios técnicos razoáveis (considerando custo, tempo, tecnologia disponível e combinação com outras bases); remoção de nome/CPF com manutenção de dados quase identificadores (CEP, data de nascimento, gênero, IDs de dispositivo) **não** é anonimização.

#### PRIV-13.02 · Pseudonimização tratada como dado pessoal
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 13, § 4º  
dados pseudonimizados (hash, tokens, IDs internos) continuam tratados como pessoais; a informação adicional que permite reverter é mantida separada, com controle de acesso.

#### PRIV-13.03 · Perfis comportamentais
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 12, § 2º  
dados usados para formar perfil comportamental de pessoa natural identificada são tratados como pessoais, mesmo que “sem nome”.

#### PRIV-13.04 · Técnica documentada
**Menor** (peso 1, origem `[M]`)  
a técnica de anonimização (agregação, k-anonimato, generalização, ruído/privacidade diferencial) e o teste de risco de reidentificação são documentados; a regulamentação da ANPD sobre anonimização e pseudonimização é acompanhada (agenda regulatória).

## PRIV-14. Decisões automatizadas, perfilamento e IA

**Como verificar:** Procure decisões automatizadas (moderação, bloqueio, antifraude, score) e uso de dados pessoais com IA. Sem decisões automatizadas relevantes, registre a busca como justificativa do N/A.

#### PRIV-14.01 · Inventário de decisões automatizadas
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 20  
estão identificadas as decisões tomadas unicamente com base em tratamento automatizado que afetam interesses do titular (crédito, preço, elegibilidade, moderação, bloqueio de conta, antifraude, recrutamento, score, perfil de consumo).

#### PRIV-14.02 · Direito de revisão
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 20, caput  
o titular pode solicitar revisão dessas decisões; o canal existe, o pedido é registrado e a revisão é efetivamente executada com análise substantiva (preferencialmente humana e com poder de alterar a decisão).

#### PRIV-14.03 · Explicabilidade
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 20, § 1º  
o controlador fornece, quando solicitado, informações claras e adequadas sobre critérios e procedimentos usados na decisão, observados segredos comercial e industrial; a explicação é gerada a partir de registro da decisão (entradas, versão do modelo/regra, fatores principais).

#### PRIV-14.04 · Auditoria de discriminação
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 20, § 2º; art. 6º, IX  
modelos e regras são avaliados quanto a vieses e efeitos discriminatórios antes da implantação e periodicamente; resultados são registrados e disponíveis para eventual auditoria da ANPD.

#### PRIV-14.05 · Dados pessoais e modelos de IA
**Importante** (peso 2, origem `[A]`) · Fundamento: arts. 6º, 7º, 11, 46  
uso de dados pessoais para treinar, ajustar ou avaliar modelos tem finalidade compatível, base legal, minimização e RIPD quando de alto risco; prompts e respostas com dados pessoais enviados a provedores têm contrato que veda treinamento pelo provedor e define retenção; modelos não expõem dados de outros titulares (ver SEC-10.04).

#### PRIV-14.06 · Opt-out de uso em IA
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: dados do usuário alimentam indexação semântica, personalização por IA ou treinamento* · Fundamento: arts. 8º, § 5º; 18, § 2º  
o usuário tem opção granular e efetiva de excluir seus dados dessas finalidades quando a base legal permite oposição/revogação; a escolha é respeitada no pipeline de ingestão e remove dados já indexados. *(Movido de AI Readiness.)*

#### PRIV-14.07 · Acompanhamento regulatório de IA
**Menor** (peso 1, origem `[M]`)  
a organização acompanha a regulamentação da ANPD sobre IA e decisões automatizadas (agenda regulatória) e a tramitação do PL 2338/2023, que ainda não está em vigor; obrigações normativas setoriais já vigentes (ex.: saúde, financeiro) são verificadas.

## PRIV-15. Compartilhamento, operadores e terceiros

**Como verificar:** Liste os terceiros que recebem dados (código, SDKs, integrações) e verifique DPA/registro de suboperadores e os campos efetivamente enviados nos payloads.

#### PRIV-15.01 · Contratos com operadores
**Crítico** (peso 3, origem `[B]`) · Fundamento: arts. 37–39, 42  
contratos (DPA) definem: instruções e finalidade, confidencialidade, medidas de segurança, subcontratação apenas com autorização, localização dos dados e transferência internacional, retorno/eliminação ao fim, auditoria e evidências, apoio ao atendimento de direitos, notificação de incidentes em prazo compatível com o prazo do controlador, cooperação com a ANPD e responsabilidades.

#### PRIV-15.02 · Due diligence de fornecedores
**Importante** (peso 2, origem `[A]`)  
fornecedores que tratam dados pessoais passam por avaliação de privacidade e segurança antes da contratação e periodicamente, proporcional ao risco; lista de suboperadores é conhecida e mudanças são notificadas.

#### PRIV-15.03 · Compartilhamento necessário e registrado
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 7º, § 5º; art. 9º, V; art. 18, VII  
cada compartilhamento interno (entre empresas do grupo) e externo tem finalidade, base legal, minimização dos campos enviados, registro e menção no aviso; não há venda ou cessão de dados fora da finalidade e da base.

#### PRIV-15.04 · Controle técnico do que sai
**Importante** (peso 2, origem `[A]`)  
integrações enviam apenas os campos contratados/necessários (verificado no payload real); SDKs e pixels de terceiros não coletam automaticamente mais do que o declarado (configurações de coleta automática revisadas).

#### PRIV-15.05 · Responsabilidade solidária
**Menor** (peso 1, origem `[M]`) · Fundamento: arts. 42–45  
a organização entende e gerencia o risco de responsabilização solidária (operador que descumpre a lei ou instruções; controladores diretamente envolvidos) e mantém evidências que sustentem excludentes (art. 43).

#### PRIV-15.06 · Quando a empresa é operadora
**Importante** (peso 2, origem `[A]`) · Condicional — *Se: SaaS B2B*  
a aplicação permite ao cliente (controlador) cumprir suas obrigações: exportar e eliminar dados dos titulares dele, configurar retenção, obter registro de suboperadores, receber notificação de incidente e auditar; a empresa não usa dados dos clientes para finalidades próprias sem base.

## PRIV-16. Transferência internacional

**Como verificar:** Identifique regiões de hospedagem (DB, storage, app, e-mail, IA) e o mecanismo de transferência documentado para cada destino fora do Brasil.

#### PRIV-16.01 · Inventário de transferências
**Crítico** (peso 3, origem `[B]`) · Fundamento: arts. 33–36; Res. 19/2024  
cada transferência é inventariada, incluindo hospedagem em nuvem fora do Brasil, acesso remoto por equipes ou suporte no exterior, provedores de SaaS, IA, e-mail e analytics estrangeiros e suboperadores. “Está na nuvem” não é exceção.

#### PRIV-16.02 · Mecanismo válido por transferência
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 33; Res. 19/2024; Res. 32/2026  
cada transferência tem mecanismo válido: decisão de adequação (a União Europeia/EEE é reconhecida como adequada pela Res. 32/2026), cláusulas-padrão contratuais da ANPD, cláusulas específicas aprovadas, normas corporativas globais ou outra hipótese do art. 33. Transferências para destinos sem adequação usam as cláusulas-padrão da ANPD **incorporadas na íntegra e sem alteração** (prazo de adequação encerrado em 23/08/2025); cláusulas de outras jurisdições sozinhas (ex.: SCCs europeias) não bastam.

#### PRIV-16.03 · Transparência sobre transferência
**Importante** (peso 2, origem `[A]`) · Fundamento: Res. 19/2024; art. 9º  
o titular é informado sobre transferências internacionais e pode obter as informações e cláusulas aplicáveis, conforme a Res. 19/2024.

#### PRIV-16.04 · Transferências ulteriores e mudanças
**Importante** (peso 2, origem `[A]`)  
transferências posteriores pelo importador estão cobertas pelas cláusulas; troca de provedor, de região de hospedagem ou novo suboperador estrangeiro dispara revisão antes da mudança.

## PRIV-17. Incidentes de segurança com dados pessoais

**Como verificar:** Procure playbook de incidente com dados pessoais, critérios de risco relevante, prazo de 3 dias úteis, registro de incidentes (5 anos), capacidade de dimensionar titulares afetados via logs.

#### PRIV-17.01 · Procedimento integrado
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 48; Res. 15/2024  
playbook integrado entre segurança, privacidade, jurídico, comunicação e operadores, com papéis, contatos, critérios de avaliação de risco ou dano relevante, preservação de evidências, contenção, investigação e mitigação.

#### PRIV-17.02 · Avaliação de risco ou dano relevante
**Importante** (peso 2, origem `[A]`) · Fundamento: Res. 15/2024  
existe critério documentado para decidir se o incidente pode gerar risco ou dano relevante (considerando dados sensíveis, de crianças/adolescentes/idosos, financeiros, de autenticação, protegidos por sigilo, volume e possibilidade de dano material ou moral), com decisão registrada.

#### PRIV-17.03 · Comunicação à ANPD e aos titulares
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 48, § 1º; Res. 15/2024  
quando houver risco ou dano relevante, o controlador comunica a ANPD **e** os titulares em até **3 dias úteis** a partir do conhecimento de que o incidente afetou dados pessoais (prazo em dobro para agentes de pequeno porte), contendo: natureza e categorias de dados e titulares afetados, medidas técnicas e de segurança utilizadas, riscos, motivos de eventual demora, medidas adotadas para reverter ou mitigar, data do incidente e contato do encarregado. A comunicação aos titulares é em linguagem simples, direta e individual quando possível. Informações complementares são enviadas no prazo regulamentar.

#### PRIV-17.04 · Registro de incidentes
**Importante** (peso 2, origem `[A]`) · Fundamento: Res. 15/2024  
**todos** os incidentes com dados pessoais (inclusive os não comunicados) são registrados com data, descrição, dados e titulares afetados, avaliação de risco, medidas e justificativa da não comunicação, mantidos por no mínimo 5 anos.

#### PRIV-17.05 · Capacidade técnica de dimensionar o incidente
**Importante** (peso 2, origem `[A]`)  
logs e trilhas permitem responder rapidamente quais titulares e quais dados foram afetados (escopo exato), evitando notificação excessiva ou insuficiente.

#### PRIV-17.06 · Operadores
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 39  
operadores e suboperadores comunicam incidentes ao controlador sem demora injustificada, em prazo contratual compatível com os 3 dias úteis, e cooperam na investigação.

#### PRIV-17.07 · Simulação
**Menor** (peso 1, origem `[M]`)  
o procedimento é exercitado periodicamente (tabletop) e o tempo para decidir e comunicar é medido.

## PRIV-18. Encarregado (DPO)

**Como verificar:** Verifique designação do encarregado, divulgação pública (nome e contato) no site/app e na política.

#### PRIV-18.01 · Designação formal
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 41; Res. 18/2024  
encarregado indicado por ato formal (pessoa natural ou jurídica, interna ou externa), com substituto para ausências; dispensa só se agente de pequeno porte elegível, que ainda assim mantém canal de comunicação com titulares (Res. 2/2022).

#### PRIV-18.02 · Divulgação
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 41, § 1º; Res. 18/2024  
identidade e contato do encarregado são divulgados publicamente, de forma clara e objetiva, em local de destaque no site/app.

#### PRIV-18.03 · Atribuições, recursos e independência
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 41, § 2º; Res. 18/2024  
o encarregado recebe reclamações e comunicações de titulares e da ANPD, orienta colaboradores, participa das decisões relevantes de privacidade, tem acesso à alta gestão, recursos e autonomia técnica; conflitos de interesse são avaliados e documentados; consegue se comunicar com clareza em português com titulares e ANPD.

## PRIV-19. RIPD e gestão de risco

**Como verificar:** Procure RIPD/DPIA, critérios de quando elaborar e a triagem de privacidade no processo de produto.

#### PRIV-19.01 · Gatilhos de RIPD
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 5º, XVII; art. 10, § 3º; art. 38; Res. 2/2022  
está definido quando o RIPD é elaborado: tratamentos de alto risco (usar como referência os critérios da Res. 2/2022 enquanto não houver regulamento específico: larga escala ou impacto significativo combinados com tecnologia inovadora, vigilância, decisão automatizada, dados sensíveis ou de crianças/adolescentes/idosos), tratamento por legítimo interesse quando solicitado, e sempre que a ANPD determinar. A regulamentação específica do RIPD ainda é tema da agenda regulatória — acompanhar.

#### PRIV-19.02 · Conteúdo do RIPD
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 38, parágrafo único  
contém, no mínimo, descrição dos tipos de dados coletados, metodologia de coleta e de garantia da segurança, e análise do controlador sobre medidas, salvaguardas e mecanismos de mitigação de risco; recomenda-se também: agentes, sistemas, operações, titulares, fontes, finalidades, bases legais, compartilhamentos, retenção, necessidade e proporcionalidade, matriz de risco (probabilidade × impacto), riscos residuais, aprovação e data de revisão.

#### PRIV-19.03 · Momento e atualização
**Importante** (peso 2, origem `[A]`)  
o RIPD é feito **antes** de iniciar o tratamento de alto risco (ou assim que identificado), revisado em mudanças relevantes e periodicamente, e está pronto para entrega à ANPD quando solicitado.

#### PRIV-19.04 · Integração ao desenvolvimento
**Menor** (peso 1, origem `[M]`)  
o processo de produto tem triagem de privacidade (questionário curto) que indica quando é necessário RIPD, para que ele não seja feito depois do lançamento.

## PRIV-20. Governança, boas práticas e accountability

**Como verificar:** Procure programa de governança, políticas internas, indicadores e auditorias periódicas registradas (inclusive execuções anteriores deste assessment).

#### PRIV-20.01 · Programa de governança em privacidade
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 50, § 2º, I  
existe programa que demonstra: comprometimento da gestão; aplicação a todo o conjunto de dados; adaptação à estrutura, escala e volume; políticas e salvaguardas baseadas em avaliação sistemática de risco; relação de confiança com o titular; integração à governança corporativa; planos de resposta a incidentes e remediação; atualização constante com monitoramento contínuo e avaliações periódicas.

#### PRIV-20.02 · Políticas internas
**Menor** (peso 1, origem `[M]`)  
políticas de privacidade interna, retenção, classificação, uso aceitável, gestão de fornecedores, resposta a incidentes e atendimento a titulares estão aprovadas, publicadas internamente e revisadas.

#### PRIV-20.03 · Indicadores
**Menor** (peso 1, origem `[M]`)  
indicadores de privacidade são acompanhados pela gestão: pedidos de titulares e prazos, incidentes, achados abertos, RIPDs pendentes, fornecedores avaliados, treinamentos concluídos.

#### PRIV-20.04 · Auditoria interna periódica
**Menor** (peso 1, origem `[M]`)  
este checklist (ou equivalente) é executado periodicamente, com resultados reportados e plano de ação; boas práticas adotadas são documentadas, pois são consideradas na dosimetria de sanções (Res. 4/2023).

## PRIV-21. Poder público *(Se: o controlador é órgão/entidade pública ou trata dados em nome do poder público)*

**Como verificar:** Aplica-se apenas a órgão público ou tratamento em nome do poder público; caso contrário, N/A com justificativa.

#### PRIV-21.01 · Finalidade pública e competência legal
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 23  
o tratamento atende à finalidade pública, na persecução do interesse público, com objetivo de executar competências legais; hipóteses e procedimentos são divulgados.

#### PRIV-21.02 · Uso compartilhado e transferência a entes privados
**Importante** (peso 2, origem `[A]`) · Fundamento: arts. 25–27  
dados são mantidos em formato interoperável; compartilhamento com entes privados segue as hipóteses legais, com informação à ANPD quando exigido e regulamentação aplicável.

#### PRIV-21.03 · Encarregado e publicidade
**Importante** (peso 2, origem `[A]`) · Fundamento: art. 23, III  
encarregado indicado e informações sobre tratamentos publicadas em veículos de fácil acesso.

## PRIV-22. Normas conexas e setoriais

**Como verificar:** Verifique guarda de registros do Marco Civil, relação de consumo (CDC) e normas setoriais aplicáveis ao produto.

#### PRIV-22.01 · Marco Civil da Internet
**Importante** (peso 2, origem `[A]`) · Fundamento: Lei 12.965/2014, arts. 7º, 10, 11, 15  
guarda de registros (ver PRIV-11.04), sigilo das comunicações, informações claras sobre coleta, uso e proteção, e jurisdição brasileira para dados coletados no Brasil.

#### PRIV-22.02 · Código de Defesa do Consumidor
**Menor** (peso 1, origem `[M]`) · Condicional — *Se: relação de consumo* · Fundamento: CDC, arts. 43 e 44  
direitos de acesso e correção de cadastros de consumidores e comunicação de abertura de cadastro são observados em conjunto com a LGPD.

#### PRIV-22.03 · Normas setoriais
**Importante** (peso 2, origem `[A]`)  
normas aplicáveis ao setor estão mapeadas e cumpridas (ex.: Banco Central para instituições financeiras e Open Finance, ANS e CFM para saúde, CVM, Cadastro Positivo, normas de telemedicina, normas trabalhistas para dados de empregados).

## PRIV-23. Fiscalização e preparação

**Como verificar:** Avalie se as evidências exigidas pela ANPD estão reunidas e recuperáveis (ROPA, avisos, consentimentos, contratos, incidentes, RIPDs).

#### PRIV-23.01 · Prontidão para fiscalização
**Importante** (peso 2, origem `[A]`) · Fundamento: arts. 52–54; Lei 15.352/2026; Res. 4/2023; Res. 30/2025  
a organização consegue responder a uma requisição da ANPD em prazo curto com: ROPA, avisos e versões, registros de consentimento, testes de legítimo interesse, RIPDs, contratos com operadores, registro de incidentes, evidências de segurança e de atendimento a titulares. Temas prioritários de fiscalização 2026–2027 recebem atenção reforçada.

#### PRIV-23.02 · Conhecimento das sanções
**Menor** (peso 1, origem `[M]`) · Fundamento: art. 52  
o mapa de risco considera as sanções possíveis (advertência; multa de até 2% do faturamento no Brasil, limitada a R$ 50 milhões por infração; multa diária; publicização; bloqueio ou eliminação dos dados; suspensão do banco de dados ou da atividade; proibição do tratamento) e o impacto de cada uma no negócio.

#### PRIV-23.03 · Reclamações e petições
**Menor** (peso 1, origem `[M]`)  
reclamações de titulares (canal próprio, consumidor.gov, Procon, ANPD) são monitoradas e tratadas como indicador de falha de processo.

## PRIV-24. Evidência de conformidade

**Como verificar:** Procure repositório de evidências versionado e matriz requisito → evidência (este relatório versionado conta como parte da evidência).

#### PRIV-24.01 · Repositório de evidências
**Crítico** (peso 3, origem `[B]`) · Fundamento: art. 6º, X; art. 50  
RIPDs, ROPA, avisos e versões, consentimentos, logs de preferências, testes de legítimo interesse, contratos, avaliações de terceiros, pedidos de titulares, registro de incidentes, treinamentos, testes técnicos e decisões de risco são versionados, datados e recuperáveis.

#### PRIV-24.02 · Matriz requisito → evidência
**Importante** (peso 2, origem `[A]`)  
cada item deste pilar mapeia para owner, sistema, evidência, frequência de verificação e status; evidências técnicas (capturas de rede, testes de eliminação, testes de consentimento) são regeneradas a cada ciclo.
