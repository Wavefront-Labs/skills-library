---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.budgets-as-code
name: budgets-as-code
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cloud-budgeting, budgets-as-code, terraform-budgets, aws-budgets, azure-consumption-budget, budget-automation]
level: practitioner
status: docs-checked
description: "Manage cloud budgets as code with Terraform: AWS Budgets, Azure consumption budgets and Google billing budgets per team, with thresholds, notifications and actions."
sources: ["https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/budgets_budget", "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/budgets_budget_action", "https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/consumption_budget_subscription", "https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/billing_budget"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Budgets as code

## Why
Budgets created by hand drift from the org structure; code makes them reviewable, consistent and
created automatically with each new account/team.

## AWS
```hcl
resource "aws_budgets_budget" "team" {
  name         = "team-payments-monthly"
  budget_type  = "COST"
  limit_amount = "12000"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"
  cost_filter {
    name   = "TagKeyValue"
    values = ["user:team$payments"]
  }
  notification {
    comparison_operator = "GREATER_THAN"
    threshold                 = 80
    threshold_type            = "PERCENTAGE"
    notification_type         = "FORECASTED"
    subscriber_sns_topic_arns = [aws_sns_topic.finops.arn]
  }
}
```
`notification` takes `comparison_operator` (`LESS_THAN`, `EQUAL_TO`, `GREATER_THAN`), `threshold`,
`threshold_type` (`PERCENTAGE` or `ABSOLUTE_VALUE`), `notification_type` (`ACTUAL` or `FORECASTED`)
and either `subscriber_email_addresses` or `subscriber_sns_topic_arns`. `time_unit` can be `DAILY`,
`MONTHLY`, `QUARTERLY` or `ANNUALLY`. `cost_filter` and `filter_expression` conflict; `cost_filter`
names include `TagKeyValue`, `Service` and `LinkedAccount`.

Budget actions (`aws_budgets_budget_action`) have `action_type` `APPLY_IAM_POLICY`,
`APPLY_SCP_POLICY` or `RUN_SSM_DOCUMENTS`; the SSM definition's `action_sub_type` is
`STOP_EC2_INSTANCES` or `STOP_RDS_INSTANCES`.

## Azure
`azurerm_consumption_budget_subscription` / `_resource_group` / `_management_group` with
`amount`, `time_grain` (default `Monthly`), `notification` blocks (`threshold_type` `Actual` or
`Forecasted`, `operator`, `threshold` as a percent from 0 to 1000, and `contact_emails`,
`contact_groups` or `contact_roles`) and an optional `filter` with `dimension` or `tag` blocks.

## Google Cloud
`google_billing_budget` with `budget_filter` (projects, services, labels, `credit_types_treatment`
and more), `threshold_rules` (`threshold_percent`, `spend_basis` `CURRENT_SPEND` (default) or
`FORECASTED_SPEND`) and an `all_updates_rule` that can name a `pubsub_topic` for automation.

## Steps
1. Source budget amounts from a single table (YAML/CSV) maintained with finance.
2. Generate one budget per team/account via `for_each`.
3. Notifications: forecasted 100% and actual 80/100/120% to team channel.
4. Review amounts each planning cycle via pull request.

## Gotchas
- A budget notifies; it is not a hard cap. Only AWS budget actions (or your own automation on the
  Google Pub/Sub notification) act on a threshold.
- Tag filters only match spend that carries the tag in the provider's cost data; check the
  provider's tag documentation for any activation step.

## Verify
- [ ] Every team/account has a code-managed budget; no hand-made budgets remain.

## Checked
2026-11-08. Confirmed against the provider documentation sources for `aws_budgets_budget`, `aws_budgets_budget_action`, `azurerm_consumption_budget_subscription` (plus its resource group and management group siblings) and `google_billing_budget`, read from the providers' GitHub docs (the registry pages themselves render empty to scripts). The HCL example uses only arguments listed there, including the `user:team$payments` `TagKeyValue` format shown in the AWS examples.
Removed: the "alerts lag billing data by hours" claim and the AWS cost allocation tag activation claim (not stated in the provider docs). The 80/100/120% notification thresholds and the single-table `for_each` workflow are practice guidance. The example was not applied.
Method: documentation only; no commands were run.
