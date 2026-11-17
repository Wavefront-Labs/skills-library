---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.saas-spend-management
name: saas-spend-management
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, licensing-and-saas, saas-spend-management, saas-management-platform, licence-reclamation, saas-licence-reclaim]
level: practitioner
status: docs-checked
description: "Manage SaaS spend with the FinOps Licensing and SaaS capability: identify SaaS in use, allocate its cost with FOCUS, track consumption and reclaim unused entitlements."
sources: ["https://www.finops.org/framework/capabilities/licensing-saas/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SaaS spend management

## Steps
1. **Identify** what SaaS is in use, in particular products that integrate with, deploy,
   monitor, provide analytics about or secure your applications and infrastructure. Billing data
   may arrive inside cloud billing or separately from the vendor.
2. **Understand how it is bought**: Procurement is typically responsible, and an ITAM or SAM
   function (if present) should share how licences and software are used and assess contract
   risk.
3. **Define tagging and allocation** for SaaS cost, both when it appears in billing data and when
   it does not, using FOCUS to normalise data where possible. Walk maturity expects billing
   data in FOCUS format so showback includes marketplace and subscription SaaS spend.
4. **Collect the data**: billing data, provider data and business context, ideally in FOCUS,
   plus licence servers and contract commitment data.
5. **Track consumption** against total contract value and overage thresholds, and report the
   Active-to-Provisioned User Ratio (active users / provisioned users x 100) to find dormant
   accounts that may be candidates for deprovisioning or licence reduction.
6. **Reclaim**: at Run maturity reclamation triggers are automated against usage thresholds.
7. **Include in forecasts and TCO**: forecasting and showback cover software spend, so total
   cost of a service includes it.
8. **Review requests**: Leadership should have a process that checks whether the organisation
   already has a product with the same or similar function before a new purchase.
9. **Time changes to contracts**: agreements are multi-year and cannot be changed quickly, so
   plan adjustments ahead with Procurement and ITAM/SAM (see `saas-renewals`).

## Verify
- [ ] SaaS costs are visible and reported.
- [ ] Each material SaaS product has an owner and a contract record.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Licensing and SaaS capability page (read through the KPI definitions). The FinOps SaaS scope page was not read and was dropped. Removed unconfirmed: discovery sources (card data, SSO, OAuth, CASB), named SaaS management platforms, 30-90 day inactivity rule, SCIM deprovisioning, 90-day renewal alerts, and the gotchas on usage-based SaaS and mid-term seat removal.
