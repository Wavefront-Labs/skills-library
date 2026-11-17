---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-centre-mapping
name: cost-centre-mapping
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, invoicing-and-chargeback, chargeback, cost-centre-hierarchy, cost-centre-mapping, allocation]
level: practitioner
status: docs-checked
description: "Map cloud spend to finance cost centres using the FinOps allocation strategy: account lists, tag-based refinement, multiple views and shared cost rules."
sources: ["https://www.finops.org/framework/capabilities/allocation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost centre mapping

Finance and engineering slice the same spend differently. The FinOps Allocation capability says
finance may need costs by cost centre or by type of spending (for example R&D or COGS), while
engineering teams need application-level detail and operations teams may want all production
costs. The allocation strategy defines how the organisation wants to see costs for showback,
chargeback and allocation to cost centres.

## Steps
1. **Define the groupings** costs are allocated to and the terminology for them. Finance
   determines the organisational and budgetary units.
2. **Start simple**: at Crawl maturity, allocate account, project or subscription cost to
   business units, portfolios or cost centres using a list of accounts known to belong to each.
3. **Refine with metadata**: naming standards and tags or labels give finer granularity, and the
   CMDB can add more for shared elements. Combine accounts, tags and shared-cost rules as
   maturity grows (Walk).
4. **Handle shared cost**: decide for each shared item whether to fund it centrally or split it
   (fixed, proportional or proxy metric); see `unallocated-costs`.
5. **Validate compliance** with the allocation strategy and keep an allocation taxonomy of
   categories for usage.
6. **Feed chargeback**: per the Budgeting page, Invoicing and Chargeback applies costs to the
   budget cost centres each period.

## Notes
- Multiple versions of the allocation strategy can be in force at once, so perfect
  consistency may not be reachable; aim for enough to support decisions.

## Verify
- [ ] Every account or project in scope maps to a cost centre or an owned central bucket.
- [ ] Finance has confirmed the grouping list.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Allocation capability page (read through the functional activities) and the chargeback sentence in the FinOps Budgeting page. The AWS Cost Categories source was not readable and was dropped. Removed unconfirmed: the mapping table columns, ERP extract and code validation, effective dating, reorg procedure, many-to-many split percentages, the 2 percent unmapped threshold and the provider tooling advice.
