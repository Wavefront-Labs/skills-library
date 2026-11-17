---
id: computing-software.cloud-infrastructure-engineering.terraform.targeted-applies-with-target-and-exclude
name: targeted-applies-with-target-and-exclude
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, target, exclude, targeted-apply, resource-targeting, partial-apply, incident-response, anti-pattern, dependency-graph]
level: practitioner
status: verified
description: "Use -target (Terraform and OpenTofu) and -exclude (OpenTofu 1.9+ only) only for recovery, understand what they silently skip, and fix the config problems that make people reach for them."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan#resource-targeting", "https://opentofu.org/docs/cli/commands/plan/#resource-targeting", "https://developer.hashicorp.com/terraform/tutorials/state/resource-targeting"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# -target and -exclude, and why to avoid them

**Goal:** know exactly what a targeted plan does and does not do, use it to get out
of a hole during an incident, and never let it become the normal deploy path.

## 1. Syntax
```bash
terraform plan  -target=module.network -target='aws_instance.web["a"]' -out=tfplan
terraform apply tfplan                         # the saved plan keeps the targeting (ran: apply printed `Applied changes may be incomplete`)
terraform apply -target=aws_security_group.lb   # one-shot, prompts
terraform destroy -target=aws_instance.scratch  # destroys that resource and its dependents only

tofu plan -exclude=module.expensive_batch       # OpenTofu 1.9+ only: everything except these (Terraform has no -exclude flag through 1.17)
```
- A module address targets every resource in it (and child modules).
- `-target` includes the target's **dependencies** (what it needs) but **not its
  dependents** (what needs it).
- `-exclude` removes the address **and everything that depends on it**; it cannot
  be combined with `-target`.
- Every targeted plan prints `Warning: Resource targeting is in effect` and the
  apply prints `Applied changes may be incomplete`.

## 2. What is silently skipped
- Outputs: root outputs are not updated unless every resource they reference is in
  the plan, so a downstream `terraform_remote_state` reader keeps seeing stale values.
- `removed` and `import` blocks outside the target set are ignored (ran). A pending `moved` block is different: if the targets do not cover both sides Terraform refuses (`Error: Moved resource instances excluded by targeting` and lists the `-target` options to add; ran).
- Data sources not needed by the target are not read (ran: a missing file behind an untargeted data source gave `No changes` on a targeted plan and `Read local file data source error` on the full plan).
- `check` blocks and `precondition`s on untargeted resources do not run (ran with a failing `postcondition`: the targeted apply succeeded, the full apply failed `Resource postcondition failed`).
- Drift on untargeted resources is neither reported nor corrected (ran: `No changes` for a targeted plan, `will be created` for the drifted `local_file` in the full plan); the next full
  plan can be large and surprising.

## 3. Legitimate uses
- **Incident recovery:** a broken resource blocks the whole apply (provider bug,
  rate limit, cycle); apply the fix for that one address, then run a full plan.
- **Bootstrapping ordering a provider cannot express:** e.g. create the EKS cluster
  before the kubernetes provider can be configured, then a full apply. Prefer
  splitting into separate root modules/stacks long-term.
- **Staged destruction** of one component before a refactor.
- **Debugging** with `TF_LOG` on a single resource.
In each case the final step is a **full, untargeted plan that shows no changes**.

## 4. Why it is an anti-pattern as a deploy strategy
- Partial applies let state and config diverge for weeks; nobody wants to run the
  "big scary plan" afterwards.
- CI pipelines with `-target` lists drift from the code; new resources are silently
  never applied.
- It hides design problems that have real fixes:
  - Apply too slow → split root modules (`computing-software.cloud-infrastructure-engineering.terraform.remote-state-and-module-layout`), raise `-parallelism`, fix `performance-at-scale` issues.
  - Need to apply only one environment → workspaces or per-env directories, not targeting.
  - One resource keeps failing → fix it or `-replace` it, do not route around it.
  - Provider depends on a resource in the same config → two stacks.

## 5. Safer alternatives
| Want | Use |
|---|---|
| Skip one slow/flaky module this once | OpenTofu: `-exclude=module.x` and run a full plan after (Terraform: no equivalent; use `-target` for the rest) |
| Not manage a resource anymore | `removed` block or `terraform state rm` |
| Recreate one thing | `-replace=<addr>` |
| Stop a resource changing | `lifecycle { ignore_changes = [...] }` |
| Deploy independently | separate state per component |

## Gotchas
- `-target` on a resource inside a module with `count`/`for_each` on the module
  needs the module index: `-target='module.svc["api"].aws_lambda_function.fn'`.
  Quote it; shells eat the brackets.
- Targeting a resource whose dependency has a *pending* change applies that
  dependency's change too, which can be more than you intended; read the plan.
- `-exclude` and `-target` cannot be set in `TF_CLI_ARGS_plan` persistently without
  affecting every run; if you find them in a CI env var, that is the problem.
- `-exclude` is an OpenTofu 1.9 feature. Terraform's changelogs (1.10 to 1.17) and its `plan` documentation do not list it, so an earlier version of this skill that said Terraform 1.12 followed was wrong.

## Verify
- [ ] After any targeted apply, `terraform plan` (no flags) reports `No changes` or only changes you can explain.
- [ ] No `-target` appears in CI configuration or shared scripts.
- [ ] The reason for the targeted run is written in the PR/incident log.

## Checked
- Terraform 1.17.0 (and OpenTofu 1.13.2 for `-exclude`) on `terraform_data`, `local_file` and a local module with `for_each`: `-exclude` rejected by Terraform (`flag provided but not defined: -exclude`), accepted by OpenTofu, excluding the address and its dependents, and refused together with `-target` (`mutually-exclusive`); targets include dependencies not dependents; module-instance targets with quotes; targeted plan/apply warnings; saved-plan targeting; outputs not updated for untargeted resources; `plan -destroy -target` lists the dependents; the moved-block error; skipped imports/removed; skipped conditions, data sources and drift; `TF_CLI_ARGS_plan` carrying `-target` produced the warning. OpenTofu 1.9 introduced `-exclude` per its v1.9 CHANGELOG (raw GitHub file); Terraform changelogs 1.10 to 1.16 contain no `-exclude`.
