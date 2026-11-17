---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.commitment-utilisation
name: commitment-utilisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, rate-optimisation, commitment-utilisation, commitment-coverage, ri-utilisation, savings-plan-utilisation, ri-exchange, ri-marketplace, expiry-tracking]
level: practitioner
status: docs-checked
description: "Keep commitments working: FinOps Framework utilisation and waste KPIs, daily detection of unused commitment, alerts on drops and expiry notice."
sources: ["https://www.finops.org/framework/capabilities/rate-optimization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Commitment coverage and utilisation management

## Measures (FinOps Framework KPIs)
- **Commitment Utilization Score** = (used commitment / total commitment) x 100. Near 100
  percent indicates good forecasting; much lower values signal shelfware; above 100 percent
  means exposure to on-demand rates.
- **Percentage of commitment discount waste** = (cost of unused commitment discount / total
  cost of commitment discount) x 100.
- **Effective savings rate**, which falls with under-utilised commitments and with significant
  usage not covered by discounts.
- Resource-based commitments on steady-state usage: the page names an upper waterline of about
  80 percent utilisation as a KPI.

## Monitoring
1. Identify unused commitment discounts with daily resolution (a stated measure of success).
2. At Walk maturity, alert when commitment utilisation declines, stops, or deviates from norms.
3. Notify stakeholders of expiring commitments early enough to plan a new purchase.
4. From FOCUS data, commitment discount fields (status, type, id) allow the same view across
   providers; the FOCUS spec carries contract commitments in a separate dataset.

## Fixing under-utilisation
1. Find why: usage was rightsized, changed type, moved or retired. The page notes that
   rightsizing recommendations can conflict with commitment purchases, so double counting of
   avoidance is a risk, and that a commitment still costs money if nothing matches it.
2. Where the provider allows it, change the commitment or move matching workloads onto it.
   Provider exchange and refund rules were not verified here; check the provider's current
   documentation.
3. Feed the finding into later purchases, and keep them staggered so expiries come in tranches.

## Verify
- [ ] Utilisation and waste are reported at least daily for unused commitment.
- [ ] Expiring commitments are flagged to owners ahead of the end date.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Rate Optimization capability page (read through the KPI section). The AWS and Azure sources were not readable and were dropped. Removed unconfirmed: the 95 percent utilisation threshold, provider monitoring tool names, RI/SP exchange, modify, sell and refund rules, and the 90/30/7 day expiry calendar.
