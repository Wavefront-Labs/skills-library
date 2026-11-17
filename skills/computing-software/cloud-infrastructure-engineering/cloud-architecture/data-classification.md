---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.data-classification
name: data-classification
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, information-systems-architecture, togaf, data-classification, data-governance, sensitivity-labels]
level: practitioner
status: draft
description: "Design a data classification scheme for cloud: levels, handling rules per level, labelling via tags and DLP tooling, and ownership."
sources: ["https://csrc.nist.gov/pubs/sp/800/60/v1/r1/final", "https://learn.microsoft.com/purview/sensitivity-labels", "https://docs.aws.amazon.com/whitepapers/latest/data-classification/data-classification.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data classification scheme

## Steps
1. **Define 4 levels** (more are rarely used consistently): Public, Internal, Confidential,
   Restricted (regulated: personal data under GDPR special categories, cardholder data,
   health records, secrets, M&A).
2. **Handling rules per level** in a matrix: allowed regions, encryption (provider keys vs
   customer-managed keys vs HSM), access model (MFA, JIT), logging, sharing outside the
   organisation, retention and deletion, backup copies, allowed environments (no
   Restricted data in dev).
3. **Owners**: each dataset has a data owner who assigns the level; default to Internal
   when unknown, never Public.
4. **Label in the cloud**: mandatory tag (e.g. `data-classification=confidential`) on
   storage accounts, buckets, databases; enforce with policy (deny create without tag);
   map to Microsoft Purview sensitivity labels, Amazon Macie or Google Sensitive Data
   Protection findings for discovery.
5. **Enforce by level**: policies that block public access for Confidential and above,
   require CMK for Restricted, restrict regions.
6. **Review** classifications when data use changes and at least annually.

## Gotchas
- Aggregation raises sensitivity: individually Internal fields can be Confidential together.
- Copies in analytics, logs and backups inherit the level; logs often leak Restricted data.

## Verify
- [ ] 100% of data stores carry a classification tag (policy compliance report).
- [ ] Discovery scans show no Restricted data in lower-level stores.
