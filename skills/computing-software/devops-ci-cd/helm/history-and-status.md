---
id: computing-software.devops-ci-cd.helm.history-and-status
name: history-and-status
category: computing-software
field: devops-ci-cd
product: helm
tags: [history, status, release-state, pending-install, revisions, output-format]
level: practitioner
status: docs-checked
description: "Read a release's revision history and current status, including the possible release states and the revision selector."
sources:
  - "https://helm.sh/docs/helm/helm_history/"
  - "https://helm.sh/docs/helm/helm_status/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`helm history RELEASE_NAME` prints a table with REVISION, UPDATED, STATUS, CHART, APP VERSION and DESCRIPTION. It returns at most 256 revisions by default; `--max` changes that. `-o` gives table, json or yaml, and `--show-rollback-revision` adds a ROLLBACK column.

`helm status RELEASE_NAME` shows:

- the last deployment time and the namespace,
- the release state,
- the revision and a description (a completion or error message),
- the resources of the release,
- details of the last test suite run, if any,
- the chart's notes.

State values listed in the reference: `unknown`, `deployed`, `uninstalled`, `superseded`, `failed`, `uninstalling`, `pending-install`, `pending-upgrade` and `pending-rollback`.

Use `helm status RELEASE --revision N` to look at an earlier revision and `-o json` for scripts.

If `--history-max` is low, older revisions disappear from the history table and cannot be rolled back to.

## Checked

2026-11-03. Confirmed against https://helm.sh/docs/helm/helm_history/ (columns, --max default 256, -o, ROLLBACK column) and https://helm.sh/docs/helm/helm_status/ (status contents, state values, --revision). Removed: the pending-state troubleshooting paragraph (not on the pages).
Method: documentation only; no commands were run.

