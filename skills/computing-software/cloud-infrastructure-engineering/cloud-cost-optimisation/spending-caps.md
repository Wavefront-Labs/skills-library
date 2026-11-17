---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.spending-caps
name: spending-caps
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, budgeting, spending-caps, hard-limits, budget-actions, sandbox-accounts, cost-guardrails]
level: practitioner
status: docs-checked
description: "Implement spending caps where the platform allows: AWS budget actions, the Azure spending limit, Google billing-disable on budget notifications, and their gaps."
sources: ["https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-controls.html", "https://cloud.google.com/billing/docs/how-to/disable-billing-with-notifications", "https://learn.microsoft.com/azure/cost-management-billing/manage/spending-limit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spending caps

Most cloud budgets are soft: they alert and the bill keeps growing. True caps exist only in a few
places, and each has side effects. Use them for sandboxes, training, hackathons and prepaid
experiments.

## What exists
- **AWS**: AWS Budgets can run an action automatically or after manual approval when a cost or
  usage threshold is crossed. Actions apply an IAM policy or a service control policy (SCP), or
  target specific EC2 or RDS instances. An SCP means nothing new needs provisioning during the
  budget period. From the management account you can apply an SCP to another account but you
  cannot target EC2 or RDS instances in another account. Several actions can fire at one threshold
  (for example a Deny IAM policy plus targeting instances). This limits new provisioning; it is
  not a hard billing cap, and running services keep charging.
- **Azure**: the **spending limit** is on by default for free accounts and subscription types with
  credits over multiple months. It equals the credit amount and cannot be customised. When it is
  reached, deployed services are disabled for the rest of the billing period (VMs stopped and
  de-allocated, storage read-only). It is not available on pay-as-you-go or commitment-plan
  subscriptions, and it does not prevent all charges (see the page's list of exceptions). Settings
  such as virtual IP addresses can be lost when resources de-allocate.
- **Google Cloud**: budgets send notifications. Google's tutorial wires them to a function that
  **disables billing on the project**, terminating all services including free-tier ones;
  resources might be irretrievably deleted. You cannot disable billing on a project locked to its
  billing account. For a gentler response, Google points to controlling resource usage with
  notifications.

## Steps
1. Define cap classes: sandbox (hard stop), training/hackathon (hard stop and auto-delete), dev
   (stop compute), production (no hard cap, alert and escalate).
2. Sandboxes: dedicated account/subscription/project per user or team, with a budget action that
   restricts new resources and stops instances at the threshold; a reaper for expired resources.
3. Tell users the cap and what happens when it trips; provide an extension request path.

## Gotchas
- Cost data arrives with a delay, so caps trip late; Google warns the tutorial does not guarantee
  you stay under budget, and suggests setting the budget below your available funds.
- Stopping compute does not stop storage, snapshots, IPs or managed databases; include a cleanup step.
- Never attach destructive caps to production or shared projects.

## Verify
- [ ] Each sandbox has a tested cap and an owner informed of behaviour.
- [ ] Production scopes are excluded from destructive actions by explicit filter.

## Checked

Method: docs-checked 2026-11-09 against AWS budget actions page, Azure spending limit page (first 40 lines) and Google disable-billing-with-notifications page (opening and limitations). Removed unconfirmed: "no native hard cap on AWS" as a blanket statement, EA/MCA cap wording, AI API per-key limits, quotas as caps, project label cap=hard, GPU overshoot claim.
