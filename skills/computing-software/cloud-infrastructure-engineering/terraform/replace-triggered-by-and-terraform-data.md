---
id: computing-software.cloud-infrastructure-engineering.terraform.replace-triggered-by-and-terraform-data
name: replace-triggered-by-and-terraform-data
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, replace-triggered-by, replace-triggered-by-usage, triggers-replace, terraform-data, terraform-data-triggers, terraform-data-input, null-resource]
level: practitioner
status: verified
description: "Force replacement when something else changes with replace_triggered_by, use terraform_data (triggers_replace, input/output) to trigger on variables, and replace null_resource."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#replace_triggered_by", "https://developer.hashicorp.com/terraform/language/resources/terraform-data"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `replace_triggered_by` and `terraform_data`

## replace_triggered_by
Ran under Terraform 1.17.0 with `terraform_data`:
```hcl
resource "terraform_data" "web" {
  input = "web"
  lifecycle {
    replace_triggered_by = [
      terraform_data.src,                   # any change (update or replace) of the resource
      terraform_data.src.input.a,           # only when this attribute changes
    ]
  }
}
```
- Accepts references to **managed resources** (or their attributes) only: a variable
  and a local each failed validation (`Invalid reference in replace_triggered_by
  expression`). The docs say data sources are not allowed either, although `validate`
  accepted one; do not rely on it.
- With `count`/`for_each`, `terraform_data.src[count.index]` / `[each.key]` ties instance
  to instance (run: changing only `src[1]` replaced only `dst[1]`).
- Triggers on planned *changes*, so a no-op plan never replaces. Changing a tag-like
  field of `src` replaced the whole-resource dependent but not the one that referenced
  `src.input.a`.
## Triggering on a variable: terraform_data
```hcl
resource "terraform_data" "ami_revision" {
  input = var.ami_id
}

resource "terraform_data" "web" {
  input = var.ami_id
  lifecycle {
    replace_triggered_by = [terraform_data.ami_revision]
  }
}
```
`terraform_data` (built in since 1.4, no provider needed) changes whenever `input`
changes, which then replaces the instance (plan text: `will be replaced due to changes
in replace_triggered_by`).

## terraform_data as a provisioner host (replaces null_resource)
```hcl
resource "terraform_data" "mig" {
  triggers_replace = [var.sv, "const"]
  input            = "addr-${var.sv}"                 # exposed as .output
  provisioner "local-exec" {
    command = "echo MIGRATE ${self.output}"
  }
}
```
- `triggers_replace`: any change → replace (re-runs creation provisioners; plan said `must be replaced`).
- `input` → `output`: stores a value; changing only `input` is an in-place update and
  `output` shows `(known after apply)`.
- Migrate existing `null_resource` with `moved { from = null_resource.x  to = terraform_data.x }`
  (the 1.9 changelog added this cross-type move; run: `has moved to terraform_data.x`, no
  changes); `triggers` map → `triggers_replace`.
## Gotchas
- `replace_triggered_by` on a resource with `prevent_destroy` fails the plan (`Instance cannot be destroyed`).
- Referencing a whole resource replaces on any update of it (above); reference a specific attribute instead.
- `terraform_data.input` is stored in state (do not put secrets there).

## Verify
- [ ] Changing `var.ami_id` produces `# terraform_data.web will be replaced due to changes in replace_triggered_by`.
- [ ] Unrelated changes do not replace.

## Checked
- Terraform 1.17.0 with `terraform_data` and `hashicorp/null`: `replace_triggered_by` on a resource, a whole resource vs an attribute (tag-only change), count-instance references, variable and local references (validation errors), a data source reference (validate accepted it), `prevent_destroy` conflict, `moved` from `null_resource` to `terraform_data`, `triggers_replace` replacement, `input`/`output` behaviour and a `local-exec` provisioner with `self.output`.
- Docs (lifecycle meta-argument page): only managed resources are allowed. Changelogs: v1.4 (`terraform_data`), v1.9 (null_resource to terraform_data move).
