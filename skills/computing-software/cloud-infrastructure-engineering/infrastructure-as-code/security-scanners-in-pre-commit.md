---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.security-scanners-in-pre-commit
name: security-scanners-in-pre-commit
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, security-scanning, pre-commit-security, pre-commit, secret-scanning]
level: practitioner
status: verified
description: "Run IaC security and secret scanners (gitleaks, checkov, trivy, tflint, ansible-lint) as pre-commit hooks with pinned revisions, fast scopes and CI parity."
sources: ["pre-commit documentation (https://pre-commit.com/)", "gitleaks pre-commit hook (https://github.com/gitleaks/gitleaks#pre-commit)", "Checkov pre-commit hooks (https://www.checkov.io/4.Integrations/pre-commit.html)", "pre-commit-terraform (https://github.com/antonbabenko/pre-commit-terraform)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Security scanners in pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.96.2
    hooks:
      - id: terraform_fmt
      - id: terraform_tflint
      - id: terraform_trivy          # trivy config scan on changed dirs
        args: [--args=--severity=HIGH,CRITICAL]
  - repo: https://github.com/bridgecrewio/checkov
    rev: 3.2.300
    hooks:
      - id: checkov
        args: [--quiet, --compact, --framework, terraform, ansible]
  - repo: https://github.com/ansible/ansible-lint
    rev: v24.10.0
    hooks:
      - id: ansible-lint
```
Revs above are examples whose tags and hook ids were confirmed in each repo's `.pre-commit-hooks.yaml` at that tag (latest releases on 2026-10-21: gitleaks v8.30.1, pre-commit-terraform v1.109.3, checkov 3.3.30, ansible-lint v26.10.1); run `pre-commit autoupdate` for current ones.
`pre-commit validate-config` accepted the gitleaks entry, and `pre-commit run --files cfg.py` on a staged file with a fake AWS key failed the hook (exit code 1, rule `aws-access-token`, secret redacted). The gitleaks hook builds from source with Go (`language: golang`), so Go must be installed; the ansible-lint hook runs `python3 -m ansiblelint` with `pass_filenames: false`; the checkov hook entry is `checkov -d .`; `terraform_trivy` and `terraform_tflint` need the trivy/tflint binaries on PATH.
```bash
pip install pre-commit && pre-commit install
pre-commit run --all-files          # first run / CI
pre-commit autoupdate               # bump revs (review the diff)
```

## Design
- **Fast first**: secret scan and formatters on every commit; heavy scans (full checkov, trivy) can run on `pre-push` (`stages: [pre-push]`) or only in CI.
- **Pinned revs** so local and CI results match; Renovate can update `.pre-commit-config.yaml`.
- **CI parity**: run `pre-commit run --all-files` in CI too; local hooks can be skipped with `--no-verify`.
- Baselines for legacy findings (`gitleaks --baseline-path`, checkov `--baseline`) so new code is held to the bar without blocking on old debt.

## Gotchas
- Hooks needing binaries (tflint, trivy) fail on machines without them; use hook repos that ship containers or document prerequisites (`language: docker_image`).
- ansible-lint in pre-commit needs collections installed for accurate results; set `additional_dependencies` or run in an EE in CI.
- Secrets already committed stay in history: rotate them, then rewrite history if needed.

## Verify
- [ ] Committing a fake AWS key is blocked locally and the same commit fails CI.
