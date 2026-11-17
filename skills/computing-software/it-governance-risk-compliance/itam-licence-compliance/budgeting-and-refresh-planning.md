---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.budgeting-and-refresh-planning
name: budgeting-and-refresh-planning
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [budgeting-and-refresh-planning, asset-financial-management, refresh cycle, budget forecast, renewal calendar, lifecycle planning, itam-licence-compliance]
level: practitioner
status: draft
description: "Forecast refresh and renewal spend from asset age, warranty and licence data, and smooth it into annual budgets."
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

# Budgeting and refresh planning

Goal: no surprise capital or renewals.

Method:
- Query assets by age and warranty end to build a 3-year refresh forecast by cost.
- Combine with licence renewal calendar and support expiries.
- Smooth spikes by staggering refresh into cohorts or switching to DaaS.
- Include growth from headcount plan and one-off projects.
- Reforecast quarterly and flag deviations.

Gotchas:
- Stretching refresh cycles increases failure and security risk; show the trade-off.
- Currency exposure on overseas contracts.

Verify: forecast variance below 10% year-on-year.
