---
id: computing-software.devops-ci-cd.concourse-ci.get-step
name: get-step
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [get-step, steps, trigger, passed, version, every, artifacts, resource]
level: practitioner
status: docs-checked
description: "Configure a get step: artifact naming, the resource rename, passed constraints with globs for fan-in, trigger, version latest/every/pinned, params, and metadata as a local var."
sources:
  - https://concourse-ci.org/docs/steps/get/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `get` step fetches a version of a resource and registers it in the build's artifact namespace under the identifier you give; later `task` and `put` steps that list that identifier as an input get a copy in their working directory.

- `resource` (default: the `get` value) renames a pipeline resource into a job-specific artifact name: `get: thecode` with `resource: repo`.
- `trigger` (default `false`): when `true`, a new version of this input automatically creates a build. If no `get` in the job has `trigger: true`, the job can only be triggered manually.
- `passed`: a list of jobs (AND-ed together) whose builds the version must have passed through. Shell globs evaluated with Go's `path.Match()` are allowed, so `lvl-2-*` covers several jobs. If several `get` steps have `passed`, the named jobs are correlated, which gives safe fan-in: a final job only receives versions that went through every upstream job.
- `version` (default `latest`): `latest` takes the newest and may skip versions, which is usually right if someone pushes 100 commits; `every` walks through all versions (only those satisfying `passed`, if set); a pinned version such as `{ref: abcdef123}` must have been detected by the resource, otherwise the input is never satisfied. Use `fly check-resource` to force detection of older versions, since new resources start at the latest.
- `params` pass resource-type-specific configuration.

If the resource exposes metadata for the version, it is a local var named after the step, read as `((.:my-resource.hello))`.

## Checked

2026-11-04. All fields, defaults and examples confirmed on the Get Step page.

Method: documentation only; no commands were run.
