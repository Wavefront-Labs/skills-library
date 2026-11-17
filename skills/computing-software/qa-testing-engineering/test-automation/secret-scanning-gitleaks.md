---
id: computing-software.qa-testing-engineering.test-automation.secret-scanning-gitleaks
name: secret-scanning-gitleaks
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [secret-scanning, gitleaks, static-analysis, credentials, pre-commit]
level: practitioner
status: verified
description: "Detect committed secrets with gitleaks in pre-commit and CI, tune rules and allowlists, scan history, and respond correctly when a secret leaks."
sources:
  - https://github.com/gitleaks/gitleaks
  - https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secret scanning in repositories (gitleaks)

**Goal:** no API keys, tokens or passwords in source, history or test fixtures.

## Run it
```bash
gitleaks git -v --redact .            # scan full git history (v8.19+; older: gitleaks detect)
gitleaks dir -v ./config              # scan files without git
gitleaks git --staged --redact        # pre-commit style (older: gitleaks protect --staged)
```
Exit code 1 when leaks are found (checked on gitleaks 8.30.1: `git`, `dir` and `git --staged` all exit 1 on a finding; `protect` and `detect` still exist as older commands); `--report-format sarif --report-path gitleaks.sarif` for code-scanning upload.

## CI and pre-commit
```yaml
# .pre-commit-config.yaml
- repo: https://github.com/gitleaks/gitleaks
  rev: v8.30.1   # current release when checked; the hook runs `gitleaks git --pre-commit --redact --staged --verbose`
  hooks: [{ id: gitleaks }]
```
In GitHub Actions use `gitleaks/gitleaks-action@v3` with `fetch-depth: 0`: the action's README says v2 runs on Node 20, which GitHub removed from hosted runners on 16 September 2026, so v2 no longer works. `GITLEAKS_LICENSE` (free key) is required only for repositories owned by an organization, not personal accounts. Also enable the platform's own scanning and push protection (GitHub secret scanning) where available.

## Tuning
```toml
# .gitleaks.toml
[extend]
useDefault = true
[[rules]]
id = "internal-api-token"
regex = '''ixa_[A-Za-z0-9]{32}'''
[allowlist]
paths = ['''tests/fixtures/fake_keys\.json''']
```
Ignore a specific confirmed false positive by adding its fingerprint to `.gitleaksignore` (checked: the fingerprint comes from a JSON report and has the form `commit:file:rule:line`; it removed that finding). Custom rule `internal-api-token` and `[extend] useDefault = true` fired as written. Note the AWS rule only matches key bodies in the base32 alphabet (A-Z, 2-7), so a made-up `AKIA...` value containing 0, 1, 8 or 9 is not detected, which matters for the Verify step below.

## When a real secret is found
1. **Revoke/rotate it first**; assume it is compromised.
2. Check provider logs for misuse.
3. Then remove from history if needed (`git filter-repo`), knowing forks and caches may keep copies.
4. Add a rule or test so the pattern is caught next time.

## Gotchas
- Test fixtures with realistic-looking fake keys trigger alerts; use obviously fake values or allowlist the path.
- Shallow CI clones miss history; scan with full depth at least once.
- High-entropy generic rules are noisy; prefer provider-specific patterns.

## Verify
A commit containing a dummy AWS key pattern (use only A-Z and 2-7 after `AKIA`) is blocked locally and in CI; the full-history scan is clean or every finding is rotated and documented.
