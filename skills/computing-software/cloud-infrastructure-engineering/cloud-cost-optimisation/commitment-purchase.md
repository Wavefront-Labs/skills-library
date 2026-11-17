---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.commitment-purchase
name: commitment-purchase
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, rate-optimisation, commitment-purchase, savings-plans, reserved-instances, committed-use-discounts, azure-savings-plan, break-even, payment-options, purchase-recommendations]
level: advanced
status: docs-checked
description: "Size and buy a commitment using FinOps Framework guidance: usage before rate, instrument types, term, break-even and ROI tests, staggered purchases."
sources: ["https://www.finops.org/framework/capabilities/rate-optimization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Commitment purchase analysis

## Steps
1. **Evaluate consistently running usage** that a given discount can cover, and set a purchasing
   strategy to reach coverage or effective savings rates suited to the variability and
   financial posture of your usage.
2. **Pick the instrument**: resource-based (Reserved Instances, Committed Use Discounts) or
   spend-based (Savings Plans), usually over 1 or 3 years. The page says discounts are higher
   the more restrictive the mechanism: a 3-year commitment to one size in one geography earns
   more than a 1-year spend commitment across many compute types and geographies.
3. **Usage optimisation versus rate**: ideally do usage optimisation first, but do not wait for
   usage to be fully optimised, because that almost always costs more than a balanced approach.
   A commitment is a coupon, not a resource, so if nothing matching runs you still pay.
4. **Test the purchase**: the Framework lists returns above 10 percent and a break-even within 9
   months as risk mitigation, and says to view the commitment as an investment whose cost is
   the full term. Arithmetic check: a commitment at discount d beats on-demand only if
   utilisation exceeds 1 minus d.
5. **Supplement the analysis** with planned infrastructure changes and any negotiated enterprise
   discounts, and consider interruptible, batch and highly variable usage.
6. **Stagger purchases** over the year so some commitment is always expiring and levels can be
   re-evaluated against forecast usage.
7. **Compare recommendations**: provider and tool recommendation engines exist; compare ones
   from different approaches and treat them as inputs, not decisions. Finance models
   prepayment and pre-approvals; the central FinOps team coordinates the purchase.

## Verify
- [ ] Break-even and return were checked against the organisation's thresholds before purchase.
- [ ] Utilisation and effective savings rate are tracked after purchase.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Rate Optimization capability page (read through the KPI section). The AWS, Azure and Google Cloud purchase-recommendation sources were not readable and were dropped. Removed unconfirmed: the 30-90 day baseline and percentile rule, provider instrument tiers by service, payment option effects, lookback windows for native recommendations, the 95 percent utilisation target and the approval packet contents.
