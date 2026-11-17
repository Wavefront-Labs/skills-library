---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-output-json-and-raw-in-scripts
name: terraform-output-json-and-raw-in-scripts
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, output-json, output-raw, output-sensitive, terraform-output, scripting, jq]
level: practitioner
status: verified
description: "Consume outputs from scripts with terraform output -json and -raw: sensitive values, types, jq recipes, CI masking, and avoiding stale or wrong-workspace reads."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/output", "https://developer.hashicorp.com/terraform/language/values/outputs#sensitive-suppressing-values-in-cli-output"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform output -json` and `-raw`

## Forms
```bash
terraform output                       # human; sensitive shown as <sensitive>
terraform output vpc_id                # HCL-quoted: "vpc-0abc"
terraform output -raw vpc_id           # vpc-0abc   (no quotes, no newline)
terraform output -json                 # all outputs: {"name":{"value":..,"type":..,"sensitive":bool}}
terraform output -json subnet_ids      # just the value, JSON-encoded
```

## Recipes
```bash
VPC_ID=$(terraform output -raw vpc_id)
mapfile -t SUBNETS < <(terraform output -json subnet_ids | jq -r '.[]')
terraform output -json | jq -r 'to_entries[] | select(.value.type=="string") | "\(.key)=\(.value.value)"' > outputs.env   # strings only (jq 1.8.2 ran it)
DB_PASS=$(terraform output -raw db_password)                               # sensitive: printed in full!
```

## Sensitive values
`-json` and `-raw` print sensitive values **in plaintext** (the CLI assumes a script
is asking deliberately). In CI:
```bash
PASS=$(terraform output -raw db_password)
echo "::add-mask::$PASS"          # GitHub Actions; GitLab: masked variables
```
Never `terraform output -json` into a build log.

## Types
- `-raw` works only for strings, numbers and bools; a list errors with `Unsupported value for raw output ... is tuple` (exit 1) — use `-json`.
- Numbers come out as JSON numbers; quote carefully in shell arithmetic.
- Null-valued outputs are not kept in state: after apply, `terraform output nul`,
  `-raw nul` and `-json nul` all fail with `Output "nul" not found` (exit 1), and
  `-json` with no name omits it. Default to `""` in the output if scripts need the key.

## Gotchas
- Output reads state, not config: after editing an output's value in config,
  `terraform output` still showed the old value (`vpc-0abc`) until
  `terraform apply -refresh-only` updated it (`vpc-NEW`).
- Reads the **selected workspace** — set `TF_WORKSPACE` explicitly in scripts
  (`TF_WORKSPACE=dev terraform output` read the `dev` workspace, which here had no outputs).
- The `hashicorp/setup-terraform` action installs a wrapper that exposes stdout, stderr
  and exit code as step outputs; set `terraform_wrapper: false` to skip it (action README).

## Verify
- [ ] `terraform output -raw vpc_id | od -c` shows `v p c - 0 a b c` and no trailing quote or newline.
- [ ] CI logs show `***` where sensitive outputs are used.

## Checked
- Terraform 1.17.0 with outputs of every type (string, tuple, number, bool, map, null, sensitive): ran `output`, `output name`, `-raw` (od shows no quote or newline; tuple errors; num/bool print), `-json` (all and one name; sensitive printed in plaintext), the jq recipes with jq 1.8.2, nonexistent output (exit 1), stale output vs `apply -refresh-only`, and `TF_WORKSPACE`.
- GitHub docs: `::add-mask::{value}`; setup-terraform README: `terraform_wrapper` input. Removed the unchecked HCP Terraform permission claim and the kubeconfig/mapfile specifics were left as plain bash.
