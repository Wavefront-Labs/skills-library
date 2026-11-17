---
id: computing-software.data-engineering.data-quality.metadata-standards-and-tagging-taxonomy
name: metadata-standards-and-tagging-taxonomy
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, metadata-taxonomy, tagging, classification, metadata-management]
level: advanced
status: draft
description: "Define a metadata standard and tagging taxonomy: required fields per asset, controlled vocabularies for domain, sensitivity and tier, and enforcing tags across tools."
sources:
  - https://www.dama.org/cpages/body-of-knowledge
  - https://dublincore.org/specifications/dublin-core/dcmi-terms/
  - https://docs.snowflake.com/en/user-guide/object-tagging
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Metadata standards and tagging taxonomy

**Goal:** every data asset carries consistent, searchable metadata so people can find, trust and govern it, and policies can be automated from tags.

## Required metadata per asset (example standard)
| Field | Example | Source of truth |
|---|---|---|
| Owner (team) | `finance-data` | dbt `meta.owner`, catalog |
| Domain | `finance` | controlled list |
| Description | one paragraph, business language | YAML/catalog |
| Sensitivity | `public / internal / confidential / restricted` | classification policy |
| PII category | `email, phone, national_id, none` | scanners + review |
| Tier / criticality | `tier1` (SLA, on-call) ... `tier3` | data product registry |
| Lifecycle | `active / deprecated / experimental` | YAML |
| Retention | `7y` | policy |

## Controlled vocabularies
- Short, closed lists; each value defined in a glossary page. No free-text tags for governance fields.
- Hierarchy where useful (`domain: finance > accounts_payable`).
- Version the taxonomy; changes go through governance review.

## Implement in tools
- dbt: `meta` and `tags` in YAML (`+meta: {owner: finance-data, tier: tier1}` at folder level).
- Warehouse tags: Snowflake object tags with `ALLOWED_VALUES`; Unity Catalog governed tags; BigQuery policy tags (taxonomies) for columns.
```sql
CREATE TAG governance.tags.sensitivity ALLOWED_VALUES 'public', 'internal', 'confidential', 'restricted';
ALTER TABLE finance.gl.journal SET TAG governance.tags.sensitivity = 'confidential';
```
- Catalog (DataHub/OpenMetadata/Collibra): glossary terms and tags synced from code.
- Tag-based policies: masking policies attached to tags, access rules by sensitivity.

## Enforce
- CI checks: models must declare owner, tier, sensitivity (project evaluator, dbt-checkpoint, custom script on manifest).
- Periodic report of untagged assets per owner.
- PII scanners propose tags; humans confirm.

## Gotchas
- Too many tags: nobody applies them consistently. Start with 5-8 required fields.
- Tags in multiple systems drift; choose one source of truth per field and sync outward.

## Verify
More than 95% of tier1/tier2 assets have all required fields; tag-based masking applies automatically to a newly tagged column.
