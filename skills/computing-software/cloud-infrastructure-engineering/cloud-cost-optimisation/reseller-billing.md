---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.reseller-billing
name: reseller-billing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, invoicing-and-chargeback, chargeback, reseller-billing, csp, partner-billing, invoice-reconciliation]
level: practitioner
status: draft
description: "Validate cloud bills bought through a reseller or partner: CSP and Solution Provider models, markup and discount checks, missing data access, and invoice reconciliation."
sources: ["https://www.finops.org/framework/capabilities/invoicing-chargeback/", "https://learn.microsoft.com/en-us/partner-center/billing/", "https://docs.aws.amazon.com/billingconductor/latest/userguide/what-is-billingconductor.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reseller / partner billing validation

When cloud is bought through a partner (Microsoft CSP, AWS Solution Provider / Partner-led,
Google Cloud reseller), the invoice comes from the partner and may not match provider list or
contracted prices. You also may lose native data access.

## Know the model
- **Microsoft CSP**: partner bills you; you see costs in Azure Cost Management at retail (pay-as-
  you-go) rates unless the partner enables cost visibility; partner earns margin and may add fees.
- **AWS partner-led accounts**: the partner owns the payer account; AWS Billing Conductor lets the
  partner present pro-forma rates to you, so your CUR shows the partner's pricing, not AWS's.
- **Google Cloud reseller**: billing account under the reseller; check BigQuery export access.

## Steps
1. **Contract terms**: markup or discount on list, which discounts (EDP-like, commitments, credits)
   pass through to you, support fees, payment terms, data access obligations (export of detailed
   usage daily, FOCUS if possible).
2. **Get detailed data**: insist on resource-level daily usage export (CUR via Billing Conductor,
   Azure exports with cost visibility, BigQuery export). Without it, allocation is impossible.
3. **Reprice independently**: usage quantity x list price (provider price list APIs) x contracted
   discount; compare with the partner invoice per service.
4. **Check commitments**: who owns RIs/Savings Plans bought on your behalf and whether the savings
   reach your invoice or stay with the partner.
5. **Credits and promotions**: provider credits (migration programmes, MAP, Azure Migrate offers)
   must be passed through per contract.
6. **Monthly reconciliation** with variance thresholds; raise discrepancies within the contractual
   dispute window.

## Gotchas
- Native tool costs at retail rates make in-tool savings numbers wrong; apply the contracted rate.
- Partner-owned commitments leave with the partner when you switch; plan exit terms.

## Verify
- [ ] Invoice reprices within tolerance from detailed usage and contract rates.
- [ ] Commitment savings and credits are visibly passed through.
