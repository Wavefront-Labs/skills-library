---
id: computing-software.cybersecurity-defensive.application-security.github-actions-security
name: github-actions-security
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [supply-chain-security, github-actions-security, pull-request-target, script-injection, github-token-permissions, oidc, zizmor]
level: advanced
status: docs-checked
description: "Harden GitHub Actions: least-privilege GITHUB_TOKEN, pull_request_target and script-injection traps, SHA-pinned actions, OIDC over secrets, runners, auditing."
sources: ["https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions", "https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/", "https://github.com/woodruffw/zizmor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitHub Actions security

## Token permissions
Set org/repo default workflow permissions to read-only, then grant per workflow/job:
```yaml
permissions:
  contents: read
jobs:
  release:
    permissions:
      contents: write
```

## Untrusted input: script injection
`${{ github.event.issue.title }}`, PR titles, branch names, commit messages are attacker-controlled.
Interpolated into `run:` they execute as shell:
```yaml
# vulnerable
- run: echo "Title: ${{ github.event.pull_request.title }}"
# safe: pass through env, quote
- env:
    TITLE: ${{ github.event.pull_request.title }}
  run: echo "Title: $TITLE"
```

## pull_request_target and workflow_run
`pull_request_target` runs in the base repo context **with secrets and write token**. Checking out and
building the PR head (`ref: ${{ github.event.pull_request.head.sha }}`) runs fork code with those privileges
("pwn request"). Use `pull_request` for building untrusted code; if you need privileged follow-up (labels,
comments), split into a separate `workflow_run` that only consumes artefacts as data, never executes them.

## Third-party actions
- Pin to a full commit SHA (`uses: actions/checkout@<40-char-sha> # <version tag>`), and update them with a dependency-update tool.
- Allow list actions at org level.
- Review what each action does with secrets; prefer official/verified creators.

## Secrets and cloud access
- OIDC federation to AWS/Azure/GCP instead of long-lived keys; constrain the cloud trust to specific subject claims (repository, environment, branch).
- Environments with required reviewers and branch restrictions for production secrets.
- Never echo secrets; masking is best effort (transformed values are not masked).

## Runners
- GitHub-hosted runners are ephemeral. Self-hosted: never for public repos; ephemeral and separated by trust level via runner groups.

## Audit tooling
`zizmor` (static analysis of workflows), OpenSSF Scorecard (including its Dangerous-Workflow check), org audit log for workflow and secret changes; CODEOWNERS on `.github/workflows/`.

## Verify
zizmor reports no high findings, all actions SHA-pinned, default token read-only, and a test fork PR cannot
access secrets.

## Checked
2026-10-28. Confirmed against official pages: full-length commit SHA pinning, pull_request_target risks, script injection, OIDC for cloud access, self-hosted runner caution, CODEOWNERS, zizmor (GitHub security hardening guide, Security Lab pwn-requests article, zizmor README).
Removed or rewritten: the id-token YAML line, the Settings menu path, the --ephemeral flag, subject-claim formats, the Dependabot/Renovate mention and the Scorecard check list.
Method: documentation only; no commands were run.
