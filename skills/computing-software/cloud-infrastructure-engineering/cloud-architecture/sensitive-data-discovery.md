---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.sensitive-data-discovery
name: sensitive-data-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-protection, sensitive-data-discovery, amazon-macie, microsoft-purview, sensitive-data-protection, pii-scanning, data-classification-automation]
level: practitioner
status: draft
description: "Find sensitive data across cloud storage and databases with Macie, Purview or Sensitive Data Protection: scope, custom identifiers, sampling, findings triage and labelling."
sources: ["https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html", "https://learn.microsoft.com/purview/concept-best-practices-sensitivity-labels", "https://cloud.google.com/sensitive-data-protection/docs/sensitive-data-protection-overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sensitive data discovery

## Tools
- **Amazon Macie**: S3 automated discovery (sampling) and targeted jobs; managed data identifiers
  (credentials, financial, PII) plus custom regex/keyword identifiers; findings to Security Hub/EventBridge.
- **Microsoft Purview**: scans Azure storage, SQL, multicloud sources; classifications and
  sensitivity labels; Data Map.
- **Google Sensitive Data Protection (Cloud DLP)**: inspection jobs on Cloud Storage/BigQuery/
  Datastore, discovery profiles per table/bucket, de-identification transforms.

## Steps
1. Scope: start with object storage and analytics stores (largest unknowns).
2. Enable automated discovery/profiling org-wide; sample to control cost.
3. Add custom identifiers for internal IDs (customer numbers, employee IDs).
4. Triage findings: true positive -> label/classify, move or restrict, tokenise; false positive ->
   tune identifiers / allow lists.
5. Feed classification tags back to resources for policy (ABAC, DLP, retention).
6. Re-run on schedule; alert on sensitive data appearing in unexpected locations (public buckets,
   dev accounts).

## Gotchas
- Full scans of petabyte buckets are expensive; use sampling and prioritise.
- Images/scanned PDFs need OCR support; check tool capabilities.
- Discovery without ownership routing: findings pile up.

## Verify
- [ ] Coverage report: % of storage profiled in last 30 days.
- [ ] No unresolved high-severity findings older than SLA.
