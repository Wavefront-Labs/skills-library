---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.finops-optimise-commitments
name: finops-optimise-commitments
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [finops-optimise-commitments, finops-for-software-and-cloud-spend, reserved instances, savings plans, committed use discounts, spot, commitment coverage, utilisation, itam-licence-compliance]
level: advanced
status: draft
description: "Use reserved instances, savings plans, committed use and enterprise discounts without overcommitting."
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

# FinOps optimise: commitments and discounts

Goal: lower rates while keeping flexibility.

Method:
- Measure baseline steady-state usage over 30-90 days.
- Commit to a portion (e.g. 60-80% of steady-state) via Savings Plans/RIs (AWS), reservations/savings plans (Azure), committed use discounts (GCP).
- Track coverage and utilisation; adjust monthly.
- Use spot/preemptible for fault-tolerant workloads.
- Negotiate private pricing or EDP for large spend; consider marketplace purchase for commit drawdown.

Gotchas:
- Commitments are hard to unwind; prefer flexible instruments first.
- Licence-included software may not be reducible by RIs.

Verify: effective savings rate reported against on-demand.
