---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cloud-marketplace
name: cloud-marketplace
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, licensing-and-saas, cloud-marketplace, commitment-burn-down, private-offers]
level: practitioner
status: docs-checked
description: "Use cloud marketplaces for software purchases per the FinOps Licensing and SaaS capability: on-demand buying, duplicate-BYOL waste, FOCUS showback and procurement checks."
sources: ["https://www.finops.org/framework/capabilities/licensing-saas/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Marketplace purchases

## What the Framework says
- Licences and SaaS are increasingly available through cloud provider marketplaces.
  A marketplace can offer a more on-demand experience: buy a licence for a purpose and stop
  paying when it is no longer needed, rather than buying perpetual licences with multi-year
  support.
- Marketplace terms may differ from your organisation's own terms.
- If the organisation already has BYOL rights to the software in the cloud, buying a duplicate
  through the marketplace may be wasteful.

## Steps
1. **Compare options before buying**: pricing, commitment, marketplace and BYOL options against
   validated demand (the pre-signature checklist at Walk maturity). Procurement does this with
   Engineering, FinOps and Finance, covering the whole contract term, whether the purchase is
   through a marketplace, a private contract, or a reseller.
2. **Check enterprise agreement effects**: Procurement reviews how each procurement option
   affects spend thresholds set in cloud provider enterprise agreements.
3. **Include ITAM**: ITAM analyses marketplace software purchased against existing entitlements
   and maximises BYOL where it is more economical than marketplace software.
4. **Allocate and show back**: showback should include licence and SaaS spend arriving through
   the marketplace or subscriptions, with billing data in FOCUS format at Walk maturity.
5. **Measure**: licences purchased through the marketplace should be fully utilised, and report
   key renewal and expiry dates for marketplace purchases.

## Verify
- [ ] Marketplace purchases are compared with existing entitlements before approval.
- [ ] Marketplace spend appears in showback and in forecasts.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Licensing and SaaS capability page (read through the KPI definitions) and the Reporting and Analytics page for renewal and expiry reporting. The AWS, Azure and Google Cloud marketplace pages were not readable and were dropped. Removed unconfirmed: commitment drawdown eligibility rules per provider (EDP, MACC, Google), private offer mechanics, private marketplace controls, contract auto-renewal and the gotchas.
