---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.commitment-renewal
name: commitment-renewal
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, rate-optimization, commitment-renewal, commitment-expiry, auto-renew, queued-purchases, reserved-instances, savings-plans]
level: practitioner
status: docs-checked
description: "Manage commitment expiry and renewal: an expiry calendar, re-sizing on current usage, queued and auto-renew purchases, and avoiding on-demand gaps after expiry."
sources: ["https://docs.aws.amazon.com/savingsplans/latest/userguide/queued-sp-cart.html", "https://docs.aws.amazon.com/savingsplans/latest/userguide/queue-sp-replace.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ri-market-concepts-buying.html", "https://learn.microsoft.com/azure/cost-management-billing/reservations/reservation-renew", "https://cloud.google.com/compute/docs/instances/signing-up-committed-use-discounts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Commitment expiry and renewal management

Commitments expire silently; the day after, covered usage reverts to on-demand and the bill jumps.
Renewal is also the best moment to re-size, since usage has changed since purchase.

## Steps
1. **Expiry calendar**: list every commitment (id, type, scope, hourly value / quantity, end date,
   auto-renew flag) from provider APIs:
   - AWS: `aws savingsplans describe-savings-plans --states active`,
     `aws ec2 describe-reserved-instances --filters Name=state,Values=active`, plus the equivalent
     commands for other services that sell reserved capacity.
   - Azure: `az reservations reservation-order list`.
   - GCP: `gcloud compute commitments list`.
   Alert at 90, 60 and 30 days before end.
2. **Re-size at renewal**: compute the current usage floor (hourly, last 30-90 days) for the scope;
   renew only the part still needed, possibly in a more flexible form (e.g. replace EC2 Instance SP
   with Compute SP, RIs with savings plans).
3. **Stagger**: split large renewals into tranches with different end dates so future decisions
   are smaller and risk is spread.
4. **Avoid gaps**:
   - AWS Savings Plans support **queued purchases** up to three years ahead; the Inventory page has
     a Renew Savings Plan action that queues a same-configuration plan starting one second after the
     old one expires, charged at the current rate. A queued plan must pass validation and be invoiced
     in the same calendar month (UTC) as its start date, or it is marked payment-failed and
     discounts nothing. Regional EC2 RIs can also be queued up to three years ahead (not zonal RIs or
     RIs from other sellers) and the queue can be cancelled before its time.
   - Azure reservations have an **auto-renew** setting, on by default at purchase. The renewal
     inherits SKU, region, scope, term and quantity but you can change quantity, billing frequency
     and term. Renewal price is visible 30 days before expiry, and if it changes after you lock it the
     renewal is not processed. You can change the setting up to 48 hours before expiry; an expired
     reservation cannot be renewed.
   - GCP resource-based commitments can be set to auto-renew (not software licence commitments);
     each renewed term matches the plan length (1 or 3 years).
5. **Approve** renewals in the same process as new purchases (see `commitment-policy`).
6. **After expiry**, confirm coverage did not drop on the day.

## Gotchas
- Auto-renew and AWS Renew Savings Plan repeat the old configuration, which may no longer match usage.
- Azure cancels a pending renewal if you split, merge or transfer the reservation, and may not
  process it if payment fails or the SKU is no longer active; you get an email in that case.
- Renewing a 3-year commitment just before a planned migration strands it; check roadmaps.
- Expiring commitments inflate next month's forecast if forgotten; include renewals in forecasts.

## Verify
- [ ] No commitment expires without a recorded decision (renew, resize, let lapse).
- [ ] Coverage chart shows no dip at expiry dates.

## Checked
2026-11-08. Confirmed on the AWS Savings Plans pages (Queuing a Savings Plan purchase, Renewing a Savings Plan), the EC2 Reserved Instance purchase page (queued purchases), the Azure reservation renewal page and the Compute Engine committed use discount purchase page (auto-renewal). The four listing commands were checked against the botocore model and CLI references (all exist with the flags shown).
Removed: RDS/ElastiCache queue claims, the "savings plans in Cost Management" listing pointer, the claim that GCP and AWS RIs have an auto-renew setting. The 90/60/30 day alerts, tranche staggering and re-sizing advice are practice guidance, not vendor claims.
Method: documentation only; no commands were run.
