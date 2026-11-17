---
id: law-government.platform-and-community-governance.platform-regulatory-response.legal-removal-requests-and-transparency-reporting
name: legal-removal-requests-and-transparency-reporting
category: law-government
field: platform-and-community-governance
product: platform-regulatory-response
tags: [platform-regulatory-response, platform-and-community-governance, platform-regulation, online-safety-regulation, digital-services-act, dsa, online-safety-act, osa, ofcom, vlop, very-large-online-platform, systemic-risk-assessment, independent-audit, transparency-report, transparency-reporting, dsa-transparency-database, legal-removal-requests, government-takedown-requests, court-orders, geo-blocking, country-withholding, dmca-takedown, notice-and-action, trusted-flaggers, lumen-database, regulator-information-request, compliance-function, risk-register, gni-principles]
level: advanced
status: draft
description: "Meet platform-regulation demands: triage legal and government removal requests, geo-restrict lawfully, keep records, publish transparency reports and run systemic-risk assessments and audits."
sources: ["EU Digital Services Act (Regulation (EU) 2022/2065)", "UK Online Safety Act 2023 and Ofcom codes and guidance", "US DMCA section 512 notice-and-takedown", "Global Network Initiative Principles on Freedom of Expression and Privacy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Legal removal requests and transparency reporting

**Goal:** handle demands from courts, governments, regulators and rights-holders lawfully
and consistently, protect users against overbroad requests, and produce the transparency
reports and risk assessments regulators now expect. Reference regimes: EU Digital
Services Act (DSA), UK Online Safety Act (OSA, enforced by Ofcom), US DMCA
notice-and-takedown. Obligations scale with service type and size (e.g. extra DSA duties
for very large online platforms and search engines above the EU user threshold), and
secondary rules and codes keep changing — maintain a live obligations register.

## 1. Build an obligations register
For each market: applicable laws, which services are in scope, designated status,
deadlines (removal, reporting, notification), required contact points or legal
representative, and the responsible owner internally. Review quarterly.

## 2. Triage legal removal requests
1. **Log** every request with a unique ID: requester, legal basis cited, jurisdiction,
   content/accounts targeted, deadline.
2. **Validate:** is the requester authorised (court, competent authority, verified
   rights-holder)? Is the order properly formed (DSA orders must contain specified
   elements)? Is the legal basis stated?
3. **Assess:**
   - Does the content also violate our global policies? If yes, enforce globally under policy.
   - If not, is it unlawful in the requesting jurisdiction? If yes, restrict **only in that
     jurisdiction** (geo-blocking / country withholding).
   - Is the request overbroad, politically motivated or inconsistent with international
     human-rights standards? Escalate to legal and human-rights review; consider narrowing,
     seeking clarification or challenging it.
4. **Act** within the legal deadline; notify the affected user of the action and the
   reason unless legally prohibited (e.g. gag order).
5. **Respond** to the requester with the action taken; DSA orders require informing the
   authority of the effect given.
Keep a separate workflow for copyright notices (DMCA-style: notice, takedown, counter-notice,
restoration window) and for law-enforcement data requests.

## 3. Handle regulator information requests and audits
- One coordinating owner per regulator; a request log with deadlines.
- Answer accurately and completely; misleading a regulator is often a separate offence.
- Prepare document productions with legal privilege review.
- For DSA VLOP/VLOSE independent audits: maintain evidence of compliance per obligation,
  give auditors access, and track implementation of audit recommendations.

## 4. Systemic-risk assessment (where required)
DSA VLOPs and OSA-regulated services must assess risks such as illegal content, harms to
children, effects on fundamental rights and civic discourse. A workable method:
1. Inventory features and systems (recommendation, ads, search, messaging, live).
2. For each risk, rate likelihood and severity with evidence (incident data, research,
   external consultation).
3. Document existing mitigations and their measured effectiveness.
4. Plan additional mitigations with owners and dates.
5. Sign-off by senior management/board as required; repeat on schedule and before
   launching features likely to change the risk profile.

## 5. Transparency reporting
- Decide metrics up front and instrument systems so they are reproducible: notices
  received by type, government and court orders by country, actions taken by policy,
  automated vs human decisions, appeal volumes and outcomes, median handling times,
  moderator resources by language (a DSA requirement for VLOPs).
- Follow mandated templates and periods where they exist (the EU has introduced
  harmonised templates — check the current implementing rules) and submit statements of
  reasons to the EU DSA Transparency Database where required.
- Publish definitions and methodology; footnote changes in counting from previous periods.
- Reconcile numbers across reports; regulators and researchers compare them.

## Gotchas
- Removing globally for a local legal request, silencing lawful speech elsewhere.
- Missing statutory deadlines because requests arrive via general support channels.
- Transparency numbers that cannot be reproduced from logs.
- Risk assessments written after launch rather than before.

## Verify
- [ ] Obligations register current per market, with owners and deadlines.
- [ ] Every legal request logged, validated, assessed (policy vs local law) and answered on time.
- [ ] Users notified of restrictions unless legally barred; geo-restriction used for local-only illegality.
- [ ] Systemic-risk assessment documented with mitigations and sign-off where required.
- [ ] Transparency report metrics reproducible, methodology published, mandatory templates met.
