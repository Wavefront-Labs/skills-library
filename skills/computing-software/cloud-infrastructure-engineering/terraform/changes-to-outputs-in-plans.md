---
id: computing-software.cloud-infrastructure-engineering.terraform.changes-to-outputs-in-plans
name: changes-to-outputs-in-plans
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, output-changes, outputs, plan-review, output-values]
level: practitioner
status: gated
description: "Read the Changes to Outputs section of a plan, apply output-only changes, and understand why outputs show known after apply or change when resources do not."
sources: ["https://developer.hashicorp.com/terraform/language/values/outputs", "https://developer.hashicorp.com/terraform/internals/json-format#change-representation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# "Changes to Outputs" in plans

```
Changes to Outputs:
  + api_url       = (known after apply)
  ~ subnet_ids    = [
      - "subnet-0aaa",
      + "subnet-0ccc",
    ]
  - legacy_name   = "web-old" -> null

You can apply this plan to save these new output values to the Terraform state,
without changing any real infrastructure.
```

## Cases
| Plan shows | Meaning |
|---|---|
| Only a `Changes to Outputs:` section and no resource actions | New/renamed/removed outputs; `terraform apply` writes them to state without touching resources (Terraform 1.17.0 prints no `No changes` line for such a plan) |
| `(known after apply)` | Depends on an attribute unknown until apply (new resource, deferred data source) |
| Output changes but no resource diff | Value derives from refreshed data (drift) or a data source returning something new |
| Sensitive output | `~ token = (sensitive value)` |

## Why it matters
- Downstream stacks reading `terraform_remote_state`/`tfe_outputs` see the **state**
  value. Until you apply, a new output does not exist for them.
- HCP Terraform: output-only plans can be applied normally; run triggers then fire for
  downstream workspaces (gated: unconfirmed, source is paywalled or blocked).

## JSON
```bash
terraform show -json tfplan | jq '.output_changes | to_entries[]
  | select(.value.actions != ["no-op"]) | {k: .key, a: .value.actions}'
```
The `select` matters: unchanged outputs are listed too, with `["no-op"]`. Use in CI to flag output contract changes (`delete` on an output that downstream
consumers read = breaking).

## Gotchas
- Removing an output breaks consumers immediately on apply; deprecate first.
- `-target` applies update only outputs whose referenced resources are in the target set; the rest stay stale (ran: targeting `r` updated `r_in`, `s_in` kept its old value).
- `-detailed-exitcode` returns 2 for output-only changes too.

## Verify
- [ ] Output deletions/renames coordinated with consumers.
- [ ] After apply, `terraform output` shows the new values.

## Checked
- Terraform 1.17.0, `terraform_data` only: a plan with one removed, one added and one changed sensitive output printed `Changes to Outputs:` with `-`, `+` and `~ tok = (sensitive value)`, then the quoted "You can apply this plan to save these new output values..." sentence; `-detailed-exitcode` returned 2; `show -json` listed `output_changes` with actions delete, create, update and `no-op` for the unchanged output; a new output of a new resource printed `(known after apply)`; `-target` apply updated only the targeted resource's output.
- Gated: the HCP Terraform run-trigger claim and any `terraform_remote_state`/`tfe_outputs` consumer behaviour were not run (no HCP account).
