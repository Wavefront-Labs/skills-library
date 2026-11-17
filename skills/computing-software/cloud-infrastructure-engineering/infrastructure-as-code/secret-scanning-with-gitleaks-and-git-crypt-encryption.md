---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.secret-scanning-with-gitleaks-and-git-crypt-encryption
name: secret-scanning-with-gitleaks-and-git-crypt-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, secrets-in-iac, gitleaks, trufflehog, secret-scanning, git-crypt, pre-commit]
level: practitioner
status: gated
description: "Stop secrets reaching IaC repositories with gitleaks or trufflehog in pre-commit and CI, respond to leaks, and transparently encrypt sensitive files with git-crypt."
sources: ["gitleaks README and configuration (https://github.com/gitleaks/gitleaks)", "TruffleHog documentation (https://github.com/trufflesecurity/trufflehog)", "git-crypt README (https://github.com/AGWA/git-crypt)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secret scanning with gitleaks/trufflehog, and git-crypt

## Prevent: pre-commit hook
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.30.1     # pin the current release tag
    hooks: [{id: gitleaks}]
```
`pre-commit install`. The hook entry is `gitleaks git --pre-commit --redact --staged --verbose` (also `gitleaks-docker` and `gitleaks-system` ids exist; tag v8.21.2 also exists). Hook install on a real repo: (gated: unconfirmed, pre-commit run not performed here). Developers can bypass hooks, so CI must scan too.

## Detect: CI
```bash
gitleaks git --redact --report-format sarif --report-path gitleaks.sarif .     # history of the repo/branch
gitleaks dir --redact .                                                        # working tree only
trufflehog git file://. --since-commit main --branch HEAD --results=verified --fail   # verifies keys against providers
```
`--results=verified` is the documented current option (TruffleHog 3.99.3; the old `--only-verified` was still accepted silently but is not in `--help`). It reports only credentials confirmed live (fewer false positives); `--fail` exits 183 when results exist. `gitleaks` exits 1 on leaks (`--exit-code` changes it); `gitleaks git` accepts `--log-opts`.

Config for IaC repos (`.gitleaks.toml`, auto-loaded from the scanned path, or `-c`, or `GITLEAKS_CONFIG`; checked: the path allowlist suppressed a token under `tests/fixtures/`, the regex suppressed a token containing `EXAMPLEKEY`):
```toml
[extend]
useDefault = true
[allowlist]
paths = ['''tests/fixtures/''']
regexes = ['''EXAMPLEKEY''']
```
Inline allow: `# gitleaks:allow` on the line (checked, suppresses it; review these in PRs). gitleaks uses Go RE2 regexes
(no lookaheads), so "file must be encrypted" checks are simpler as a separate CI step:
```bash
for f in $(git ls-files '*vault.yml' '*vault.yaml'); do
  head -1 "$f" | grep -q '^\$ANSIBLE_VAULT' || { echo "unencrypted: $f"; exit 1; }
done
```
Checked: the loop prints `unencrypted: bad_vault.yml` for a file without the `$ANSIBLE_VAULT` header and passes one with it.

## When a secret leaks
1. **Revoke/rotate first** — assume it is compromised the moment it was pushed.
2. Then clean history if required (`git filter-repo --replace-text`), force-push, and ask hosting to purge caches/PR refs. Rewriting history does not un-leak a secret.
3. Add a rule/allowlist update so it can't recur.

## git-crypt: transparent file encryption
(gated: unconfirmed, git-crypt is not installed here; commands below follow its README and were not run)
For files that must live in the repo encrypted (alternatives: ansible-vault, SOPS):
```bash
git-crypt init
cat >> .gitattributes <<'EOF'
secrets/** filter=git-crypt diff=git-crypt
*.tfvars.secret filter=git-crypt diff=git-crypt
EOF
git-crypt add-gpg-user ops-lead@example.com     # GPG-based access
git-crypt export-key ../repo.key                # symmetric key for CI (store in CI secrets)
# CI: git-crypt unlock /path/to/repo.key
git-crypt status -e                             # list encrypted files
```
Files are plaintext in working copies of unlocked clones and ciphertext in Git objects.

Trade-offs: no per-file access control, revoking a user requires key rotation and re-encryption,
`.gitattributes` must be committed **before** adding the secret files (otherwise they are committed
in plaintext). For Ansible, ansible-vault is usually preferable; for Terraform, prefer secret stores
over encrypted tfvars.

## Verify
- [ ] Committing a fake AWS key is blocked locally and fails CI.
- [ ] `git-crypt status -e` lists every intended file; a fresh clone without the key shows binary content.
