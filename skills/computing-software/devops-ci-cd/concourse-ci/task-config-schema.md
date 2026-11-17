---
id: computing-software.devops-ci-cd.concourse-ci.task-config-schema
name: task-config-schema
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [task, task-config, platform, image-resource, inputs, outputs, params, run]
level: practitioner
status: docs-checked
description: "Write a task config: platform, image_resource, inputs with path and optional, outputs, params, run path/args/dir/user, rootfs_uri, and the ENTRYPOINT behaviour that needs v8."
sources:
  - https://concourse-ci.org/docs/tasks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A task is a function from `inputs` to `outputs` that succeeds or fails; ideally pure, though flaky tests and internet dependencies make real ones impure. Conventionally the config lives with the code it tests, possibly under a `ci` directory.

- `platform` (required): `linux`, `darwin` or `windows`; it selects the worker pool.
- `image_resource`: an anonymous resource (`type`, `source`, optional `params` and `version`) whose latest version is checked and fetched before the task runs. Required only for Linux; ignored on Windows and Darwin, where the task runs in a clean temp directory and dependencies must be pre-installed. To use an image from an earlier step, set `image` on the task step.
- `inputs`: `name`, optional `path` (default the name; relative paths recommended, `../` is removed) and `optional: true` (default false). A missing required input errors the task immediately.
- `outputs`: directories created before the task runs; whatever the task puts there is exported under the output name.
- `params`: environment variables, overridable by the task step.
- `run`: `path`, `args`, `dir` and `user`. If `run` is omitted, the image's `ENTRYPOINT`/`CMD` is used (v8 and later only); args are appended. `run` is explicit path and args rather than a script blob so `fly` can forward arguments.
- `rootfs_uri`: a Garden-backend rootfs, only if you have no other option.

```yaml
platform: linux
image_resource:
  type: registry-image
  source:
    repository: golang
run:
  path: go
  args:
    - version
```

## Checked

Checked 2026-11-09 against the raw docs source of the Tasks page (read in full): every field, default and note above matches the task-config schema section.

Method: docs-checked 2026-11-09 against concourse docs Tasks page (github.com/concourse/docs source); documentation only, no commands were run.
