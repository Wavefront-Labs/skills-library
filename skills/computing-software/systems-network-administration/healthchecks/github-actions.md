---
id: computing-software.systems-network-administration.healthchecks.github-actions
name: github-actions
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, github-actions, workflow-run, actions-secrets, scheduled-workflows]
level: practitioner
status: docs-checked
description: "Report GitHub Actions scheduled workflow results to Healthchecks using success and failure ping jobs in the same workflow or a workflow_run monitor."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/github_actions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Store the ping URL as a repository secret (`secrets.ping_url`) and reference it through the `secrets` context.

Method 1, extra jobs in the same workflow:

```
jobs:
  Main-Job:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Running housekeeping tasks..."
  Ping-Success:
    runs-on: ubuntu-latest
    needs: [Main-Job]
    steps:
      - run: curl -m 10 --retry 5 ${{ secrets.ping_url }}
  Ping-Failure:
    runs-on: ubuntu-latest
    if: ${{ failure() }}
    needs: [Main-Job]
    steps:
      - run: curl -m 10 --retry 5 ${{ secrets.ping_url }}/fail
```

Method 2, a separate monitoring workflow triggered by `workflow_run`:

```
on:
  workflow_run:
    workflows: ['Hourly Housekeeping']
    types: [completed]
```

Its jobs check `github.event.workflow_run.conclusion` for `'success'` (ping the URL) or `'failure'` (ping `/fail`).

The docs examples schedule the main job hourly with `cron: '15 * * * *'`.

## Checked

2026-11-04: confirmed against the GitHub Actions page (both methods, secrets context, workflow_run with conclusion checks). Removed an unsourced pairing recommendation.
Method: documentation only; no commands were run.
