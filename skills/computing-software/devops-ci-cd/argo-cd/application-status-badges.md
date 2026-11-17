---
id: computing-software.devops-ci-cd.argo-cd.application-status-badges
name: application-status-badges
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, status-badge, sync-status-badge, health-badge, statusbadge-enabled]
level: intro
status: docs-checked
description: "Show Argo CD application sync and health status in READMEs with status badges: enabling them, URL parameters, and the information they expose."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/status-badge/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Status badges

## 1. Enable (`argocd-cm`)
```yaml
data:
  statusbadge.enabled: "true"
  statusbadge.url: "https://argocd-badges.example.com/"     # optional, overrides the base URL
```

## 2. Use
```markdown
[![App Status](https://argocd.example.com/api/badge?name=payments-prod&revision=true&showAppName=true)](https://argocd.example.com/applications/payments-prod)
```
Parameters (all optional except `name`):
- `name=<app>`
- `revision=true` (default false) shows the revision targeted by the application (first source in multi-source apps), truncated to 7 characters
- `keepFullRevision=true` (default false) shows the full revision
- `showAppName=true` (default false), `width=<integer>` replaces the calculated width
The application details page (Details button, **Status Badge** section) gives copyable URL, Markdown and HTML.

## 3. Exposure
The feature is disabled by default because the badge image is available to any user without authentication:
anyone who knows the URL learns that the app exists, its sync/health status and (with `revision=true`) the revision.
For internet-facing Argo CD, keep badges off unless that exposure is acceptable.

## Verify
- [ ] Badge renders "Healthy | Synced" and changes to OutOfSync after a drift test.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: `statusbadge.enabled` and `statusbadge.url` keys in `argocd-cm`, `/api/badge?name=` URL form, parameters `showAppName`, `revision`, `keepFullRevision`, `width` with defaults, UI location, unauthenticated exposure. Removed unconfirmed `project=` and `appNamespace=` parameters.

Method: documentation only; no commands were run.
