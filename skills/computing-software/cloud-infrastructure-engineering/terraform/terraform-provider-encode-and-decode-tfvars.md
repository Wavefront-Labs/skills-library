---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-provider-encode-and-decode-tfvars
name: terraform-provider-encode-and-decode-tfvars
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, encode-tfvars, decode-tfvars, provider-terraform-functions, encode-expr, terraform-provider-functions, tfvars]
level: practitioner
status: verified
description: "Use the built-in terraform provider functions encode_tfvars, decode_tfvars and encode_expr (Terraform 1.8+) to read and generate tfvars content and HCL expressions."
sources:
  - https://developer.hashicorp.com/terraform/language/functions/terraform-encode_tfvars
  - https://developer.hashicorp.com/terraform/language/functions/terraform-decode_tfvars
  - https://developer.hashicorp.com/terraform/language/functions/terraform-encode_expr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# terraform provider functions: encode_tfvars and decode_tfvars

Terraform 1.8 added `decode_tfvars`, `encode_tfvars` and `encode_expr` to the built-in `terraform` provider (`terraform.io/builtin/terraform`). Unlike the `terraform_data` resource, the functions are **not** available without declaring the provider; call them with the `provider::terraform::` prefix after adding:
```hcl
terraform {
  required_providers {
    terraform = { source = "terraform.io/builtin/terraform" }
  }
}
```
Without that entry Terraform 1.17.0 fails with `Unknown provider function ... Ensure that provider name "terraform" is declared in this module's required_providers block`.

## decode_tfvars: read tfvars content
```hcl
locals {
  env = provider::terraform::decode_tfvars(file("${path.module}/envs/prod.tfvars"))
}
output "region" { value = local.env.region }
```
- Input is a string in `.tfvars` syntax (attributes only, literal values); returns an object (`region = "eu-west-1"`, `size = 3`, `tags = { a = "b" }` came back as an object with those keys).
- Expressions referencing variables or functions are rejected - the content must be static values (`a = upper("x")` fails with `Function calls not allowed`, `a = var.x` with `Variables not allowed`).
- Handy for sharing one tfvars file between a root module (as `-var-file`) and other configurations that just need to read values (e.g. a Terraform test file or a stack wrapper).

## encode_tfvars: generate tfvars
```hcl
resource "local_file" "child_vars" {
  filename = "${path.module}/generated/child.auto.tfvars"
  content  = provider::terraform::encode_tfvars({
    region = var.region
    tags   = { Owner = "platform", CostCenter = "1234" }
    azs    = ["eu-west-2a", "eu-west-2b"]
  })
}
```
Produces canonical tfvars formatting:
```
azs    = ["eu-west-2a", "eu-west-2b"]
region = "eu-west-2"
tags = {
  CostCenter = "1234"
  Owner      = "platform"
}
```
The argument must be an object (a list fails with `must be an object whose attribute names will become the encoded variable names`) whose keys are valid variable names (`1bad` fails with `must be a valid identifier`; `bad-key` was accepted, since hyphens are legal in identifiers). Keys come out sorted, as shown. Unknown values are accepted: with `id = terraform_data.x.id` the plan showed the file `content` as `(known after apply)` and the apply wrote `id = "<uuid>"`.

## encode_expr: one HCL expression
```hcl
locals {
  expr = provider::terraform::encode_expr(["a", "b"])   # -> ["a", "b"]
}
```
Useful when templating HCL snippets (generated config for other tools) without hand-escaping strings.

## Use cases
- Generating per-environment tfvars for downstream pipelines from a central definition (instead of jsonencode, which yields `.tfvars.json`).
- Reading existing tfvars in tests or wrappers without duplicating values.
- Templating Terragrunt/other HCL files.

## Gotchas
- Not available before Terraform 1.8 (the v1.8 changelog lists the three functions as new). OpenTofu 1.13.2 ran the same `encode_tfvars`, `decode_tfvars` and `encode_expr` calls with the same `required_providers` entry, and without the entry failed with `Unknown function provider`; check its docs for other versions.
- Writing files from Terraform (local_file) to feed another Terraform run is a coupling smell; prefer remote state outputs or a parameter store for live values.
- Sensitive values passed into encode_tfvars produce sensitive output (`(sensitive value)` in console); writing them to disk leaks them.

## Verify
- [ ] `terraform console` round trip: `provider::terraform::decode_tfvars(provider::terraform::encode_tfvars({a = 1}))` returns `{ a = 1 }`.
- [ ] `terraform version` shows 1.8+ in every pipeline using these functions.

## Checked
- Terraform 1.17.0 and OpenTofu 1.13.2, local tfvars file: every snippet in the skill ran with the `required_providers` entry added: decode of a tfvars file, `encode_tfvars` output byte-for-byte as in the skill (sorted keys, nested object formatting), `encode_expr(["a","b"])` gave `["a", "b"]` as a string, and the console round trip `decode_tfvars(encode_tfvars({a = 1}))` returned `{ a = 1 }`. The `local_file` generation example applied and wrote the file.
- Error messages quoted above were reproduced in `terraform console`; the claim "no `required_providers` entry needed" was wrong (provider function not found without it) and was fixed; "valid identifiers" and "known at plan time" were corrected from runs.
- Source: v1.8 changelog (raw.githubusercontent.com/hashicorp/terraform/v1.8/CHANGELOG.md) lists the three functions. `terraform version` is 1.17.0, satisfying the 1.8+ check.
