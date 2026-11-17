---
id: computing-software.cloud-infrastructure-engineering.terraform.blast-radius-review-and-pr-sizing
name: blast-radius-review-and-pr-sizing
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, blast-radius-review, pr-sizing, code-review, plan-json, change-management, codeowners, stateful-resources]
level: advanced
status: docs-checked
description: "Size Terraform PRs and review their blast radius: count and classify plan actions from the plan JSON, flag deletes and replacements, and separate drift from intended changes."
sources: ["https://developer.hashicorp.com/terraform/internals/json-format", "https://developer.hashicorp.com/terraform/cli/commands/show", "https://developer.hashicorp.com/terraform/cli/commands/plan"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blast radius review and PR sizing

The diff in git is not the change; the plan is. Review what the plan touches, how
much of it, and what cannot be recreated.

## 1. Measure the plan, not the diff
```bash
terraform plan -out=tfplan && terraform show -json tfplan > plan.json
jq -r '.resource_changes[] | select(.change.actions != ["no-op"])
       | "\(.change.actions | join(","))\t\(.address)"' plan.json | sort | uniq -c | sort -rn
```
- `terraform plan -out=FILE` saves the plan; `terraform show -json FILE` prints the plan,
  configuration and current state as JSON (the format is documented as "JSON Output
  Format"). A saved plan file contains your full configuration and all values associated
  with planned changes, and sensitive data is saved in cleartext in it; `show -json`
  also displays sensitive values in plain text. Treat both files as sensitive.
- `resource_changes` lists every resource in the configuration, one element per instance
  object, so filter out `["no-op"]`. Each element has `address` and a `change` object
  whose `actions` is one of: `["no-op"]`, `["create"]`, `["read"]`, `["update"]`,
  `["delete","create"]`, `["create","delete"]` or `["delete"]`.
- The two replace forms are written as pairs so a caller can scan the list for `"delete"`
  to recognise all three situations where the object will be deleted:
```bash
jq '[.resource_changes[] | select(.change.actions | index("delete"))] | length' plan.json
```
- For a replacement, `change.replace_paths` lists the attribute paths that caused it
  (omitted if no path caused it, for example a tainted resource). `action_reason` gives
  optional context such as `replace_because_tainted`, `replace_because_cannot_update`,
  `replace_by_request` or `delete_because_no_resource_config`; the docs say these are
  display hints, that the set may change, and callers must tolerate unknown reasons.
- `resource_drift` holds changes Terraform detected between the prior saved state and
  the most recent state, in the same structure as `resource_changes`; `relevant_attributes`
  lets you filter drift to what affected the plan.

Review each deletion and replacement deliberately: confirm intent, and for objects that
cannot be recreated (databases, buckets, keys) have a recovery plan before approving.

## 2. Sizing
- Other changes to the target system after a plan was made can change the effect of a
  configuration change, so the plan docs say to re-check the final non-speculative
  plan before applying. Re-plan after rebasing a branch.
- The plan docs say `-target` is for exceptional circumstances (recovering from mistakes,
  working around Terraform limitations), not routine use, because it can lead to
  undetected configuration drift. For very large configurations they recommend
  splitting into smaller configurations that can each be applied independently.

## 3. Review questions
1. Does the plan match the PR description, with nothing extra?
2. Do `resource_drift` entries (external changes) need their own decision?
3. Which items in the `actions` list contain `"delete"`, and why?

## Checked
Date: 2026-11-07

Read: the Terraform `show` page in full, the `plan` page in full, and from the JSON output format page the `resource_changes`, `resource_drift`, `relevant_attributes`, `output_changes` and "Change Representation" sections (lines 90-224 and 520-595 of the stripped text); the rest of that page (state values, configuration, provider schema sections) was not read. No code tabs were present.

Trimmed as unconfirmed: the "delete,create vs create,delete" review recipe beyond what the page says; stateful-type list and second-reviewer rule; one-intent-per-PR and per-environment rollout rules; "moved/import/removed blocks only" refactor PRs and the zero-diff expectation; thresholds and the `::warning::` CI snippet; CODEOWNERS and `prevent_destroy` advice (their pages were not read, so both are removed from `sources`); truncated-comment and "`-target` hides blast radius" gotchas; all Verify items.

Method: documentation only; no commands were run.
