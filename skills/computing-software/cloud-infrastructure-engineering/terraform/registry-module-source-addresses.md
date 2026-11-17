---
id: computing-software.cloud-infrastructure-engineering.terraform.registry-module-source-addresses
name: registry-module-source-addresses
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, registry-source, module-source, module-registry, version-constraint, private-registry]
level: practitioner
status: docs-checked
description: "Write registry module source addresses correctly: public NAMESPACE/NAME/PROVIDER, private hostnames, submodules with //, and the version argument."
sources: ["https://developer.hashicorp.com/terraform/language/modules/configuration", "https://developer.hashicorp.com/terraform/registry/modules/use", "https://developer.hashicorp.com/terraform/language/block/module"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Registry module source addresses

## Forms
```hcl
module "consul" {
  source  = "hashicorp/consul/aws"                       # public registry
  version = ">= 0.10.0"
}
module "net" {
  source  = "app.terraform.io/example_corp/vpc/aws"      # HCP Terraform private registry
  version = "0.9.3"
}
module "net_tfe" {
  source  = "tfe.example.com/example_corp/vpc/aws"       # Terraform Enterprise: your hostname
  version = ">= 2.4.0, < 3.0.0"
}
module "cluster" {
  source = "hashicorp/consul/aws//modules/consul-cluster"   # subdirectory of the module
}
```
- Public registry: `<NAMESPACE>/<NAME>/<PROVIDER>`.
- Private registry: `<HOSTNAME>/<NAMESPACE>/<NAME>/<PROVIDER>`, the same format with a
  hostname prefix. For HCP Terraform the hostname is `app.terraform.io`; for Terraform
  Enterprise it is your deployment's hostname. On both you can instead use
  `localterraform.com`, which requests modules from the instance the platform runs on.
- Add `//` followed by a path to select a sub-directory within the package. Put any query
  parameters (such as `ref`) after the sub-directory segment.
- The `source` value must be a literal string, except that it can reference constant
  input variables and local values (variables declared with `const = true`).
- Private registries may need credentials; see your registry's documentation.

## version
- The `version` argument applies only to modules installed from a registry. Modules from
  local paths do not support it, because they share the version of their caller.
- Git sources have no `version`; select a revision with the `ref` query parameter
  (branch, tag or SHA-1 hash), for example `git::https://example.com/vpc.git?ref=v1.2.0`.
  Without `ref`, Terraform uses the default branch referenced by HEAD.
- Without `version` the default is the latest version available from the source.
  HashiCorp recommends explicitly constraining acceptable versions to avoid unwanted
  changes. Registry versions follow semantic versioning, and constraint syntax is the same
  as for providers.
- After changing `source`, or changing `version` for a registry module, rerun
  `terraform init`. For already-installed modules, `terraform init -upgrade` moves to the
  latest version the constraint allows.
- Versioned registry resolution needs Terraform 0.11 or later; before that, Terraform
  downloaded the latest version regardless of the constraint.

## Checked
Date: 2026-11-07
Read in full: "Use modules in your configuration" (the page the `modules/sources#terraform-registry` link redirects to), "Find and use modules". The module block reference (`language/block/module`, redirect target of the old `modules/syntax#version` link): read the source Terraform registry section, the `version` section and the version/subdirectory examples, not every section of the large page.
Confirmed: address formats, hostnames, `localterraform.com`, `//` subdirectories, literal-string rule, `ref`, version scope, default, `init` and `init -upgrade` behaviour, semver and 0.11 notes.
Removed (not on the pages): the `terraform-<PROVIDER>-<NAME>` naming convention, the OpenTofu `registry.opentofu.org` statement, the whole error table (Module not found, Unsupported argument, 401, no available releases), the `terraform login` / `TF_TOKEN_` advice, the modules.json Verify step, and real-looking third-party module names (replaced with the docs' examples). Updated the `sources` URLs to the redirect targets.
Method: documentation only; no commands were run.
