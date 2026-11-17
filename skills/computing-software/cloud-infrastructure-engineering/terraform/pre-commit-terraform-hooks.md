---
id: computing-software.cloud-infrastructure-engineering.terraform.pre-commit-terraform-hooks
name: pre-commit-terraform-hooks
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, pre-commit-terraform, pre-commit-hooks, pre-commit, terraform-fmt, terraform-validate, tflint, terraform-docs, trivy, checkov, git-hooks]
level: practitioner
status: docs-checked
description: "Set up antonbabenko/pre-commit-terraform: fmt, validate, tflint, terraform_docs and trivy hooks with the args that make them fast and correct in monorepos, plus the CI mirror job."
sources: ["https://github.com/antonbabenko/pre-commit-terraform", "https://pre-commit.com/", "https://developer.hashicorp.com/terraform/cli/commands/fmt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pre-commit-terraform hooks

**Goal:** catch formatting, validation, lint and docs drift on the developer's
machine, before the PR, with one `.pre-commit-config.yaml`.

## 1. Install
```bash
pip install pre-commit            # or brew install pre-commit
# also install the tools the hooks wrap: tflint, terraform-docs (0.12.0+), trivy
pre-commit install                # writes .git/hooks/pre-commit
```

## 2. Config
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: <VERSION>    # latest tag from the repo's releases page
    hooks:
      - id: terraform_fmt
        args: [--args=-recursive]
      - id: terraform_validate
        args:
          - --hook-config=--retry-once-with-cleanup=true   # deletes cached modules/providers and retries once (needs jq)
          - --args=-no-color
        exclude: ^modules/.*/examples/   # or whatever cannot validate standalone
      - id: terraform_tflint
        args: [--args=--config=__GIT_WORKING_DIR__/.tflint.hcl]
      - id: terraform_docs
        args: [--args=--config=.terraform-docs.yml]
      - id: terraform_trivy
        args: [--args=--skip-dirs=**/.terraform]
      - id: terraform_providers_lock
        args: [--hook-config=--mode=check-lockfile-is-cross-platform,
               --args=-platform=linux_amd64, --args=-platform=darwin_arm64]
```
Hooks run in parallel by default (tune with `--hook-config=--parallelism-limit=N`).
`__GIT_WORKING_DIR__` expands to the Git working directory (repo root) at run time.

## 3. Run
```bash
pre-commit run -a                 # everything, all files (first time / CI)
```

## 4. CI mirror
Run the same config in CI so a developer who skipped the hooks cannot merge:
```yaml
# after a Python setup step:
- run: pip install pre-commit && pre-commit run -a
```

## Gotchas
- `terraform_validate` reinitialises directories before validating and can pass custom
  arguments to `terraform init` (`--tf-init-args=`). If you use `TF_PLUGIN_CACHE_DIR`,
  enable `--hook-config=--retry-once-with-cleanup=true` or `--parallelism-limit=1` to
  avoid races when `terraform init` writes to the cache.
- `terraform_docs` rewrites README sections between
  `<!-- BEGIN_TF_DOCS -->` markers; the hook fails the first time (file changed)
  — re-add and commit.
- `terraform_tfsec` hook is deprecated; use `terraform_trivy`.
- Monorepos with many roots: hooks are slow on `run -a`; scope with
  `files: ^(infra|modules)/`.
- Windows developers: the README recommends WSL/WSL2 (or Docker); with Git for Windows,
  its `bash.exe` must come before the System32 `bash.exe` on PATH.

## Verify
- [ ] A commit with a mis-indented `.tf` is rejected and the file is reformatted in place.
- [ ] `pre-commit run -a` is green on `main`.
- [ ] CI runs the same hook set and fails when a hook would.

## Checked
- 2026-10-28. Confirmed against the pre-commit-terraform README (hook ids `terraform_fmt`, `terraform_validate`, `terraform_tflint`, `terraform_docs`, `terraform_trivy`, `terraform_providers_lock`; `__GIT_WORKING_DIR__`; `--retry-once-with-cleanup` needs `jq`; `--tf-init-args=`; `--parallelism-limit`; `terraform_providers_lock` mode `check-lockfile-is-cross-platform` and `--args=-platform=...`; `terraform_tfsec` deprecated in favour of `terraform_trivy`; `BEGIN_TF_DOCS` markers; terraform-docs 0.12.0+; Windows advice) and the pre-commit site (`pip install pre-commit`, `pre-commit install`, `pre-commit run --all-files`).
- Removed: the pinned `v1.96.1` tag, trivy `--severity` args, the `--tflint-init` hook flag, the `init -backend=false` claim, `SKIP=`, `autoupdate`, the pre-commit cache hint and `brew` install line (not in the fetched docs).
Method: documentation only; no commands were run.
