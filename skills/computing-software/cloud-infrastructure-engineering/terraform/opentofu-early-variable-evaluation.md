---
id: computing-software.cloud-infrastructure-engineering.terraform.opentofu-early-variable-evaluation
name: opentofu-early-variable-evaluation
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, early-evaluation, early-variable-evaluation, backend-configuration, module-sources, tofu-files, static-evaluation]
level: advanced
status: gated
description: "Use OpenTofu 1.8+ early evaluation to put variables and locals in backend blocks, module source/version and encryption config, and keep Terraform compatibility."
sources: ["https://opentofu.org/docs/intro/whats-new/", "https://opentofu.org/docs/language/settings/backends/configuration/", "https://opentofu.org/docs/language/modules/sources/", "https://opentofu.org/docs/language/files/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenTofu early variable evaluation

Terraform rejects variables in `terraform {}` and module `source` with "Variables may
not be used here" (Terraform 1.17.0: `Error: Variables not allowed` for a backend argument). OpenTofu 1.8.0 added early (static) evaluation
(v1.8 changelog: "Variables and Locals allowed in module sources and backend configurations (with limitations)"): these places can use
input variables, locals and pure functions, as long as the value is known at `init`.

## 1. Where it works
```hcl
variable "env" { type = string }
variable "vpc_ref" {
  type    = string
  default = "v3.2.0"
}
variable "eks_module_version" {
  type    = string
  default = "20.24.0"
}
locals { state_key = "${var.env}/network.tfstate" }

terraform {
  backend "s3" {
    bucket = "acme-tfstate-${var.env}"
    key    = local.state_key
    region = "eu-west-1"
  }
}

module "vpc" {
  source = "git::https://github.com/acme/terraform-aws-vpc.git?ref=${var.vpc_ref}"
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = var.eks_module_version
}
```
The `encryption` block (state/plan encryption) can also reference variables (1.8.0 changelog: "Allow variables and other static values to be used in
encryption configuration"), which is how key providers get per-environment keys. Tested on OpenTofu 1.13.2: a `key_provider "pbkdf2"` whose `passphrase = var.pass`
with `aes_gcm` state encryption wrote an encrypted state file (`meta` holds `key_provider.pbkdf2.k`) and a plan with a different passphrase failed with
`decryption failed for all provided methods` (shown inside the state-lock error).
A local-backend and local-module version of the same pattern, which ran here:
```hcl
variable "env" { type = string }
variable "mod" {
  type    = string
  default = "a"
}
locals { state_path = "state/${var.env}.tfstate" }
terraform {
  backend "local" { path = local.state_path }
}
module "m" { source = "./mods/${var.mod}" }
```
`tofu init -var env=dev` then `tofu apply -var env=dev` wrote `state/dev.tfstate` and the module output came from `mods/a`; `tofu init -var env=prod` then failed with `Backend configuration changed` and the `tofu init -reconfigure` hint.

## 2. What is allowed in the expression
- Input variables, locals derived from them, literals, and built-in functions that do
  not depend on infrastructure.
- Not allowed: resource or data source attributes, module outputs, anything unknown
  until plan. Those fail at `init` with an error naming the reference (`Error: Dynamic value in static context ... Unable to use terraform_data.x in static context, which is required by backend.local`).

## 3. Supplying the values at init
Variables used early must be available when `tofu init` runs, not just at plan:
```bash
tofu init -var-file=env/prod.tfvars       # init accepts -var / -var-file (ran `tofu init -var env=dev` on 1.13.2)
tofu plan -var-file=env/prod.tfvars
# or once for both
export TF_VAR_env=prod
```
Changing a value that feeds the backend or a module source requires re-running
`init` (`-reconfigure` for a different backend, `-migrate-state` to move state, `-upgrade`
for new module refs). This replaces most `-backend-config` partial configuration files
and many Terragrunt `generate` blocks.

## 4. Keeping Terraform compatibility
Early evaluation is OpenTofu-only. If a module must work with both:
- Put the OpenTofu-only version in a `.tofu` file (`backend.tofu`) next to the
  Terraform version (`backend.tf`). OpenTofu prefers `x.tofu` over `x.tf` with the same
  base name and Terraform ignores `.tofu` files (tested with `main.tf` and `main.tofu` declaring different local-backend paths:
  `tofu` wrote `from-tofu.tfstate`; `terraform init` did not use the `.tofu` file and reported `Backend configuration changed`). The `.tofu` extension was added in 1.8.0.
- Reusable shared modules should not need any of this; it belongs in root modules.

## Gotchas
- A variable without a default used in the backend makes every `init` prompt (`var.env  Enter a value:` appeared without `-var`; the prompt can
  only be answered interactively, so pass `-var`/`-var-file`, set `TF_VAR_env`, or use `-input=false` in CI); give CI the var file at init.
- Sensitive variables in a backend block still end up in `.terraform/terraform.tfstate`
  (the backend config cache); prefer environment variables for backend credentials.
- Workspaces plus variable backends are two ways to separate environments; pick one per
  root module.

## Verify
- [ ] `tofu init -var env=dev` and `-var env=prod` point at different state buckets.
- [ ] Bumping `vpc_ref` and running `tofu init -upgrade` fetches the new module ref.
- [ ] `terraform init` still works on the same directory if compatibility is required.

## Checked
- OpenTofu 1.13.2 and Terraform 1.17.0 on Windows with the local backend and local modules: variable in `backend "local"` path and in a module `source` worked on OpenTofu and was rejected on Terraform; `init -var`; re-init with a changed variable needed `-reconfigure`; resource attribute in a backend gave `Dynamic value in static context`; `.tofu` precedence; encryption with a variable passphrase.
- Changelog source: raw.githubusercontent.com/opentofu/opentofu/v1.8/CHANGELOG.md, section 1.8.0 (variables and locals in module sources and backends, `.tofu` files, variables in encryption configuration).
- Not run: the S3 backend, the git-sourced module with `?ref=${var.vpc_ref}`, the registry module with `version = var.eks_module_version` (needs registry downloads of AWS-dependent modules), `-upgrade` for new module refs, per-environment KMS keys, sensitive variables in the backend cache, and the workspaces comparison (gated: unconfirmed, source is paywalled or blocked). The reason is that no S3, AWS or git module repository was used.
