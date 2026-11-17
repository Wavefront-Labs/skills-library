---
id: computing-software.cloud-infrastructure-engineering.terraform.state-pull-with-jq-for-inspection
name: state-pull-with-jq-for-inspection
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, state-pull-jq, state-pull, state-inspection, jq]
level: practitioner
status: verified
description: "Query raw state with terraform state pull and jq: resource counts by type, find by attribute or tag, serial and lineage, provider usage and tainted or deposed instances."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/state/pull", "https://developer.hashicorp.com/terraform/internals/json-format", "https://jqlang.github.io/jq/manual/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform state pull | jq`

`state pull` prints the raw state JSON (format version 4) from any backend, read-only.
For a stable schema prefer `terraform show -json` (`.values.root_module`); use the
raw form when you need serial, lineage, deposed or private details.

```bash
terraform state pull > s.json
jq '{version, terraform_version, serial, lineage}' s.json
```

## Useful queries
```bash
# Count of instances by resource type
jq -r '[.resources[] | select(.mode=="managed") | {t: .type, n: (.instances|length)}]
  | group_by(.t) | map("\(map(.n)|add)\t\(.[0].t)") | .[]' s.json | sort -rn | head

# Find which address owns a cloud ID
jq -r --arg id "i-0abc123" '.resources[] | . as $r | .instances[]
  | select(.attributes.id == $id)
  | "\($r.module // "root").\($r.type).\($r.name)\(if .index_key then "[\(.index_key|tojson)]" else "" end)"' s.json

# Everything tagged Owner=team-x
jq -r '.resources[] | . as $r | .instances[] | select((try .attributes.tags.Owner catch null) == "team-x")
  | "\($r.type).\($r.name)"' s.json

# Tainted and deposed instances (deposed instances have a "deposed" key and no status)
jq -r '.resources[] | . as $r | .instances[] | select(.status=="tainted" or .deposed)
  | "\($r.type).\($r.name) status=\(.status // "") deposed=\(.deposed // "")"' s.json

# Providers referenced by state
jq -r '[.resources[].provider] | unique[]' s.json
```

## Caution
- The pulled file contains every secret in state; write it to a temp dir and delete.
- Do not edit and `state push` casually (see the manual state edit skill); queries only.
- `index_key` is a number for count and a string for for_each.
- Root-module resources have no `module` key (the `// "root"` fallback above); module resources have `module` such as `module.m`.
- Instances with no `status` key are healthy; `status` appears only as `tainted`.
- Use `try ... catch null` (not a trailing `?`) around nested paths: `?` guards only the last step, so a resource whose parent attribute is a string still raises an error.
- `terraform_version` in the pulled file is the version that last wrote the state.

## Verify
- [ ] Query result matches `terraform state list` / `state show` for a sample address.
- [ ] Temp state files removed.

## Checked
- Terraform 1.17.0 state with `terraform_data`, `null_resource` (count 2), `local_file` and a tainted `for_each` instance: `state pull` gave `version: 4`, `terraform_version`, `serial`, `lineage`; the count-by-type pipeline printed `3 terraform_data / 2 null_resource / 1 local_file`; the id lookup printed `root.terraform_data.a`; the tag query (absent attribute) ran clean with no output; the tainted/deposed query listed the tainted instance and, after a failed `create_before_destroy` replace, a `deposed` key with an 8-character value; `[.resources[].provider] | unique` printed the three provider addresses (including `terraform.io/builtin/terraform`); `index_key` was `0`,`1` for count and `"p"`,`"q"` for for_each.
- The tag query: `.attributes.tags.Owner?` errored (`Cannot index string with string`) when another resource's `tags` attribute was a string, because `?` guards only the last step, so it now uses `try ... catch null`; that form returned the right resource on `terraform_data` with `input = { tags = { Owner = "team-x" } }` (there the path is `.attributes.input.value.tags.Owner`, because dynamically typed attributes are stored as `{value, type}`). Real cloud tag shapes depend on the provider schema and were not exercised.
