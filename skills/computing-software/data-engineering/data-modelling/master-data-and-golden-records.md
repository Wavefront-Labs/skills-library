---
id: computing-software.data-engineering.data-modelling.master-data-and-golden-records
name: master-data-and-golden-records
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, master-data-management, golden-record, mdm-styles, survivorship-rules, cross-reference, reference-data, dmbok, data-stewardship]
level: advanced
status: draft
description: "Build golden records for customers, products or suppliers: MDM implementation styles, cross-reference tables, survivorship rules per attribute, stewardship queues and publishing."
sources:
  - https://www.dama.org/cpages/body-of-knowledge
  - https://www.gartner.com/en/information-technology/glossary/master-data-management-mdm
  - https://learn.microsoft.com/en-us/sql/master-data-services/master-data-services-overview-mds
  - https://www.informatica.com/resources/articles/what-is-a-golden-record.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Master data and golden records

**Goal:** one trusted record per real-world customer/product/supplier, traceable to every source record, with rules for which source wins each attribute.

## 1. Pick the implementation style (DAMA-DMBOK / industry styles)
| Style | Golden record lives | Sources updated? | Effort |
|---|---|---|---|
| Registry | virtual: index of matches, attributes stay in sources | no | low |
| Consolidation | hub/warehouse builds golden record for analytics | no | medium |
| Coexistence | hub builds it and publishes back to sources | yes, async | high |
| Centralised (transactional) | hub is the system of entry | sources consume | highest |
Analytics teams usually start with **consolidation** in the warehouse; move to coexistence only with business ownership and integration budget.

## 2. Data model
```
src_customer_records (source_system, source_id, name, email, phone, address, updated_at, ...)
xref_customer (master_id, source_system, source_id, match_rule, match_score, linked_at, linked_by)
customer_golden (master_id, name, email, phone, address, name_source, email_source, ..., last_rebuilt_at)
```
- `xref` is the heart: every source record maps to exactly one `master_id`. Keep history (SCD2 on xref) so merges/splits are auditable.
- `master_id` is a stable surrogate — never derived from a source key, never reused after a merge (keep a `merged_into` pointer).

## 3. Survivorship rules (per attribute)
| Rule | Example |
|---|---|
| Source priority | legal name: ERP > CRM > web signup |
| Most recent | phone: latest `updated_at` among trusted sources |
| Most complete / longest | address with postcode + street over partial |
| Most frequent | gender/DOB across many sources |
| Validated wins | email with verified flag |
| Steward override | manual value always wins until cleared |
```sql
SELECT master_id,
  -- ordering key is NULL when the value is NULL, so empty values never win
  MAX_BY(email, CASE WHEN email IS NOT NULL
                     THEN CASE WHEN email_verified THEN 2 ELSE 1 END * 1e12 + UNIX_TIMESTAMP(updated_at) END) AS email,
  MAX_BY(legal_name, CASE WHEN legal_name IS NOT NULL
                          THEN CASE source_system WHEN 'ERP' THEN 3 WHEN 'CRM' THEN 2 ELSE 1 END END) AS legal_name
FROM src_customer_records JOIN xref_customer USING (source_system, source_id)
GROUP BY master_id;
```
(`MAX_BY`/`ARG_MAX` names vary by engine; ties in the ordering key need a deterministic tie-breaker such as `source_id`.) Store which source supplied each attribute for lineage.

## 4. Matching feeds the xref
Use deterministic rules first (same tax ID, same verified email), then probabilistic matching (see entity resolution) for the rest. Low-confidence pairs go to a **stewardship queue** — never auto-merge below the threshold.

## 5. Governance
- A named data owner per domain approves rules; stewards work the queue with SLAs.
- Reference data (country codes, currencies, product categories) is a separate, simpler problem: one curated table per code set, versioned, sourced from standards (ISO 3166, ISO 4217) and mapped from source codes via mapping tables.
- Publish golden records to consumers (marts, reverse ETL, APIs) with `master_id`; downstream joins use `master_id`, not source keys.

## Verify
- [ ] Every source record maps to exactly one master_id (no orphans, no duplicates in xref).
- [ ] Each golden attribute has a documented survivorship rule and recorded source.
- [ ] Duplicate rate (sources per master) and steward queue age are reported.
