---
id: computing-software.ai-ml-engineering.llm-application-engineering.nist-ai-rmf-govern-function
name: nist-ai-rmf-govern-function
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, ai-governance-policy, nist-ai-rmf, govern-function, ai-risk-management, accountability]
level: practitioner
status: docs-checked
description: "Implement the NIST AI RMF GOVERN function: AI policies, roles and accountability, risk tolerance, inventory, workforce training, third-party oversight and feedback channels."
sources:
  - https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf
  - https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
  - https://airc.nist.gov/airmf-resources/playbook/govern/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NIST AI RMF GOVERN: policies, roles and accountability

GOVERN is the cross-cutting function enabling MAP, MEASURE and MANAGE. Its categories (GOVERN 1-6) translate into concrete artifacts.

## Categories to artifacts
| Category | What it asks | Artifacts |
|---|---|---|
| GOVERN 1 | policies, processes and practices for mapping, measuring and managing AI risk are in place and transparent | AI policy, acceptable-use policy, risk tolerance statement, AI system inventory, lifecycle procedures (review gates) |
| GOVERN 2 | accountability structures; roles and training | RACI per AI system, named owners, AI risk committee charter, training curriculum |
| GOVERN 3 | workforce diversity, equity, inclusion and accessibility processes prioritised; roles for human-AI configurations and oversight (3.2) | diverse review panels, documented oversight roles |
| GOVERN 4 | culture that considers and communicates AI risk: critical-thinking, safety-first mindset; documented impacts; practices for AI testing, incident identification and information sharing (4.3) | red-team program, incident sharing practice, documentation of impacts |
| GOVERN 5 | robust engagement with relevant AI actors; collect and integrate feedback from those external to the team | user feedback channels, appeal processes, external review |
| GOVERN 6 | AI risks and benefits from third-party software and data and other supply chain issues; contingency for third-party failures (6.2) | vendor assessment questionnaires, contract clauses, model provider monitoring |

## Minimum viable program
1. Inventory every AI system (including vendor and LLM-API features) with owner and risk tier.
2. Policy defining prohibited uses, approval requirements by tier, and documentation needed (model/system cards, impact assessment).
3. Review gate before launch for medium/high tiers: impact assessment (MAP), evaluation evidence (MEASURE), monitoring and incident plan (MANAGE).
4. Training for builders and approvers (GOVERN 2.2); set a refresh cadence.
5. Incident reporting channel and periodic review of the policy.

## Verify
- [ ] Audit sample: a launched AI feature has inventory entry, tier, owner, approvals and linked assessments.

## Checked
2026-11-01. Confirmed against NIST AI 100-1 (AI RMF 1.0), Table 1 GOVERN categories and subcategories: GOVERN 1 (policies, risk tolerance 1.3, inventory 1.6), GOVERN 2 (accountability, training 2.2), GOVERN 3 (workforce DEI, 3.2 human-AI roles), GOVERN 4 (culture, 4.3 testing and incident sharing), GOVERN 5 (external engagement and feedback), GOVERN 6 (third-party, 6.2 contingency). Removed: the unverified mapping to ISO/IEC 42001 and EU AI Act, and the annual training claim. The artifacts, tiers and minimum program are suggested practice, not NIST requirements.
Method: documentation only; no commands were run.
