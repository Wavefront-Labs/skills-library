---
id: computing-software.devops-ci-cd.github-actions.dependabot-secrets-and-restricted-runs
name: dependabot-secrets-and-restricted-runs
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, dependabot-secrets, dependabot-workflows, dependabot-actor, dependabot-registries]
level: practitioner
status: docs-checked
description: "Make CI work on Dependabot PRs: they get Dependabot secrets (not Actions secrets) and a read-only token; set them, use them in dependabot.yml registries, and gate on the actor."
sources: ["https://docs.github.com/en/code-security/dependabot/troubleshooting-dependabot/troubleshooting-dependabot-on-github-actions", "https://docs.github.com/en/code-security/dependabot/working-with-dependabot/configuring-access-to-private-registries-for-dependabot"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependabot secrets and restricted Dependabot runs

**Symptom:** every Dependabot PR fails at login/deploy with an empty token, while human PRs pass.

## 1. Why
Workflow runs that Dependabot triggers from `push`, `pull_request`, `pull_request_review` or
`pull_request_review_comment` events are treated as if opened from a fork:
- Only **Dependabot secrets** are available; Actions secrets are not. Both are read through the same `secrets` context.
- `GITHUB_TOKEN` is read-only by default (raise it with `permissions:`).
- A manual re-run keeps the privileges of the original run, whoever presses re-run.

The docs offer three fixes: skip the workflow for Dependabot (`if: github.actor != 'dependabot[bot]'`), use a
two-step `pull_request_target` process, or give Dependabot runs the secrets and `permissions` they need.

## 2. Provide what the PR build needs
Store each credential as a Dependabot secret (see the private-registries page for where). If a workflow
runs for Dependabot and for humans, giving the Actions and Dependabot secrets identical names lets one
reference serve both; otherwise use conditions. Only add read-only credentials needed to build and test — never deploy keys.

## 3. Private registries for Dependabot itself
```yaml
# .github/dependabot.yml
version: 2
registries:
  npm-internal:
    type: npm-registry
    url: https://npm.example.com
    token: ${{secrets.NPM_READ_TOKEN}}      # a Dependabot secret, referenced as ${{secrets.NAME}}
updates:
  - package-ecosystem: npm
    directory: /
    registries: [npm-internal]
    schedule: { interval: weekly }
```

## 4. Gate jobs on the actor
```yaml
jobs:
  deploy-preview:
    if: github.actor != 'dependabot[bot]'
```
To write to the repository from a Dependabot run, raise the token with a `permissions:` block
(for example `pull-requests: write`).

## Verify
- [ ] A Dependabot PR's install step authenticates to the private registry.
- [ ] Deploy jobs are skipped for Dependabot PRs; checks still report.

## Checked
2026-10-31. Confirmed in GitHub's "Troubleshooting Dependabot on GitHub Actions" and private-registries pages: the triggering events, fork-like treatment, Dependabot-secrets-only rule, read-only token and `permissions` fix, the three remedies, the actor condition, re-run privileges, `${{secrets.NAME}}` in `dependabot.yml`.
Removed: the `gh secret set` flags, the fetch-metadata auto-merge job, and the claim that re-runs switch secrets.
Method: documentation only; no commands were run.
