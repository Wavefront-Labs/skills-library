---
id: computing-software.cloud-infrastructure-engineering.terraform.importing-existing-infrastructure
name: importing-existing-infrastructure
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, terraform-import, import-block, generate-config-out, terraform-query, list-block, brownfield, bulk-import, resource-discovery, adoption, hcl-generation, import-id-syntax]
level: advanced
status: docs-checked
description: "Adopt existing cloud resources into Terraform: import blocks with -generate-config-out for a few resources, terraform query for bulk discovery, then a clean plan check."
sources:
  - "https://developer.hashicorp.com/terraform/language/import"
  - "https://developer.hashicorp.com/terraform/language/import/generating-configuration"
  - "https://developer.hashicorp.com/terraform/language/import/bulk"
  - "https://developer.hashicorp.com/terraform/cli/commands/import"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Importing existing infrastructure into Terraform

**Goal:** a resource that already exists in the cloud ends up under Terraform management
with configuration that matches it, so a later `plan` shows nothing to change.

## 1. One or a few resources: `import` blocks
An import block names the resource ID to import and declares the address it will have in
state; a resource block matching that address must exist (hand written, or generated as
below). Run `terraform apply` to import. Prefer the block over the `terraform import
ADDRESS ID` command: the command page itself points to import blocks, which let Terraform
import during `apply` and so fit CI/CD pipelines.
```hcl
import {
  to = aws_instance.web
  id = "<INSTANCE_ID>"
}
```

### Generating the resource block
Write only the import block, then:
```bash
terraform plan -generate-config-out=generated.tf
```
- Configuration generation was introduced as experimental in Terraform v1.5, and the page
  warns that the format of generated configuration may change in later minor versions.
- Give a path that does not exist; supplying an existing file is an error.
- Terraform produces HCL as a template containing its best guess at each argument. The page
  recommends iterating: remove some attributes, adjust others, and move blocks into files and modules.
- If the configuration has no other resource for that provider, add a provider block so Terraform
  knows which provider to use, and re-run `terraform init`.
- For complex schemas the generated code can be invalid, for example a "Conflicting
  configuration arguments" error when it contains both `ipv6_address_count` and `ipv6_addresses`.
  Terraform still writes the file; remove one of the conflicting arguments and plan again.
- Review the file, commit it, then `terraform apply` to perform the import.

## 2. Bulk discovery with `terraform query`
For large sets of resources, the bulk-import page describes HCL queries instead of hand-written blocks:
- Put `list` blocks in a file with the `.tfquery.hcl` extension, next to a normal `.tf`
  configuration with `required_providers`. Each `list` block takes a resource type and a local
  name, a required `provider`, a provider-specific `config` block, and optional `include_resource`
  and `limit` (up to 100 results per block by default).
- Searching by resource identity needs Terraform v1.12 or newer.
- `terraform query` prints results (identity per resource; `-json` for machine-readable output).
  `terraform query -generate-config-out=generated.tf` writes resource and import blocks; the target
  file must not already exist.
- Copy the generated blocks into your configuration and run `terraform apply`. Afterwards you may
  discard `generated.tf`, and the import blocks may be removed or kept as a record of origin.
- Check your provider's documentation for which resource types support listing.

## 3. Resource identity and import IDs
The ID is resource-type specific (the command page gives an EC2 instance ID and a Route 53 zone
ID as examples). Some resources are identified by a set of attributes instead; the overview gives
`aws_s3_bucket` identity as `account_id`, `bucket` and `region`. Always take the format from the
provider's documentation for that resource.

## 4. Verify the import
```bash
terraform plan
```
After importing, plan should show no changes for the new resources. Any diff means the
configuration differs from the real resource; correct the HCL (or accept the change as a
deliberate follow-up apply).

## Gotchas
- Import each remote object into only one resource address; importing the same object more than
  once can cause unwanted behaviour (command page warning).
- The legacy `terraform import` command can target a module address (`module.foo.aws_instance.bar`)
  or an indexed one, and quoting of `for_each` keys differs between Linux/macOS, PowerShell and
  cmd.exe (see the command page examples).
- Secrets on a legacy resource are copied into state on import; see
  `computing-software.cloud-infrastructure-engineering.terraform.secrets-handling-in-state-and-plans`.
- Third-party exporters (aztfexport, Terraformer) are not covered by the cited pages; read their own
  documentation and treat their output as a first draft.

## Verify
- [ ] `terraform plan` shows no changes right after each import.
- [ ] Generated code was reviewed and moved into the repo's module layout.

## Checked
Checked 2026-11-08 against the Terraform pages "Import resources overview", "Generating
configuration", "Import existing resources in bulk" and the `terraform import` command reference.
Removed: the claim that a leftover import block causes "resource already managed" (the bulk page says
import blocks may be kept or removed), the claims about frozen defaults and missing `for_each`
inference in generated code, and the aztfexport and Terraformer comparisons, which those pages do not state.
Method: docs-only read of cited pages, 2026-11-08
