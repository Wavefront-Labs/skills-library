---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-events
name: woodpecker-events
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [event, triggers, pull-request]
level: practitioner
status: docs-checked
description: "List the Woodpecker pipeline events and filter steps by event type."
sources: ["https://woodpecker-ci.org/docs/usage/workflow-syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker events

Pipelines are started by events. Filter on them with `when: event:`.

- `push`: a commit is pushed to a branch.
- `pull_request`: a pull request is opened or a new commit is pushed to it.
- `pull_request_closed`: a pull request is closed or merged.
- `pull_request_metadata`: pull request metadata changed (title, body, label, milestone and similar).
- `tag`: a tag is pushed.
- `release`: a release, pre-release or draft is created. Narrow it further with `evaluate` and the built-in environment variables.
- `deployment`: a deployment is created in the repository. Woodpecker can trigger it directly; GitHub also supports webhook triggers.
- `cron`: a cron job runs.
- `manual`: a user triggers the pipeline manually.

```yaml
when:
  - event: [push, tag, deployment]
```

```yaml
when:
  - event: push
    branch: main
```

Event conditions can also be written in an `evaluate` expression using `CI_PIPELINE_EVENT`, for example `CI_PIPELINE_EVENT == "push"`.

## Checked

2026-11-08. Read the Woodpecker workflow syntax page in full (raw markdown) and confirmed the nine events and their descriptions and the three event examples. Removed: the per-forge support claims about Bitbucket (from a page not cited) and the claim that only GitHub can webhook-trigger deployments (page says GitHub also supports it). Reworded the CI_PIPELINE_EVENT note to the documented evaluate example.

Method: documentation only; no commands were run.
