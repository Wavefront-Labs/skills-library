---
id: computing-software.data-engineering.data-warehouse-architecture.regulatory-compliance-mapping
name: regulatory-compliance-mapping
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-governance, regulatory-compliance, gdpr, ccpa, hipaa, ropa, dpia, controls-mapping]
level: advanced
status: draft
description: "Map GDPR, CCPA/CPRA and HIPAA obligations to concrete data platform controls: inventories and RoPA, lawful basis tagging, retention, access, erasure, DPIAs and audit evidence."
sources:
  - https://gdpr-info.eu/
  - https://oag.ca.gov/privacy/ccpa
  - https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Regulatory compliance mapping for data platforms

**Goal:** turn legal obligations into platform controls with owners and evidence, so audits are answered from systems, not memory. (Not legal advice: confirm interpretations with counsel/DPO.)

## Obligation -> control matrix
| Obligation | GDPR | CCPA/CPRA | HIPAA | Platform control |
|---|---|---|---|---|
| Know what personal data you hold | Art. 30 RoPA | notice at collection | PHI inventory | catalog with PII/PHI classification tags; RoPA fed from catalog |
| Lawful basis / purpose limitation | Art. 5-6 | purpose disclosure | minimum necessary | tag datasets with purpose; access policies by purpose; consent flags joined in marts |
| Data minimisation | Art. 5(1)(c) | data minimisation (CPRA) | minimum necessary | column-level access, drop unused PII at ingestion |
| Storage limitation | Art. 5(1)(e) | retention disclosure | 6-year documentation retention | retention policies per table, automated deletion jobs, Time Travel/backup windows documented |
| Access rights (subject access) | Art. 15 | right to know | patient access | subject-key lookup across tables via lineage/catalog |
| Erasure | Art. 17 | right to delete | n/a (amendment) | deletion pipeline incl. lake files, snapshots, downstream copies |
| Opt-out of sale/sharing | n/a | Sec. 1798.120 | n/a | consent flags enforced in reverse ETL/exports |
| Security | Art. 32 | reasonable security | Security Rule (164.312) | encryption, RBAC, MFA, audit logs, network isolation |
| Breach notification | 72 h (Art. 33) | per statute | 60 days | access monitoring, incident runbook |
| Processors / BAAs | Art. 28 DPA | service provider contracts | BAA required | vendor list with DPAs/BAAs; only BAA-covered services for PHI |
| Cross-border transfers | Ch. V (SCCs) | n/a | n/a | data residency controls, region pinning |
| High-risk processing | Art. 35 DPIA | risk assessments (CPRA regs) | risk analysis | DPIA template triggered by new PII use cases |

## Implementation steps
1. **Classify:** automated PII/PHI discovery + steward review; tags in the catalog (`pii=email`, `phi=true`, `purpose=marketing`).
2. **Policy as code:** masking/row policies driven by tags; retention configs in IaC; access via roles mapped to purposes.
3. **Data subject request pipeline:** identity resolution to all keys, search via lineage, delete/anonymise, verify, log evidence.
4. **Evidence:** access logs (Snowflake ACCESS_HISTORY, UC audit), policy change history (git), deletion job logs, quarterly access reviews.
5. **HIPAA specifics:** PHI only in BAA-covered services/regions; de-identification via Safe Harbor (remove 18 identifiers) or Expert Determination for analytics copies.

## Gotchas
- Backups, Time Travel, Fail-safe, logs, ML training sets and BI extracts all hold copies; erasure and retention must cover them or document the delay.
- "Anonymised" claims for k-anonymised or hashed data are often wrong; treat as pseudonymised unless assessed.
- Different regulations' definitions differ (CCPA "personal information" includes household and device data).

## Verify
- [ ] Each row of the matrix has an owner, a control, and a link to evidence.
- [ ] Last DSAR/erasure request completed within the statutory deadline with logs.
