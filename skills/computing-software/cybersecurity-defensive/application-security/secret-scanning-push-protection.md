---
id: computing-software.cybersecurity-defensive.application-security.secret-scanning-push-protection
name: secret-scanning-push-protection
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [secrets-scanning, push-protection, github-secret-scanning, gitleaks, pre-commit, custom-patterns, bypass-review]
level: practitioner
status: docs-checked
description: "Stop secrets reaching repositories with GitHub push protection, custom patterns, delegated bypass and gitleaks pre-commit hooks, and handle blocked pushes properly."
sources: ["https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection", "https://github.com/gitleaks/gitleaks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secret scanning push protection

**Goal:** credentials are blocked at commit/push time instead of being discovered after they are public.

## GitHub
- Push protection for repositories can be enabled at repository, organization or enterprise level; it requires GitHub Secret Protection and is off by default. It blocks pushes from the command line, commits in the GitHub UI, file uploads and REST API requests. "Push protection for users" is a separate account-level setting (on by default) that only covers pushes to public repositories on GitHub.com.
- **Custom patterns** (repositories in organizations): define patterns for internal tokens, e.g. `corp_[A-Za-z0-9]{32}`, and choose which patterns are included in push protection at organization or enterprise level.
- **Delegated bypass:** by default anyone with write access can bypass with a reason; configure delegated bypass so designated reviewers approve bypass requests.
- Review bypasses: each bypass creates an alert in the Security tab and an audit log entry.

## Other platforms
Use the platform's server-side secret push protection if it has one, with a pipeline secret detection job as backstop.

## Local hooks
`.pre-commit-config.yaml`:
```yaml
repos:
- repo: https://github.com/gitleaks/gitleaks
  rev: <pinned gitleaks release tag>
  hooks: [{id: gitleaks}]
```
Local hooks are bypassable (`--no-verify`); server-side push protection is the control, hooks are developer convenience.

## When a push is blocked
1. Do not bypass for a real secret. Remove it from the commit: `git reset --soft HEAD~1` (or interactive history rewrite for older commits), move the value to the secrets manager, recommit.
2. If the secret was ever pushed anywhere (another remote, CI logs), treat it as leaked and rotate.
3. False positive: mark as false positive or test value with justification; tune the custom pattern.

## Verify
- [ ] Pushing a test commit containing a known provider test pattern is rejected.
- [ ] Bypass requests route to the reviewer team.
- [ ] Monthly review of bypassed alerts is on someone's calendar.

## Checked
2026-10-28. Confirmed against official pages: what push protection blocks, repository versus user push protection, default bypass behaviour, bypass alerts and audit log, delegated bypass, custom patterns (GitHub Docs: Push protection), Gitleaks pre-commit use (Gitleaks README).
Removed or rewritten: the claim that user-level push protection covers web UI and API commits (it does not), menu path, free-on-public claim, audit event name, bypassed:true filter, GitLab claims and the pinned gitleaks version.
Method: documentation only; no commands were run.
