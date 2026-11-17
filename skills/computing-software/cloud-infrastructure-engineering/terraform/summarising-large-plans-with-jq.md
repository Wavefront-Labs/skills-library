---
id: computing-software.cloud-infrastructure-engineering.terraform.summarising-large-plans-with-jq
name: summarising-large-plans-with-jq
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, plan-summary-jq, show-json, resource-changes, plan-review, jq]
level: practitioner
status: verified
description: "Turn a 5,000-line plan into a reviewable summary with jq over show -json: counts by action and type, destroys and replaces, and changed attributes per resource."
sources: ["https://developer.hashicorp.com/terraform/internals/json-format", "https://developer.hashicorp.com/terraform/cli/commands/show", "https://jqlang.github.io/jq/manual/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Summarising large plans with jq

```bash
terraform plan -out=tfplan -input=false
terraform show -json tfplan > plan.json
```

## Counts by action
```bash
jq -r '[.resource_changes[] | .change.actions | join("/")] | group_by(.) |
  map("\(length)\t\(.[0])") | .[]' plan.json
# 412  no-op
#   3  create
#   1  delete/create
```

## Only things that change, grouped by type
```bash
jq -r '.resource_changes[] | select(.change.actions != ["no-op"])
  | "\(.change.actions|join("/"))\t\(.type)\t\(.address)"' plan.json | sort | column -t
```

## Dangerous set
```bash
jq -r '.resource_changes[] | select(.change.actions | index("delete"))
  | "\(.address)  replace_paths=\(.change.replace_paths // [] | tostring)"' plan.json
```
`replace_paths` is an array of attribute paths (for example `[["triggers_replace"]]`) forcing
replacement (the JSON form of `# forces replacement`). A normal replace has actions
`["delete","create"]`; with `create_before_destroy` the order is `["create","delete"]`, so
`join("/")` prints `create/delete` and the counts above gain a separate bucket; `index("delete")`
catches both.

## Which attributes change per updated resource
```bash
jq -r '.resource_changes[] | select(.change.actions==["update"]) | .address as $a
  | .change as $c | ($c.after|keys[]) as $k
  | select($c.before[$k] != $c.after[$k]) | "\($a).\($k)"' plan.json
```
Unknown values are absent from `.change.after` and appear in `.change.after_unknown` as
`true`, so iterating only `$c.after|keys` never lists them. To include known-after-apply
attributes, iterate the union of both key sets:
```bash
jq -r '.resource_changes[] | select(.change.actions==["update"]) | .address as $a
  | .change as $c | ((($c.after // {})|keys) + (($c.after_unknown // {})|keys) | unique[]) as $k
  | select(($c.before[$k] != $c.after[$k]) or ($c.after_unknown[$k] == true))
  | "\($a).\($k) (unknown=\($c.after_unknown[$k] // false))"' plan.json
```

## Drift and moves
```bash
jq -r '.resource_drift[]? | "drift: \(.address) \(.change.actions|join("/"))"' plan.json
jq -r '.resource_changes[] | select(.previous_address) | "moved: \(.previous_address) -> \(.address)"' plan.json
```

## CI summary block
Pipe the counts and dangerous set into `$GITHUB_STEP_SUMMARY` or a PR comment; keep
the full plan as an artifact.

## Gotchas
- `plan.json` contains sensitive values in clear text; do not post it.
- `resource_changes` includes data source reads (`mode == "data"`); filter with
  `select(.mode=="managed")` for counts.
- `.change.before` is null for creates; guard with `// {}`.

## Verify
- [ ] Summary counts equal the `Plan: X to add, Y to change, Z to destroy` line (replace = 1 add + 1 destroy).

## Checked
- Terraform 1.17.0, `terraform_data` resources (no-op, update, replace via `triggers_replace`, create, delete): `show -json tfplan` gave `.resource_changes` with each snippet's output as documented: counts `1 create / 1 delete / 1 delete/create / 1 no-op / 1 update`, matching `Plan: 2 to add, 1 to change, 2 to destroy`; the dangerous-set query printed `replace_paths=[["triggers_replace"]]` for the replace and `[]` for the plain delete; the moved-resource query printed `moved: old -> new`; `.resource_drift[]?` printed nothing without drift.
- The per-attribute query listed `terraform_data.upd.input` only; `output` is known after apply and was missing until iterating `after_unknown` too (the added query lists `upd.output (unknown=true)`).
- A `create_before_destroy` replacement had actions `["create","delete"]`, `action_reason` `replace_because_cannot_update`.
- The CI summary section is a pointer to `$GITHUB_STEP_SUMMARY`/PR comments and contains no command.
