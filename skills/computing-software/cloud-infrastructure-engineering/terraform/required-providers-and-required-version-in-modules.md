---
id: computing-software.cloud-infrastructure-engineering.terraform.required-providers-and-required-version-in-modules
name: required-providers-and-required-version-in-modules
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, module-required-version, required-version-modules, required-providers, version-constraints, module-design]
level: practitioner
status: docs-checked
description: "Write versions.tf for reusable modules: minimum-only required_version and provider constraints, source addresses, configuration_aliases, and why roots pin while modules do not."
sources: ["https://developer.hashicorp.com/terraform/language/modules/develop/providers", "https://developer.hashicorp.com/terraform/language/terraform", "https://developer.hashicorp.com/terraform/language/providers/requirements"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# required_version and required_providers in modules

## Reusable module (`versions.tf`)
```hcl
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.30"          # minimum that has the features you use
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.5"
    }
  }
}
```

## Rules
- **Modules declare minimums**, roots pin. The Terraform docs say a shared module should
  constrain only the minimum provider version, using `>=`, set to the minimum version
  containing the features the module relies on, so callers can select newer versions.
- Terraform must find a single provider version compatible with every module in the
  configuration, and a Terraform version satisfying every `required_version` in the tree.
  An upper bound in a widely used module therefore constrains every caller; add one only
  when you know the next major breaks the module.
- Every module declares its own provider requirements: child modules inherit provider
  *configurations* from the parent, not source or version requirements. This matters most
  for non-HashiCorp providers.
- Always include `source`. If omitted, Terraform assumes `registry.terraform.io/hashicorp/<LOCAL NAME>`
  (a backward-compatibility feature; the docs recommend explicit sources for 0.13 and later).
- `required_version` in a module = the minimum Terraform version with the language
  features it uses (look the feature up in the Terraform changelog).
- Provider configurations (`provider` blocks) are defined only in the root module;
  declare `configuration_aliases` in `required_providers` when the module needs aliased
  provider configurations.

## Root module
```hcl
terraform {
  required_version = "~> 1.9.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.70" }
  }
}
```
Locally, `terraform init` records the selected provider versions in the dependency lock
file; changing `version` and re-running `terraform init` upgrades them. Commit the lock
file for the root.

## Verify
- [ ] Every module's `versions.tf` has `source` for each provider and only minimum constraints.
- [ ] Module CI tests against the minimum and latest provider versions.

## Checked
Date: 2026-10-28.
Confirmed in the provider-requirements-in-modules page: minimum-only `>=` advice,
`configuration_aliases`, per-module requirements, inherited configurations but not
requirements, provider blocks only in the root. Confirmed in the provider requirements
page: implied `hashicorp/<LOCAL NAME>` source, lock file update on `init`. Confirmed in
the terraform block reference: all `required_version` constraints in the tree must be satisfied.
Removed as unconfirmed: the feature-to-version map, the `terraform providers` and error
message comments, the tflint rule names, the "no lock file for modules" rule, the
non-HashiCorp provider examples.
Method: documentation only; no commands were run.
