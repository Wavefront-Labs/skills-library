---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.commitment-policy
name: commitment-policy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-policy-governance, finops-governance, commitment-policy, rate-optimization, purchase-authority]
level: practitioner
status: docs-checked
description: "Write a commitment purchase policy using FinOps Framework guidance: central ownership, coverage and utilisation measures, break-even and ROI tests, and staggered expiries."
sources: ["https://www.finops.org/framework/capabilities/policy-governance/", "https://www.finops.org/framework/capabilities/rate-optimization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Commitment purchase policy

The Policy and Governance capability lists defining technology and spend-based commitment
policies as a guardrail for making, managing and evaluating commitment-based investments. Its
example policy statement: a defined, organisationally agreed proportion of optimised compute
usage must be covered by a discounted commitment instrument at all times, with coverage targets
reviewed as usage patterns evolve.

## What the policy should cover
1. **Ownership**: the Rate Optimization page says the central FinOps team should be the primary
   driver coordinating purchases of spend-based and resource-based discounts. It may not make
   every purchase (for example resources used by only one or a few applications) but should
   track them all. Analysis should use a holistic view of the estate, not each sub-account.
2. **Instruments in scope**: resource-based (Reserved Instances, Committed Use Discounts) and
   spend-based (Savings Plans) commitments, typically 1 or 3 years. Discounts are higher the
   more restrictive the mechanism.
3. **Targets and measures**: coverage (percentage of optimised usage covered), commitment
   utilisation, effective savings rate, and commitment discount waste. The page's KPIs include
   a utilisation upper waterline of about 80 percent for steady-state resource-based usage.
4. **Purchase tests**: the page lists returns above 10 percent and a break-even within 9 months
   as risk-mitigation measures, and treats a commitment as an investment whose cost is the full
   term and whose return is the savings.
5. **Cadence**: spread purchases over the year so some commitments are always expiring, which
   allows re-evaluation against forecast usage.
6. **Inputs**: consider planned infrastructure changes, negotiated enterprise discounts, and
   Spot or batch usage before sizing.
7. **Approval and risk**: Finance models prepayment, purchase levels and pre-approvals;
   Procurement and Leadership help set the strategy. Record commitment exposure as a risk with
   an owner. Thresholds for who approves what are an organisational choice and are not given
   by the Framework.
8. **Exceptions**: define escalation paths and exception handling, and track exception volume.

## Verify
- [ ] The policy names the purchasing owner, targets and measures above.
- [ ] Purchases and exceptions are recorded and reviewed on a schedule.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Policy and Governance and Rate Optimization capability pages (Rate Optimization read through the KPI section; Policy and Governance searched for commitment, exception and guardrail passages). The AWS Savings Plans source was not readable and was dropped. Removed unconfirmed: 70-80 percent coverage and 95 percent utilisation targets, flexible-first instrument preference, 1-year no-upfront default, dollar approval tiers, 60-day renewal review, auto-renew rule and the gotchas.
