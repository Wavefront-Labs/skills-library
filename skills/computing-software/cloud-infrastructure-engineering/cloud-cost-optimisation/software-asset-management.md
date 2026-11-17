---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.software-asset-management
name: software-asset-management
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, licensing-and-saas, software-asset-management, sam, licence-compliance]
level: practitioner
status: docs-checked
description: "Integrate software asset management with FinOps: licence-included versus BYOL in cloud, marketplace duplicates, shared data and renewal planning."
sources: ["https://www.finops.org/framework/capabilities/licensing-saas/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Software asset management integration

The FinOps Framework Licensing and SaaS capability says to integrate with an ITAM or SAM team where one exists, to
share how externally purchased licences are used, to plan their use or retirement and to manage contractual risk.
Over-deployment is a compliance risk and under-deployment is shelfware or waste.

## Steps
1. **Learn the buying channels**: organisational agreements, cloud provider marketplaces, direct, reseller. The
   Framework says licence and SaaS contracts typically run multiple years and often allow true-ups but not
   true-downs.
2. **Find licensed resources**: determine which cloud resources are billed with licences, which use marketplace
   licences and which are configured for BYOL or could be. Engineering supplies tags so BYOL-eligible resources are
   identifiable.
3. **Check for duplicates**: where the organisation already has BYOL rights, buying the same software through a
   marketplace may be wasteful (Framework). ITAM tracks the licence position using FinOps data.
4. **Check discount coverage**: the Framework notes licence cost may or may not be covered by savings plan, committed
   use or reserved instance discounts; confirm per case.
5. **Allocate and report**: define how to tag and allocate licence and SaaS cost, both when it appears in billing data
   and when it does not, using FOCUS to normalise. Include software in total cost of ownership showback.
6. **Plan renewals early**: analyse usage and optimise well ahead of each renewal, then forecast the renewal.
   Compare pricing, commitment, marketplace and BYOL options against validated demand before signature.
7. **Share tooling**: at Run, FinOps and SAM use the same tooling and data sources for contract details, usage and spend.

## Gotchas
- Vendors' cloud licensing rules are complex and change; ITAM, Procurement and Legal confirm the terms (Framework).
- Marketplace terms can differ from the organisation's own agreements.

## Verify
- [ ] Licensed, BYOL and marketplace resources are identified and reported.
- [ ] Resources needing a licence are compliant, and marketplace licences bought are fully used (Framework KPIs).

## Checked
Confirmed on the FinOps Framework Licensing and SaaS page (read in full): definition, buying channels, true-up and
true-down, BYOL, marketplace duplication, discount coverage caveat, Crawl/Walk/Run, persona activities and KPIs.
Removed: ISO 19770, named SAM tools, vendor-specific counting rules, the AWS License Manager and Azure Hybrid
Benefit procedures, the billing-check recipes and the shared data table (sources unreadable).
Method: docs-checked 2026-11-09 against finops.org Framework Licensing and SaaS capability page
