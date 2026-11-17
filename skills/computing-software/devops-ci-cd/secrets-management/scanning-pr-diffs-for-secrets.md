---
id: computing-software.devops-ci-cd.secrets-management.scanning-pr-diffs-for-secrets
name: scanning-pr-diffs-for-secrets
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, diff-scan, secret-scanning, gitleaks]
level: practitioner
status: verified
description: "Scan only the commits in a pull request for secrets in CI (gitleaks log-opts, trufflehog --since-commit), so checks are fast and findings attributable to the PR."
sources: ["https://github.com/gitleaks/gitleaks#git", "https://github.com/trufflesecurity/trufflehog#octocat-scanning-a-github-repository"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scanning PR diffs in CI

Full-history scans are slow and keep reporting old findings. On PRs scan only new commits.

## gitleaks
```yaml
- uses: actions/checkout@<sha>
  with: { fetch-depth: 0 }
- run: |
    gitleaks git --log-opts="--no-merges ${{ github.event.pull_request.base.sha }}..${{ github.event.pull_request.head.sha }}" \
      --redact --report-format sarif --report-path gitleaks.sarif
```
`--redact` keeps secrets out of logs (SARIF output then holds `REDACTED`, run on v8.30.1); `--log-opts` accepts any `git log` range (run: `HEAD~1..HEAD` scanned one commit). Upload SARIF for annotations if using code scanning.
GitLab: `--log-opts="$CI_MERGE_REQUEST_DIFF_BASE_SHA..$CI_COMMIT_SHA"`.

## trufflehog
```bash
trufflehog git file://. --since-commit "$BASE_SHA" --branch "$HEAD_SHA" --results=verified,unknown --fail
```
`--fail` exits 183 when results are reported (run on 3.99.2: 183 with default results; exit 0 with `--results=verified` for a fake token).
`--results` defaults to `verified,unverified,unknown`; `verified,unknown` (as in the trufflehog README) hides secrets whose detector
could not confirm them, so a fake or revoked key passes silently. Drop `unverified` only if you accept that.
`--since-commit` takes any ref (a branch name such as `main` works as well as a SHA) and `--branch HEAD` scans the checked-out tip.

## Notes
- Scanning commits (not just the final diff) catches a secret added then removed within the PR:
  it is still in history and must be rotated (and the branch history rewritten before merge, or squash merge).
- Shallow clones: fetch enough history to include the base SHA.
- Fork PRs: scanning is read-only and needs no secrets, so it can run on `pull_request` safely.
- Keep a scheduled full-history scan as backstop.

## Verify
- [ ] A PR introducing a fake AWS key fails the check with the file and line annotated; unrelated PRs pass in seconds.
