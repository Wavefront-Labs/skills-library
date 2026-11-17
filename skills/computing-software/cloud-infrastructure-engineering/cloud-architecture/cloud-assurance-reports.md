---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-assurance-reports
name: cloud-assurance-reports
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-ecosystem, cloud-assurance-reports, soc-2, iso-27001, csa-star, third-party-risk]
level: practitioner
status: draft
description: "Use provider SOC 2 Type II, ISO 27001 and CSA STAR evidence in third-party risk reviews: scope, period, exceptions and complementary user entity controls."
sources: ["https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2", "https://cloudsecurityalliance.org/star", "https://aws.amazon.com/artifact/", "https://servicetrust.microsoft.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Third-party assurance reports for cloud services

## Where to get them
AWS Artifact, Microsoft Service Trust Portal, Google Cloud Compliance Reports Manager, and the
CSA STAR registry for many SaaS vendors. SOC reports are under NDA; download per audit period.

## Reading a SOC 2 Type II
1. **Type**: Type I = design at a point in time; Type II = operating effectiveness over a
   period (usually 6-12 months). Require Type II.
2. **Period and bridge letter**: if the period ended months ago, ask for a bridge (gap) letter.
3. **Scope**: which services and regions are in scope; a service you use may be missing.
4. **Trust services criteria** covered (security always; availability, confidentiality,
   processing integrity, privacy optional).
5. **Exceptions / deviations** in the test results and management's responses.
6. **Complementary user entity controls (CUECs)**: controls the customer must operate (MFA,
   access reviews, encryption settings). Map each to your own control owner.
7. **Subservice organisations** (carve-out vs inclusive) - a SaaS on AWS carves out AWS.

## ISO 27001 and CSA STAR
ISO 27001 certificate: check the scope statement and Statement of Applicability, the
certification body accreditation and expiry. CSA STAR Level 1 = self-assessment (CAIQ);
Level 2 = third-party audit or certification against the Cloud Controls Matrix.

## Gotchas
- A certificate logo on a website is not evidence; get the report.
- CUECs unmapped means you inherited a control gap.

## Verify
- [ ] Each critical vendor has a current Type II or equivalent on file with exceptions reviewed.
- [ ] CUECs mapped to internal control owners.
