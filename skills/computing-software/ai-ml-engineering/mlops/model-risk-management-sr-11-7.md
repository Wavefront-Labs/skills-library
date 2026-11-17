---
id: computing-software.ai-ml-engineering.mlops.model-risk-management-sr-11-7
name: model-risk-management-sr-11-7
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, model-risk-management, sr-11-7, model-validation, model-inventory, model-governance]
level: practitioner
status: draft
description: "Run model risk management in the SR 11-7 style: model inventory and tiering, development documentation, independent validation, ongoing monitoring and effective challenge."
sources:
  - https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm
  - https://www.occ.gov/publications-and-resources/publications/comptrollers-handbook/files/model-risk-management/index-model-risk-management.html
  - https://www.nist.gov/itl/ai-risk-management-framework
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Model risk management and independent validation (SR 11-7)

**Context:** US banking guidance (Fed SR 11-7 / OCC 2011-12) is the de facto template for model governance in finance and increasingly elsewhere. Model risk = losses from incorrect or misused models.

## Three pillars
1. **Development, implementation and use:** sound theory, data quality checks, documented methodology, testing (sensitivity, stress, benchmarking), implementation verified against design.
2. **Validation (independent):** conceptual soundness review, ongoing monitoring, outcomes analysis (back-testing). Performed by people not involved in development, with authority to challenge ("effective challenge").
3. **Governance:** board/senior management policies, model inventory, roles, internal audit.

## Practical program
- **Inventory:** every model (including vendor models, spreadsheets, LLM-based tools) with owner, purpose, inputs, version, tier, validation status.
- **Tiering:** risk tier by materiality (financial impact, customers affected), complexity and regulatory exposure; tier drives validation depth and frequency (e.g. tier 1 annually).
- **Documentation package:** purpose and limitations, data lineage, feature rationale, methodology, performance across segments, fairness analysis, assumptions, monitoring plan, fallback procedure.
- **Validation report:** findings with severity, required remediations and deadlines; model approved, approved with conditions, or rejected.
- **Ongoing monitoring:** KPIs with thresholds, periodic revalidation, change management (material changes trigger revalidation).

## ML-specific concerns
Explainability for adverse-action reasons (credit), fairness testing, hyperparameter and data-change governance, third-party/foundation model use, and challenger models as benchmarks.

## Mapping to tooling
Registry tags for tier/validation status; approval workflows gating promotion on validation sign-off; model cards as the documentation core; monitoring tied to the documented KPIs.

## Verify
- [ ] Sample audit: pick a production model and trace inventory entry -> documentation -> validation report -> monitoring evidence.
