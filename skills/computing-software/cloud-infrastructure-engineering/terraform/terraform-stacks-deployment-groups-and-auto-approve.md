---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-stacks-deployment-groups-and-auto-approve
name: terraform-stacks-deployment-groups-and-auto-approve
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, deployment-group, orchestrate-rule, deployment-auto-approve, terraform-stacks, tfdeploy-hcl, hcp-terraform]
level: practitioner
status: docs-checked
description: "Control Terraform Stacks rollouts with deployment groups and auto-approve rules in tfdeploy.hcl: grouping deployments, context checks on plans, eager plan and failure tolerance."
sources:
  - https://developer.hashicorp.com/terraform/language/stacks/deploy/conditions
  - https://developer.hashicorp.com/terraform/language/stacks/deploy/config
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Deployment groups and auto-approve rules

In Terraform Stacks (HCP Terraform), each `deployment` block in `*.tfdeploy.hcl` is an instance of the stack (for example dev, staging, prod, or per region). A `deployment_group` block groups deployments to share settings and orchestration rules.

Running orchestration rules for deployment groups needs the HCP Terraform Plus Edition (premium tier).

## Groups and auto-approve
```hcl
# deployments.tfdeploy.hcl
deployment_auto_approve "no_changes" {
  check {
    condition = context.plan.changes.total == 0
    reason    = "Plan contains too many changes for automatic approval."
  }
}
deployment_auto_approve "successful_plans" {
  check {
    condition = context.success == true
    reason    = "Operation failed and requires manual intervention."
  }
}

deployment_group "staging_group" {
  auto_approve_checks = [
    deployment_auto_approve.no_changes,
    deployment_auto_approve.successful_plans,
  ]
}

deployment "staging" {
  inputs = { environment = "staging", region = "us-west-2" }
  deployment_group = deployment_group.staging_group
}
```
- A deployment with no explicit group gets an automatically created default group; you cannot define custom rules on default groups.
- Stacks have a default auto-approve rule named `empty_plan` that approves a plan with no changes.
- Rules use a `check` block with `condition` and `reason`; `condition` can read the `context` of the current deployment run (for example `context.plan.changes.total` and `context.success`). See the deployment_auto_approve reference for the full context object.
- Several rules in `auto_approve_checks` combine into stricter conditions.

## Eager plan
By default all deployments start planning immediately, which can exhaust concurrent operation capacity with many deployments. Set `eager_plan = "off"` in a group to stop its deployments planning until you start the group from the UI or API.

## Failure tolerance
By default a group places no limit on failed deployments. `failure_tolerance` sets how many failures the group tolerates before halting the automated rollout, and also limits concurrency: up to `failure_tolerance + 1` deployments apply at a time. `0` means deployments run one at a time (a failure halts the rest); omit it or set `null` for unlimited.

## Verify
- [ ] A staging plan with no changes auto-approves; one with changes waits for a person and shows the rule reason.
- [ ] A group with `failure_tolerance = 0` applies its deployments sequentially.

## Checked

Method: docs-checked 2026-11-09 against the "Set conditions for deployment runs" page (read from the deployment groups section through failure tolerance) and the deployment configuration page (deployment_group description). Dropped unconfirmed claims: the full context.plan fields (remove, add, mode, applyable), the older orchestrate rule syntax, the no implicit dev to prod sequencing note, and the deferred-changes remark. Removed the unread stacks overview source.
