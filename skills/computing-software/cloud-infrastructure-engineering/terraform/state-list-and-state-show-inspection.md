---
id: computing-software.cloud-infrastructure-engineering.terraform.state-list-and-state-show-inspection
name: state-list-and-state-show-inspection
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, state-list, state-show, state-pull, address-quoting, state-inspection]
level: practitioner
status: verified
description: "Inspect state with terraform state list (address prefixes, -id) and state show, quote indexed addresses per shell, and query state pull output with jq."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/state/list", "https://developer.hashicorp.com/terraform/cli/commands/state/show", "https://developer.hashicorp.com/terraform/cli/state/resource-addressing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `state list` and `state show`

## List
Ran in Terraform 1.17.0 on a config with `terraform_data` for_each and count resources,
two module calls, a data source and a `local_sensitive_file`:
```bash
terraform state list                                  # every resource instance, data sources included
terraform state list module.app                       # everything under a module (prefix match)
terraform state list 'terraform_data.private'         # all instances of one resource
terraform state list 'terraform_data.private["a"]'    # one instance
terraform state list -id=d5572749-c8f9-88bd-b641-1e6c03207042   # which address manages this ID?
terraform state list | grep -c .                      # resource count (performance planning)
```
`-id` is the fastest way to answer "is this thing managed, and where?". An ID that
matches nothing printed nothing and exited 0.
## Show
```bash
terraform state show 'terraform_data.private["a"]'
terraform state show 'module.app.terraform_data.web[0]'
```
Prints the attributes as HCL-like text (`id`, `input`, `output`); a sensitive attribute
prints as `content = (sensitive value)`. The address must name one instance:
`terraform_data.private[a]` failed with `Error parsing instance address ... This command
requires that the address references one specific instance`.
## Quoting addresses
| Shell | Form |
|---|---|
| bash/zsh | `'terraform_data.private["a"]'` |
| PowerShell 5.1 | `'terraform_data.private[\"a\"]'` (PowerShell strips inner quotes passed to native exes) |
| cmd.exe | `"terraform_data.private[\"a\"]"` |
All three forms worked in 1.17.0; the PowerShell form without backslashes and the cmd form
without them gave the `Error parsing instance address ...[a]` error above, which is the
sign that the quotes were eaten.

## Structured queries
`state show` is for humans. For scripts use JSON:
```bash
terraform show -json | jq -r '.values.root_module.resources[] | select(.type=="terraform_data") | [.address, .values.id] | @tsv'
terraform show -json | jq -c '[.values.root_module.child_modules[].address]'     # ["module.app","module.network"]
terraform state pull | jq '.resources[] | select(.module=="module.app") | .type' | sort | uniq -c
```
`.values.root_module.resources` lists only root-module resources (the first query did
not return the module instances); module resources sit under `child_modules[].resources`,
nested modules under `child_modules[].child_modules`, so walk them (for example with
jq `..`). `state pull` gives the raw state format: `resources[]` carry a `module` key
for module resources and `instances[]` carry `index_key` (`0`, `1`); the third query counts
resource blocks (1 for `module.app`), not instances.
## Gotchas
- `state list` reads the current workspace (a new workspace `w2` printed `No state file was found!`); select the right one first.
- Data sources appear as `data.<type>.<name>` — they are in state but not managed.
- `state show` refreshes nothing: after editing the file a data source read, its
  `content_sha1` was unchanged.
- `state pull` output contains secrets in plain text — do not paste it into tickets.

## Verify
- [ ] `terraform state list -id=<cloud-id>` returns exactly one address (or none, meaning unmanaged).
- [ ] The jq query result count matches `terraform state list | grep -c <type>` (compare instances, not resource blocks).

## Checked
- Terraform 1.17.0 with `terraform_data` (for_each, count, module calls), a data source and `local_sensitive_file`: `state list` (all, module prefix, resource, instance, `-id`, unmatched id), `state show` (instance, module instance, sensitive value, bad address), quoting in bash, Windows PowerShell 5.1 and cmd.exe, `show -json` and `state pull` jq recipes (jq 1.8.2), `state show` after the data file changed, and a new workspace.
- Corrections: `show -json` `root_module.resources` lists only root resources (child modules need walking); the quoting error text is `Error parsing instance address`.
