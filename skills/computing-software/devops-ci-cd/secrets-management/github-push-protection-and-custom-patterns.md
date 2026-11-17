---
id: computing-software.devops-ci-cd.secrets-management.github-push-protection-and-custom-patterns
name: github-push-protection-and-custom-patterns
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, secret-scanning, github-push-protection, custom-patterns, github-secret-scanning, push-protection-bypass, delegated-bypass, partner-patterns, validity-checks, secret-protection, org-security-configuration]
level: practitioner
status: gated
description: "Turn on GitHub secret scanning and push protection org-wide, define custom patterns with dry runs, control bypasses with delegated approval, and handle the alerts it raises."
sources: ["https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection", "https://docs.github.com/en/code-security/secret-scanning/using-advanced-secret-scanning-and-push-protection-features/custom-patterns/defining-custom-patterns-for-secret-scanning", "https://docs.github.com/en/code-security/secret-scanning/using-advanced-secret-scanning-and-push-protection-features/delegated-bypass-for-push-protection/about-delegated-bypass-for-push-protection"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitHub push protection and custom patterns

Free for public repos; private/internal repos need **GitHub Secret Protection** (part of
former Advanced Security).

## Enable org-wide
*Org settings -> Advanced Security -> Configurations* (menu names change; confirm in the current GitHub UI: gated: unconfirmed, no org to click through): create a security configuration
with *Secret scanning* + *Push protection* (+ *Validity checks*, *Non-provider patterns*)
enabled, apply to all repos and set as default for new repos. Per-repo toggles drift;
configurations don't.

## Push protection behaviour
- Blocks `git push` (and web edits, API commits) containing a supported token with high
  confidence. The developer sees the secret type, file and line, and a URL.
- Options at block time: remove the secret from the commits (amend/rebase; it's still in
  local history otherwise), or bypass with a reason: *used in tests*, *false positive*,
  *I'll fix it later* (creates an open alert; "used in tests" and "false positive" create closed alerts, per GitHub docs).
- **Delegated bypass**: only listed roles/teams may approve bypass requests; others
  submit a request and wait. Turn this on for orgs with compliance needs; review requests
  daily or developers will be blocked.
- Users can also enable push protection for their own pushes to any public repo.

## Custom patterns
*Repo/org/enterprise -> Advanced Security -> Custom patterns -> New pattern*:
- **Secret format** regex (Hyperscan library: a subset of PCRE, option modifiers unsupported), optional
  **before/after secret** context (default `\A|[^0-9A-Za-z]` and `\z|[^0-9A-Za-z]`),
  and additional match requirements (secret must / must not match other expressions). Limits: 500 custom patterns per organization or enterprise, 100 per repository.
- **Dry run** against up to 10 selected repos or all repos in the org; results are a sample of up to 1000. Review hits, tune, then publish.
- Tick *Enable push protection* on the pattern only after the dry run shows low false
  positives.
- Copilot can generate a regex from a description; still dry-run it.

Example: internal token `acme_live_` + 32 alphanumerics:
```
Secret format:   acme_(live|test)_[0-9A-Za-z]{32}
Must not match:  acme_test_0{32}
```

## Alerts
- *Security -> Secret scanning*: provider alerts (partner program: GitHub notifies the
  issuer, who may auto-revoke), user alerts, generic/AI-detected passwords.
- Validity checks show *active/inactive* for supported providers; prioritise active.
- API (checked against GitHub's OpenAPI description): `GET /orgs/{org}/secret-scanning/alerts?state=open&validity=active` for dashboards;
  resolve with `PATCH /repos/{owner}/{repo}/secret-scanning/alerts/{n}` `{"state":"resolved","resolution":"revoked"}` (resolution enum: false_positive, wont_fix, revoked, used_in_tests).
- Closing an alert doesn't revoke the secret; rotation is on you.

## Verify
Push a commit with a sample token from GitHub's test patterns (or your custom pattern's
dry-run sample) to a scratch repo: the push is rejected with
a push rejection naming the secret type, file and line (the exact `GH013` wording was not confirmed: gated: unconfirmed).
