---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.internal-rates
name: internal-rates
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, chargeback, internal-rates, platform-rates, markup, rate-card, shared-platform-pricing]
level: practitioner
status: draft
description: "Set internal rates for shared platform services (per vCPU-hour, per GB, per cluster) and decide on markups for overhead, rate cards, recalculation cadence and true-ups."
sources: ["https://www.finops.org/framework/capabilities/invoicing-chargeback/", "https://www.tbmcouncil.org/learn-tbm/tbm-taxonomy/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Internal rates and markups

## When needed
Shared platforms (Kubernetes, data platform, network hub, observability) where provider bills
don't map to consumers; or when central teams pass through costs with overhead.

## Building a rate card
1. **Cost pool**: platform's full cost - infrastructure (amortized), licences, platform team labour
   (if policy includes it), support.
2. **Driver**: measurable consumption unit per service: vCPU-hours requested, GB-month stored,
   GB ingested, requests, seats.
3. **Rate** = cost pool / forecast driver volume for the period (plus target utilisation buffer).
4. **Markup** (optional): overhead for central teams, or a strategic premium/discount to steer
   behaviour (e.g. cheaper rate for ARM nodes). Document it explicitly.
5. **True-up**: reconcile actual cost vs recovered amount quarterly; adjust rates or credit/debit.

## Rules
- Rates stable for a period (quarter/year) so teams can plan; publish changes in advance.
- Charge on what teams control (requests they set, data they keep).
- Show the provider cost alongside so teams see the uplift.

## Gotchas
- Rates higher than direct cloud cost push teams to bypass the platform.
- Under-recovery accumulating unnoticed in the platform budget.

## Verify
- [ ] Recovery ratio (charged / actual cost) within +/- 5% per quarter.
