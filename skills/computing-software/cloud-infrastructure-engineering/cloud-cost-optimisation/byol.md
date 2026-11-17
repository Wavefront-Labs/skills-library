---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.byol
name: byol
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, licensing-and-saas, byol, licence-mobility, azure-hybrid-benefit, dedicated-hosts]
level: practitioner
status: docs-checked
description: "Manage bring-your-own-licence use in cloud per the FinOps Licensing and SaaS capability: identify BYOL-eligible resources, tag them, track entitlements and avoid duplicate buys."
sources: ["https://www.finops.org/framework/capabilities/licensing-saas/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BYOL in cloud

The FinOps Licensing and SaaS capability asks teams to understand BYOL rights and the licence
management considerations in each technology category: matching specific services to workload
needs, using vendor-specific metering tools, and compliance issues from overuse or underuse of
licence rights. Vendor terms differ, so read the vendor's current product terms.

## Steps
1. **Find candidates**: FinOps determines which cloud resources are billed with software
   licences, which use licences bought from a provider marketplace, and which are configured
   with BYOL or could be.
2. **Tag for identification**: Engineering provides resource metadata through tagging so
   BYOL-eligible resources are easy to identify. The page also lists identifying BYOL independently of
   licensed resource type, for example a virtual resource sold without a licence that runs
   software or an OS the customer installed.
3. **Get the entitlement position**: ITAM/SAM makes available a summary of unallocated or hybrid
   use licence entitlements with budget and ownership information, and tracks the licence
   position of cloud resources using information from FinOps.
4. **Compare before buying**: Procurement compares pricing, commitment, marketplace and BYOL
   options and validates demand, entitlements and contract flexibility. ITAM maximises BYOL
   where it is more economical than marketplace software, and checks marketplace purchases
   against existing entitlements to avoid paying twice.
5. **Design with licences in mind**: Engineering weighs existing or BYOL licences against SaaS
   when architecting new infrastructure or software.
6. **Review before renewal**: confirm cloud resources were reviewed and optimised before licence
   or contract renewal.
7. **Use licence servers and SAM data** as inputs, alongside billing data and SaaS contract
   details.

## Verify
- [ ] BYOL resources are identifiable in billing data or by tag.
- [ ] Entitlements are reconciled against cloud use and marketplace purchases.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Licensing and SaaS capability page (read through the inputs and outputs). The Microsoft Azure SQL, AWS Windows licensing and Microsoft Licensing Mobility pages were not readable and were dropped. Removed unconfirmed: Azure Hybrid Benefit scope and ratios, Software Assurance rules, Microsoft Licence Mobility partner rules, dedicated host and sole-tenant requirements, AWS License Manager, Oracle vCPU counting, loss of rights on dropping SA, and the gotchas.
