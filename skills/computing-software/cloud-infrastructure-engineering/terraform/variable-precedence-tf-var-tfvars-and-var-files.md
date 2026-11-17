---
id: computing-software.cloud-infrastructure-engineering.terraform.variable-precedence-tf-var-tfvars-and-var-files
name: variable-precedence-tf-var-tfvars-and-var-files
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, variable-precedence, tf-var-env, tf-var-prefix, var-file-order, auto-tfvars-ordering, tfvars-json, var-complex, var-cli-complex]
level: practitioner
status: verified
description: "Know exactly which variable value wins: TF_VAR_ env, terraform.tfvars, *.auto.tfvars order, -var-file and -var, JSON tfvars, and passing lists/maps on the CLI."
sources: ["https://developer.hashicorp.com/terraform/language/values/variables#variable-definition-precedence", "https://developer.hashicorp.com/terraform/language/values/variables#environment-variables", "https://developer.hashicorp.com/terraform/language/values/variables#variable-definitions-tfvars-files"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variable precedence and input forms

## Order (later wins)
1. Variable `default`.
2. `TF_VAR_<name>` environment variables.
3. `terraform.tfvars`, then `terraform.tfvars.json` (the JSON file won when both set the variable).
4. `*.auto.tfvars` / `*.auto.tfvars.json`, in **lexical filename order** (`05.auto.tfvars.json` beat `04.auto.tfvars`; `zz-local.auto.tfvars` beat `20-prod`).
5. `-var` and `-var-file` on the command line, in the **order given** (they are
   processed together, left to right).

So `-var-file=prod.tfvars -var region=us-east-1` → region from `-var`; reversing the
order lets the file win (both ran). A `TF_VAR_` value lost to `terraform.tfvars`.

## TF_VAR_
```bash
export TF_VAR_region=eu-west-1
export TF_VAR_db_password="$(vault kv get -field=pw secret/db)"
```
Names are case-sensitive on Linux (`TF_VAR_Region` ≠ `region`); not tested here, and Windows environment variable names are case-insensitive.

## Complex values
On the CLI and in `TF_VAR_`, values for non-string types are parsed as **HCL**:
```bash
terraform plan -var 'azs=["eu-west-1a","eu-west-1b"]'
terraform plan -var 'tags={team="core",cost="42"}'
export TF_VAR_sizes='{ api = 2, worker = 4 }'
```
Windows PowerShell 5.1: `-var 'azs=[\"a\",\"b\"]'` worked and the unescaped form failed with `Variables not allowed`. When quoting gets painful, use a var file.

## tfvars.json
```json
{ "region": "eu-west-1", "azs": ["eu-west-1a", "eu-west-1b"], "tags": { "team": "core" } }
```
Useful when another tool generates inputs. Same precedence slot as its HCL twin.

## auto.tfvars ordering trap
`10-defaults.auto.tfvars` then `20-prod.auto.tfvars`: prod wins. A stray
`zz-local.auto.tfvars` from someone's laptop wins over everything except CLI flags —
gitignore `*.local.auto.tfvars`.

## Undeclared variables
Values for variables not declared: in tfvars files (`terraform.tfvars`, `*.auto.tfvars`, `-var-file`) → warning; via `-var` → error (`plan`, `apply` and `console` all failed); via `TF_VAR_` → ignored silently.

## Gotchas
- Map values from multiple sources do not merge — the winning source replaces the whole map (an auto file with `{ c = "3" }` replaced the default `{ a, b }`).
- With `-chdir=sub`, `-var-file=s.tfvars` was found in `sub/` and `-var-file=sub/s.tfvars` failed (`Failed to read variables file`): relative `-var-file` paths follow `-chdir` (1.17.0).

## Verify
- [ ] `terraform console` (with the same flags) → `var.region` shows the expected winner.
- [ ] Precedence is deterministic — document the intended source per variable.

## Checked
- Terraform 1.17.0 in a scratch module, reading `var.region` through `terraform console` with each source: default, `TF_VAR_`, `terraform.tfvars`, `terraform.tfvars.json`, `*.auto.tfvars` and `.auto.tfvars.json` (lexical order), `-var` and `-var-file` in both orders, map replacement, `-var` HCL lists and maps, `TF_VAR_` map, `-chdir` with relative `-var-file`, undeclared values from each source, and Windows PowerShell 5.1 quoting of a list `-var`.
- Corrections: `-var-file` paths follow `-chdir` (the skill said they do not); the HCP Terraform remote-run claim was removed as unchecked. Case sensitivity of `TF_VAR_` names is stated as untested.
