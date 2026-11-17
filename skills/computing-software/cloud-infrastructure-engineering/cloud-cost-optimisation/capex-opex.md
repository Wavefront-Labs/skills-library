---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.capex-opex
name: capex-opex
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cloud-budgeting, capex-opex, capitalisation, prepaid-commitments, software-development-capitalisation, accounting-treatment, asc-350-40, ias-38]
level: advanced
status: draft
description: "Work with finance on capex vs opex for cloud: why usage is opex, where capitalisation may apply (development costs, prepaid commitments), and the tagging needed to support it."
sources: ["https://www.finops.org/framework/capabilities/budgeting/", "https://www.finops.org/wg/cloud-cost-capitalization/", "FASB ASC 350-40 Internal-Use Software; IFRS IAS 38 Intangible Assets"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capex and opex treatment of cloud spend

**Not accounting advice** — the accounting decision is finance's/auditors'. Your job is to supply
data that makes their policy applicable.

## Background
- Cloud usage is generally an operating expense (service contract), unlike owned hardware which
  is capitalised and depreciated.
- Some organisations capitalise **cloud costs incurred during development of internal-use
  software** (application development stage under US GAAP ASC 350-40; development phase under
  IAS 38 when criteria are met) — e.g. dev/test environments for a capitalisable project.
- **Upfront commitment payments** (all-upfront RIs/SPs) are typically recorded as prepaid assets
  and expensed over the term — matches the amortised view.

## What FinOps provides
1. Tag/account structure to identify project and phase: `project-id`, `environment`,
   `capitalisable=true`, so dev-stage costs can be separated.
2. Monthly report of costs per capitalisable project and phase, in amortised terms.
3. Commitment amortisation schedules for prepaid accounting.
4. Evidence trail (allocation method per row).

## Gotchas
- Changing tags retroactively breaks audit trails — freeze monthly reports once closed.
- Shared environments mixing capitalisable and non-capitalisable work need an allocation rule finance accepts.

## Verify
- [ ] Finance policy documented; tags implemented accordingly.
- [ ] Month-end report per capitalisable project produced automatically.
