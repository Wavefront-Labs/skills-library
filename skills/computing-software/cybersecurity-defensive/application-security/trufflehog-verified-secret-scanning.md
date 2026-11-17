---
id: computing-software.cybersecurity-defensive.application-security.trufflehog-verified-secret-scanning
name: trufflehog-verified-secret-scanning
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [secrets-scanning, trufflehog, verified-secrets, git-history-scan, ci-secret-scan, s3-scan, credential-exposure]
level: practitioner
status: gated
description: "Scan repos, orgs, images and buckets for secrets with TruffleHog: verified vs unverified results, full-history scans, CI usage with --since-commit, and triage."
sources: ["https://github.com/trufflesecurity/trufflehog", "https://docs.trufflesecurity.com/", "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TruffleHog verified secret scanning

TruffleHog detects 800+ credential types (README: "over 800 secret types") and, for many, **verifies** them by calling the provider API
(e.g. AWS `GetCallerIdentity`). Verified = live credential: highest priority.

## Common scans
```
trufflehog git https://github.com/org/repo.git --results=verified,unknown
trufflehog github --org=myorg --token=$GITHUB_TOKEN --include-members --results=verified   # (gated: unconfirmed, no org or token here; flags checked in --help)
trufflehog filesystem ./ --exclude-paths=.trufflehog-exclude
trufflehog docker --image registry.example.com/app:1.2.3      # also file://image.tar (gated: unconfirmed, Docker not available here)
trufflehog s3 --bucket=my-bucket                              # (gated: unconfirmed, no AWS account here)
trufflehog git file://. --since-commit main --branch HEAD --fail     # CI: only new commits, exit code 183 on finding
```
Output `-j`/`--json` for pipelines (also `--sarif`, `--github-actions`). `--no-verification` when scanning must not make outbound calls (e.g.
sensitive environments; verification contacts third-party APIs with the found credential).

Checked locally (TruffleHog 3.99.3, a repo with a fake GitHub-format token committed on `main`, `--no-verification`):
`git file://. --since-commit main --branch HEAD --fail` on a branch whose own commit holds no secret found 0 and exited 0; with
`--since-commit HEAD~2` it found the token and exited **183**. `--results=verified,unknown` hid the unverified match. `filesystem ./`
also walks `.git/objects`, so use the `git` source for history and a directory that excludes `.git` for working-tree scans.
A line ending `# trufflehog:ignore` is skipped; `--no-ignore-tag` reports it again.

## Results
- **verified**: confirmed active. Revoke/rotate immediately, then investigate use (provider logs).
- **unknown**: verification failed for reasons other than invalid (network, rate limits): check manually.
- **unverified**: pattern match, credential invalid or not verifiable (the default `--results` is `verified,unverified,unknown`): lower priority but may still be
  real (internal systems TruffleHog cannot reach).

## CI integration
GitHub Action `trufflesecurity/trufflehog@main` with `extra_args: --results=verified,unknown` on push/PR
(`base`/`head` set). Pre-commit hook for developer machines. Combine with platform push protection.

## Full-history sweeps
Run org-wide history scans periodically and after acquisitions; secrets deleted in later commits are still
in history and forks. Removing them from history does not un-leak them: rotate first.

## Custom detectors
Config file with regex and optional verification endpoint for internal token formats
(`--config=detectors.yaml`).

## Gotchas
- Verification calls are visible to the provider (and in your own logs as API calls from the scanner).
- Test fixtures with fake keys: use `.trufflehog-exclude`/`# trufflehog:ignore` comments sparingly and review them.
- Large orgs: rate limits; scan incrementally.

## Verify
Commit a canary credential (e.g. a deliberately created, low-privilege test key that you then revoke) on a
branch and confirm CI fails with a verified result.
