---
id: computing-software.devops-ci-cd.concourse-ci.resource-config-schema
name: resource-config-schema
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [resources, resource-schema, check-every, check-timeout, tags, public, icon, old-name, pinning]
level: practitioner
status: docs-checked
description: "Configure a pipeline resource: name, type, source, old_name rename, icon, pinned version, check_every and never, check_timeout, worker tags, public metadata and build-created-by."
sources:
  - https://concourse-ci.org/docs/resources/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A resource is a versioned artifact with an external source of truth, continuously `check`ed for new versions and flowing through `get` steps. Resources run as containers on workers. Fields under `pipeline.resources`:

- `name`, `type` (required) and `source` (required): the source is a black box passed to the resource at runtime. Its documentation lives in each resource type's README.
- `old_name`: inherit the history of the old resource, then remove the field once the pipeline is set.
- `icon`: a Material Design name like `github`, or a Simple Icons name prefixed `si/` such as `si/concourse` (Simple Icons since v8.2.0).
- `version`: pin the resource across the pipeline, like `version` on every `get`. It overrides a temporary pin made in the UI or API, which is disabled while a config pin exists.
- `check_every` (default `1m`): a Go `time.ParseDuration` string, or `never` to check only when a connected job is triggered (manual checks via UI, fly or webhooks still work).
- `check_timeout` (default `1h`).
- `tags`: workers on which checks run, needed when the source is inside a worker's network. These do not apply to `get` or `put` steps; set step `tags` for those.
- `public` (default `false`): metadata of each version visible to unauthenticated users when the pipeline is exposed. Version identifiers are visible regardless, and metadata is also shown in the output of a `job.public` job.
- `expose_build_created_by` (default `false`): makes `BUILD_CREATED_BY` available in the metadata of `put` steps, not `get` steps.

## Checked

2026-11-04. Every field and default confirmed on the Resources page.

Method: documentation only; no commands were run.
