---
id: computing-software.cloud-infrastructure-engineering.terraform.forgetting-resources-with-state-rm-or-removed-blocks
name: forgetting-resources-with-state-rm-or-removed-blocks
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, state-remove, forget-resource, state-rm, removed-block, removed-destroy-false, forget-without-destroy]
level: practitioner
status: verified
description: "Stop managing a resource without destroying it: declarative removed blocks with destroy = false versus imperative terraform state rm, and handing it to another state."
sources: ["https://developer.hashicorp.com/terraform/language/resources/syntax#removing-resources", "https://developer.hashicorp.com/terraform/cli/commands/state/rm", "https://opentofu.org/docs/language/resources/syntax/#removing-resources"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forgetting resources: `removed` vs `state rm`

Deleting a resource block makes Terraform plan a **destroy**. To keep the real
object and only drop it from state, use one of these.

## Declarative: `removed` block (Terraform 1.7+, OpenTofu 1.7+)
```hcl
removed {
  from = aws_s3_bucket.legacy_logs

  lifecycle {
    destroy = false
  }
}
```
- Delete the `resource` block in the same change. The plan shows
  `# aws_s3_bucket.legacy_logs will no longer be managed by Terraform`.
- Works on whole modules: `from = module.legacy` (no instance keys allowed —
  `from` addresses the resource/module, not `[0]`).
- Every environment that applies the commit forgets it consistently.
- Remove the `removed` block after all states have applied it (keeping it is harmless).

## Imperative: `terraform state rm`
```bash
terraform state rm -dry-run 'aws_s3_bucket.legacy_logs'
terraform state rm 'aws_s3_bucket.legacy_logs' 'module.legacy'
```
Use for single-workspace fixes, removing individual instances (`'aws_instance.x[3]'`),
or when another state is about to `import` the object.

## Handing an object to another state
1. Target state: add the resource + `import` block; plan shows `will be imported`.
2. Source state: `removed { destroy = false }`; apply.
3. Apply target. Order matters only in that both must not apply destructive
   changes in between; neither step touches the real object.

## Gotchas
- `removed` without the lifecycle block (or `destroy = true`) **destroys** — that is the
  other use, documented in removed-provisioner skill.
- If the resource block still exists, `removed` errors: `Removed resource still exists`.
- `state rm` leaves no trace in code; a later plan from a branch that still has the
  block will re-create it. Pair it with the code deletion in one PR.
- Dependent resources still reference the forgotten one in code? Plan errors with
  `Reference to undeclared resource` — refactor them to data sources or variables.

## Verify
- [ ] Plan shows "will no longer be managed" and **0 to destroy**.
- [ ] The object still exists in the cloud console/CLI after apply.
- [ ] `terraform state list | grep legacy_logs` is empty.

## Checked
- Terraform 1.9.8 with the local provider: deleting a resource block plans a destroy; the same change plus `removed { lifecycle { destroy = false } }` plans `will no longer be managed by Terraform, but will not be destroyed` (and the file stays after apply); a remaining resource block gives `Removed resource still exists`; `from = local_file.idx[0]` gives `Resource instance keys not allowed`; `from = module.legacy` works; a `removed` block without the lifecycle block plans `will be destroyed`; an unresolved dependent reference gives `Reference to undeclared resource`; `state rm -dry-run` prints `Would remove ...` and `state rm` leaves the real file; an `import` block on `terraform_data` plans `will be imported` (`1 to import`, with `# (imported from ...)` when attributes differ). The 1.7 changelog introduces `removed` blocks. The cross-state handoff order was not run.
