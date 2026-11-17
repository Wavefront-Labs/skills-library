---
id: computing-software.cloud-infrastructure-engineering.terraform.per-environment-tfvars-files
name: per-environment-tfvars-files
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, env-tfvars, tfvars, var-file-order, multi-environment, environment-layout]
level: practitioner
status: docs-checked
description: "Organise per-environment tfvars: one root plus envs/<env>.tfvars, pairing them with backend config, auto.tfvars pitfalls, and CI matrices that plan every environment."
sources: ["https://developer.hashicorp.com/terraform/language/values/variables#variable-definitions-tfvars-files", "https://developer.hashicorp.com/terraform/language/backend#partial-configuration", "https://developer.hashicorp.com/terraform/cli/commands/init", "https://developer.hashicorp.com/terraform/cli/commands/plan"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Per-environment tfvars

## Layout
```
infra/payments/
  main.tf variables.tf outputs.tf versions.tf
  envs/
    dev.tfvars        dev.s3.tfbackend
    staging.tfvars    staging.s3.tfbackend
    prod.tfvars       prod.s3.tfbackend
```
Backend files are named `*.backendname.tfbackend` (here `s3`), the pattern HashiCorp
recommends so editors understand the content. Each holds the backend block's
arguments as top-level attributes, and the root declares an empty `backend "s3" {}`.
```bash
ENV=prod
terraform init -reconfigure -backend-config=envs/$ENV.s3.tfbackend
terraform plan -var-file=envs/$ENV.tfvars -out=$ENV.tfplan
```
Changing backend settings on an already-initialised directory needs `-reconfigure`
or `-migrate-state`. `-reconfigure` disregards the existing configuration and does not
migrate state, which is what you want when hopping between environments with separate
states. Name the plan file with a suffix such as `.tfplan`, never `.tf`.

## What goes in tfvars
- Sizes, counts, CIDRs, feature flags, account/region IDs, domain names.
- Not secrets: ignore definition files that hold sensitive values in version control,
  and supply secrets through `TF_VAR_` environment variables instead.
- Not structure differences: if prod needs extra resources, use flags, not different code.

## Pitfalls
| Pitfall | Effect |
|---|---|
| `terraform.tfvars` or `*.auto.tfvars` in the root | loaded automatically for **every** environment; `-var-file` values override them, so a key missing from the env file silently takes the auto-loaded value |
| Backend and tfvars mismatched (prod tfvars, dev backend) | plans dev state with prod values: massive replace plan |
| Missing key in one env file | uses the variable's `default`; remove defaults for env-critical vars |

Precedence, lowest to highest: variable `default`, environment variables,
`terraform.tfvars`, `terraform.tfvars.json`, `*.auto.tfvars*` in lexical order, then
`-var` and `-var-file` in the order given.

Guard the mismatch by deriving both files from one argument, never typing them twice:
```bash
#!/usr/bin/env bash
# tf.sh <env>
set -euo pipefail
ENV=$1
terraform init -input=false -reconfigure -backend-config="envs/$ENV.s3.tfbackend"
terraform plan -input=false -var-file="envs/$ENV.tfvars" -var="environment=$ENV"
```
and give `environment` no default, so a missing value cannot slip through: a variable
without a default makes Terraform prompt for it, and `-input=false` disables the prompt.
Do not put spaces around the `=` in `-var`.

## CI matrix
```yaml
strategy:
  matrix: { env: [dev, staging, prod] }
steps:
  - run: terraform init -input=false -reconfigure -backend-config=envs/${{ matrix.env }}.s3.tfbackend
  - run: terraform plan -input=false -var-file=envs/${{ matrix.env }}.tfvars
```

## Checked
Date: 2026-11-07
Read in full: "Use input variables to add module arguments" (variables page, incl. Variable definition files and precedence list), "Backend block configuration overview" (incl. Partial configuration, File), `terraform init` (Backend Initialization, General Options), `terraform plan` (all sections).
Confirmed: precedence order, auto-loaded file names, `-var-file`, `-out=FILENAME` and the `.tf` suffix warning, `-input=false`, `-backend-config=PATH`, `*.backendname.tfbackend` naming, empty backend block for partial configuration, no spaces around `=` in `-var`, prompting for variables with no default.
Changed: renamed `*.backend.hcl` to the recommended `.s3.tfbackend`; replaced the wrong claim that omitting `-reconfigure` "reuses the previous backend" with the init page wording (`-reconfigure` or `-migrate-state` required, `-reconfigure` prevents state migration); dropped "ephemeral lookups"; the helper script no longer forwards arbitrary arguments; removed the Verify checklist.
Not opened: the GitHub Actions matrix is a generic example, not from HashiCorp docs.
Method: documentation only; no commands were run.
