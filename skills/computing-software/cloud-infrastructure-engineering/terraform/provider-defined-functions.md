---
id: computing-software.cloud-infrastructure-engineering.terraform.provider-defined-functions
name: provider-defined-functions
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, provider-functions, provider-defined-functions, provider-function, terraform-1-8, opentofu-1-7, aws-arn-parse, kubernetes-manifest-decode, plugin-framework, function-protocol, provider-function-syntax]
level: practitioner
status: docs-checked
description: "Call provider-defined functions (provider::aws::arn_parse, provider::kubernetes::manifest_decode) in Terraform 1.8+ and OpenTofu 1.7+; how names resolve from required_providers."
sources: ["https://developer.hashicorp.com/terraform/language/functions#provider-defined-functions", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/functions/arn_parse.html.markdown", "https://raw.githubusercontent.com/hashicorp/terraform-provider-kubernetes/main/docs/functions/manifest_decode.md", "https://developer.hashicorp.com/terraform/plugin/framework/functions", "https://opentofu.org/docs/language/functions/#provider-defined-functions"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Provider-defined functions

**Goal:** use functions shipped by providers (ARN parsing, manifest decoding) instead of fragile `split()`/`regex()`
chains, and know how calls resolve.

## 1. Requirements and syntax
- Provider-defined functions are supported in Terraform **1.8 and later** (Plugin Framework docs) and OpenTofu **1.7.0
  and later**. You cannot define your own functions in the configuration language; they come from providers.
- Call them as `provider::<local-name>::<function>(args)`, where `<local-name>` matches an entry in
  `required_providers`. A provider example from the kubernetes docs:
```hcl
terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
    }
  }
  # Provider functions require Terraform 1.8 and later.
  required_version = ">= 1.8.0"
}

output "example_output" {
  value = provider::kubernetes::manifest_decode(file("manifest.yaml"))
}
```
- OpenTofu: functions are added under `provider::<provider_name>::<function_name>`; aliases are supported as
  `provider::<provider_name>::<provider_alias>::<function_name>`. Functions are scoped to the module that requires the
  provider and are not inherited by child modules, so declare the provider in every module that calls its functions.

## 2. Functions worth knowing
```hcl
locals {
  arn = provider::aws::arn_parse("arn:aws:iam::444455556666:role/example")
  # => { partition = "aws", service = "iam", region = "", account_id = "444455556666", resource = "role/example" }

  manifest = provider::kubernetes::manifest_decode(file("${path.module}/deploy.yaml"))
}
```
- `provider::aws::arn_parse(arn string) object`: parses an ARN into its parts.
- `provider::kubernetes::manifest_decode(manifest string) object`: decodes YAML for a Kubernetes manifest into a
  dynamic object that mirrors the YAML structure.
- Functions defined by external providers are documented by those providers in the Terraform Registry; check the
  provider's own functions page for the current set and signatures.
- Terraform's built-in provider `terraform` offers functions such as `provider::terraform::encode_tfvars`. OpenTofu has
  a built-in provider `terraform.io/builtin/terraform` with additional functions.

## 3. Testing
`terraform console` (or `tofu console`) lets you try functions interactively.

## 4. Writing one
Functions are added to a provider through the Terraform Plugin Framework (supported in Terraform 1.8 and later). The
framework docs cover concepts, implementation, testing and documentation of a provider-defined function. For
OpenTofu, function support was added in provider protocol versions 5.5 and 6.5, and providers that supply functions
may also be configured. See
`computing-software.cloud-infrastructure-engineering.terraform.provider-development-with-the-plugin-framework`.

## Gotchas
- Set `required_version` (Terraform) so older CLIs fail with a clear version message rather than a syntax error.
- The prefix is the provider's local name from `required_providers`, so a renamed provider changes every call.

## Verify
- [ ] `terraform version` is 1.8 or later (or `tofu` 1.7 or later) and `required_version` enforces it.
- [ ] `terraform console` evaluates `provider::aws::arn_parse("arn:aws:s3:::b")` to an object.

## Checked
Confirmed 2026-11-08 against the Terraform built-in functions page, the aws `arn_parse` and kubernetes
`manifest_decode` function docs, the Plugin Framework functions overview and the OpenTofu functions page. Removed:
the claim that functions never use a provider block (OpenTofu page says providers supplying functions may be
configured), the unconfirmed `arn_build`, `trim_iam_role_path`, `manifest_decode_multi`, `manifest_encode`,
`provider::time::*`, google and azurerm function names, parse-error wording, unknown-argument and purity rules,
`providers schema -json` output, provider-lock behaviour, `provider::tofu::` names, and Framework implementation details
(`function.Function` methods, parameter flags) that the cited overview page does not cover.
Method: docs-only read of cited pages, 2026-11-08
