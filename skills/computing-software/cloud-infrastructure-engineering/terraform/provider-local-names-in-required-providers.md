---
id: computing-software.cloud-infrastructure-engineering.terraform.provider-local-names-in-required-providers
name: provider-local-names-in-required-providers
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, provider-local-name, required-providers, source-address, provider-configuration]
level: practitioner
status: docs-checked
description: "Use provider local names correctly: the key in required_providers, how resource type prefixes map to providers, two providers with the same type name, and module consistency."
sources: ["https://developer.hashicorp.com/terraform/language/providers/requirements#local-names", "https://developer.hashicorp.com/terraform/cli/commands/state/replace-provider"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Provider local names

```hcl
terraform {
  required_providers {
    aws = {                          # <- local name
      source  = "hashicorp/aws"      # <- source address (global identity)
      version = "~> 5.70"
    }
  }
}
provider "aws" { region = "eu-west-1" }   # configured by local name
```

## Two identifiers
- The **source address** (`[<HOSTNAME>/]<NAMESPACE>/<TYPE>`) is the provider's global
  identifier and is only used when requiring a provider. The hostname defaults to
  `registry.terraform.io`.
- The **local name** is module-specific, assigned in `required_providers`, must be unique
  per module, and is used everywhere else in the module.

## How resources find their provider
If a resource does not set `provider`, Terraform interprets the first word of the
resource type as the local provider name (`aws_instance` -> `aws`). If you omit
`source` in `required_providers`, Terraform uses the implied address
`registry.terraform.io/hashicorp/<LOCAL NAME>`; that is a backward-compatibility
feature, and for Terraform 0.13+ modules HashiCorp recommends explicit source
addresses for all providers. Declare `required_providers` in every module, which is
especially important for non-HashiCorp providers.

## Same type name, different providers
When two providers share a preferred local name (for example `http`) HashiCorp
recommends compound local names, namespace plus type, with a dash:
```hcl
required_providers {
  hashicorp-http = { source = "hashicorp/http", version = "~> 2.0" }
  mycorp-http    = { source = "mycorp/http",    version = "~> 1.0" }
}
data "http" "example" {
  provider = hashicorp-http
}
```
Terraform cannot guess either provider from resource types, so every affected resource
needs an explicit `provider` meta-argument.

## Conventions
- Use the provider's preferred local name (usually the type part of its source
  address, and the prefix of its resource types: `aws`, `google`, ...) whenever
  possible. It makes configuration easier to read and lets you omit `provider` on most
  resources. Exception: `hashicorp/google-beta` has the preferred local name `google`.
- Compound names are for the rare conflict only.

## Changing the source
To change the source address of a provider that already has resources in state, use
`terraform state replace-provider FROM_PROVIDER_FQN TO_PROVIDER_FQN`; it updates all
resources using the "from" provider and always writes a backup first.

## Checked
Date: 2026-11-07
Read in full: "Provider Requirements" (all sections, including Names and Addresses, Handling Local Name Conflicts, Built-in Providers) and `terraform state replace-provider`.
Confirmed: local name versus source address, uniqueness per module, first-word rule, implied `hashicorp/<LOCAL NAME>` source, compound-name recommendation and example, preferred-name guidance, google-beta exception, replace-provider behaviour.
Removed (not on the pages): the claim that state records the full source address and that renaming a local name is therefore safe, the claim that changing a local name breaks `providers = {}` passing, the `integrations/github` error text, and the Verify steps. Dropped the second source (the resource-provider meta-argument page returned 404).
Method: documentation only; no commands were run.
