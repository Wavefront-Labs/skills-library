---
id: computing-software.cloud-infrastructure-engineering.terraform.taint-untaint-and-replace
name: taint-untaint-and-replace
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, taint, untaint, replace, forced-replacement, replace-triggered-by, lifecycle, recreate, terraform-apply-replace, state]
level: practitioner
status: verified
description: "Force Terraform to recreate a resource: why -replace superseded taint/untaint, when to use replace_triggered_by instead, and how to recover from a stuck tainted resource."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/taint", "https://developer.hashicorp.com/terraform/cli/commands/untaint", "https://developer.hashicorp.com/terraform/cli/commands/plan#replace-address", "https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# taint/untaint and -replace

**Goal:** recreate a resource that is degraded, mis-bootstrapped or compromised
without editing config — and do it so the replacement is visible in a plan that
someone reviews.

## 1. Use `-replace`, not `taint`
```bash
terraform plan  -replace="aws_instance.web[0]" -out=tfplan
terraform apply tfplan
# or one shot (prompts as usual)
terraform apply -replace="module.db.aws_db_instance.main"
```
- Available since 0.15.2 (0.15.2 changelog); the Terraform docs page for `terraform taint`
  says the command is deprecated in favour of `-replace` (recommended from 0.15.2).
- `-replace` lives in the plan: the reviewer sees `# aws_instance.web[0] will be
  replaced, as requested` and nothing is changed in state until apply.
- Repeatable: `-replace=a -replace=b`. Addresses are quoted exactly as in
  `terraform state list` (including `["key"]` for `for_each`).
- Replacement obeys `create_before_destroy` if the resource sets it; otherwise it is
  destroy-then-create with the usual downtime.

## 2. What `taint` did and why it is worse
`terraform taint aws_instance.web` writes a "tainted" flag **into state immediately**,
with no plan and no lock-free review. The next apply by *anyone* (including a
scheduled CI run) replaces it. `terraform untaint <addr>` clears the flag. Keep
`untaint` in your toolbox: Terraform itself still marks a resource tainted when a
creation-time provisioner fails, and `untaint` is how you stop the resulting
replace loop once you have fixed the host by hand.

## 3. Automatic replacement: `replace_triggered_by`
When a resource must be recreated whenever another changes (an instance when its
launch template or user-data changes, a Lambda alias when the function hash changes):
```hcl
resource "aws_instance" "app" {
  # ...
  lifecycle {
    replace_triggered_by = [aws_launch_template.app.latest_version, terraform_data.bootstrap]
  }
}
```
- Terraform 1.2+ (1.2 changelog). References must be managed resources or their attributes; a
  variable fails with `Invalid reference in replace_triggered_by expression` ("Only resources,
  count.index, and each.key may be used") and a data source with `Missing resource reference`. To key on an arbitrary value, route it through a
  `terraform_data` resource's `input` (1.4+) and reference that.
- Replacement triggers on any *planned* change to the referenced attribute, so a
  no-op plan never cascades.

## 4. Recovering from a failed replacement
1. Apply failed after destroy but before create: the resource is gone from state and
   the cloud; a plain `terraform apply` creates it.
2. Apply failed after create with `create_before_destroy`: both exist; state holds
   the new one as `deposed`. `terraform plan` shows "deposed object will be
   destroyed" — apply it.
3. Replacement loops every apply: check `terraform state show <addr>` for
   `(tainted)` in the header (`# terraform_data.pf: (tainted)`; run `untaint`), or an attribute that differs every run
   (timestamp, random value without `keepers`, `user_data` from `templatefile` with
   non-deterministic input).

## 5. When replacement is the wrong tool
- A single attribute is wrong: fix the config; let Terraform update in place.
- Terraform wants to replace and you do not: find the `forces replacement` attribute
  (`computing-software.cloud-infrastructure-engineering.terraform.reading-plan-output-and-diffs`),
  add `ignore_changes` for externally-managed attributes, or use `moved`/`import`.
- Stateful resources (RDS, EBS, buckets): `-replace` deletes data. Snapshot first;
  check `skip_final_snapshot`/`deletion_protection`.

## Gotchas
- `-replace` on a resource with `prevent_destroy = true` errors at plan; you must
  remove the lifecycle rule in the same change.
- `-replace` of a `count`/`for_each` parent address without an index is an error;
  list the instances.
- A tainted resource shows as `-/+` even when nothing else changed (`is tainted, so must
  be replaced`).

## Verify
- [ ] `terraform plan -replace=<addr>` shows exactly one `-/+` block for that address plus any dependents you expect.
- [ ] `terraform state show <addr>` no longer shows `(tainted)` after a successful apply.
- [ ] Stateful resources were snapshotted before replacement.

## Checked
- Terraform 1.17.0, `terraform_data`: `terraform taint` printed `has been marked as tainted` and the state changed at once (`state show` header `# terraform_data.web: (tainted)`); the next plan showed `terraform_data.web is tainted, so must be replaced` and, via `replace_triggered_by = [terraform_data.bootstrap, terraform_data.web.output]`, `terraform_data.app will be replaced due to changes in replace_triggered_by`; `untaint` restored `No changes`; changing `bootstrap` in place also replaced `app`, while an unchanged plan replaced nothing; a failing `local-exec` left `terraform_data.pf` tainted and the next plan wanted `-/+`; a variable and a data source in `replace_triggered_by` gave the errors quoted; `-replace` on `prevent_destroy` failed with `Instance cannot be destroyed`.
- Changelogs: `-replace` and `replace_triggered_by` (0.15.2, 1.2), `terraform_data` (1.4). `aws_db_instance` documents `skip_final_snapshot` and `deletion_protection` (provider docs source); the HCP Terraform replacement note was removed (not checkable without an account).
