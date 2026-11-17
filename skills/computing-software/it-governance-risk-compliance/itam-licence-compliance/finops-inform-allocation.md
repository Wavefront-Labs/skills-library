---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.finops-inform-allocation
name: finops-inform-allocation
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [finops-inform-allocation, finops-for-software-and-cloud-spend, finops, cost allocation, showback, unit economics, focus specification, shared costs, itam-licence-compliance]
level: practitioner
status: draft
description: "Allocate cloud and SaaS cost with tags, shared cost rules and showback dashboards, and track unit economics."
sources:
  - https://www.iso.org/standard/68291.html
  - https://spdx.github.io/spdx-spec/
  - https://cyclonedx.org/specification/overview/
  - https://www.ntia.gov/page/software-bill-materials
  - https://openchainproject.org/
  - https://reuse.software/spec/
  - https://opensource.org/licenses
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FinOps inform: allocation and showback

Goal: transparent, attributable spend.

Method:
- Ingest billing exports (AWS CUR, Azure cost export, GCP billing export); use the FinOps FOCUS specification for common columns where available.
- Allocate by tag, account, or rule; split shared costs proportionally (usage-based or fixed).
- Provide showback dashboards by team, product, environment.
- Track unit metrics (cost per customer, per transaction).
- Manage the untagged bucket as a KPI.

Gotchas:
- Amortise commitments so allocation is fair.
- Mixing list and discounted rates confuses owners; choose a basis.

Verify: allocated total equals invoice total.
