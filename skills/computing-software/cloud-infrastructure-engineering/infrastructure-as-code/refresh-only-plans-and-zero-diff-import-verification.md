---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.refresh-only-plans-and-zero-diff-import-verification
name: refresh-only-plans-and-zero-diff-import-verification
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, state-management, brownfield-import, refresh-only, zero-diff, import-verification, terraform-import]
level: advanced
status: docs-checked
description: "Use terraform plan/apply -refresh-only to reconcile state with out-of-band changes, and prove brownfield imports are complete by iterating until the plan is empty."
sources:
  - https://developer.hashicorp.com/terraform/cli/commands/plan
  - https://developer.hashicorp.com/terraform/language/import
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Refresh-only plans and zero-diff import verification

## Refresh-only
```bash
terraform plan -refresh-only
terraform apply -refresh-only
```
- Refresh-only mode creates a plan whose only goal is to update Terraform state and root module output values to match changes made to remote objects outside Terraform. The default (normal) mode instead changes the remote system to match your configuration.
- The docs suggest it for reconciling records after you intentionally changed objects outside the usual workflow, for example while responding to an incident.
- Planning modes are mutually exclusive; you cannot combine refresh-only with `-destroy`, and `-refresh=false` cannot be used in refresh-only mode. The option needs Terraform 0.15.4 or later.
- Accepting drift into state does not change your code; a later normal plan compares the configuration with the updated state, so update the code if you want to keep the out-of-band change.
- `-refresh=false` and `-minimal-refresh` make Terraform ignore external changes and can give an incomplete or incorrect plan; avoid them when upgrading provider versions.

## Zero-diff import verification
Goal: after import, state and code describe the existing resource and the plan reports that no actions are needed.
1. Write an `import` block (unique resource ID and a target address) plus a matching `resource` block, or write only the `import` block and run `terraform plan -generate-config-out=PATH` to generate the resource blocks.
2. `-generate-config-out` is experimental. PATH must be a new file or Terraform errors, and Terraform may still write config if the plan fails for another reason. Treat the output as a draft to review.
3. Run `terraform plan` and read each `~` (in-place update) and `-/+` (destroy and recreate) line; adjust the code until the plan shows no changes. A `-/+` replace on an imported resource would destroy and recreate it, so resolve it before applying.
4. Run `terraform apply` to import. Terraform identifies a resource by the provider ID or by an `identity` made of specific attributes (for example account_id, bucket and region for an AWS S3 bucket); check provider docs.

## Verify
- [ ] `terraform plan -detailed-exitcode` exits 0 (succeeded, empty diff; 1 is an error, 2 is a non-empty diff).
- [ ] A saved plan file (`-out`) is treated as sensitive: it holds the full configuration and planned values, and sensitive data is stored in cleartext even though terminal output obscures it.

## Checked
Method: docs-checked 2026-11-09 against the HashiCorp "terraform plan command" page (full text read) and the "Import resources overview" page (full text read).
Removed: terraform refresh deprecation claim, tutorial source (unread), S3 split-resource and tag-ignore advice, "import blocks can stay in code", the exact apply summary line, the one-day-later drift check (not on pages read).
