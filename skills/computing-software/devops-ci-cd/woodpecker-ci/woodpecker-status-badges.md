---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-status-badges
name: woodpecker-status-badges
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [badges, status-badge, readme]
level: intro
status: docs-checked
description: "Add Woodpecker pipeline status badges to a README with branch and event options."
sources: ["https://woodpecker-ci.org/docs/usage/badges"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker status badges

Woodpecker serves repository status badges you can embed in a website or README.

```text
<scheme>://<hostname>/api/badges/<repo-id>/status.svg
```

By default the badge shows the latest build on the default branch (for example `main`). Pick another branch with the `branch` query parameter:

```text
<scheme>://<hostname>/api/badges/<repo-id>/status.svg?branch=<branch>
```

By default badges do not include pull request results, because a pull request's status does not accurately represent the repository state; the badge reflects the last `push` event. To include other events, pass the `events` parameter:

```text
<scheme>://<hostname>/api/badges/<repo-id>/status.svg?events=manual,cron
```

## Checked

2026-11-03. Confirmed against: badges (endpoint, branch and events parameters, pull requests excluded). Removed: the numeric repo-id remark (CI_REPO_ID) and a closing paragraph of generic advice.

Method: documentation only; no commands were run.
