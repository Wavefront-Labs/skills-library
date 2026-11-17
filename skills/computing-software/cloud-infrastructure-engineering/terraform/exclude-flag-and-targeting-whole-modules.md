---
id: computing-software.cloud-infrastructure-engineering.terraform.exclude-flag-and-targeting-whole-modules
name: exclude-flag-and-targeting-whole-modules
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, exclude-flag, exclude-addresses, target-module, module-target, resource-targeting]
level: practitioner
status: verified
description: "Scope a plan to a whole module with -target=module.x or skip parts with -exclude, knowing exactly which dependencies are pulled in or dropped."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan#resource-targeting", "https://opentofu.org/docs/cli/commands/plan/#resource-targeting", "https://developer.hashicorp.com/terraform/tutorials/state/resource-targeting"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Targeting modules and `-exclude`

## `-target` on modules
```bash
terraform plan -target=module.network                 # every instance of the module call
terraform plan -target='module.app["eu"]'             # one module instance
terraform plan -target='module.app["eu"].module.cache'  # nested module (key the for_each parent)
terraform plan -target=module.network -target=aws_iam_role.ci
```
Semantics: the target **plus everything it depends on** is planned, and a targeted module
includes its child modules. Things that depend on the target are *not* - so consumers of
changed outputs stay stale until a full plan. Outputs of the root are skipped unless their
dependencies are fully targeted (with `-target=module.network` only the output reading
`module.network` appeared in `Changes to Outputs`). On a `for_each` module, an unkeyed
`-target=module.app.module.cache` matched none of the instances in the local test (only the
dependencies were planned), so spell out the key.

## `-exclude` (OpenTofu 1.9+; not in Terraform 1.17.0)
`terraform plan -exclude=...` on Terraform 1.17.0 fails with `flag provided but not defined:
-exclude` and `terraform plan -help` lists only `-target`; check your version's help before
relying on it. OpenTofu added it in 1.9 (1.9 changelog; also `-exclude-file`).
```bash
tofu plan -exclude=module.batch_jobs
tofu plan -exclude='aws_instance.web["canary"]'
```
Semantics: drops the address **and everything that depends on it**, plans the rest
(in the test, `-exclude=module.network` also dropped the root resource and the `for_each`
modules that read its output, and kept the unrelated ones). Use when one area is broken
(provider outage, API quota) and the rest must ship. `-target` and `-exclude` cannot be
combined: `Invalid combination of arguments ... mutually-exclusive`.

## Reading the result
Every targeted/excluded plan carries:
```
Warning: Resource targeting is in effect

You are creating a plan with the -target option, which means that the result
of this plan may not represent all of the changes requested by the current
configuration.
```
(OpenTofu words it "-target option or the -exclude option".) Follow up with a full `plan`
as soon as possible and expect it to show the consumers you skipped.

## Picking the right scope
| Situation | Flag |
|---|---|
| Recreate the network module after a manual teardown | `-target=module.network` |
| Provider for one region is down | `-exclude=module.region_ap` |
| Bootstrap: resource whose ID feeds a `for_each` key | `-target=<that resource>` (then full apply) |

## Gotchas
- `-target=module.x` includes all of `module.x`'s *dependencies* outside the module
  (VPC, IAM) — often more than expected; read the plan.
- Addresses with keys need shell quoting (`'module.app["eu"]'`).
- `moved` blocks and targeting interact: a `-target` that leaves out a moved resource fails
  with `Error: Moved resource instances excluded by targeting` and suggests the extra
  `-target` options to add.

## Verify
- [ ] Plan lists only the intended module's resources (+ explained dependencies).
- [ ] A full plan run afterwards and reviewed.

## Checked
- Terraform 1.17.0 and OpenTofu 1.13.2, a config with `module.network`, a `for_each` module `app` (with nested `module.cache`), a root resource reading the network output and a `for_each` resource: `-target=module.network`, `-target='module.app["eu"]'` (planned the instance, its nested module and the network dependency), `-target='module.app["eu"].module.cache'` and two `-target` flags behaved as described; the unkeyed nested target planned only the dependency; `-exclude` was rejected by Terraform 1.17.0 and, in OpenTofu, `-exclude=module.batch_jobs`, `-exclude=module.network` and `-exclude='terraform_data.web["canary"]'` dropped exactly the address and its dependents; `-exclude` with `-target` gave the mutually-exclusive error; root outputs were limited as stated; the moved-plus-target error text is quoted from a real run.
- Sources: OpenTofu 1.9 changelog and plan docs (`-exclude`, `-exclude-file`). The HCP Terraform targeting statement was removed (not confirmable here).
