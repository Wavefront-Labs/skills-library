---
id: computing-software.cloud-infrastructure-engineering.terraform.plan-json-schema-with-show-json
name: plan-json-schema-with-show-json
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, show-json, plan-json-schema, resource-changes, terraform-show, plan-json, jq, after-unknown, before-sensitive, policy-input]
level: practitioner
status: verified
description: "Navigate terraform show -json plan output: resource_changes actions, before/after/after_unknown/after_sensitive, prior_state and configuration blocks, with jq recipes for review and policy."
sources: ["https://developer.hashicorp.com/terraform/internals/json-format", "https://developer.hashicorp.com/terraform/cli/commands/show"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plan JSON schema with `show -json`

**Goal:** extract exactly what a plan will do, programmatically, from the
versioned JSON representation instead of the text UI.

## 1. Produce it
```bash
terraform plan -out=tfplan
terraform show -json tfplan > plan.json
terraform show -json            # current STATE as JSON (no plan file) — different top-level shape
```
`format_version` was `"1.2"` for the plan JSON and `"1.0"` for the state JSON in 1.17.0;
parsers should accept any `1.*`. The state JSON has `values`, `checks` and no `planned_values`.

## 2. Top-level keys
| Key | Content |
|---|---|
| `terraform_version` | version that made the plan |
| `variables` | input values (`{name: {value}}`) — sensitive ones included in plaintext |
| `planned_values` | full predicted state tree after apply (`root_module.resources[]`, `child_modules[]`) |
| `resource_changes[]` | the diff, one entry per resource instance |
| `resource_drift[]` | changes detected during refresh (outside Terraform) |
| `output_changes` | per output: `actions`, `before`, `after` |
| `prior_state` | state before the plan (same shape as `show -json` state) |
| `configuration` | parsed config: provider configs, module calls, expressions with `references` |
| `relevant_attributes` | present only for some plans (absent in the plan below) |
| `checks` | results of check blocks / conditions |
| `timestamp`, `applyable`, `complete`, `errored` | plan status flags (all four present in 1.17.0) |

## 3. `resource_changes[]` entry
All of this was produced by one plan (`-var ver=2 -replace=terraform_data.byreq`, a tainted
resource, a `removed` block, a `create_before_destroy` resource, a deleted local file) in
Terraform 1.17.0; keys of `change` are `actions`, `after`, `after_sensitive`,
`after_unknown`, `before`, `before_sensitive` (plus `replace_paths` when set):
```json
{ "address": "terraform_data.rep", "mode": "managed", "type": "terraform_data", "name": "rep",
  "provider_name": "terraform.io/builtin/terraform",
  "change": { "actions": ["delete","create"],
              "after_sensitive": { "input": true },
              "replace_paths": [["triggers_replace"]] },
  "action_reason": "replace_because_cannot_update" }
```
- `actions` seen: `["no-op"]`, `["create"]`, `["delete","create"]` (replace, destroy first),
  `["create","delete"]` (create_before_destroy) and `["forget"]` (a `removed` block with
  `destroy = false`). `["update"]`, `["read"]` and `["delete"]` are the other standard values.
- `after_unknown` mirrors `after` with `true` where the value is known after apply.
- `after_sensitive` tells you which `after` values are masked in text output;
  the JSON itself contains the real values (`.variables.pw.value` was `pw1`).
- `replace_paths` lists the attributes that forced replacement; it is **null/absent** for
  `-replace` and tainted replacements, so guard it in jq (`// []`).
- `action_reason` seen: `replace_by_request` (`-replace`), `replace_because_tainted`,
  `replace_because_cannot_update`, `delete_because_no_resource_config` (the `forget`).
  The full list of reasons is in the Terraform JSON output docs.
## 4. jq recipes
```bash
# summary by action  ->  {"create":1,"create,delete":1,"delete,create":3,"forget":1,"no-op":4}
jq -r '[.resource_changes[].change.actions|join(",")] | group_by(.) | map({(.[0]): length}) | add' plan.json
# every replacement with the attribute that caused it
jq -r '.resource_changes[] | select(.change.actions|index("delete")) | select(.change.actions|index("create"))
  | "\(.address)\t\((.change.replace_paths // [])|map(join("."))|join(","))\t\(.action_reason)"' plan.json
# deletes of one resource type (swap in your stateful types)
jq -r '.resource_changes[] | select(.change.actions==["delete"]) | select(.type|test("terraform_data")) | .address' plan.json
# drift (the deleted local file showed as local_file.drift  delete)
jq -r '.resource_drift[]? | "\(.address)\t\(.change.actions|join(","))"' plan.json
# which variables fed a resource (configuration.references)
jq '.configuration.root_module.resources[] | select(.address=="terraform_data.rep") | .expressions' plan.json
```
The last query returned `{"input":{"references":["var.pw"]},"triggers_replace":{"references":["var.ver"]}}`.
The summary counts matched the text line `Plan: 5 to add, 0 to change, 4 to destroy.`
## Gotchas
- `plan.json` contains sensitive variable and attribute values in plaintext; do
  not upload it as a public artefact.
- `planned_values` omits attributes unknown until apply; look in `after_unknown`.
- Instances from `for_each` have `index` as a string (`"k"`), from `count` an integer (`0`);
  `address` already includes `["key"]`/`[0]`.
- Nested module resources live in `planned_values.root_module.child_modules[]`
  recursively, but `resource_changes` is **flat** (`module.db.terraform_data.m` has
  `module_address`) — use it for diffs.
- `show -json` for a **state** has `values.root_module` under `values`, not
  `planned_values`; parsers often confuse the two.

## Verify
- [ ] `jq .format_version plan.json` starts with `1.`.
- [ ] Sum of action counts from jq equals the `Plan: X to add, Y to change, Z to destroy` line.
- [ ] A `-replace=` plan shows `action_reason: replace_by_request` for that address (ran).

## Checked
- Terraform 1.17.0 with `terraform_data` and `hashicorp/local`: one plan combining `-replace`, a tainted resource, a `create_before_destroy` resource, a `removed` block (`forget`), a module call, a for_each and a count resource, a deleted local file (drift), a failing check and an output change; `show -json tfplan` read with jq 1.8.2 for every key, recipe and number in the skill, plus `terraform show -json` on state (`format_version` 1.0).
- Corrections: `replace_paths` is null for `-replace` and tainted replacements (the original replacement recipe failed with `Cannot iterate over null`); the plan JSON is `format_version` 1.2; `relevant_attributes` was absent. Removed the AWS examples, the unrun action_reason entries and the OpenTofu sentence.
