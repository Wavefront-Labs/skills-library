---
id: computing-software.ai-ml-engineering.llm-application-engineering.nist-ai-600-1-generative-ai-profile
name: nist-ai-600-1-generative-ai-profile
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, genai-profile, nist-ai-rmf, ai-risk-management, generative-ai-risks, ai-governance]
level: practitioner
status: docs-checked
description: "Apply the NIST AI 600-1 Generative AI Profile: its twelve GAI risks, mapping suggested actions to GOVERN/MAP/MEASURE/MANAGE, and building a GenAI risk register."
sources:
  - https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
  - https://www.nist.gov/itl/ai-risk-management-framework
  - https://airc.nist.gov/airmf-resources/playbook/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Generative AI Profile risks and actions (NIST AI 600-1)

**Goal:** a GenAI application's risks are identified against a recognised catalogue, each has owners and controls, and evidence exists for auditors and leadership.

## The twelve GAI risks
1. CBRN information or capabilities
2. Confabulation (confident false output)
3. Dangerous, violent or hateful content
4. Data privacy (leakage, inference of personal data)
5. Environmental impacts (energy, compute)
6. Harmful bias and homogenization
7. Human-AI configuration (over-reliance, automation bias, anthropomorphism)
8. Information integrity (mis/disinformation, synthetic media)
9. Information security (prompt injection, model exfiltration, lowering barriers for attacks)
10. Intellectual property (copyright, trademark, trade secrets in outputs/training)
11. Obscene, degrading and/or abusive content (including CSAM and NCII)
12. Value chain and component integration (third-party models, data, opaque components)
The profile also highlights four cross-cutting considerations: governance, content provenance, pre-deployment testing, and incident disclosure.

## Suggested actions
Actions are organised under the AI RMF functions and subcategories with ids such as `GV-1.3-001`, `MP-2.3-001`, `MS-2.5-001`, `MG-4.1-001`, each tagged with the risks it addresses. Use them as a control library: pick those relevant to your system rather than all of them.

## Building the risk register
| Column | Example |
|---|---|
| Risk (GAI category) | Confabulation |
| System context | Support assistant answering billing questions |
| Impact / likelihood | Medium / High |
| Controls (action ids) | RAG grounding with citations (MS-2.5-xxx), abstention prompt, human escalation |
| Measurement | Faithfulness score on eval set and online sample |
| Owner | Support AI product lead |
| Residual risk / acceptance | Accepted by VP Support on <date> |
Revisit on model changes, new features, incidents, and at least annually.

## Practical mapping
- Confabulation, information integrity -> grounding, citations, evals (MEASURE), UX disclosure.
- Information security -> OWASP LLM Top 10 controls, red-teaming (see the MS-2.7 actions).
- Value chain -> vendor due diligence (GOVERN 6, MANAGE 3).
- Human-AI configuration -> UX design, training, human oversight.
- Incident disclosure -> incident logging and response process.

## Verify
- [ ] Every GAI risk is either assessed or explicitly marked not applicable with a reason.
- [ ] Each assessed risk has controls, metrics, an owner and acceptance.

## Checked
2026-11-01. Confirmed in NIST AI 600-1: the twelve risks (section 2 list, names as in the skill), the four primary considerations (Governance, Content Provenance, Pre-deployment Testing, Incident Disclosure), and the action id format with examples GV-1.3-001, MP-2.3-001, MS-2.5-001, MG-4.1-001 (also MS-2.7-001, GV-6.1-001, MG-3.1-001 exist). Removed: the approximate action count and the example acceptance date. The register layout is suggested practice.
Method: documentation only; no commands were run.
