---
id: computing-software.cloud-infrastructure-engineering.terraform.providers-tree-and-providers-schema-json
name: providers-tree-and-providers-schema-json
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, providers-schema, providers-tree, terraform-providers, provider-requirements]
level: practitioner
status: verified
description: "Inspect provider requirements with terraform providers (module tree view) and dump full resource schemas with providers schema -json for tooling and audits."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/providers", "https://developer.hashicorp.com/terraform/cli/commands/providers/schema"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform providers` and `providers schema -json`

## Requirement tree
```bash
terraform providers
```
```
Providers required by configuration:
.
├── provider[registry.terraform.io/hashicorp/random] 3.7.2
└── module.m
    └── provider[registry.terraform.io/hashicorp/random] >= 3.5.0

Providers required by state:

    provider[registry.terraform.io/hashicorp/null]

    provider[registry.terraform.io/hashicorp/random]
```
(Real output from Terraform 1.17.0: `null` was removed from the configuration but its resource stayed in state, so it is listed
only under "required by state"; the "required by state" section is absent until something has been applied. The command
needs an initialised directory: without init it fails with `Required plugins are not installed`.)
Use it to answer: which module pins a provider so tightly that `init -upgrade`
cannot move (`Failed to query available provider packages... no available releases
match`)? Which providers are only in state (removed from config but resources
remain, so destroy still needs them)?

## Full schema dump
```bash
terraform init
terraform providers schema -json > schema.json
```
Shape: `.provider_schemas["registry.terraform.io/hashicorp/random"].resource_schemas["random_id"].block.attributes`
(a map of attribute name to `{type, description, optional, computed, required, sensitive, deprecated, write_only}`; absent flags are omitted, not false,
so `required` printed `null` for optional/computed attributes).

Useful queries:
```bash
# Every argument of a resource and whether it is required/optional/computed
# (select(.) skips providers that do not define the resource; without it jq fails with "null (null) has no keys")
jq '.provider_schemas[].resource_schemas.random_id.block.attributes | select(.)
    | to_entries[] | {k: .key, required: .value.required, computed: .value.computed, sensitive: .value.sensitive}' schema.json
# All deprecated attributes across a provider
jq -r '.provider_schemas[].resource_schemas | to_entries[] | .key as $r
    | .value.block.attributes // {} | to_entries[] | select(.value.deprecated) | "\($r).\(.key)"' schema.json
# Which attributes are write-only (Terraform 1.11 added write-only attributes; the JSON key is write_only)
jq -r '.. | objects | select(.write_only == true)' schema.json | head
```

## Uses
- Generating module variable stubs from a resource schema.
- Policy/linters that need attribute lists (checking `sensitive` attributes).
- Diffing two provider versions' schemas before a major upgrade:
  dump with each version and `diff <(jq -S . a.json) <(jq -S . b.json)`.

## Gotchas
- Needs an initialised directory; `schema -json` and `providers` error otherwise (`Inconsistent dependency lock file` when a registry provider is not in the lock file, `Required plugins are not installed` when the lock file names a provider whose package is missing).
- Output grows with the number of providers (23 KB for `null` + `random`); filter with `jq` immediately.
- `providers` shows **constraints**, not the selected version; selected versions are in `.terraform.lock.hcl` or `terraform version`.

## Verify
- [ ] `terraform providers` shows no unexpected provider only in state.
- [ ] Schema queries return the attributes you expected for the target resource.

## Checked
- Terraform 1.17.0 with `null` and `random` providers and a child module: `terraform providers` output matched the tree format (blank lines included) before and after applying and removing a provider from config; the dump `providers schema -json` listed both provider keys; the required/optional/computed query failed on the multi-provider file exactly as the old text would ("null (null) has no keys") and works with `select(.)`; the deprecated-attribute query printed `random_password.number` and `random_string.number`; attribute keys seen were `computed, deprecated, description, description_kind, optional, required, sensitive, type`.
- Source check (github.com/hashicorp/terraform internal/command/jsonprovider/attribute.go): `write_only` and `deprecated` are real JSON keys; Terraform v1.11 changelog: "Add write-only attributes to resources".
- `terraform version` printed the selected provider versions (`+ provider registry.terraform.io/hashicorp/null v3.3.2`) and `.terraform.lock.hcl` has `version = "3.3.2"`, confirming "constraints, not selected versions". The AWS-specific names from the old text were replaced with local providers; the `diff <(jq -S . a.json) <(jq -S . b.json)` form ran in Git Bash on two copies of the dump and printed nothing (identical).
