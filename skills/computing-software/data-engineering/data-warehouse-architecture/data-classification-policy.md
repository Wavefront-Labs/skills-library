---
id: computing-software.data-engineering.data-warehouse-architecture.data-classification-policy
name: data-classification-policy
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, classification-policy, data-classification, sensitivity-labels, pii-tagging, handling-rules, auto-classification]
level: practitioner
status: docs-checked
description: "Write and operationalise a data classification policy: sensitivity levels, handling rules, column labelling, automated discovery and tag enforcement."
sources:
  - https://csrc.nist.gov/pubs/sp/800/60/v1/r1/final
  - https://docs.snowflake.com/en/user-guide/classify-intro
  - https://cloud.google.com/sensitive-data-protection/docs/data-profiles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Data classification policy

## Levels (keep the set small)
The levels below are a common practitioner scheme, not one mandated by the cited sources. NIST SP 800-60 is a US federal guide for mapping information types to security categories by risk level, so use it as a reference for risk-based categorisation, not as this four-level scheme.
| Level | Examples | Handling |
|---|---|---|
| Public | published prices, marketing content | no restriction |
| Internal | org charts, internal metrics | employees only; no public sharing |
| Confidential | customer PII, contracts, unreleased financials | need-to-know access, encryption, masked in non-prod, logged access |
| Restricted | payment card data, health data, credentials, special category data, government IDs | named approvals, tokenisation or strong masking, no copies to analytics sandboxes, strict retention |
Add **categories** orthogonal to level where regulation differs: PII, PCI, PHI, financial, children's data.

## Policy content
- Scope (all data, all formats, all locations including SaaS and backups).
- Who classifies (data owner accountable; stewards apply labels; a conservative default level when unknown).
- Handling matrix per level: storage location/residency, encryption, sharing externally, non-production use, retention and disposal, export, logging.
- Review: classification reassessed on schema changes and on a set cadence.
- Exceptions process.

## Labelling in the platform
- Column-level tags in the warehouse or catalog, using the platform's tag mechanism.
- Inherit downward: a table containing a Restricted column is Restricted for sharing decisions.
- Propagate through lineage: check that derived models keep the tags (Snowflake notes that tag-based masking assigns the masking policy automatically as tags are applied to new columns).

## Automated discovery
- Snowflake sensitive data classification (Enterprise Edition or higher): every column found to hold sensitive data gets a semantic category (such as name) and a privacy category (IDENTIFIER, QUASI_IDENTIFIER or SENSITIVE), applied through the system tags `SNOWFLAKE.CORE.SEMANTIC_CATEGORY` and `SNOWFLAKE.CORE.PRIVACY_CATEGORY`. You can map your own tags to the system tags and create custom categories. Classification is configured through classification profiles tied to databases, uses serverless compute that consumes credits, and excludes views by default. The page also describes Autopilot and AI mode, both in preview at the time of checking.
- Google Sensitive Data Protection: a discovery scan configuration scoped to an organization, folder or project generates table, column and project data profiles for BigQuery and Cloud SQL (and file store profiles for Cloud Storage), with predicted infoTypes and calculated data risk and sensitivity levels. It can send a Pub/Sub notification when a profile's sensitivity changes.
- Automation proposes; stewards confirm. Review free-text columns by hand and treat them conservatively (this is practice guidance, not stated by the pages).
- Other tools (Macie, Purview, Presidio) were not checked.

## Enforcement via tags
Snowflake documents combining tags and masking policies: a masking policy associated with a user-defined tag is applied automatically to columns when classification applies the tag, including new data added later. Beyond masking, consider blocking sharing or export of Restricted-tagged objects, requiring tags before promotion to production, and alerting on untagged new columns (design suggestions, not platform features confirmed here).

## Verify
- [ ] Every production table has a level; columns in PII categories carry tags and masking.
- [ ] Untagged new columns are flagged promptly; non-prod copies of Confidential data are masked.

## Checked
Date: 2026-11-09. Confirmed from the Snowflake classification page (first half read: categories, tags, profiles, tag-based masking, cost), the Sensitive Data Protection data profiles page (searched for profile types and sensitivity levels) and the NIST SP 800-60 abstract page. The ISO 27001 page returned 403 and was removed from sources. Removed as unconfirmed: the SQL masking example, SYSTEM$CLASSIFY, BigQuery policy tags and Dataplex, Databricks and Purview labels, dbt meta syncing, the one-day flagging target and the annual review.
Method: documentation only; no commands were run.
