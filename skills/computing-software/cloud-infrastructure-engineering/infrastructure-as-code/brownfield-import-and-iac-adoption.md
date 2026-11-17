---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.brownfield-import-and-iac-adoption
name: brownfield-import-and-iac-adoption
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac, brownfield, import, adoption, terraform-import, import-blocks, generate-config-out, migration-plan]
level: advanced
status: docs-checked
description: "Bring click-ops infrastructure under IaC safely: inventory first, then Terraform import blocks with generate-config-out, bulk import queries, and a zero-diff gate."
sources: ["https://developer.hashicorp.com/terraform/language/import", "https://developer.hashicorp.com/terraform/cli/commands/plan"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Brownfield import and IaC adoption

**Goal:** resources built by hand become code-managed without being destroyed or changed in the
process, with a clear line between "owned by IaC" and "not yet".

## 1. Inventory reality first (practitioner guidance)
- List what exists on the cloud side with the provider's own inventory tooling, with tags and creators.
- Classify: stateful resources (highest care), shared foundations (network, identity, DNS), app resources, and orphans (candidates for deletion rather than import).
- Freeze changes on targeted resources during an import window; console changes mid-import are a common cause of diffs.
- Start with low-blast-radius resources to learn the workflow, and do stateful ones last. Keep a "not yet imported" list in the repo.

## 2. Terraform import
How the documented workflow works:
- An `import` block names the resource's unique infrastructure ID and declares an address for it in state (`to`). A matching destination `resource` block must exist in configuration.
- **Single or small batches:** write the `import` and `resource` blocks by hand and run `terraform apply`. Alternatively write only the `import` block and run `terraform plan` with the `generate-config-out` flag to generate the `resource` blocks. The plan page marks `-generate-config-out=PATH` as experimental; PATH must not already exist, and Terraform may still write configuration if the plan fails for another reason.
- **Bulk:** define queries as HCL to discover large sets of unmanaged resources, add the results to your configuration, and run `terraform apply` to import them. HCP Terraform can show query results and apply import configurations in its UI.
- Resource identity: Terraform identifies a resource by the provider-assigned ID or by a set of provider-defined attributes. Reference it with `id` or `identity` as the provider documents (for an AWS S3 bucket the identity attributes are account ID, bucket and region); the provider documentation is authoritative for each type.

```hcl
import {
  to = aws_security_group.web
  id = "sg-0123456789abcdef0"
}
```
Review generated configuration before committing: move it into proper files or modules and replace literals with variables.

## 3. Prove ownership (practitioner guidance)
After an import batch, `terraform plan` should show the imports and no other changes. Keep running the plan on a schedule and treat any later diff as drift to investigate before declaring the resource code-owned.

## Gotchas
- Importing a resource that another stack or tool already manages creates a fight; check other state first.
- Generated configuration contains every attribute, including defaults; trim to intent so provider upgrades do not show spurious diffs.
- Passwords and similar secrets are usually not readable from provider APIs; set the real value from a secret source or you may change it on the first apply.

## Verify
- [ ] After each import batch, the plan shows no add, change or destroy beyond the intended imports.

## Checked
Method: docs-checked 2026-11-09 against the Terraform "Import resources overview" page and the terraform plan command page (for `-generate-config-out`).
Removed as unconfirmed (sources not readable or not read): terraformer, aws2tf, aztfexport, gcloud bulk-export commands, Pulumi import, CloudFormation import, Bicep existing and decompile, Ansible and Kubernetes adoption sections, all `prevent_destroy` and `ignore_changes` claims, module-address import and `moved` block advice, the CLI `terraform import` comparison, and the day-count zero-diff gate. Tags trimmed to match.
