---
id: computing-software.devops-ci-cd.secrets-management.gitleaks-config-and-pre-commit
name: gitleaks-config-and-pre-commit
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, secret-scanning, gitleaks, gitleaks-config, gitleaks-pre-commit, gitleaks-toml, allowlist, gitleaksignore, baseline, custom-rules, gitleaks-action, protect-staged]
level: practitioner
status: verified
description: "Configure gitleaks: extend the default rules with custom ones, path/regex allowlists, .gitleaksignore fingerprints, baselines for legacy repos, and run it in pre-commit and CI."
sources: ["https://github.com/gitleaks/gitleaks/blob/master/README.md", "https://github.com/gitleaks/gitleaks/blob/master/config/gitleaks.toml", "https://github.com/gitleaks/gitleaks-action"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gitleaks config and pre-commit

## Commands (v8.19+ naming)
```bash
gitleaks git -v                         # scan git history of the repo (was: detect)
gitleaks git --log-opts="origin/main..HEAD"   # only commits on this branch
gitleaks dir .                          # scan files on disk, no git (was: detect --no-git)
gitleaks git --staged                   # staged changes (was: protect --staged)
gitleaks git --report-format sarif --report-path gitleaks.sarif --redact
```
Exit code 1 when leaks are found (`--exit-code` to change).

## .gitleaks.toml
```toml
title = "acme gitleaks config"
[extend]
useDefault = true                      # keep the built-in rules (over 200 in the v8.30 default config)

[[rules]]
id = "acme-internal-token"
description = "Acme service token"
regex = '''acme_(?:live|test)_[0-9a-zA-Z]{32}'''   # non-capturing group, see note
keywords = ["acme_live_", "acme_test_"]   # fast prefilter; required for performance
entropy = 3.5

[[allowlists]]                         # legacy [allowlist] still works
description = "global allowlist"
paths = ['''(^|/)testdata/''', '''\.snap$''', '''(^|/)package-lock\.json$''']
regexes = ['''EXAMPLE_KEY_[A-Z0-9]+''']
stopwords = ["dummy", "changeme"]
```
- Entropy trap (run on v8.30.1): when the regex has a capture group, the "secret" is the FIRST group,
  and `entropy` is measured on it. `acme_(live|test)_...` has secret `live` (entropy 1.5) so the rule never fired;
  `secretGroup = 0` did not fix it. Use `(?:...)` groups or wrap the whole token in one group.
- Per-rule `[rules.allowlist]` for false positives specific to one rule.
- Inline: append `gitleaks:allow` in a comment on the line (use sparingly; it's visible
  in code review).
- **.gitleaksignore**: one finding fingerprint per line
  (`<commit>:<file>:<rule-id>:<line>`; `dir` scans print `<file>:<rule-id>:<line>` with no commit), printed as `Fingerprint` in the report; use for historic findings
  you've rotated already.
- **Baseline** for a legacy repo: `gitleaks git --report-path baseline.json` once, then
  `gitleaks git --baseline-path baseline.json` reports only new leaks (run: 0 findings with the baseline,
  1 after a new leaking commit; the baseline did not suppress anything in `gitleaks dir`).

## pre-commit
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.30.1             # pin the current release tag
    hooks:
      - id: gitleaks           # runs `gitleaks git --pre-commit --redact --staged --verbose`
```
Developers can skip hooks (`SKIP=gitleaks git commit`, `--no-verify`), so CI must scan too.

## CI
```yaml
- uses: actions/checkout@v6
  with: { fetch-depth: 0 }          # history needed for commit-range scans
- uses: gitleaks/gitleaks-action@v3        # v2 runs on Node 20, removed from GitHub-hosted runners 2026-09-16
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}   # only for organization-owned repos (free key)
```
Or run the binary/container directly: `docker run --rm -v "$PWD:/repo" zricethezav/gitleaks:latest git /repo -v`
(pin a version tag instead of latest).

## Gotchas
- A finding in history is still a leak after deleting the line: rotate the secret (see
  `computing-software.devops-ci-cd.secrets-management.remediating-a-leaked-secret`).
- Shallow clones make history scans silently partial.
- Too many allowlist regexes hide real leaks; prefer path allowlists for fixtures and
  fingerprints for one-offs.

## Verify
Commit a fake `ghp_` + 36 random alphanumerics token in a scratch repo: the hook blocks it (exit 1);
the same in `testdata/` passes with the allowlist above.
