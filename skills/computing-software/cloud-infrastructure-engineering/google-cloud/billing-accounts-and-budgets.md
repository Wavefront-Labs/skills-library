---
id: computing-software.cloud-infrastructure-engineering.google-cloud.billing-accounts-and-budgets
name: billing-accounts-and-budgets
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, billing, billing-account, billing-accounts, billing-export, budgets, billing-budgets, budget-alerts, bigquery-billing-export, cost-allocation, labels, billing-roles, billing-admin, cloud-billing-api, pubsub-budget-notifications, cost-controls]
level: practitioner
status: docs-checked
description: "Set up Google Cloud billing: link projects, billing IAM roles, export usage to BigQuery, and budgets with Pub/Sub notifications that can trigger automation."
sources: ["https://cloud.google.com/billing/docs/how-to/manage-billing-account", "https://cloud.google.com/billing/docs/how-to/export-data-bigquery", "https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables", "https://cloud.google.com/billing/docs/how-to/budgets", "https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications", "https://cloud.google.com/billing/docs/how-to/billing-access", "https://cloud.google.com/billing/docs/how-to/disable-billing-with-notifications", "https://cloud.google.com/sdk/gcloud/reference/billing/budgets/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Billing accounts, budgets and export

**Goal:** every project is linked to the right billing account, only a few named people can
move money, usage lands in BigQuery, and a budget breach triggers something more than an email.

## 1. Account shape
- A billing account is linked to one or more projects and defines who pays for them. A project
  that is not linked to an active billing account cannot use Google Cloud services, even free ones.
- Link a project: `gcloud billing projects link <PROJECT_ID> --billing-account=<ACCOUNT_ID>`;
  list the projects on an account with `gcloud billing projects list --billing-account=<ACCOUNT_ID>`.
- The common onboarding bug is a project creator who has `roles/resourcemanager.projectCreator`
  but not `roles/billing.user` on the account: the two roles together let a user create
  projects linked to that account (`billing.user` carries `billing.resourceAssociations.create`).

## 2. Billing IAM (keep it small)
| Role | Who | Why |
|---|---|---|
| `roles/billing.admin` | 2-3 named humans in a group | owner role: payment methods, exports, link/unlink projects, manage billing IAM |
| `roles/billing.user` | project-factory service account, platform team | link projects (restricted permissions, safe to grant broadly) |
| `roles/billing.viewer` | FinOps, finance | read cost and payment information |
| `roles/billing.costsManager` | FinOps | budgets, cost views and cost export; cannot link or unlink projects |
| `roles/billing.projectManager` | on the *project* | with `billing.user`, link/unlink that project without resource access |

Grant on the billing account (`gcloud billing accounts add-iam-policy-binding`). These roles
can also be set at organization level, where they apply to every billing account in the
organization, so prefer the account.

## 3. Export to BigQuery
Enable the export types you need: **Standard usage cost**, **Detailed usage cost** (adds
resource-level cost data such as the VM or SSD that generated usage) and optionally **Pricing**.
Table names: `gcp_billing_export_v1_<BILLING_ACCOUNT_ID>` (standard),
`gcp_billing_export_resource_v1_<BILLING_ACCOUNT_ID>` (detailed), `cloud_pricing_export` (pricing).
Do not modify or insert into these tables.

- Dataset location: all multi-region locations (EU or US) are supported, only a subset of regions.
  A multi-region dataset is backfilled from the start of the previous month (the first backfill can
  take up to five days); a regional dataset only receives data from the day you enable export, and
  pricing data is never backfilled. The dataset location cannot be changed after creation.
- Export schemas can change, so point dashboards at BigQuery views rather than the raw tables.
- For GKE cost breakdown in the detailed export you must also enable cost allocation for GKE.
- Labels are part of the standard usage cost export; use the "example queries" page for SQL.

## 4. Budgets that do something
```bash
gcloud billing budgets create --billing-account=<ACCOUNT_ID> --display-name="prod-monthly" \
  --budget-amount=10000USD --filter-projects=projects/<PROJECT_ID> \
  --threshold-rule=percent=0.5 --threshold-rule=percent=0.9 \
  --threshold-rule=percent=1.0,basis=forecasted-spend \
  --notifications-rule-pubsub-topic=projects/<PROJECT_ID>/topics/budget-alerts \
  --notifications-rule-monitoring-notification-channels=projects/<PROJECT_ID>/notificationChannels/<CHANNEL_ID>
```
- `percent` is a 0.0 to 1.0 fraction; `basis` is `current-spend` (default) or `forecasted-spend`.
  Forecasted thresholds fire when the cost forecast to the end of the budget period exceeds the
  threshold; budgets with a custom date range cannot alert on forecasted cost.
- Threshold rules drive the alert emails. Default recipients are the billing account's Billing
  Account Administrators and Users; `--notifications-rule-monitoring-notification-channels`
  adds Cloud Monitoring email channels (full resource name, maximum 5).
- Programmatic notifications go to the Pub/Sub topic several times a day. The message includes
  `costAmount` and `budgetAmount`; `alertThresholdExceeded` appears only when you set at least one
  threshold rule and the actual cost has exceeded one.
- A Cloud Run function can disable billing on a sandbox project (Cloud Billing API
  `projects.updateBillingInfo` with an empty `billingAccountName`). This terminates all
  services in the project and resources might be irretrievably deleted; because budget
  notifications are delayed it does not guarantee you stay under budget. Use only on throwaway projects.
- An alerts-only budget does not cap spend. Where the service supports it, a spend cap budget on a
  project pauses the specified services until you lift the cap.

## Gotchas
- Closing a billing account stops all billable services in the projects linked to it; move or
  unlink projects first. Accounts cannot be deleted, only closed.
- A monthly budget keeps tracking costs for the first two days of the next month to catch late usage.
- Set budget amounts below your available funds to allow for usage-reporting delay.

## Verify
- [ ] `gcloud billing projects describe <PROJECT_ID>` shows the project linked to the expected billing account.
- [ ] No principal outside the named group holds `roles/billing.admin` (`gcloud billing accounts get-iam-policy <ACCOUNT_ID>`).

## Checked
Date: 2026-11-07.
Method: documentation only; no commands were run.
Read in full: "Manage your Cloud Billing account", "Export Cloud Billing data to BigQuery", "Understand the Cloud Billing data tables in BigQuery", "Disable billing usage with notifications" (including the script and function code), gcloud reference pages for `billing projects list`, `billing projects describe` and `billing budgets create`, REST `projects.updateBillingInfo`, and the roles table of "Cloud Billing access control" (permission lists for roles were read only for billing.admin, user and projectManager). The "Set budgets" page (about 60 KB) and the budget notifications page were searched by keyword (threshold, forecast, email recipients, spend cap), not read end to end.
Corrections: removed "export is not retroactive" (multi-region datasets backfill from the previous month); removed `_PARTITIONTIME`, the SQL query, `project.labels`, "1-2 day lag", the org policy label constraint, "billing accounts live at organization level", the grace-period claim, the credits/CUD claim and the Slack/PagerDuty claim (Monitoring channels here are email channels); `--filter-projects` now uses the `projects/{project_id}` form from the reference page; "budgets never cap spend" corrected for spend cap budgets; removed the invented test-budget Verify step. The `gcloud billing accounts get-iam-policy` and `add-iam-policy-binding` commands were confirmed to exist by the command checker and the tutorial script, not read page by page.
