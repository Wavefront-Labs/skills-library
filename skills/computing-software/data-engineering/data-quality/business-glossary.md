---
id: computing-software.data-engineering.data-quality.business-glossary
name: business-glossary
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, metadata-management, business-glossary, data-catalog, term-definitions, critical-data-elements, semantic-alignment, datahub, unity-catalog]
level: practitioner
status: draft
description: "Build a business glossary that people use: term template, ownership and approval workflow, linking terms to tables, columns and metrics in the catalog, and resolving conflicting definitions."
sources:
  - https://www.dama.org/cpages/body-of-knowledge
  - https://datahubproject.io/docs/glossary/business-glossary/
  - https://docs.open-metadata.org/latest/how-to-guides/data-governance/glossary
  - https://learn.microsoft.com/en-us/purview/concept-business-glossary
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Business glossary

**Goal:** one agreed definition for each business term ("active customer", "net revenue", "churn"), owned by the business, linked to the exact data that implements it.

## 1. Start small and painful
Seed with the 20-50 terms that cause arguments: those on executive dashboards, regulatory reports, and KPIs with conflicting numbers between teams. A glossary of 2,000 unreviewed terms is ignored.

## 2. Term template
| Field | Example |
|---|---|
| Term | Active customer |
| Definition | A customer with at least one paid order in the trailing 90 days, excluding internal and test accounts. |
| Calculation / rule | `COUNT(DISTINCT customer_id) WHERE last_paid_order_date >= current_date - 90 AND NOT is_internal` |
| Owner (business) | VP Customer Success |
| Steward | CS operations analyst |
| Synonyms / not to confuse with | "Engaged user" (product usage based) |
| Related terms | Customer, Churned customer |
| Linked assets | `gold.dim_customer.is_active`, metric `active_customers` in the semantic layer, dashboard "CS Weekly" |
| Status | Draft / Approved / Deprecated |
| Classification | Critical data element: yes |
Definitions describe the business meaning in plain language; the calculation field ties it to implementation.

## 3. Workflow
1. Propose (anyone) → 2. steward drafts with examples and edge cases → 3. owner approves → 4. linked to assets → 5. reviewed annually or on change.
Conflicting definitions: escalate to the governance forum; either pick one, or create **two distinct terms** with qualified names ("Active customer (Finance)", "Active user (Product)") — never one name with two meanings.

## 4. Put it in the catalog, linked to data
- DataHub / OpenMetadata / Microsoft Purview / Collibra / Alation glossaries support terms, hierarchies and term-to-asset links; Unity Catalog and Snowflake support tags/comments that can carry term references.
- Link terms to columns and to semantic-layer metrics, so a user browsing a table sees the definition and a user reading a definition finds the table.
- Keep definitions in Git (YAML) and sync to the catalog via API if you want PR review.

## 5. Keep it alive
- Show definitions where people work: tooltips in BI (dbt `description` → BI), semantic layer descriptions, data contract descriptions.
- Measure usage (catalog views, search hits) and stale terms (no review in 12 months).
- New KPIs aren't published to executive dashboards without an approved term.

## Verify
- [ ] Every executive KPI maps to an approved glossary term with an owner.
- [ ] Each approved term links to at least one physical asset or metric.
- [ ] No two approved terms share a name with different meanings.
