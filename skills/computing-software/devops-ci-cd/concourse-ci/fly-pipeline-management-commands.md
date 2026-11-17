---
id: computing-software.devops-ci-cd.concourse-ci.fly-pipeline-management-commands
name: fly-pipeline-management-commands
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [fly, pipelines, pause-pipeline, archive-pipeline, expose-pipeline, destroy-pipeline, rename-pipeline]
level: practitioner
status: docs-checked
description: "Manage pipelines with fly: list, rename, pause, expose and hide, get-pipeline as YAML or JSON, order, destroy, and archive, including what archiving deletes and what it keeps."
sources:
  - https://concourse-ci.org/docs/pipelines/managing-pipelines/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Commands from the Managing Pipelines page, each with `-t example`:

- `fly pipelines` lists pipelines and paused state; `--include-archived` adds archived ones.
- `rename-pipeline --old-name a --new-name b` keeps all job history.
- `pause-pipeline --pipeline p` stops scheduling and the periodic checking of resources; in-flight builds finish. `unpause-pipeline` resumes both.
- `expose-pipeline --pipeline p` makes a pipeline visible to other teams and unauthenticated users. It reveals nearly everything except build output and resource metadata. Metadata needs `resource.public: true`; build output needs `job.public: true`, which also reveals resource metadata of `get` and `put` steps in that output. `hide-pipeline` (short form `hp`) undoes it.
- `get-pipeline --pipeline p` prints the config; `-j` or `--json` gives JSON for jq.
- `order-pipelines --pipeline a --pipeline b` only guarantees relative order; unlisted pipelines may appear before, between or after. Instanced pipelines inside a group use `order-instanced-pipelines`.
- `destroy-pipeline` stops activity and removes all data, including build history and collected versions.
- `archive-pipeline -p p` pauses and hides the pipeline and deletes its config, so interpolated secrets are removed, but keeps build logs. `get-pipeline` no longer works for it. Setting a pipeline again with the same name unarchives it, and logs return for jobs with matching names.

## Checked

2026-11-04. All commands and behaviours confirmed on the Managing Pipelines page.

Method: documentation only; no commands were run.
