---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-version-json-output
name: terraform-version-json-output
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, version-json, terraform-version, version-check, ci-guard, provider-versions, upgrade-terraform-version]
level: practitioner
status: verified
description: "Use terraform version -json in scripts and CI: parse the CLI version, platform and provider selections, check outdated status, and enforce version policy before plans run."
sources:
  - https://developer.hashicorp.com/terraform/cli/commands/version
  - https://developer.hashicorp.com/terraform/language/terraform#specifying-a-required-terraform-version
  - https://developer.hashicorp.com/terraform/cli/commands/providers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# terraform version -json

## Output
```bash
terraform version -json
```
```json
{
  "format_version": "1.0",
  "terraform_version": "1.17.0",
  "platform": "windows_amd64",
  "provider_selections": {
    "registry.terraform.io/hashicorp/local": "2.9.1",
    "registry.terraform.io/hashicorp/random": "3.9.1"
  },
  "terraform_outdated": false
}
```
- `provider_selections` reflects providers installed in the **current working directory** after `terraform init` (from `.terraform/` and the lock file); empty before init.
- `terraform_outdated` comes from the version check (the checkpoint service); with `CHECKPOINT_DISABLE=1` it printed `false`, and it was also `false` on the latest release with the check on.
- Before `init`, `provider_selections` is `{}` (run).

## Script uses
```bash
v=$(terraform version -json | jq -r .terraform_version)
# guard: CI must use the version in .terraform-version
want=$(cat .terraform-version)
[ "$v" = "$want" ] || { echo "Terraform $v but repo pins $want"; exit 1; }

# inventory provider versions across many roots
for d in $(find live -name .terraform.lock.hcl -exec dirname {} \;); do
  (cd "$d" && terraform init -backend=false -input=false >/dev/null && \
   terraform version -json | jq -r --arg d "$d" '.provider_selections | to_entries[] | "\($d)\t\(.key)\t\(.value)"')
done | sort > provider-inventory.tsv
```
Use the inventory to find roots stuck on old AWS provider majors before a planned upgrade.

## Version policy in config (complements the CI guard)
```hcl
terraform {
  required_version = "~> 1.17.0"
  required_providers { local = { source = "hashicorp/local", version = "~> 2.9" } }
}
```
`required_version` fails `init`/`plan` with a clear error on mismatch; the CI guard catches drift earlier and also enforces exact versions in pipelines.

## Related
- `terraform providers` - dependency tree of provider requirements per module.
- `terraform providers lock -platform=...` - multi-platform hashes in the lock file.

## Verify
- [ ] CI fails fast when the runner's Terraform differs from the pinned version.
- [ ] Provider inventory produced for all roots before an upgrade campaign.

## Checked
- Terraform 1.17.0 with `hashicorp/local` and `hashicorp/random`: `terraform version -json` (fields, `format_version`, `provider_selections` empty before init and populated after), the CI guard against `.terraform-version`, and the provider-inventory loop across two roots (jq 1.8.2) all ran; `terraform providers lock -platform` wrote hashes for two platforms.
- Added the missing `format_version` field; dropped the unchecked compatibility-promise and OpenTofu statements. `required_version` mismatch errors were run in the version-constraint skill.
