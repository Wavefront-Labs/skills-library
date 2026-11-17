---
id: computing-software.ai-ml-engineering.llm-application-engineering.eu-ai-act-risk-classification-and-obligations
name: eu-ai-act-risk-classification-and-obligations
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, ai-risk-management, eu-ai-act, high-risk-ai, transparency-obligations, gpai, ai-compliance]
level: practitioner
status: docs-checked
description: "Map an AI system to EU AI Act categories (prohibited, high-risk, transparency, GPAI), provider vs deployer duties, key articles, and the engineering evidence needed."
sources:
  - https://eur-lex.europa.eu/eli/reg/2024/1689/oj
  - https://artificialintelligenceact.eu/article/5/
  - https://artificialintelligenceact.eu/article/6/
  - https://artificialintelligenceact.eu/article/50/
  - https://artificialintelligenceact.eu/high-level-summary/
  - https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EU AI Act: risk classification and obligations

**Goal:** know which obligations apply to your AI system and what the engineering team must produce. (This is an engineering orientation, not legal advice; confirm with counsel, and check the current timeline - implementation dates have been subject to amendment proposals.)

## Classify
1. **Prohibited practices (Art. 5):** e.g. manipulative techniques causing significant harm, exploiting vulnerabilities, social scoring, certain biometric categorisation and real-time remote biometric identification uses, emotion recognition in workplaces/schools (with exceptions). Most prohibitions have applied since 2 February 2025.
2. **High-risk (Art. 6, Annex I and III):** safety components of products under Annex I laws that need third-party conformity assessment, and Annex III areas such as biometrics, critical infrastructure, education (admissions, grading), employment (recruiting, promotion, termination), access to essential services (credit scoring, benefits, insurance pricing for life/health), law enforcement, migration, justice. Annex III systems can be exempt in narrow cases (e.g. narrow procedural or preparatory tasks, Art. 6(3)), but never if they profile individuals; a provider who concludes its Annex III system is not high-risk must document that assessment before placing it on the market.
3. **Transparency obligations (Art. 50):** inform people they are interacting with an AI system unless obvious; providers mark synthetic audio/image/video/text outputs in machine-readable form; deployers disclose deepfakes and AI text published to inform the public. Applies from 2 August 2026 per the Article 50 text, with a grace period for Art. 50(2) for systems already on the market (see the summary page).
4. **General-purpose AI models (Chapter V):** obligations for GPAI model providers (technical documentation, information for downstream providers, a Copyright Directive compliance policy, a published training-content summary; extra duties for systemic-risk models: evaluations, risk mitigation, serious-incident reporting, cybersecurity). These applied from 2 August 2025.
5. Everything else: minimal risk (voluntary codes).

## Roles
**Provider** (develops the system to place on the market or put into service) carries most high-risk duties; **deployer** (uses it in a professional capacity) has some duties, fewer than providers. Check the Act's text for each role's exact duties.

## High-risk provider obligations (Arts. 8-21) -> engineering evidence
- Risk management system across the lifecycle -> risk register, impact assessments, TEVV plans.
- Data governance: relevant, representative datasets -> dataset documentation, bias examination, data quality checks.
- Technical documentation -> model cards, architecture, evaluation reports.
- Record-keeping/logging -> automatic event logs over the system's lifetime.
- Instructions for use to deployers -> instructions for use, limitations, performance.
- Human oversight by design -> UI and process design allowing intervention/override.
- Accuracy, robustness, cybersecurity -> metrics, adversarial testing, security controls.
- Quality management system, conformity assessment with EU declaration of conformity and CE marking, registration in the EU database, accessibility.

## Verify
- [ ] Classification and role (provider/deployer) documented per AI system with reasoning.
- [ ] Transparency notices implemented where Art. 50 applies.
- [ ] For high-risk systems, an evidence map from each article to existing artifacts, with gaps assigned.

## Checked
2026-11-01. Confirmed against the text of Articles 5, 6 and 50 (artificialintelligenceact.eu) and its high-level summary (updated 31 August 2026): prohibition examples, Annex III areas, Art. 6(3) exemption and profiling carve-out, Arts. 8-21 provider duties, GPAI obligations, dates. Removed: per-article numbers for Arts. 9-15 and Annex IV, deployer duty list, substantial-modification role claims. eur-lex.europa.eu returned no readable text.
Method: documentation only; no commands were run.
