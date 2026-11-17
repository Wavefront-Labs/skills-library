---
id: computing-software.devops-ci-cd.secrets-management.secret-scanning-baselines-and-allowlists
name: secret-scanning-baselines-and-allowlists
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, gitleaks-baseline, secret-allowlist, secret-scanning]
level: practitioner
status: verified
description: "Adopt secret scanning on an existing repo without drowning in old findings: gitleaks baselines, allowlists for test fixtures, inline ignores and keeping exceptions reviewed."
sources: ["https://github.com/gitleaks/gitleaks#creating-a-baseline", "https://github.com/gitleaks/gitleaks#configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Baselines and false-positive allowlists

## Baseline existing findings
```bash
gitleaks git --report-path gitleaks-baseline.json          # full history once
gitleaks git --baseline-path gitleaks-baseline.json --report-path new.json   # CI: only new findings
```
A baseline is any gitleaks JSON report; it matches by fingerprint, which includes the commit, so it applies to `gitleaks git`
(run: 0 findings with the baseline; a later commit with a new secret reported 1) and did not suppress findings in `gitleaks dir`.
Commit the baseline; triage its contents separately (rotate anything real; a baseline hides, it does not fix).

## Allowlists (.gitleaks.toml)
```toml
[extend]
useDefault = true

[[allowlists]]                  # legacy single-table [allowlist] also works (run on v8.30.1)
description = "test fixtures and docs"
paths = ['''(^|/)testdata/''', '''\.md$''']
regexes = ['''EXAMPLE_KEY_[A-Z0-9]+''']
stopwords = ["dummy", "notasecret"]
```
Per-finding: add the `Fingerprint` from the report to `.gitleaksignore` (`<commit>:<file>:<rule>:<line>` for `git` scans, no commit
prefix for `dir` scans), or put `gitleaks:allow` in a comment on the line (`--ignore-gitleaks-allow` turns that off).

## trufflehog / GitHub equivalents
- trufflehog: `--exclude-paths exclude.txt` (`-x`; one regex per line, run: `testdata/` and `^c\.txt$` removed both findings),
  `--results=verified` to only report live credentials, `trufflehog:ignore` comment on the line (`--no-ignore-tag` to see them again).
- GitHub secret scanning: close alerts as "false positive"/"used in tests"; push protection bypass
  reasons are logged.

## Governance
- Allowlist changes need security review (CODEOWNERS on `.gitleaks.toml` and `.gitleaksignore`).
- Prefer narrow fingerprints over broad path allowlists; review allowlists quarterly.
- Fake secrets in tests should look obviously fake and match a stopword.

## Verify
- [ ] CI passes on the baseline; adding a new real-looking key fails the scan.
