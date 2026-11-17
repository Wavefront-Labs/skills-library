---
id: computing-software.cloud-infrastructure-engineering.terraform.console-plan-evaluating-planned-values
name: console-plan-evaluating-planned-values
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, console-plan, terraform-console, planned-values, debugging]
level: practitioner
status: verified
description: "Run terraform console -plan to evaluate expressions against freshly planned values, so new resources, changed locals and data sources show real results."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/console", "https://github.com/hashicorp/terraform/blob/v1.7/CHANGELOG.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform console -plan`

## What changes with `-plan`
Plain console evaluates against **current state**. `-plan` (Terraform 1.7+; the 1.7 changelog introduced it) first
creates a plan in memory and evaluates against **planned values**:
- New resources not yet applied have their known planned attributes.
- Changed variables/locals flow through to dependent expressions (`-var n=two` changed a resource input from `one-v1` to `two-v2` under `-plan`; plain console with the same `-var` still showed the state value `one-v1`).
- Data sources are re-read (as during plan), so you see current upstream values; plain console shows the value stored at the last apply (run: a `local_file` data source returned the old content in plain console and the new content with `-plan`).
- Unknown attributes still print `(known after apply)`.

```bash
terraform console -plan -var-file=prod.tfvars
> local.subnet_map
> terraform_data.app.input
> module.cluster.node_group_names
```

Pass variables exactly as you would to `terraform plan` (`-var`, `-var-file`,
`TF_VAR_*`). It never writes state or creates a saved plan (the state serial was
unchanged). Piped input prints only the LAST expression's result; see
`evaluating-expressions-with-console-stdin`. Terraform 1.16 added
`-scope=module.child` to evaluate inside a module instance.

## When to use it
- Debugging a `for_each` map built from variables before the first apply:
  `> { for s in var.subnets : s.name => s }` with real tfvars.
- Checking what a `templatefile()` renders with planned resource IDs.
- Confirming a refactor of locals produces the same map as before
  (compare plain console vs `-plan` output).

## Costs
- It runs a plan like `terraform plan` does (so providers must be initialised and configured as for a plan).
  On large states that can be slow. `console` has no `-refresh` or `-lock` flag
  (`flag provided but not defined`), so test in a small module instead.
- Plain console on state needs no plan, so it is the cheaper first try.

## Verify
- [ ] Expressions over not-yet-created resources return planned values rather than errors.
- [ ] No state change after exiting (`terraform state pull | jq .serial` unchanged).

## Checked
- Terraform 1.17.0 (Windows, scratch dir, `terraform_data` + `hashicorp/local`): ran plain `console` vs `console -plan`, with and without `-var`, against a state with a data source whose file changed after apply; state serial read via `state pull` before and after (3, 3). `console -help` lists `-plan`, `-scope`, `-var`, `-var-file`, `-state`, no `-lock`/`-refresh` (`terraform console -refresh=false` errors).
- Version gate: CHANGELOG v1.7 ("`terraform console`: Now supports a `-plan` option"); the old claim of 1.4 was wrong. `-scope` is in the v1.16 changelog.
