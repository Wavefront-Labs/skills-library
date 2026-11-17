---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.budget-alerts
name: budget-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cloud-budgeting, budget-alerts, aws-budgets, budget-actions, azure-budgets, action-groups, gcp-budgets, pubsub-budget-notifications, forecasted-alerts]
level: practitioner
status: docs-checked
description: "Configure budget alerts and automated actions on AWS, Azure and GCP: actual vs forecasted thresholds, routing, and safe automated responses (stop non-prod, apply deny policies)."
sources: ["https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-controls.html", "https://learn.microsoft.com/azure/cost-management-billing/costs/tutorial-acm-create-budgets", "https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications", "https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-create.html", "https://cloud.google.com/billing/docs/how-to/budgets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Budget alerts and automated actions

## Thresholds
Illustrative per-team set (choose your own): forecasted 100% (early warning), actual 80%, actual 100%,
actual 120%. Forecasted alerts give the most lead time. Azure alert limits accept 0.01% to 1000% of the
budget, and allow up to five thresholds per budget. GCP forecasted alerts are not available on budgets
with a custom time range.

## AWS Budgets
- Create a cost budget, optionally scoped through a billing view across the accounts in your organisation.
- **Budget actions**: apply an IAM policy or an SCP (e.g. a custom Deny policy that restricts
  provisioning more EC2 resources) or target specific EC2 or RDS instances, automatically or after
  manual approval. From the management account you can apply an SCP to another account but cannot target
  EC2 or RDS instances in another account. Use only in sandboxes/non-prod.
```bash
aws budgets create-budget --account-id 111122223333 --budget file://budget.json \
  --notifications-with-subscribers file://notifications.json
```

## Azure
Budgets at management group, subscription or resource group scope (plus billing scopes) with filters.
Alert type is actual or forecasted. Budgets only notify; resources are not affected and consumption is
not stopped. **Action groups** (subscription and resource group scopes only) can trigger
automation such as Azure Functions or webhooks. Budget evaluation uses actual cost, not amortised cost.
Notifications are normally emailed within an hour of the evaluation.

## GCP
Budgets on a billing account can be scoped to services and to one label (label scope is billing-account
level only); thresholds can trigger on actual or forecasted spend. **Programmatic notifications to Pub/Sub**
can drive automation such as disabling Cloud Billing on a project, but an alerts-only budget does not cap
spend by itself. Pub/Sub delivery is at-least-once, can arrive out of order, and misconfiguration failures
do not notify you. Read Google's "Disable billing usage with notifications" example before using it.

## Rules for automated actions
- Prod: alert only, never auto-stop.
- Sandbox/dev: auto-stop or deny-new-resources at 100-120%, documented and agreed upfront.
- Budget data lags: Azure cost data is typically available within 8-24 hours and budgets are evaluated
  every 24 hours; the first GCP Pub/Sub notification can take several hours. Pair with usage alerts.

## Verify
- [ ] Every team budget has forecasted + actual alerts routed to a team channel.
- [ ] Sandbox action tested end to end.

## Checked
Date: 2026-11-08. Confirmed against AWS "Configuring budget actions" and "Creating a budget", the Azure budgets
tutorial, and the Google Cloud budgets and programmatic notifications pages; the CLI command shape matched the
AWS CLI model. Removed unconfirmed AWS claims (tag and cost category scope, amortised option, SNS and Chatbot
delivery) and the claim that disabling billing deletes resources. The 80/100/120 percent set is labelled illustrative.
Method: documentation only; no commands were run.
