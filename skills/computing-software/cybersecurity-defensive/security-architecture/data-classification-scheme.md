---
id: computing-software.cybersecurity-defensive.security-architecture.data-classification-scheme
name: data-classification-scheme
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [data-protection, data-classification, sensitivity-labels, microsoft-purview, handling-rules, data-owner, labelling]
level: practitioner
status: draft
description: "Design a data classification scheme (levels, handling rules, owners) and implement it with labels such as Microsoft Purview sensitivity labels."
sources: ["CompTIA Security+ SY0-701 objective 3.3 (data types and classifications)", "CIS Control 3 (3.2 data inventory, 3.7 data classification scheme)", "Microsoft Learn - Sensitivity labels in Microsoft Purview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data classification scheme

**Goal:** every important dataset has a sensitivity level that drives concrete controls
(encryption, access, sharing, retention), and people can apply it without a manual.

## Levels (keep to 3-5)
| Level | Definition | Examples | Handling |
|---|---|---|---|
| Public | Approved for release | Marketing site, published reports | No restrictions |
| Internal | Default for business data | Policies, most email | Staff only; no public sharing |
| Confidential | Harm if disclosed | Contracts, customer lists, source code | Need-to-know groups, encrypted at rest and in transit, external sharing approved |
| Restricted | Severe harm, regulated | Payment card data, health records, credentials, M&A | Named access, MFA, DLP blocking, logging of access, no personal devices |

Map regulated types (PII, PHI, PCI, export-controlled) to levels explicitly.

## Roles
- **Data owner** (business): assigns level, approves access.
- **Data custodian** (IT): implements controls.
- **Users**: label what they create, handle per rules.

## Implementation with Microsoft Purview (example)
1. Create sensitivity labels mirroring the levels; publish a label policy with a default label (Internal) and mandatory labelling for documents and email.
2. Restricted/Confidential labels apply encryption (rights management) and headers/watermarks.
3. Auto-labelling: sensitive information types (credit card numbers, national IDs) recommend or apply labels.
4. Label containers (Teams, SharePoint sites) to control guest access and sharing.
5. DLP policies use labels as conditions.

Other platforms: Google Workspace labels, file-share classification (FCI), database column
tags (BigQuery policy tags, Snowflake object tagging).

## Gotchas
- Too many levels or ambiguous definitions lead to everything being labelled Confidential (useless) or Internal (risky).
- Encryption labels break some workflows (search, third-party apps, scanners): pilot first.
- Classification without an inventory of where data lives covers only new documents.

## Verify
- [ ] Each level has written handling rules mapped to technical controls.
- [ ] Label usage reports show adoption by department; spot-check mislabelled documents.
