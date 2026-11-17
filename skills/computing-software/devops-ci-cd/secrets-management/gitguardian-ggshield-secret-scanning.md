---
id: computing-software.devops-ci-cd.secrets-management.gitguardian-ggshield-secret-scanning
name: gitguardian-ggshield-secret-scanning
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, ggshield, gitguardian, secret-scanning, pre-commit, pre-receive, secret-incident]
level: practitioner
status: gated
description: "Scan for secrets with GitGuardian ggshield: pre-commit and pre-push hooks, CI scans of commit ranges, Docker image and path scans, ignore rules, and incident remediation."
sources:
  - https://docs.gitguardian.com/ggshield-docs/getting-started
  - https://docs.gitguardian.com/ggshield-docs/integrations/git-hooks/pre-commit
  - https://docs.gitguardian.com/ggshield-docs/integrations/cicd-integrations/github-actions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GitGuardian ggshield

ggshield is the CLI for GitGuardian's detection engine (hundreds of specific detectors plus generic high-entropy secrets). Needs `GITGUARDIAN_API_KEY` (personal or service account token); content is sent to the API for scanning (self-hosted GitGuardian available). Checked against ggshield 1.56.0 (`pip install ggshield`): the CLI structure, hook ids and config keys below; actual scans were not run (gated: unconfirmed, no API key).

## Developer hooks
```yaml
# .pre-commit-config.yaml
repos:
- repo: https://github.com/gitguardian/ggshield
  rev: v1.56.0          # pin the current release tag
  hooks:
  - id: ggshield        # runs `ggshield secret scan pre-commit`; `ggshield-push` is the pre-push hook
    language_version: python3
    stages: [pre-commit]
```
Or global: `ggshield install --mode global` (pre-commit) / `-t pre-push` (`--mode` local|global is required; `-t` also accepts AI-assistant hook types such as claude-code). Authenticate with `ggshield auth login`.

## CI
```yaml
# GitHub Actions
- uses: actions/checkout@v6
  with: { fetch-depth: 0 }
- uses: GitGuardian/ggshield-action@v1      # env var names below not re-checked (gated: unconfirmed)
  env:
    GITHUB_PUSH_BEFORE_SHA: ${{ github.event.before }}
    GITHUB_PUSH_BASE_SHA: ${{ github.event.base }}
    GITHUB_PULL_BASE_SHA: ${{ github.event.pull_request.base.sha }}
    GITHUB_DEFAULT_BRANCH: ${{ github.event.repository.default_branch }}
    GITGUARDIAN_API_KEY: ${{ secrets.GITGUARDIAN_API_KEY }}
```
Generic: `ggshield secret scan ci` detects the CI provider and scans new commits. Other modes:
```bash
ggshield secret scan commit-range origin/main..HEAD
ggshield secret scan repo .                  # entire history (first adoption)
ggshield secret scan path -r ./config
ggshield secret scan docker myimage:1.2      # layers of a built image
ggshield secret scan pypi requests           # a package from a registry
ggshield secret scan changes                 # changes since the default branch (also: archive, pre-push, pre-receive)
```

## Ignoring
- Inline: `# ggignore` comment on the line.
- `.gitguardian.yaml`:
```yaml
version: 2
secret:
  ignored_paths: ['tests/fixtures/**']
  ignored_matches:
    - name: test stripe key
      match: 3a1f0c...sha256-of-the-secret
  ignored_detectors: [Generic Password]
```
- `ggshield secret ignore --last-found` (or `--name NAME`) records the previous scan's findings (after confirming they are false positives).

## When a secret is found
1. Revoke/rotate it at the provider first - history rewriting does not un-leak a pushed secret.
2. Remove from code, move to a secret manager, reference by name.
3. If it never left the laptop (pre-commit caught it), amend the commit.
4. Resolve the incident in the GitGuardian dashboard with the remediation note.

## Verify
- [ ] Committing a dummy AWS key pair is blocked locally and in CI.
- [ ] Full-history scan done once at adoption; findings triaged.
