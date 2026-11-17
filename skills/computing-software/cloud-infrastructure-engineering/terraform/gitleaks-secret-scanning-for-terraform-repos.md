---
id: computing-software.cloud-infrastructure-engineering.terraform.gitleaks-secret-scanning-for-terraform-repos
name: gitleaks-secret-scanning-for-terraform-repos
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, gitleaks, secret-scanning, pre-commit, tfvars, tfstate, credentials-leak, ci-security]
level: practitioner
status: docs-checked
description: "Stop secrets reaching Terraform repos with gitleaks: pre-commit and CI scans, full-history audits, allowlists and fingerprints, plus .gitignore and leak response."
sources: ["https://github.com/gitleaks/gitleaks", "https://github.com/gitleaks/gitleaks-action", "https://github.com/github/gitignore/blob/main/Terraform.gitignore", "https://developer.hashicorp.com/terraform/language/state/sensitive-data"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gitleaks secret scanning for Terraform repos

Terraform repos leak secrets in predictable places: `*.tfvars` with keys, provider
blocks with inline credentials, committed `terraform.tfstate`, `crash.log`, saved plan
files and HCP Terraform API tokens in scripts. Block them before commit, scan in CI,
and audit history once.

## 1. Ignore the files that should never be committed
```gitignore
.terraform/
*.tfstate
*.tfstate.*
crash.log
crash.*.log
*.tfplan
tfplan
# only if these hold environment secrets (gitignore has no trailing comments)
*.auto.tfvars
override.tf
override.tf.json
*_override.tf
.terraformrc
terraform.rc
```

## 2. Pre-commit
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.24.2
    hooks:
      - id: gitleaks
```
Developers can skip the hook (the README documents prefixing the commit command with `SKIP=gitleaks`), which is why CI scans too.

## 3. CI
```bash
gitleaks git --redact --report-format sarif --report-path gitleaks.sarif -v .
```
- The scanning modes are `git` (commits), `dir` (files and directories) and `stdin`;
  v8.19.0 deprecated `detect` and `protect`, which stay available but hidden from `--help`.
- On PRs, limit to the PR's commits: `--log-opts="origin/main..HEAD"`.
- One-off history audit: `gitleaks git --log-opts="--all" --redact -v .`
- GitHub Action `gitleaks/gitleaks-action@v2` needs a (free) licence key for
  organisation repos; running the binary directly avoids that.

## 4. Config and false positives
```toml
# .gitleaks.toml
[extend]
useDefault = true

[[rules]]
id = "tfvars-password"
description = "password assignments in tfvars"
regex = '''(?i)password\s*=\s*"[^"$]{8,}"'''
path = '''\.tfvars$'''

[[allowlists]]
description = "test fixtures"
paths = ['''^tests/fixtures/''']
```
For a single known false positive, append `#gitleaks:allow` to the line, or add the
finding's `Fingerprint` (from the report) to `.gitleaksignore`. Older gitleaks versions
use a single `[allowlist]` table instead of `[[allowlists]]`.

## 5. When a secret leaks
1. Rotate it first. Rewriting history does not un-leak it; forks, clones and CI caches
   already have it.
2. Then remove it from history if policy requires, and force-push with coordination.
3. Move the value to a secret store (Vault, cloud secret manager, HCP Terraform
   sensitive variables) and read it via data source, ephemeral resource or
   environment variable.

## Gotchas
- gitleaks finds secrets in files, not in remote state; state still contains secrets
  in plain text and must be protected by backend access controls and encryption.
- Keep saved plan files out of git entirely rather than relying on scanning.

## Verify
- [ ] A commit containing a fake AWS key is blocked locally and fails CI.
- [ ] Full-history audit has been run once and findings triaged.
- [ ] `.gitignore` covers state, plans and crash logs.

## Checked
2026-10-28. Confirmed against the gitleaks README (pre-commit `rev: v8.24.2` and `SKIP=gitleaks`, modes git/dir/stdin, v8.19.0 deprecation of detect/protect, `--redact`, `-f/--report-format` incl. sarif, `-r/--report-path`, `-v`, `--log-opts`, `#gitleaks:allow`, `.gitleaksignore` with `Fingerprint`, `[extend] useDefault`, `[[allowlists]]` replacing `[allowlist]` in v8.25.0), the gitleaks-action README (licence key required for organisation accounts, free) and the github/gitignore Terraform template (state, crash log, override and `.terraformrc` entries).
Removed: the `--no-verify` claim (README documents `SKIP=gitleaks`), "staged changes only", the default-ruleset claim about `*.atlasv1.*` and cloud key formats, the saved-plan-is-zip statement, the `git filter-repo` name, and the lock-file sentence (not in the fetched pages).
Method: documentation only; no commands were run.
