---
id: computing-software.ai-ml-engineering.llm-application-engineering.ai-system-impact-assessment-nist-map
name: ai-system-impact-assessment-nist-map
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, ai-risk-management, nist-ai-rmf, ai-impact-assessment, map-function, use-case-risk, stakeholders]
level: practitioner
status: docs-checked
description: "Run an AI impact assessment following the NIST AI RMF Map function: context and intended use, stakeholders, categorizing the system, benefits and harms, and go/no-go inputs."
sources:
  - https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf
  - https://airc.nist.gov/AI_RMF_Knowledge_Base/Playbook/Map
  - https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AI system impact assessment (NIST AI RMF Map)

**Goal:** before building or launching an AI feature, document its context, who it affects, what can go wrong, and whether to proceed - the "Map" function of the NIST AI RMF, which feeds Measure and Manage.

## Map categories (AI RMF 1.0)
1. **Context is established** (Map 1): intended purpose, setting, users, laws and norms that apply, assumptions, and what "success" means. Also: is AI the right tool at all?
2. **System is categorised** (Map 2): task type (generation, classification, recommendation, agentic actions), autonomy level, human-in-the-loop design, data used, known limitations of the model.
3. **Capabilities, benefits and costs compared with alternatives** (Map 3): including the non-AI baseline and cost of errors.
4. **Risks and benefits mapped for all components** (Map 4): including third-party models, data and tools (value chain).
5. **Impacts characterised** (Map 5): likelihood and magnitude of harms to individuals, groups, organisations, society; feedback channels from affected people.

## Practical template (one to three pages)
- Use case, users, decisions the system influences, and what happens on error.
- Affected stakeholders (direct users, subjects of decisions, bystanders) - consult representatives for high-impact uses.
- Out-of-scope uses and how they are prevented.
- Data: sources, personal/sensitive data, consent, retention.
- Risk register: for GenAI, walk the GenAI Profile risk list (confabulation, harmful bias, information security incl. prompt injection, data privacy, information integrity, IP, dangerous or violent content, harmful human-AI configuration such as over-reliance, value-chain issues) and rate likelihood x impact.
- Controls planned for each top risk and the evidence (evals) that will show they work.
- Residual risk and the accountable owner's decision: proceed / proceed with conditions / don't proceed.

## When to do it
At design time, again before launch, and on material changes (new model, new user group, new autonomy such as tools that take actions). Scale the depth to impact - a code-comment summariser needs less than a benefits-eligibility assistant.

## Verify
- [ ] Assessment exists, signed by an accountable owner, before launch.
- [ ] Each top risk has a control and a measurement plan (feeds the TEVV plan).
- [ ] Re-assessment triggers defined (model change, new use, incident).

## Checked
2026-11-01. Confirmed in NIST AI 100-1 Table 2: MAP 1 (context: purposes, laws and norms, settings, users, assumptions), MAP 2 (categorization: tasks and methods, knowledge limits and human oversight documented), MAP 3 (capabilities, benefits and costs compared with benchmarks), MAP 4 (all components including third-party software and data), MAP 5 (impacts characterised: likelihood and magnitude). The GenAI risk names match NIST AI 600-1. The template, tiers and go/no-go wording are suggested practice.
Method: documentation only; no commands were run.
