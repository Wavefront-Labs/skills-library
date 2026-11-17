---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.terraform-plan-blast-radius-policy
name: terraform-plan-blast-radius-policy
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [terraform, plan-json, opa-exec, blast-radius, policy-as-code]
level: advanced
status: docs-checked
description: "Gate Terraform changes with OPA: terraform show -json, a weighted blast-radius score over resource_changes, opa exec with --decision, and plan-time data limits."
sources:
  - https://www.openpolicyagent.org/docs/terraform
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: auto-approve small Terraform changes and flag large ones before apply.

Pipeline:

```
terraform plan --out tfplan.binary
terraform show -json tfplan.binary > tfplan.json
opa exec --decision terraform/analysis/authz --bundle policy/ tfplan.json
```

`opa exec` prints `{"result": [{"path": "tfplan.json", "result": true}]}`. Ask for `terraform/analysis/score` to see the number behind the decision.

Policy outline (package `terraform.analysis`, `import input as tfplan`):
- parameters: `blast_radius := 30` and per-type weights, for example `"aws_autoscaling_group": {"delete": 100, "create": 10, "modify": 1}`
- `default authz := false`; `authz if { score < blast_radius; not touches_iam }`
- `score` is the sum of weight times the count of creates, deletes and modifies per resource type
- counts come from `tfplan.resource_changes`, filtering `res.change.actions` for `"create"`, `"delete"` and `"update"`

The tutorial plan (one auto-scaling group and one instance created) scores 11 and is authorised; a larger plan exceeds 30 and is not.

To decide per user, wrap the input as `{"user": ..., "plan": ...}` and read `input.user` and `input.plan`.

Plan-time limits: policies see only the JSON plan, so unknown computed values, dynamic blocks and unevaluated function results may be missing. Confirm the field you need appears in the plan JSON before writing the rule.

Check: run against a small plan (expect true), then a plan creating many auto-scaling groups (expect false).

## Checked

The pipeline commands, the weights, the threshold, the score of 11 and the plan-time limitations note were confirmed against the Terraform page.

Method: docs-checked 2026-11-09 against the OPA docs terraform page (docs/docs/terraform.md in the OPA repository, full file read).
