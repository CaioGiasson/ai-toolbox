# Criteria catalog — Privacy (LGPD)

> Derived from the *Senior checklist for application assessment — v3* (October 2026). This file is maintained directly in this repository. Item IDs, severities and criteria are the basis of the score and must stay stable between runs: changing an ID or a severity breaks score comparison across runs, so record any such change in the pull request. Legal references are to Brazilian law (LGPD, Law 13.709/2018) and ANPD resolutions.

**Severity (fixed per item):** `[B]` Blocking → **Critical** (weight 3) · `[A]` High → **Important** (weight 2) · `[M]` Medium and `[R]` Recommended → **Minor** (weight 1).

**Conditional items** (*If: …*): when the condition does not apply, mark **N/A with justification and evidence** (e.g., a code search with no hits). N/A without evidence counts as Non-compliant.

**Total items:** 126 — Critical: 37 · Important: 66 · Minor: 23. Maximum score (all applicable): 266.

## Pillar goal

> **Pillar goal:** identify **every** gap that keeps the application (and the operation that supports it) from complying with the LGPD and related rules, traceable to a statute article or ANPD resolution. Compliance is assessed on the **real behavior of the system** (what is actually collected, sent, stored and erased), not just on the published policy.
>
> **Assessment rules for this pillar:**
> - Each item gives its legal basis in the line below the severity. When recording a finding, cite the article.
> - A divergence between the privacy notice and the observed behavior (network capture, database, logs) is always an `[A]` finding or higher.
> - When the ANPD has not yet regulated a topic (e.g., impact report, portability), apply the law, the guidance currently in force and best practice; the item records that condition.
> - Small-scale agents (Res. CD/ANPD no. 2/2022) may have a simplified regime — mark when applicable and check whether the processing is high-risk (which removes part of the benefits).
> - Always check the version of the resolutions currently in force; the ANPD became a regulatory agency (Law 15.352/2026), has an active regulatory agenda and a map of priority inspection topics for 2026–2027 (Res. 30/2025), with a declared focus on data subject rights, sensitive data, children and adolescents, and the public sector.

## PRIV-1. Applicability, roles and scope

**How to verify:** Look for the privacy policy, terms, ROPA, documentation of roles (controller/processor) and the product's target audience. No documentation of applicability and roles = Not met.

#### PRIV-1.01 · Territorial and material applicability
**Critical** (weight 3, origin `[B]`) · Basis: arts. 3 and 4  
it is documented why the LGPD applies (processing in Brazil, offering goods/services to people in Brazil, or data collected in Brazil) and which processing is outside the scope (art. 4), with justification. Other applicable jurisdictions (e.g., GDPR for data subjects in the EU) are identified.

#### PRIV-1.02 · Roles per operation
**Critical** (weight 3, origin `[B]`) · Basis: art. 5, VI–IX; arts. 37–40  
for **each processing operation** it is defined who is controller, joint controller, processor and sub-processor, based on who decides the purpose and essential elements (not on what the contract says). Situations in which the company acts as a processor for customers (B2B SaaS) are kept separate from those in which it is a controller.

#### PRIV-1.03 · Size of the agent
**Minor** (weight 1, origin `[M]`) · Basis: Res. 2/2022  
it is assessed whether the organization qualifies as a small-scale agent and, if so, whether it performs high-risk processing (large scale or significant impact **and** use of innovative technology, surveillance, automated decisions or sensitive/children's/elderly people's data), which limits the relaxations.

#### PRIV-1.04 · Categories of data subjects
**Important** (weight 2, origin `[A]`)  
all categories of data subjects are identified (customers, customers' end users, visitors, leads, employees, candidates, representatives of legal entities, dependents, third parties mentioned in content), including indirect data subjects.

## PRIV-2. Inventory and record of operations (ROPA)

**How to verify:** Compare the data inventory (ROPA/docs) with the real schema (models and fields with personal data) and with the third parties called in the code and frontend (SDKs, pixels, APIs). A personal field or third party not in the inventory = Partial or Not met.

#### PRIV-2.01 · End-to-end data inventory
**Critical** (weight 3, origin `[B]`) · Basis: art. 37; art. 6, X  
the inventory maps each flow from collection to deletion: systems, tables/fields, integrations, regions, categories of data subjects, volume, personal and sensitive data, purpose, legal basis, sharing, retention and controls. It includes direct and indirect collection, cookies, SDKs, pixels, logs, analytics, session recording, support/CRM, backups, non-production environments, exported spreadsheets, model training/evaluation and data sent to AI providers.

#### PRIV-2.02 · Inventory verified against the real system
**Important** (weight 2, origin `[A]`)  
the inventory is checked by technical evidence: scanning schemas/databases for personal data (data discovery), capturing frontend and app traffic (which third parties receive what), reviewing log and event payloads. Personal fields not in the inventory are a finding.

#### PRIV-2.03 · Classification in the code
**Minor** (weight 1, origin `[M]`)  
fields with personal and sensitive data are annotated in the schema/models (tags, structured comments or a data catalog), allowing tests, linters, masking and deletion pipelines to locate them automatically.

#### PRIV-2.04 · Record of operations
**Important** (weight 2, origin `[A]`) · Basis: art. 37; Res. 2/2022  
an up-to-date record of processing operations exists, with an owner per purpose, especially for processing based on legitimate interest; a simplified format only for eligible small-scale agents. Product changes trigger an update (a trigger in the development process).

## PRIV-3. Principles (art. 6)

**How to verify:** Assess registration forms/APIs and events field by field: need for each piece of data, declared purposes, data subject access to their own data, correction mechanisms. Use the privacy notice as the reference for what is declared.

#### PRIV-3.01 · Good faith and purpose
**Critical** (weight 3, origin `[B]`) · Basis: art. 6, caput and I  
each processing has a legitimate, specific, explicit and informed purpose; there is no later incompatible processing (e.g., support data used for marketing, registration data used to train a model without assessment).

#### PRIV-3.02 · Adequacy
**Important** (weight 2, origin `[A]`) · Basis: art. 6, II  
the processing is compatible with the data subject's context and expectations (assessed by what the data subject reasonably expects when using the feature).

#### PRIV-3.03 · Necessity and minimization
**Critical** (weight 3, origin `[B]`) · Basis: art. 6, III  
each collected field has a justification tied to the purpose; optional fields are really optional; there is no “just in case” collection; data is truncated/aggregated when full precision is not needed (e.g., date of birth → age range; precise geolocation → city). Forms, APIs and analytics events are reviewed field by field.

#### PRIV-3.04 · Free access
**Important** (weight 2, origin `[A]`) · Basis: art. 6, IV; art. 9  
the data subject can consult, in an easy and free way, how and for how long their data is processed and the entirety of their data.

#### PRIV-3.05 · Data quality
**Minor** (weight 1, origin `[M]`) · Basis: art. 6, V  
there are mechanisms for correction and updating (by the data subject and by internal process); outdated data that drives decisions about the data subject is reviewed.

#### PRIV-3.06 · Transparency
**Important** (weight 2, origin `[A]`) · Basis: art. 6, VI  
clear, precise and accessible information about the processing and the agents, respecting trade and industrial secrets (detailed in section 9).

#### PRIV-3.07 · Security and prevention
**Important** (weight 2, origin `[A]`) · Basis: art. 6, VII and VIII  
technical and administrative measures protect against unauthorized access and accidental or unlawful situations, and prevent harm (detailed in section 12 and in the Security pillar).

#### PRIV-3.08 · Non-discrimination
**Important** (weight 2, origin `[A]`) · Basis: art. 6, IX  
there is no processing for unlawful or abusive discriminatory purposes; models, scoring rules, pricing and segmentations are assessed for discriminatory effects (including through proxy variables).

#### PRIV-3.09 · Accountability
**Critical** (weight 3, origin `[B]`) · Basis: art. 6, X  
the controller can **demonstrate**, with evidence, the adoption of effective measures and their effectiveness (see section 24).

## PRIV-4. Legal bases

**How to verify:** Look for the legal bases per purpose in the notice/ROPA and check consistency with behavior (e.g., marketing cannot be under "performance of a contract").

#### PRIV-4.01 · Legal basis per purpose
**Critical** (weight 3, origin `[B]`) · Basis: art. 7  
each purpose has **one** documented, coherent legal basis among the ten hypotheses of art. 7 (consent; legal/regulatory obligation; public policies; research; performance of a contract or preliminary procedures; regular exercise of rights; protection of life; health protection; legitimate interest; credit protection). Consent is not used when the processing would happen anyway (an incorrect basis creates a false expectation of revocation).

#### PRIV-4.02 · Rigorous use of contract performance
**Important** (weight 2, origin `[A]`) · Basis: art. 7, V  
the “contract” basis covers only what is strictly necessary to deliver the contracted service; marketing, non-essential analytics, profiling and sharing with partners are not justified by it.

#### PRIV-4.03 · Legal obligation identified
**Minor** (weight 1, origin `[M]`) · Basis: art. 7, II  
when the basis is a legal/regulatory obligation, the specific rule and the required period are cited (e.g., tax records, retention of access logs under the Marco Civil).

#### PRIV-4.04 · Public and manifestly public data
**Important** (weight 2, origin `[A]`) · Basis: art. 7, §§ 3, 4 and 7  
data obtained from public sources or made public by the data subject is processed considering the purpose, good faith and the public interest that justified its disclosure; scraping and data enrichment have their own legal basis and assessment.

#### PRIV-4.05 · Change of basis or purpose
**Important** (weight 2, origin `[A]`) · Basis: art. 9, § 2  
a change of purpose incompatible with the original consent is communicated **beforehand**, with the possibility of revocation; switching legal basis is not used to circumvent a consent revocation.

## PRIV-5. Consent

**How to verify:** Look for a consent record (model/table with version, date, channel), granular options, a revocation flow, and whether the code checks consent before using the data. If no purpose uses consent, mark the section N/A with justification.

*(If: any purpose uses consent.)*

#### PRIV-5.01 · Validity requirements
**Critical** (weight 3, origin `[B]`) · Basis: art. 5, XII; art. 8  
consent is free, informed and unambiguous, for specific purposes (generic authorizations are void), given in writing or by a means that shows the expression of will; a clause highlighted from the others when in a contract; not a condition for a service that does not depend on that processing.

#### PRIV-5.02 · Granularity
**Important** (weight 2, origin `[A]`) · Basis: art. 8, § 4  
distinct purposes have distinct options (e.g., newsletter, partner offers, personalization, analytics); there is no “accept all” as the only option.

#### PRIV-5.03 · Proof of consent
**Critical** (weight 3, origin `[B]`) · Basis: art. 8, § 2  
the burden of proof is on the controller: each consent is recorded with the data subject, purpose, version of the text presented, date/time, channel, interface/app version and evidence of the affirmative action; the record is intact and retrievable.

#### PRIV-5.04 · Revocation
**Critical** (weight 3, origin `[B]`) · Basis: art. 8, § 5; art. 18, IX  
revocation is free, easy, through the same channel as or a simpler one than the grant, and **technically effective**: the system stops processing (events stop being sent, lists are updated, third parties are notified) within a defined period verified by a test.

#### PRIV-5.05 · Enforcing consent in the code
**Important** (weight 2, origin `[A]`)  
the consent state is checked at the point of use (sending marketing e-mail, firing a pixel, using data for personalization), not only at collection; an automated test ensures that no optional tracker/event fires without consent (verification by network capture).

#### PRIV-5.06 · Defects of consent
**Important** (weight 2, origin `[A]`) · Basis: art. 8, § 3  
there is no consent obtained through error, fraud, coercion or a deceptive interface (see PRIV-9.04 on dark patterns).

## PRIV-6. Legitimate interest

**How to verify:** Look for documented balancing tests (LIA) for each purpose based on legitimate interest, and the objection channel. If legitimate interest is not used, mark N/A with justification.

*(If: any purpose uses legitimate interest.)*

#### PRIV-6.01 · Documented balancing test
**Critical** (weight 3, origin `[B]`) · Basis: art. 10; art. 7, IX; ANPD guidance on legitimate interest  
for each purpose there is a recorded assessment of: (i) a legitimate purpose and a concrete situation; (ii) necessity (only strictly necessary data, no less invasive alternative); (iii) balancing against the data subject's legitimate expectations and rights; (iv) safeguards (transparency, opt-out, minimization, security).

#### PRIV-6.02 · Prohibition for sensitive data
**Critical** (weight 3, origin `[B]`) · Basis: art. 11  
legitimate interest is **not** used as a basis for sensitive personal data.

#### PRIV-6.03 · Transparency and objection
**Important** (weight 2, origin `[A]`) · Basis: art. 10, § 2; art. 18, § 2  
the data subject is informed about processing under legitimate interest and can object through a simple channel; the objection is assessed and, when upheld, made technically effective.

#### PRIV-6.04 · Availability to the ANPD
**Minor** (weight 1, origin `[M]`) · Basis: art. 10, § 3; art. 37  
the balancing test and the record of operations are ready to be handed to the ANPD; the ANPD may require an impact report (RIPD) in these cases.

## PRIV-7. Sensitive personal data

**How to verify:** Look for sensitive data in the schema and flows (health, biometrics, origin, religion etc., including data inferred from photos/purchases) and the art. 11 basis. If there is no sensitive data, record the search as the evidence for the N/A.

#### PRIV-7.01 · Identification of sensitive data
**Critical** (weight 3, origin `[B]`) · Basis: art. 5, II  
all data on racial or ethnic origin, religious belief, political opinion, union membership or membership of a religious/philosophical/political organization, health, sex life, genetic and **biometric** data is mapped — including **inferred** data (e.g., purchases that reveal a health condition, a photo used for facial recognition).

#### PRIV-7.02 · Legal basis under art. 11
**Critical** (weight 3, origin `[B]`) · Basis: art. 11  
each sensitive processing uses a hypothesis of art. 11 (specific and highlighted consent for specific purposes, or the hypotheses that do not require consent, such as legal obligation, regular exercise of rights including in a contract, protection of life, health protection, and fraud prevention and security of the data subject in registration identification and authentication processes). Biometrics for login/anti-fraud expressly cite the hypothesis used.

#### PRIV-7.03 · Specific prohibitions
**Important** (weight 2, origin `[A]`) · Basis: art. 11, §§ 4 and 5  
health data is not communicated or shared for economic advantage outside the legal exceptions; health plan operators do not process data for risk selection.

#### PRIV-7.04 · Reinforced protection
**Important** (weight 2, origin `[A]`) · Basis: arts. 11, 46  
sensitive data has additional controls: field-level encryption, restricted and per-person audited access, exclusion from logs/analytics, segregation, minimal retention and an impact report (see SEC-6.04 and section 19).

#### PRIV-7.05 · Use in advertising and profiling
**Important** (weight 2, origin `[A]`) · Basis: arts. 6, IX; 11; Res. 30/2025  
sensitive data (including inferred) does not feed ad targeting or audiences on advertising platforms without an adequate legal basis; this is a priority ANPD inspection topic.

## PRIV-8. Children, adolescents and other vulnerable people

**How to verify:** Check the target audience, age gate, age verification, protective defaults and ECA Digital obligations. A "does not apply" conclusion requires documented justification in the repository.

#### PRIV-8.01 · Determining audience and likely access
**Critical** (weight 3, origin `[B]`) · Basis: ECA Digital (Law 15.211/2025)  
it is assessed whether the product is aimed at children/adolescents **or likely to be accessed** by them (ECA Digital concept, in force since 03/17/2026), with evidence (nature of the service, analytics, marketing audience). A “does not apply” conclusion is documented.

#### PRIV-8.02 · Best interest and legal basis
**Critical** (weight 3, origin `[B]`) · Basis: art. 14, caput; Statement CD/ANPD no. 1/2023  
processing of children's and adolescents' data observes the best interest and uses the legal hypotheses of arts. 7 or 11, with specific and highlighted consent from one of the parents or the guardian when consent is the basis for children (art. 14, § 1), and reasonable efforts to verify that consent was given by the guardian (§ 5).

#### PRIV-8.03 · Minimization in games and applications
**Important** (weight 2, origin `[A]`) · Basis: art. 14, § 4  
participation in games, applications and activities is not conditioned on providing data beyond what is strictly necessary.

#### PRIV-8.04 · Age-appropriate transparency
**Important** (weight 2, origin `[A]`) · Basis: art. 14, §§ 2 and 6  
the types of data collected, how they are used and the procedure to exercise rights are public; the information is simple, clear, accessible and suited to the child's understanding, with audiovisual resources when appropriate.

#### PRIV-8.05 · ECA Digital obligations
**Critical** (weight 3, origin `[B]`) · Conditional — *If: aimed at or likely to be accessed by minors* · Basis: Law 15.211/2025 and the implementing decrees of 03/18/2026  
verify, by type of service: a **reliable** age verification mechanism (self-declaration alone is not enough); protective settings by default (*safety by default*); parental supervision tools; a ban on profiling for advertising aimed at children and adolescents; a ban on loot boxes in games; reporting and removal channels; and other specific obligations by category (social networks, games, app stores, video platforms). The ANPD is the inspecting authority.

#### PRIV-8.06 · Proportionate, privacy-preserving age verification
**Important** (weight 2, origin `[A]`)  
the age verification method collects the minimum necessary (preferring estimation/attestation that does not retain a document or image), deletes verification data after use and does not create an unnecessary new biometric database.

#### PRIV-8.07 · Elderly people and other vulnerable groups
**Minor** (weight 1, origin `[M]`) · Basis: art. 6; Res. 2/2022  
elderly people, people with disabilities and other vulnerable groups are considered in the risk assessment, in the design of consent, in interface accessibility (WCAG) and in communication.

## PRIV-9. Transparency, privacy notice and cookies

**How to verify:** Read the privacy notice and compare it with real behavior (third parties in the code/HTML, cookies set, storage). Check the cookie banner (refusing as easy as accepting), contextual notices and notice versioning.

#### PRIV-9.01 · Minimum content of the notice
**Critical** (weight 3, origin `[B]`) · Basis: art. 9; art. 18  
the notice states: the specific purpose; how and for how long data is processed; the controller's identity and contact; the DPO's identity and contact; shared use and its purpose; the agents' responsibilities; the data subject's rights and how to exercise them; international transfer; the legal basis per purpose; retention criteria; and, when processing is a condition of the service, that fact and the means to exercise rights (art. 9, § 3).

#### PRIV-9.02 · Notice consistent with real behavior
**Critical** (weight 3, origin `[B]`)  
every third party that receives data (detected in network capture, integrations and contracts) is in the notice; every piece of data collected is in the notice; there is no undeclared collection. Differences are a finding.

#### PRIV-9.03 · Contextual and versioned notice
**Minor** (weight 1, origin `[M]`) · Basis: art. 8, § 6; art. 9  
besides the general policy, there are notices at the moment of collection (just-in-time) for non-obvious data (location, contacts, camera, biometrics); notice versions are dated and archived; relevant changes are communicated to the data subject.

#### PRIV-9.04 · No dark patterns
**Critical** (weight 3, origin `[B]`) · Basis: art. 6, I and VI; art. 8; ANPD guidance on cookies  
the consent banner/flow does not use deceptive patterns: refusing is as easy and visible as accepting (same layer, same prominence), there are no pre-checked boxes, deceptive contrast or language, fatigue by repetition (re-asking after a refusal within a short interval), unjustified “cookie wall” or interpretation of scrolling/navigation as consent.

#### PRIV-9.05 · Cookies and tracking technologies
**Important** (weight 2, origin `[A]`) · Basis: ANPD guidance on cookies  
cookies, local storage, pixels, SDKs, fingerprinting and server-side tagging are inventoried by category (necessary, performance, functional, advertising); only the strictly necessary ones operate before the choice; the choice is recorded, can be changed at any time through an always-accessible link and is also respected in server-side tagging and conversion integrations (e.g., sending hashed e-mail/phone to ad platforms remains personal data).

#### PRIV-9.06 · Session recording and behavior tools
**Important** (weight 2, origin `[A]`) · Conditional — *If: session replay, heatmaps*  
input fields, displayed personal data and sensitive screens are masked by default; the tool is in the notice, has a legal basis and short retention.

#### PRIV-9.07 · Accessibility of information
**Minor** (weight 1, origin `[M]`)  
the notice and the privacy center are accessible (screen readers, plain language, Portuguese), reachable from any page and in the app.

## PRIV-10. Data subject rights

**How to verify:** Look for endpoints/flows for access/export, correction, deletion, revocation and objection; a request log (protocol, deadlines); end-to-end tests of these flows.

#### PRIV-10.01 · Channel and identity verification
**Critical** (weight 3, origin `[B]`) · Basis: art. 18, caput and §§ 3 and 5  
there is a free, accessible, publicized channel (self-service in the account and an alternative channel for people without an account); identity verification is proportionate to the risk (does not require more data than necessary nor become a barrier); requests by legal representatives are handled.

#### PRIV-10.02 · Coverage of all art. 18 rights
**Critical** (weight 3, origin `[B]`) · Basis: art. 18, I–IX and § 2  
the process and the system serve: (I) confirmation that processing exists; (II) access; (III) correction of incomplete, inaccurate or outdated data; (IV) anonymization, blocking or deletion of unnecessary, excessive or non-compliantly processed data; (V) portability; (VI) deletion of data processed with consent (subject to art. 16); (VII) information about the entities with which data was shared; (VIII) information about the possibility of not consenting and its consequences; (IX) revocation of consent; and objection (§ 2).

#### PRIV-10.03 · Deadlines under art. 19
**Critical** (weight 3, origin `[B]`) · Basis: art. 19  
confirmation of existence or access: **immediately**, in a simplified format, or within **15 days** through a clear and complete statement (origin, absence of a record, criteria and purpose). Deadlines are measured per request, with an alert before expiry. When the action cannot be immediate, the data subject receives a reply with the reasons (art. 18, § 4). Small-scale agents: check the differentiated deadline rule in Res. 2/2022.

#### PRIV-10.04 · Reply format and full copy
**Important** (weight 2, origin `[A]`) · Basis: art. 19, §§ 1 to 3  
data is stored in a way that favors the exercise of access; the reply may be electronic or printed; when processing is based on consent or contract, the data subject can obtain a full electronic copy in a format that allows later use.

#### PRIV-10.05 · Automated compilation (DSAR)
**Important** (weight 2, origin `[A]`)  
the system generates a data subject's data export from **all** sources in the inventory (main database, satellite services, data warehouse, support/CRM tools, relevant logs, third parties) through an automated, tested process; the package does not include other data subjects' data.

#### PRIV-10.06 · Portability
**Minor** (weight 1, origin `[M]`) · Basis: art. 18, V; art. 40  
the export is structured and in an interoperable format (e.g., documented JSON/CSV); the ANPD's specific portability regulation is followed (a regulatory agenda topic).

#### PRIV-10.07 · Propagated correction
**Important** (weight 2, origin `[A]`) · Basis: art. 18, § 6  
correction, deletion, anonymization and blocking are communicated **immediately** to the agents with whom data was shared so that they repeat the procedure (except when demonstrably impossible or disproportionate, with a record).

#### PRIV-10.08 · Request log and audit
**Important** (weight 2, origin `[A]`)  
each request has a protocol, date received, verification, actions executed per system, reply date, content sent and evidence of fulfillment; metrics (volume, average time, delays) are reported to the DPO.

#### PRIV-10.09 · End-to-end rights test
**Important** (weight 2, origin `[A]`)  
a test (automated or a periodic script) creates a synthetic data subject, generates data in all features, performs access, correction, deletion and revocation, and verifies the result in each system and third party.

## PRIV-11. End of processing, retention and deletion

**How to verify:** Look for a retention table/policy, purge jobs (cron) and their tests, coverage of deletion (storage, caches, logs, backups, third parties), inactive-account policy.

#### PRIV-11.01 · Retention table
**Critical** (weight 3, origin `[B]`) · Basis: arts. 15 and 16; art. 6, III  
each data item/category has a period, justification (purpose, legal obligation, exercise of rights), the event that starts the count, the action at the end (delete, anonymize, block), legal exceptions and an owner. Data is not kept indefinitely “just in case”.

#### PRIV-11.02 · End-of-processing hypotheses
**Important** (weight 2, origin `[A]`) · Basis: art. 15  
the system recognizes the end of processing when the purpose is achieved or the data is no longer necessary, when the period ends, when the data subject revokes/requests (subject to public interest) or by ANPD determination.

#### PRIV-11.03 · Authorized retention
**Important** (weight 2, origin `[A]`) · Basis: art. 16  
data kept after the end of processing falls under: legal/regulatory obligation; study by a research body (anonymized whenever possible); transfer to a third party subject to the requirements; or exclusive use by the controller with anonymized data and no third-party access. Each exception is recorded.

#### PRIV-11.04 · Minimum mandatory retention under the Marco Civil
**Important** (weight 2, origin `[A]`) · Conditional — *If: application provider incorporated as a for-profit legal entity* · Basis: Law 12.965/2014, art. 15  
application access logs (date, time, IP) are kept for 6 months, in a controlled and secure environment, with confidentiality — and are **not** extended without justification; the apparent conflict between “keep” and “minimize” is resolved in the retention table.

#### PRIV-11.05 · Effective and complete deletion
**Critical** (weight 3, origin `[B]`)  
deletion, anonymization or blocking reach production, replicas, caches, search indexes, vector indexes/embeddings, queues and DLQs, the data warehouse, logs, exports, files in storage, non-production environments, backups (deletion on expiry or a documented “do not restore” mechanism, e.g., an exclusion list reapplied after restore) and sub-processors.

#### PRIV-11.06 · Propagation to third parties
**Important** (weight 2, origin `[A]`) · Basis: art. 18, § 6  
deletion requests are propagated by API/webhook to integrated SaaS (CRM, e-mail marketing, analytics, support, ad platforms), with confirmation and a record.

#### PRIV-11.07 · Tested retention jobs
**Important** (weight 2, origin `[A]`)  
purge routines are automated, idempotent, observable (how many records removed), alert on failure and are tested; they do not depend on manual execution.

#### PRIV-11.08 · Inactive accounts
**Minor** (weight 1, origin `[M]`)  
there is a policy for inactive users' accounts and data (notice and deletion/anonymization after a defined period).

## PRIV-12. Security, privacy by design and privacy by default

**How to verify:** Use the Security pillar's result for PRIV-12.01. Check for a PR template with privacy questions, protective defaults (visibility, opt-ins), use of real data in seeds/fixtures, masking in logs.

#### PRIV-12.01 · Proportionate security measures
**Critical** (weight 3, origin `[B]`) · Basis: arts. 46, 47 and 49  
technical and administrative measures able to protect data from unauthorized access and from accidental or unlawful situations, proportionate to the risk — verified by the Security pillar (minimum: a Security score with no open `[B]` on the items that touch personal data). Everyone involved in processing maintains security even after it ends (art. 47).

#### PRIV-12.02 · Privacy by design
**Important** (weight 2, origin `[A]`) · Basis: art. 46, § 2  
privacy is considered from the design stage: the design/PR template includes privacy questions (new data? new purpose? new third party? retention?); privacy review is mandatory for changes that alter the inventory.

#### PRIV-12.03 · Privacy by default
**Important** (weight 2, origin `[A]`) · Basis: art. 6, III; art. 46, § 2  
default settings are the most protective: profiles not public by default, optional sharing off, optional tracking off, minimal retention.

#### PRIV-12.04 · Internal access
**Important** (weight 2, origin `[A]`)  
employee access to personal data is based on role and need, with justification, approval, periodic review and an audit trail for each query of an identified data subject's data; direct production access is exceptional and recorded.

#### PRIV-12.05 · Non-production environments
**Important** (weight 2, origin `[A]`)  
dev, test, staging, demos and analyses do not use real personal data, or use anonymized/synthetic data; production copies to these environments go through automated, irreversible masking.

#### PRIV-12.06 · Logs and telemetry
**Important** (weight 2, origin `[A]`)  
logs, traces, metrics, crash reports and error tools contain no personal data beyond what is necessary, with automatic masking and defined retention (see SEC-6.08, PERF-2.14).

#### PRIV-12.07 · Exports and spreadsheets
**Minor** (weight 1, origin `[M]`)  
exports of personal data are limited by permission, logged, with link expiry and watermark/identification when appropriate; data does not circulate in spreadsheets and e-mails outside controlled systems.

#### PRIV-12.08 · Training and awareness
**Minor** (weight 1, origin `[M]`)  
employees with access to personal data receive periodic, recorded training on the LGPD, security and internal procedures.

## PRIV-13. Anonymization and pseudonymization

**How to verify:** Look for where data is declared "anonymized" (e.g., account deletion) and assess whether quasi-identifiers remain; pseudonyms treated as personal data; documentation of the technique.

#### PRIV-13.01 · Anonymization criterion
**Important** (weight 2, origin `[A]`) · Basis: art. 5, III and XI; art. 12  
data declared “anonymized” resists re-identification by reasonable technical means (considering cost, time, available technology and combination with other databases); removing name/CPF while keeping quasi-identifying data (postal code, date of birth, gender, device IDs) is **not** anonymization.

#### PRIV-13.02 · Pseudonymization treated as personal data
**Important** (weight 2, origin `[A]`) · Basis: art. 13, § 4  
pseudonymized data (hashes, tokens, internal IDs) continues to be treated as personal; the additional information that allows reversal is kept separate, with access control.

#### PRIV-13.03 · Behavioral profiles
**Important** (weight 2, origin `[A]`) · Basis: art. 12, § 2  
data used to build a behavioral profile of an identified natural person is treated as personal, even if “nameless”.

#### PRIV-13.04 · Documented technique
**Minor** (weight 1, origin `[M]`)  
the anonymization technique (aggregation, k-anonymity, generalization, noise/differential privacy) and the re-identification risk test are documented; the ANPD's regulation on anonymization and pseudonymization is followed (regulatory agenda).

## PRIV-14. Automated decisions, profiling and AI

**How to verify:** Look for automated decisions (moderation, blocking, anti-fraud, scoring) and the use of personal data with AI. If there are no relevant automated decisions, record the search as the justification for the N/A.

#### PRIV-14.01 · Inventory of automated decisions
**Critical** (weight 3, origin `[B]`) · Basis: art. 20  
decisions made solely on the basis of automated processing that affect the data subject's interests (credit, price, eligibility, moderation, account blocking, anti-fraud, recruitment, scoring, consumption profile) are identified.

#### PRIV-14.02 · Right to review
**Critical** (weight 3, origin `[B]`) · Basis: art. 20, caput  
the data subject can request a review of these decisions; the channel exists, the request is recorded and the review is actually carried out with substantive analysis (preferably human and with power to change the decision).

#### PRIV-14.03 · Explainability
**Important** (weight 2, origin `[A]`) · Basis: art. 20, § 1  
the controller provides, on request, clear and adequate information about the criteria and procedures used in the decision, respecting trade and industrial secrets; the explanation is generated from a record of the decision (inputs, model/rule version, main factors).

#### PRIV-14.04 · Discrimination audit
**Important** (weight 2, origin `[A]`) · Basis: art. 20, § 2; art. 6, IX  
models and rules are assessed for bias and discriminatory effects before deployment and periodically; results are recorded and available for a possible ANPD audit.

#### PRIV-14.05 · Personal data and AI models
**Important** (weight 2, origin `[A]`) · Basis: arts. 6, 7, 11, 46  
use of personal data to train, tune or evaluate models has a compatible purpose, a legal basis, minimization and an impact report when high-risk; prompts and responses with personal data sent to providers are covered by a contract that forbids training by the provider and defines retention; models do not expose other data subjects' data (see SEC-10.04).

#### PRIV-14.06 · Opt-out of use in AI
**Important** (weight 2, origin `[A]`) · Conditional — *If: user data feeds semantic indexing, AI personalization or training* · Basis: arts. 8, § 5; 18, § 2  
the user has a granular, effective option to exclude their data from these purposes when the legal basis allows objection/revocation; the choice is respected in the ingestion pipeline and removes data already indexed. *(Moved from AI Readiness.)*

#### PRIV-14.07 · Regulatory follow-up on AI
**Minor** (weight 1, origin `[M]`)  
the organization follows the ANPD's regulation on AI and automated decisions (regulatory agenda) and the progress of Bill 2338/2023, which is not yet in force; sectoral regulatory obligations already in force (e.g., health, financial) are checked.

## PRIV-15. Sharing, processors and third parties

**How to verify:** List the third parties that receive data (code, SDKs, integrations) and check the DPA/sub-processor record and the fields actually sent in payloads.

#### PRIV-15.01 · Contracts with processors
**Critical** (weight 3, origin `[B]`) · Basis: arts. 37–39, 42  
contracts (DPA) define: instructions and purpose, confidentiality, security measures, subcontracting only with authorization, data location and international transfer, return/deletion at the end, audit and evidence, support for fulfilling rights, incident notification within a period compatible with the controller's deadline, cooperation with the ANPD and responsibilities.

#### PRIV-15.02 · Supplier due diligence
**Important** (weight 2, origin `[A]`)  
suppliers that process personal data go through a privacy and security assessment before hiring and periodically, proportionate to risk; the list of sub-processors is known and changes are notified.

#### PRIV-15.03 · Necessary, recorded sharing
**Important** (weight 2, origin `[A]`) · Basis: art. 7, § 5; art. 9, V; art. 18, VII  
each internal (between group companies) and external sharing has a purpose, legal basis, minimization of the fields sent, a record and a mention in the notice; there is no sale or transfer of data outside the purpose and basis.

#### PRIV-15.04 · Technical control of what leaves
**Important** (weight 2, origin `[A]`)  
integrations send only the contracted/necessary fields (verified in the real payload); third-party SDKs and pixels do not automatically collect more than declared (automatic collection settings reviewed).

#### PRIV-15.05 · Joint liability
**Minor** (weight 1, origin `[M]`) · Basis: arts. 42–45  
the organization understands and manages the risk of joint liability (a processor that breaches the law or instructions; directly involved controllers) and keeps evidence that supports exclusions (art. 43).

#### PRIV-15.06 · When the company is the processor
**Important** (weight 2, origin `[A]`) · Conditional — *If: B2B SaaS*  
the application lets the customer (controller) fulfill its obligations: export and delete its own data subjects' data, configure retention, obtain the sub-processor record, receive incident notification and audit; the company does not use customers' data for its own purposes without a basis.

## PRIV-16. International transfer

**How to verify:** Identify hosting regions (DB, storage, app, e-mail, AI) and the documented transfer mechanism for each destination outside Brazil.

#### PRIV-16.01 · Inventory of transfers
**Critical** (weight 3, origin `[B]`) · Basis: arts. 33–36; Res. 19/2024  
each transfer is inventoried, including cloud hosting outside Brazil, remote access by teams or support abroad, foreign SaaS, AI, e-mail and analytics providers and sub-processors. “It's in the cloud” is not an exception.

#### PRIV-16.02 · Valid mechanism per transfer
**Critical** (weight 3, origin `[B]`) · Basis: art. 33; Res. 19/2024; Res. 32/2026  
each transfer has a valid mechanism: an adequacy decision (the European Union/EEA is recognized as adequate by Res. 32/2026), ANPD standard contractual clauses, approved specific clauses, binding corporate rules or another hypothesis of art. 33. Transfers to destinations without adequacy use the ANPD standard clauses **incorporated in full and unaltered** (the adaptation period ended on 08/23/2025); clauses from other jurisdictions alone (e.g., European SCCs) are not enough.

#### PRIV-16.03 · Transparency about transfer
**Important** (weight 2, origin `[A]`) · Basis: Res. 19/2024; art. 9  
the data subject is informed about international transfers and can obtain the applicable information and clauses, per Res. 19/2024.

#### PRIV-16.04 · Onward transfers and changes
**Important** (weight 2, origin `[A]`)  
later transfers by the importer are covered by the clauses; changing provider, hosting region or adding a new foreign sub-processor triggers a review before the change.

## PRIV-17. Security incidents involving personal data

**How to verify:** Look for an incident playbook for personal data, criteria for relevant risk, the 3-business-day deadline, an incident register (5 years), the ability to size the affected data subjects through logs.

#### PRIV-17.01 · Integrated procedure
**Critical** (weight 3, origin `[B]`) · Basis: art. 48; Res. 15/2024  
a playbook integrated across security, privacy, legal, communications and processors, with roles, contacts, criteria for assessing relevant risk or harm, evidence preservation, containment, investigation and mitigation.

#### PRIV-17.02 · Assessment of relevant risk or harm
**Important** (weight 2, origin `[A]`) · Basis: Res. 15/2024  
a documented criterion exists to decide whether the incident may cause relevant risk or harm (considering sensitive data, children's/adolescents'/elderly people's data, financial, authentication or confidential data, volume and the possibility of material or moral damage), with the decision recorded.

#### PRIV-17.03 · Communication to the ANPD and data subjects
**Critical** (weight 3, origin `[B]`) · Basis: art. 48, § 1; Res. 15/2024  
when there is relevant risk or harm, the controller notifies the ANPD **and** the data subjects within **3 business days** of learning that the incident affected personal data (double period for small-scale agents), including: the nature and categories of data and data subjects affected, the technical and security measures used, the risks, reasons for any delay, measures taken to reverse or mitigate, the date of the incident and the DPO's contact. Communication to data subjects is in simple, direct language and individual where possible. Complementary information is sent within the regulatory period.

#### PRIV-17.04 · Incident register
**Important** (weight 2, origin `[A]`) · Basis: Res. 15/2024  
**all** incidents involving personal data (including those not notified) are recorded with date, description, data and data subjects affected, risk assessment, measures and the reason for not notifying, kept for at least 5 years.

#### PRIV-17.05 · Technical ability to size the incident
**Important** (weight 2, origin `[A]`)  
logs and trails make it possible to quickly answer which data subjects and which data were affected (exact scope), avoiding excessive or insufficient notification.

#### PRIV-17.06 · Processors
**Important** (weight 2, origin `[A]`) · Basis: art. 39  
processors and sub-processors report incidents to the controller without unjustified delay, within a contractual period compatible with the 3 business days, and cooperate in the investigation.

#### PRIV-17.07 · Simulation
**Minor** (weight 1, origin `[M]`)  
the procedure is exercised periodically (tabletop) and the time to decide and notify is measured.

## PRIV-18. Data Protection Officer (DPO)

**How to verify:** Check the DPO's designation and public disclosure (name and contact) on the site/app and in the policy.

#### PRIV-18.01 · Formal designation
**Critical** (weight 3, origin `[B]`) · Basis: art. 41; Res. 18/2024  
a DPO appointed by a formal act (natural or legal person, internal or external), with a substitute for absences; exemption only for an eligible small-scale agent, which still maintains a communication channel with data subjects (Res. 2/2022).

#### PRIV-18.02 · Disclosure
**Important** (weight 2, origin `[A]`) · Basis: art. 41, § 1; Res. 18/2024  
the DPO's identity and contact are publicly disclosed, clearly and objectively, in a prominent place on the site/app.

#### PRIV-18.03 · Duties, resources and independence
**Important** (weight 2, origin `[A]`) · Basis: art. 41, § 2; Res. 18/2024  
the DPO receives complaints and communications from data subjects and the ANPD, advises employees, takes part in relevant privacy decisions, has access to senior management, resources and technical autonomy; conflicts of interest are assessed and documented; the DPO can communicate clearly in Portuguese with data subjects and the ANPD.

## PRIV-19. Impact report (RIPD) and risk management

**How to verify:** Look for the RIPD/DPIA, the criteria for when to prepare one, and the privacy triage in the product process.

#### PRIV-19.01 · RIPD triggers
**Critical** (weight 3, origin `[B]`) · Basis: art. 5, XVII; art. 10, § 3; art. 38; Res. 2/2022  
it is defined when the RIPD is prepared: high-risk processing (use the Res. 2/2022 criteria as a reference until a specific regulation exists: large scale or significant impact combined with innovative technology, surveillance, automated decisions, sensitive data or children's/adolescents'/elderly people's data), processing under legitimate interest when requested, and whenever the ANPD determines. The specific RIPD regulation is still a regulatory agenda topic — follow it.

#### PRIV-19.02 · RIPD content
**Important** (weight 2, origin `[A]`) · Basis: art. 38, sole paragraph  
contains, at a minimum, a description of the types of data collected, the methodology for collection and for ensuring security, and the controller's analysis of measures, safeguards and risk mitigation mechanisms; it is also recommended to include: agents, systems, operations, data subjects, sources, purposes, legal bases, sharing, retention, necessity and proportionality, a risk matrix (probability × impact), residual risks, approval and review date.

#### PRIV-19.03 · Timing and updating
**Important** (weight 2, origin `[A]`)  
the RIPD is done **before** high-risk processing starts (or as soon as it is identified), reviewed on relevant changes and periodically, and is ready to be handed to the ANPD when requested.

#### PRIV-19.04 · Integration into development
**Minor** (weight 1, origin `[M]`)  
the product process has a privacy triage (a short questionnaire) that indicates when a RIPD is needed, so that it is not done after launch.

## PRIV-20. Governance, good practices and accountability

**How to verify:** Look for a governance program, internal policies, indicators and recorded periodic audits (including previous runs of this assessment).

#### PRIV-20.01 · Privacy governance program
**Important** (weight 2, origin `[A]`) · Basis: art. 50, § 2, I  
a program exists that demonstrates: management commitment; application to the whole set of data; adaptation to structure, scale and volume; policies and safeguards based on systematic risk assessment; a relationship of trust with the data subject; integration into corporate governance; incident response and remediation plans; constant updating with continuous monitoring and periodic assessments.

#### PRIV-20.02 · Internal policies
**Minor** (weight 1, origin `[M]`)  
internal privacy, retention, classification, acceptable use, supplier management, incident response and data subject service policies are approved, published internally and reviewed.

#### PRIV-20.03 · Indicators
**Minor** (weight 1, origin `[M]`)  
privacy indicators are followed by management: data subject requests and deadlines, incidents, open findings, pending RIPDs, suppliers assessed, training completed.

#### PRIV-20.04 · Periodic internal audit
**Minor** (weight 1, origin `[M]`)  
this checklist (or an equivalent) is run periodically, with results reported and an action plan; good practices adopted are documented, as they are considered when setting sanctions (Res. 4/2023).

## PRIV-21. Public sector *(If: the controller is a public body/entity or processes data on behalf of the public sector)*

**How to verify:** Applies only to a public body or processing on behalf of the public sector; otherwise, N/A with justification.

#### PRIV-21.01 · Public purpose and legal competence
**Critical** (weight 3, origin `[B]`) · Basis: art. 23  
the processing serves a public purpose, in pursuit of the public interest, with the goal of carrying out legal competences; hypotheses and procedures are disclosed.

#### PRIV-21.02 · Shared use and transfer to private entities
**Important** (weight 2, origin `[A]`) · Basis: arts. 25–27  
data is kept in an interoperable format; sharing with private entities follows the legal hypotheses, with notice to the ANPD when required and applicable regulation.

#### PRIV-21.03 · DPO and publicity
**Important** (weight 2, origin `[A]`) · Basis: art. 23, III  
a DPO is appointed and information about processing is published in easily accessible channels.

## PRIV-22. Related and sectoral rules

**How to verify:** Check the Marco Civil record retention, the consumer relationship (CDC) and sectoral rules applicable to the product.

#### PRIV-22.01 · Marco Civil da Internet
**Important** (weight 2, origin `[A]`) · Basis: Law 12.965/2014, arts. 7, 10, 11, 15  
record retention (see PRIV-11.04), confidentiality of communications, clear information on collection, use and protection, and Brazilian jurisdiction for data collected in Brazil.

#### PRIV-22.02 · Consumer Defense Code
**Minor** (weight 1, origin `[M]`) · Conditional — *If: consumer relationship* · Basis: CDC, arts. 43 and 44  
consumers' rights of access to and correction of their records, and notice of the opening of a record, are observed together with the LGPD.

#### PRIV-22.03 · Sectoral rules
**Important** (weight 2, origin `[A]`)  
rules applicable to the sector are mapped and met (e.g., Central Bank for financial institutions and Open Finance, ANS and CFM for health, CVM, Positive Credit Registry, telemedicine rules, labor rules for employee data).

## PRIV-23. Inspection and preparedness

**How to verify:** Assess whether the evidence required by the ANPD is gathered and retrievable (ROPA, notices, consents, contracts, incidents, RIPDs).

#### PRIV-23.01 · Inspection readiness
**Important** (weight 2, origin `[A]`) · Basis: arts. 52–54; Law 15.352/2026; Res. 4/2023; Res. 30/2025  
the organization can answer an ANPD request in a short time with: ROPA, notices and versions, consent records, legitimate interest tests, RIPDs, contracts with processors, the incident register, security evidence and evidence of serving data subjects. Priority 2026–2027 inspection topics receive reinforced attention.

#### PRIV-23.02 · Knowledge of sanctions
**Minor** (weight 1, origin `[M]`) · Basis: art. 52  
the risk map considers the possible sanctions (warning; fine of up to 2% of revenue in Brazil, capped at R$ 50 million per infraction; daily fine; publicization; blocking or deletion of the data; suspension of the database or the activity; prohibition of processing) and the impact of each on the business.

#### PRIV-23.03 · Complaints and petitions
**Minor** (weight 1, origin `[M]`)  
complaints from data subjects (own channel, consumidor.gov, Procon, ANPD) are monitored and treated as an indicator of process failure.

## PRIV-24. Evidence of compliance

**How to verify:** Look for a versioned evidence repository and a requirement → evidence matrix (this versioned report counts as part of the evidence).

#### PRIV-24.01 · Evidence repository
**Critical** (weight 3, origin `[B]`) · Basis: art. 6, X; art. 50  
RIPDs, ROPA, notices and versions, consents, preference logs, legitimate interest tests, contracts, third-party assessments, data subject requests, the incident register, training, technical tests and risk decisions are versioned, dated and retrievable.

#### PRIV-24.02 · Requirement → evidence matrix
**Important** (weight 2, origin `[A]`)  
each item of this pillar maps to an owner, system, evidence, verification frequency and status; technical evidence (network captures, deletion tests, consent tests) is regenerated every cycle.
