---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.saas-renewals
name: saas-renewals
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, licensing-and-saas, saas-renewals, saas-negotiation, contract-renewal, procurement, saas-spend-management]
level: practitioner
status: docs-checked
description: "Prepare SaaS and licence renewals using the FinOps Licensing and SaaS capability: pre-signature checklist, usage analysis ahead of renewal, true-up risk and exit accountability."
sources: ["https://www.finops.org/framework/capabilities/licensing-saas/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SaaS and licence renewals

The FinOps Licensing and SaaS capability stresses that, unlike public cloud, most licence and SaaS
agreements cannot be changed quickly, and some take years to adjust or exit. Changes need careful
planning well in advance with Procurement and ITAM/SAM.

## Steps
1. **Know the terms**: contract length, renewals, secondary metrics (access count, API usage,
   data stored), and true-up and true-down parameters. The page notes agreements often allow
   true-ups but not true-downs, and that vendors can audit and apply penalties for overuse.
2. **Analyse well before renewal**: at Run maturity FinOps partners with Engineering, ITAM/SAM and
   Procurement to analyse usage and find optimisation opportunities well ahead of each renewal.
   Reviewing terms only at renewal is the Crawl pattern the Framework wants to move beyond.
3. **Optimise before estimating**: the Run description says forecasting or estimating the future
   contract happens after optimisation is done.
4. **Use a pre-signature checklist** comparing pricing, commitment, marketplace and BYOL options
   against validated demand; Procurement validates demand, entitlements and contract flexibility.
5. **Involve FinOps** in review and approval when new licensing or SaaS is acquired outside the
   cloud providers.
6. **Track consumption-based software** against the total contract amount and against thresholds
   that would trigger overages.
7. **Assign accountability**: Finance defines renewal, exit and consumption accountability, and
   Run maturity enforces these by policy with automated reclamation triggers on usage thresholds.
8. **Engineering inputs**: tell FinOps and SAM when licences are no longer needed or a SaaS
   contract will end, and review cloud resources for optimisation before renewal.

## KPIs from the page
- Active-to-Provisioned User Ratio = (active users / provisioned users) x 100.
- Consumption versus Commitment = actual consumption units / committed units.

## Verify
- [ ] Each renewal has an owner and a documented usage review before the decision date.
- [ ] Exit and consumption accountability is recorded.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Licensing and SaaS capability page (read through the KPI definitions) and the Rate Optimization page for the Consumption versus Commitment KPI. The FinOps scopes page was not read and was dropped. Removed unconfirmed: notice windows and 120/90/60 day alerts, uplift caps, multi-year and payment-term levers, benchmark sources, quarter-end timing, savings baseline policy and the gotchas.
