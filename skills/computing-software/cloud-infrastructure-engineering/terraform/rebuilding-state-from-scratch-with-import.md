---
id: computing-software.cloud-infrastructure-engineering.terraform.rebuilding-state-from-scratch-with-import
name: rebuilding-state-from-scratch-with-import
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, rebuild-state, disaster-recovery, import-block, generate-config-out, lost-state]
level: advanced
status: docs-checked
description: "Rebuild a lost state with import blocks: try backup recovery first, collect import IDs, generate configuration, and read the plan until it only imports."
sources: ["https://developer.hashicorp.com/terraform/language/import", "https://developer.hashicorp.com/terraform/language/import/generating-configuration", "https://developer.hashicorp.com/terraform/cli/state/recover", "https://developer.hashicorp.com/terraform/language/meta-arguments/for_each#limitations-on-values-used-in-for_each"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rebuilding state from scratch

Use only when no backup of the state can be recovered. First try the documented
recovery workflow: unlock the backend if a process died holding the lock (only after
you know why the lock is stuck), read state with `terraform state pull`, and write a
good copy with `terraform state push`.

## 1. Freeze (judgement, not from the docs)
Stop pipelines for this root. Terraform applied against an empty state plans to
create every resource in the configuration again, which risks duplicates and name
conflicts.

## 2. Collect each object's import ID
The import block needs the unique resource ID from your cloud provider, or the
provider's identity attributes. Terraform uniquely identifies resources by the ID the
provider assigned or by a collection of attributes the provider defines, and you can
reference either through the `id` or `identity` attribute. Which one to use and the
ID format are in each provider's documentation (for example, the AWS provider
`s3_bucket` identity is `account_id`, `bucket` and `region`).

## 3. Write import blocks
Importing requires an `import` block with the resource ID, a `to` address for the
resource in state, and a matching destination `resource` block in configuration:
```hcl
import {
  to = aws_iot_thing.bar
  id = "foo"
}
```
- `for_each` is supported on import blocks to import several resources (the for_each
  reference lists "Import multiple resources"; see the import block reference for the
  syntax, which these pages do not show).
- For large sets, define queries and import in bulk (see the import overview).
- To avoid writing resource blocks by hand, keep only the import block and run
  `terraform plan -generate-config-out="generated_resources.tf"`. The path must be
  a new file; an existing path makes Terraform error. If the configuration has no
  other resources for that provider, add a provider block (and re-run
  `terraform init`). The feature was experimental in Terraform 1.5 and its output
  format may change.

## 4. Review and apply
Review the generated HCL, which is Terraform's best guess at each argument; remove
attributes, adjust values and move blocks into files or modules. For resources with
complex schemas Terraform may produce conflicting arguments (the page shows
`ipv6_address_count` conflicting with `ipv6_addresses`); remove one and plan again.
Then run `terraform apply` to import. The plan summary reads like
`Plan: 1 to import, 0 to add, 0 to change, 0 to destroy.`
Aim for a plan that only imports. Planned adds or changes (judgement) mean an
object lacks an import block or the configuration differs from the real resource.
Commit the new configuration to version control.

## Checked
Date: 2026-11-07
Read in full: the Import resources overview, the Generating configuration page
(workflow, example output, limitations), the Recover state from backup overview and
the for_each reference (supported constructs and examples list).
Removed because the pages do not state them: the AWS tagging API command, the
inventory-by-tags and logs advice, the `for_each` import example with `each.key`
(the import block reference was not opened, so the syntax is not repeated), the
"delete imports.tf after apply" step, the recurrence checklist (versioning,
deletion protection, `prevent_destroy`, backup job) and the Verify list. The import
block reference and the bulk import page were not opened.
Method: documentation only; no commands were run.
