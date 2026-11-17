---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.enterprise-discount-program
name: enterprise-discount-program
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, rate-optimisation, enterprise-discount-program, negotiated-discounts, contract-negotiation, cloud-procurement]
level: advanced
status: docs-checked
description: "Prepare for cloud discount negotiations with FinOps Framework guidance: demand-based sizing, procurement collaboration, option comparison and commitment tracking."
sources: ["https://www.finops.org/framework/capabilities/rate-optimization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Negotiated cloud discounts

The FinOps Framework Rate Optimization capability lists negotiated discounts alongside commitment discounts and
other pricing mechanisms. Its activities include supporting negotiated discounts and fostering collaboration between
Procurement and other personas. Programme names and terms differ per vendor and are not covered on the page.

## Prepare
1. **Understand demand**: the Framework wants Procurement working with FinOps to understand likely demand over time
   when purchasing and negotiating. Forecast per year and test scenarios; choose the commitment level yourself.
2. **Compare options before signing**: compare pricing, commitment, marketplace and BYOL options against validated
   demand (Framework Walk behaviour).
3. **Inventory** existing commitments (resource-based such as RIs and CUDs, spend-based such as Savings Plans) and
   confirm with the vendor how they interact with the agreement.
4. **Treat it as an investment**: the Framework views commitment purchases as investments whose cost is the whole
   commitment period and whose return is the savings.

## Terms to raise
Ask the vendor how shortfall, marketplace purchases, credits and renewal work; the Framework does not specify these,
so confirm in the contract rather than assuming. Involve Procurement and Legal.

## Operate
- Track utilisation and alert when commitments decline or stop being used (Framework Walk behaviour).
- Notify stakeholders about expiring commitments in time to plan a new purchase.
- Spreading commitment purchases so some always expire lets you re-evaluate at intervals (Framework Run example).
- Compare commitment data across providers where FOCUS contract commitment data is available.

## Verify
- [ ] Commitment size is justified from forecast demand, with the reasoning recorded.
- [ ] Burn-down or utilisation is reported to Procurement and Finance regularly.

## Checked
Confirmed on the FinOps Framework Rate Optimization page: negotiated discounts, Procurement collaboration,
pre-purchase comparison, commitment as investment, utilisation alerting, expiry notice, staggered expiry, FOCUS
contract commitments. Removed: the 1-5 year term, committing near the low scenario, the shortfall and marketplace
burn-down claims, the negotiation term list, the 6-9 month renewal lead time, and the Azure and AWS Marketplace
sources (unreadable). The page's own numeric targets (utilisation, ROI, break-even) were not carried over.
Method: docs-checked 2026-11-09 against finops.org Framework Rate Optimization capability page
