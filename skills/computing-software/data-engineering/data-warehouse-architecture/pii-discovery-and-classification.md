---
id: computing-software.data-engineering.data-warehouse-architecture.pii-discovery-and-classification
name: pii-discovery-and-classification
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-security, pii, pii-classification, sensitive-data-discovery, snowflake-classification, amazon-macie, google-sensitive-data-protection, presidio, data-tagging]
level: practitioner
status: draft
description: "Find and tag personal data across a warehouse and lake: classification scheme, automated scanners (Snowflake, Macie, Google SDP, Purview, Presidio), review, tagging, and driving policies from tags."
sources:
  - https://docs.snowflake.com/en/user-guide/classify-intro
  - https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html
  - https://cloud.google.com/sensitive-data-protection/docs/data-profiles
  - https://learn.microsoft.com/en-us/purview/concept-classification
  - https://microsoft.github.io/presidio/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PII discovery and classification

**Goal:** know where personal and sensitive data lives — every table, column and file — and tag it so access policies, masking and retention follow automatically.

## 1. Define the scheme first
- Sensitivity levels: Public / Internal / Confidential / Restricted.
- Categories: direct identifiers (name, email, phone, national ID), quasi-identifiers (DOB, postcode, gender — identifying in combination), special category data (health, biometrics, religion, etc. under GDPR Art. 9), financial (card numbers — PCI scope), credentials/secrets.
- Map each category to required controls (masking, encryption, retention, access approval).

## 2. Scan automatically
| Platform | Tool |
|---|---|
| Snowflake | `SYSTEM$CLASSIFY` / automatic sensitive data classification → `SNOWFLAKE.CORE.SEMANTIC_CATEGORY` and `PRIVACY_CATEGORY` tags |
| BigQuery / GCS | Google Sensitive Data Protection (DLP) discovery profiles |
| S3 | Amazon Macie sensitive data discovery |
| Azure / multi-cloud | Microsoft Purview scanning and classification |
| Databricks | Unity Catalog data classification (where available), or scan with Presidio/regex jobs |
| Free text, logs, documents | Microsoft Presidio (NER + pattern recognizers), custom regex + validators (Luhn for card numbers) |
```sql
-- Snowflake: classify and auto-apply system tags
CALL SYSTEM$CLASSIFY('prod.crm.customers', {'auto_tag': true});
SELECT * FROM TABLE(prod.INFORMATION_SCHEMA.TAG_REFERENCES_ALL_COLUMNS('prod.crm.customers', 'table'));
```
Scanners combine column-name heuristics with content sampling; both miss things (`notes` column with emails, `attr_17` holding phone numbers) — schedule recurring scans for new and changed tables.

## 3. Review and tag
- Results above a confidence threshold auto-tag; the rest go to steward review.
- Tag at **column** level with the category and sensitivity (`pii=email`, `sensitivity=restricted`); propagate tags through lineage where the platform supports it (dbt `meta` + post-hooks, Unity Catalog/Snowflake tag propagation features).
- Record false positives as exceptions so rescans don't re-raise them.

## 4. Drive controls from tags
- Tag-based masking: Snowflake masking policies attached to tags; Unity Catalog ABAC policies on governed tags; BigQuery policy tags (column-level security) from Data Catalog taxonomies.
- Retention and deletion jobs select tables by tag.
- Access requests for restricted columns require approval workflow.

## 5. Shift left
- New sources: classify during onboarding (data contract `classification` field) before data lands.
- PR checks: new columns in dbt models matching PII name patterns must carry a classification in `meta`.
- Don't let PII into logs, test data and tmp tables — scan those too.

## Verify
- [ ] Every table in prod schemas has been scanned in the last scan cycle.
- [ ] All restricted-tagged columns have a masking/access policy attached.
- [ ] Sample audit: 20 random columns manually checked against their tags.
