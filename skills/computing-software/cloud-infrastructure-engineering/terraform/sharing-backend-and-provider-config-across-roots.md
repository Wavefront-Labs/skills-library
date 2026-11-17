---
id: computing-software.cloud-infrastructure-engineering.terraform.sharing-backend-and-provider-config-across-roots
name: sharing-backend-and-provider-config-across-roots
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, symlinked-config, partial-backend-configuration, backend-config-file, shared-provider-config, dry-terraform, symlinks]
level: practitioner
status: docs-checked
description: "Share backend configuration across many roots with partial backend config and -backend-config files; know what the docs say about secrets, merge order and the S3 key."
sources:
  - https://developer.hashicorp.com/terraform/language/backend
  - https://developer.hashicorp.com/terraform/cli/commands/init
  - https://developer.hashicorp.com/terraform/language/backend/s3
  - https://developer.hashicorp.com/terraform/language/block/provider
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sharing backend and provider config across roots

A backend block cannot refer to named values (input variables, locals, data source attributes), so every root module needs literal backend settings. Partial configuration is the built-in way to avoid copy-paste.

## 1. Partial backend configuration
Leave some or all arguments out of the `backend` block and supply them at `terraform init`. At minimum the root must contain an empty block naming the backend type.
```hcl
# backend.tf, identical in every root
terraform {
  backend "s3" {}
}
```
```hcl
# live/prod/prod.s3.tfbackend  (top-level attributes, no backend block)
bucket       = "acme-tfstate-prod"
region       = "eu-west-2"
encrypt      = true
use_lockfile = true
```
```bash
cd live/prod/network
terraform init \
  -backend-config=../prod.s3.tfbackend \
  -backend-config="key=prod/network/terraform.tfstate"
```
- `*.backendname.tfbackend` (for example `config.consul.tfbackend`) is the recommended file name pattern; other names work.
- Ways to supply values: a `-backend-config=PATH` file, `-backend-config="KEY=VALUE"` pairs, or interactive prompts (required values only).
- Merge order: command-line options override the main configuration, and later `-backend-config` options override earlier ones.
- Each root needs its own S3 `key`; the state lives at that key inside the bucket, so give each root a unique key (derive it from the directory path in a wrapper script so it cannot be mistyped).
- S3 locking: `use_lockfile` enables it; DynamoDB locking (`dynamodb_table`) is deprecated and can be configured alongside it during migration.

## 2. Secrets
- Terraform recommends supplying credentials through environment variables or the conventional credentials files and leaving credential arguments unset.
- If you use `-backend-config` or hardcode values, Terraform writes them in plain text to `.terraform/terraform.tfstate` and to saved plan files. Keep `.terraform/` out of Git.
- A saved plan applies using the backend settings it captured, so time-limited credentials passed that way may expire before apply.

## 3. Changing backend settings
After the backend configuration changes, `terraform init` needs `-reconfigure` (ignore existing configuration) or `-migrate-state` (copy existing state to the new backend). Back up `terraform.tfstate` before migrating.

## 4. Provider configuration
Provider blocks are defined in the root module and passed down to child modules; modules intended for reuse must not contain `provider` blocks. Put the shared provider settings in a reusable module's interface (inputs) or repeat the small block per root; the Terraform docs describe no mechanism for including one provider block in many roots.

Other tools (symlinked common files, Terragrunt `generate` blocks, Terramate `generate_hcl`) can write identical `providers.tf` and `backend.tf` into each root. They are outside the sources checked here; test them in your CI and on Windows checkouts before depending on them.

## Which to choose
| Need | Choice |
|---|---|
| A few accounts, plain Terraform | partial backend config plus a tiny wrapper that computes `key` |
| Hundreds of roots with dependencies | an orchestration tool (not covered by these sources) |

## Verify
- [ ] `terraform init` in any root uses the right bucket and a path-derived key; two roots never share a key.
- [ ] `.terraform/` is in `.gitignore` and no credential is passed through `-backend-config`.
- [ ] Re-running `init` after changing a `.tfbackend` file uses `-reconfigure` or `-migrate-state` deliberately.

## Checked
2026-11-09

Method: read the Terraform backend page (partial configuration, secrets), the `terraform init` command page, the S3 backend page and the provider block page (fetched as text). Removed as unsupported by those pages: the symlink and Windows `core.symlinks` advice, Terraform Cloud symlink behaviour, the `terraform state pull | jq .lineage` check, and the Terragrunt/Terramate claims, which are now only flagged as unchecked.
