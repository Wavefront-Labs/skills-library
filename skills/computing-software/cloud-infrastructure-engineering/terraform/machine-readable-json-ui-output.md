---
id: computing-software.cloud-infrastructure-engineering.terraform.machine-readable-json-ui-output
name: machine-readable-json-ui-output
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, json-ui, machine-readable-output, apply-json, plan-json, jq, log-streaming, ci-parsing, diagnostics-json, terraform-apply]
level: practitioner
status: verified
description: "Consume terraform plan/apply -json streaming output: message types, parsing with jq, turning diagnostics into CI annotations, and why it beats scraping human output."
sources: ["https://developer.hashicorp.com/terraform/internals/machine-readable-ui", "https://developer.hashicorp.com/terraform/cli/commands/apply#apply-options", "https://developer.hashicorp.com/terraform/internals/json-format"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Machine-readable `-json` UI output

**Goal:** stop regex-scraping "Plan: 3 to add" from coloured text; read the
structured event stream Terraform already emits.

## 1. Enable it
```bash
terraform plan  -json -input=false > plan.ndjson
terraform apply -json -input=false -auto-approve tfplan > apply.ndjson
```
- One JSON object per line (NDJSON). `-json` implies `-no-color` and disables
  prompts, so `-auto-approve` or a saved plan is required.
- Not the same as `terraform show -json tfplan` (a single document describing the
  plan); `-json` on plan/apply is a **log of events**.

## 2. Message types you will use
| `type` | When | Key fields |
|---|---|---|
| `version` | first line | `terraform` (OpenTofu: `tofu`), `ui` (schema version; `"1.3"` on Terraform 1.17.0, `"1.2"` on OpenTofu 1.13.2) |
| `planned_change` | each resource in plan | `change.resource.addr`, `change.action` (create/update/delete/replace/read) |
| `change_summary` | end of plan | `changes.add/change/remove/import`, `changes.operation` |
| `apply_start` / `apply_progress` / `apply_complete` / `apply_errored` | per resource during apply (`apply_progress` is emitted periodically for slow operations) | `hook.resource.addr`, `hook.elapsed_seconds`, `hook.id_value` (`apply_errored` carries the elapsed time; the error text arrives as a separate `diagnostic`) |
| `provision_start` / `provision_progress` / `provision_complete` / `provision_errored` | per provisioner step | `hook.provisioner`, `hook.output` |
| `refresh_start` / `refresh_complete` | state refresh before plan/apply | `hook.resource.addr` |
| `resource_drift` | refresh found drift | `change.resource.addr`, `change.action` |
| `diagnostic` | warnings and errors | `diagnostic.severity`, `summary`, `detail`, `range.filename`, `range.start.line` |
| `outputs` | end of apply | `outputs.<name>.value`, `.sensitive` |

## 3. jq recipes
```bash
# change counts
jq -r 'select(.type=="change_summary") | .changes' plan.ndjson
# addresses that will be destroyed or replaced
jq -r 'select(.type=="planned_change") | select(.change.action=="delete" or .change.action=="replace") | .change.resource.addr' plan.ndjson
# errors as GitHub Actions annotations
jq -r 'select(.type=="diagnostic" and .diagnostic.severity=="error")
  | "::error file=\(.diagnostic.range.filename // "")::\(.diagnostic.summary): \(.diagnostic.detail // "")"' plan.ndjson
# slowest applied resources
jq -r 'select(.type=="apply_complete") | "\(.hook.elapsed_seconds)\t\(.hook.resource.addr)"' apply.ndjson | sort -rn | head
```

## 4. Gates built on it
- Fail the PR if any `planned_change.change.action == "delete"` unless the PR has
  a `destroy-approved` label.
- Alert when `resource_drift` events appear in the nightly plan.
- Persist `apply_complete` timings to spot providers getting slower.

## Gotchas
- `-json` output has no colour and no "Do you want to..." prompt; a human watching
  the CI log sees only JSON — also run `terraform show tfplan` for readability.
- The UI schema version (`ui` in the `version` message) has changed between minor
  releases; pin Terraform in CI and check that field in your parser.
- Sensitive output values appear as `{"sensitive":true,"type":"string"}` with no `value` key
  in the `outputs` message - use `terraform output -json` after apply if you need them (and
  treat the log as secret).
- `terraform validate -json` and `terraform test -json` use **different** schemas
  (`validate` prints one document with `format_version`, `valid`, `error_count`,
  `warning_count`, `diagnostics`; `test -json` streams `version`, `test_abstract`, `test_file`,
  `test_run` and `test_summary` events).
- OpenTofu's stream matches Terraform's for the common types but names its version field
  `tofu` (and `@module` is `tofu.ui`); do not hard-fail on unknown types.

## Verify
- [ ] `jq -s 'map(.type) | unique' plan.ndjson` lists `version`, `planned_change`, `change_summary` (and `diagnostic` if any).
- [ ] Your parser treats an unknown `type` as ignorable, not fatal.
- [ ] A deliberately broken config produces a `diagnostic` line with `range.filename` and the CI annotation points at it.

## Checked
- Terraform 1.17.0 and OpenTofu 1.13.2: `plan -json -out` and `apply -json tfplan` produced NDJSON whose `jq -s 'map(.type) | unique'` listed `change_summary`, `diagnostic`, `outputs`, `planned_change`, `version` (plan) plus `apply_start`, `apply_complete` (apply); the four jq recipes (change counts, delete/replace addresses, GitHub annotation, slowest resources) ran; a failing `local-exec` produced `apply_errored`, `provision_*`, and a `diagnostic` with `range.filename` that the annotation recipe turned into `::error file=main.tf::...`; a forced replacement appeared as `planned_change` with `change.action` `replace`; `apply -json` without a plan or `-auto-approve` returned `Plan file or auto-approve required`; the sensitive-output shape, the validate and test schemas and the OpenTofu differences are as quoted.
- Fetched: the Terraform machine-readable UI page (message type list including `apply_progress`, `resource_drift`, `ui` version semantics).
