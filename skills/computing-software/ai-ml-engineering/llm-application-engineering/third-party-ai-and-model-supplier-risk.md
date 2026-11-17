---
id: computing-software.ai-ml-engineering.llm-application-engineering.third-party-ai-and-model-supplier-risk
name: third-party-ai-and-model-supplier-risk
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, third-party-ai-risk, vendor-due-diligence, nist-ai-rmf, model-providers, ai-procurement]
level: practitioner
status: docs-checked
description: "Manage risk from AI vendors and model providers per NIST AI RMF GOVERN 6 and MANAGE 3: due diligence, contract terms, model-change monitoring, contingency and exit plans."
sources:
  - https://airc.nist.gov/airmf-resources/playbook/govern/
  - https://airc.nist.gov/airmf-resources/playbook/manage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Third-party AI and model supplier risk

**Goal:** dependence on external models, APIs and AI-enabled SaaS is a known, monitored and contractually covered risk, with a plan when a supplier changes or fails.

## Framework anchors
- **GOVERN 6:** policies and procedures for AI risks from third-party software, data and supply chain issues, including infringement of a third party's IP or other rights, and contingency processes for failures or incidents in third-party data or AI systems deemed high-risk.
- **MANAGE 3:** risks and benefits from third-party resources are regularly monitored, and risk controls are applied and documented; the playbook suggests identifying pre-trained models in the AI system inventory and monitoring their performance and trustworthiness as part of third-party risk tracking.

## Due diligence questions
- **Data:** Is customer data used for training? Retention period? Zero-data-retention options? Sub-processors and regions?
- **Security:** independent security attestations and certifications; pen-test summaries; incident notification time.
- **Models:** system/model cards, published evaluations and safety testing; how model updates are versioned and announced; deprecation policy and notice period.
- **Legal:** IP indemnity for outputs, acceptable use policy, liability caps, audit rights, compliance support (EU AI Act role split - provider vs deployer).
- **Reliability:** SLAs, rate limits, regional availability, status history.

## Contract terms to secure
No training on your data without consent, retention limits, breach notification, change notification for models you depend on, deprecation notice, data deletion on exit, regional processing commitments, right to audit or receive reports.

## Ongoing monitoring
- Pin model versions where possible; re-run your eval suite when a provider updates or deprecates a model.
- Track provider incidents and status; measure latency/error SLOs yourself.
- Re-review vendors annually and on material change (acquisition, new sub-processor, policy change).
- Maintain an inventory: which applications use which vendor models, with data classification.

## Contingency
- Abstraction layer so a route can switch provider or model; documented and tested fallback (secondary provider, smaller self-hosted model, or degraded non-AI path).
- Exit plan: data export, re-tuning effort, prompt migration and eval costs estimated.

## Verify
- [ ] Every AI vendor has completed due diligence and contract review on file.
- [ ] Model-update eval re-runs are automated or scheduled.
- [ ] Fallback path tested for each critical AI feature.

## Checked
2026-11-01. Confirmed against the NIST AI RMF Playbook GOVERN and MANAGE pages: third-party policy and supply-chain wording, contingency processes for high-risk third-party systems, third-party monitoring and pre-trained model tracking suggestions. Removed: NIST AI 600-1 risk name (PDF unreadable) and named certification list.
Method: documentation only; no commands were run.
