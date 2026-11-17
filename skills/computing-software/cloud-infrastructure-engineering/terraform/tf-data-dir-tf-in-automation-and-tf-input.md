---
id: computing-software.cloud-infrastructure-engineering.terraform.tf-data-dir-tf-in-automation-and-tf-input
name: tf-data-dir-tf-in-automation-and-tf-input
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, tf-data-dir, tf-in-automation, tf-input, environment-variables, dot-terraform, ci, multi-environment, working-directory, tf-workspace]
level: practitioner
status: docs-checked
description: "Set TF_DATA_DIR for per-environment .terraform dirs, TF_INPUT=0 and TF_IN_AUTOMATION for CI, plus TF_WORKSPACE and TF_CLI_CONFIG_FILE."
sources: ["https://developer.hashicorp.com/terraform/cli/config/environment-variables"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `TF_DATA_DIR`, `TF_IN_AUTOMATION` and `TF_INPUT`

**Goal:** run many environments from one checkout, and run in CI, without
`.terraform/` caches fighting or prompts hanging.

## 1. `TF_DATA_DIR` — relocate `.terraform/`
```bash
TF_DATA_DIR=.terraform-prod terraform init -backend-config=env/prod.tfbackend
TF_DATA_DIR=.terraform-dev  terraform init -backend-config=env/dev.tfbackend
TF_DATA_DIR=.terraform-prod terraform plan
```
`TF_DATA_DIR` changes where Terraform keeps its per-working-directory data, such as
the current backend configuration (default: a `.terraform` subdirectory). HashiCorp
notes it is mostly useful when the working directory is not writable
(`TF_DATA_DIR=/tmp/tf-$CI_JOB_ID`). The data directory also holds providers, modules
and other artifacts, so set it consistently for every command starting with `init`.
Add the pattern to `.gitignore` (`.terraform*/`).

## 2. `TF_INPUT=0`
If set to `false` or `0`, commands behave as if `-input=false` was given: no prompts
for variables that have no value. Set it globally in CI images.

## 3. `TF_IN_AUTOMATION=1`
Any non-empty value. A purely cosmetic change to human-readable output: Terraform
avoids suggesting specific commands to run next, which is less confusing when a CI
system or wrapper drives it. The exact differences can change between minor versions.
No functional effect.

## 4. Related variables
| Variable | Effect |
|---|---|
| `TF_WORKSPACE` | selects the workspace instead of `terraform workspace select` and overrides workspace selection; HashiCorp recommends it only for non-interactive use |
| `TF_CLI_CONFIG_FILE` | location of the CLI configuration file |
| `TF_PLUGIN_CACHE_DIR` | alternative way to set `plugin_cache_dir` in the CLI configuration |
| `TF_REGISTRY_CLIENT_TIMEOUT` | client timeout for registry requests (default 10s) |
| `TF_REGISTRY_DISCOVERY_RETRY` | max retries for registry connection errors or retryable 500-range responses |
| `TF_TOKEN_<host>` | API token for a registry/HCP host, dots as underscores: `TF_TOKEN_app_terraform_io` |

## Gotchas
- `TF_IN_AUTOMATION` does not imply `-input=false` or `-auto-approve`.
- Credentials for providers are better supplied as environment variables, which are not
  written into plan files or persisted by Terraform.

## Verify
- [ ] `init` and `plan` use the same `TF_DATA_DIR` and find the same backend configuration and providers.
- [ ] With `TF_INPUT=0`, an unset required variable errors immediately instead of prompting.

## Checked
- 2026-10-28. Confirmed against the Terraform CLI environment-variables page (`TF_DATA_DIR`, `TF_INPUT`, `TF_IN_AUTOMATION` cosmetic, `TF_WORKSPACE`, `TF_CLI_CONFIG_FILE`, `TF_PLUGIN_CACHE_DIR`, `TF_REGISTRY_CLIENT_TIMEOUT` default 10s, `TF_REGISTRY_DISCOVERY_RETRY`), the CLI configuration page (`TF_TOKEN_<host>` with periods as underscores, e.g. `TF_TOKEN_app_terraform_io`) and the "Running Terraform in Automation" tutorial (credentials via environment variables are not stored in the plan).
- Removed: `TF_IGNORE`, `TF_SKIP_PROVIDER_VERIFY`, the claims about relative paths with `-chdir`, workspace markers, `-reconfigure` behaviour and OpenTofu parity (not in the fetched docs).
Method: documentation only; no commands were run.
