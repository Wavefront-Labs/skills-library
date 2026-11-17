---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.private-pricing
name: private-pricing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, rate-optimization, private-pricing, enterprise-discount-program, negotiation, macc, commit-spend, procurement]
level: advanced
status: draft
description: "Negotiate and manage private pricing agreements: EDP/PPA, MACC and Google commit contracts, service-specific rates, commitment sizing, credits, and attainment tracking."
sources: ["https://aws.amazon.com/pricing/enterprise/", "https://learn.microsoft.com/azure/cost-management-billing/manage/track-consumption-commitment", "https://cloud.google.com/billing/docs/how-to/manage-commitments", "https://www.finops.org/framework/capabilities/rate-optimization/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Private pricing agreements

Above a certain spend, providers negotiate: an overall discount for a committed spend over 1-5
years (AWS Enterprise Discount Program / Private Pricing Addendum, Azure MACC, Google Cloud
commitment agreements), plus service-specific private rates (data transfer, CDN, storage, support).

## Preparing
1. **Forecast** 1-5 years of spend per provider with low/expected/high, including migrations,
   AI growth and planned optimisation (do not commit to waste you will remove).
2. **Commit level**: typically to the low-to-expected case; shortfall terms (paying the difference)
   make over-commitment expensive.
3. **What counts**: confirm which spend counts towards attainment: marketplace purchases (often
   partly), support, savings plans and RIs (usually yes), credits (usually no).
4. **Ask list**: overall discount tiers by commit level and term; service-specific rates for your
   top usage types (egress, CDN, S3, specific instances); migration credits and funding programmes;
   training/support credits; ramped commitments (lower year 1); flexibility to move spend between
   years; price protection.
5. **Competitive tension and timing**: provider fiscal year-ends and quarter-ends matter; credible
   alternatives (multi-cloud, repatriation) improve terms.

## Managing after signing
- Track attainment monthly vs commitment curve (Azure: MACC tracking in Cost Management; AWS:
  account team reports / Billing; GCP: commitment management in Billing).
- Check discounts appear correctly on invoices (e.g. CUR line types EdpDiscount,
  PrivateRateDiscount) - reconcile monthly.
- Shortfall risk: pull forward planned spend, buy commitments or marketplace that counts.
- Renewal prep starts 6-9 months before end.

## Gotchas
- Discounts usually apply to list price and stack with commitments differently by provider; model
  the combined effective rate, not headline percentages.
- Excluded services (marketplace, some third-party) surprise teams at attainment review.
- Signing up to a big commit removes leverage to move workloads; keep exit plans realistic.

## Verify
- [ ] Attainment tracked monthly with forecast to term end.
- [ ] Negotiated rates verified on invoices each month.
