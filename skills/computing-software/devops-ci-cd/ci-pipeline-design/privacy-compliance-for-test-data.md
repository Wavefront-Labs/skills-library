---
id: computing-software.devops-ci-cd.ci-pipeline-design.privacy-compliance-for-test-data
name: privacy-compliance-for-test-data
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, test-data-privacy, data-masking, test-data-management]
level: advanced
status: docs-checked
description: "Keep test data lawful: GDPR/HIPAA rules for using production data in non-prod, masking vs synthetic data, access controls, retention and evidence for auditors."
sources: ["https://gdpr-info.eu/art-25-gdpr/", "https://www.postgresql.org/docs/current/ddl-rowsecurity.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Privacy compliance for test data

Copying production data to dev/test is processing personal data in a less controlled environment.
GDPR, HIPAA and PCI DSS all constrain it; confirm the specific requirements with your compliance owner.

## Decision order
1. **Synthetic data** first (factories, Faker, generators that follow the schema and distributions).
2. **Masked/anonymised subset** of production when realism matters (edge cases, volumes).
3. Raw production only in a production-grade environment with production access controls (rarely justified).

## Masking requirements
- Irreversible for direct identifiers (names, emails, phone, national ids): replace with consistent
  fakes (deterministic hashing with a secret salt so joins still work).
- Generalise quasi-identifiers (DOB -> year, postcode -> area); combinations re-identify people.
- Free-text fields (notes, support tickets) are the usual leak; null them or run PII detection.
- Payment data: never copy PAN/CVV; use test card numbers.
Tools: dedicated masking tools or custom SQL views.

## Controls
- Masking runs **inside** the production boundary; only masked output leaves.
- Access to non-prod copies limited and logged; retention (refresh and delete on a schedule).
- Document in the RoPA / DPIA; keep evidence: masking job logs, sample checks, access reviews.

## Verify
- [ ] Automated check scans non-prod copies for real email domains/card patterns and fails on hits.

## Checked

2026-10-28. No claim in this skill is checkable against the fetched pages (W3C and regulator pages do not cover test-data masking). Removed: GDPR article numbers, the PCI DSS requirement number, the vendor tool list and the 30-day retention figure; what remains is process advice.

Method: documentation only; no commands were run.
