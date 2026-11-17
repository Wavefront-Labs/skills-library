---
id: computing-software.cloud-infrastructure-engineering.terraform.validate-without-backend-using-init-backend-false
name: validate-without-backend-using-init-backend-false
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, backend-false, validate-without-backend, terraform-validate, terraform-init, ci, no-credentials, static-check, module-ci]
level: intro
status: gated
description: "Run init -backend=false so validate, fmt and tflint work in CI without state access or cloud credentials; what still needs network, and how to cache providers for it."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/init#backend-initialization", "https://developer.hashicorp.com/terraform/cli/commands/validate"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validate without a backend: `init -backend=false`

**Goal:** a static-check job that any contributor's PR can run — no state
bucket, no AWS keys, no HCP token.

## 1. Command
```bash
terraform init -backend=false -input=false
terraform validate
```
`-backend=false` skips backend initialisation entirely: no credentials are read,
no state is touched, the `backend`/`cloud` block is parsed but ignored. Providers
and modules are still installed, because `validate` needs provider schemas.

## 2. CI job
```yaml
validate:
  steps:
    - uses: actions/checkout@v4
    - uses: hashicorp/setup-terraform@v3
      with: { terraform_version: "1.9.8" }
    - run: terraform fmt -check -recursive
    - run: terraform init -backend=false -input=false
      env: { TF_PLUGIN_CACHE_DIR: ${{ runner.temp }}/plugin-cache }
    - run: terraform validate -json | tee validate.json
    - run: tflint --init && tflint
```
Cache `TF_PLUGIN_CACHE_DIR` keyed on `.terraform.lock.hcl` to avoid downloading
providers every run.

## 3. Module repositories
A module directory with no `provider` blocks still validates; a module that
*requires* a provider configuration (uses `configuration_aliases`) must be
validated through an example root:
```bash
for d in examples/*/; do (cd "$d" && terraform init -backend=false && terraform validate); done
```

## 4. What still needs network
- Provider downloads (registry or mirror) — unless cached.
- Module downloads for git/registry sources — the job needs read access to the
  module repos (deploy key or token). Local-path modules need nothing.
- Nothing else: no cloud API calls happen during validate.

## Gotchas
- In a fresh directory, `init -backend=false` writes no `.terraform/terraform.tfstate` (only `.terraform/providers`), so a
  following `terraform plan` fails with `Error: Backend initialization required, please run "terraform init"`; run a full
  `init` before any state operation. In a directory that was already initialised with a backend, `init -backend=false`
  keeps the cached backend and `plan` keeps working (tested with the local backend). The init docs recommend using the flag
  only when the directory was already initialised for a backend, because other init steps need one.
- Use a separate `TF_DATA_DIR` for the validate job in shared checkouts if you want the validate run isolated.
- `-backend=false` does not skip `required_version` checks; a mismatched core
  version still fails init (`Error: Unsupported Terraform Core version`, and `validate` fails the same way).
- OpenTofu: identical flag; `tofu init -backend=false`.

## Verify
- [ ] The validate job passes with no cloud credentials in its environment (`env | grep -i aws` empty).
- [ ] Deleting a required provider argument makes the job fail with a diagnostic.

## Checked
- Terraform 1.17.0 with a `backend "s3"` block naming a bucket that does not exist and no AWS credentials: `init -backend=false -input=false` succeeded and installed `hashicorp/null`; `validate` and `validate -json` returned `valid: true`; a following `plan` failed with `Backend initialization required`; no `.terraform/terraform.tfstate` was created; `required_version = ">= 9.0"` made `init` and `validate` fail with `Unsupported Terraform Core version`; a bogus argument made `validate -json` return `valid: false`, `error_count: 1`, summary `Unsupported argument`; `validate` printed the error (the shell exit code was not captured).
- Local-backend directory that was initialised first: `init -backend=false` then `plan` still printed `No changes`.
- Docs (developer.hashicorp.com/terraform/cli/commands/init): "To skip backend configuration, use -backend=false" and the recommendation about previously initialised directories.
- The GitHub Actions job, `setup-terraform@v3`, `tflint --init` and the plugin-cache caching key were not run (Actions is unavailable here), and module downloads from git or registry sources were not run (gated: unconfirmed, source is paywalled or blocked). The reason is that no workflow runner or private module repository was available.
