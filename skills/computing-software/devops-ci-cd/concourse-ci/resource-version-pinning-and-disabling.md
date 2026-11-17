---
id: computing-software.devops-ci-cd.concourse-ci.resource-version-pinning-and-disabling
name: resource-version-pinning-and-disabling
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [resource-versions, pinning, unpinning, disable-version, passed, scheduler]
level: practitioner
status: docs-checked
description: "Pin, unpin and disable resource versions, with the precedence of config pins over UI pins, how pins interact with passed constraints, and what unpinning triggers."
sources:
  - https://concourse-ci.org/docs/resources/resource-versions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A version is the exact state of a resource at a point in time, defined by the resource type's `check` behaviour: commits for `git`, image digests for a docker image resource. The resource checker saves versions to the database, the web UI lists them on the resource page, and the build scheduler uses them to schedule builds.

**Pinning** runs a job on an old version instead of the latest. Two routes:
- In pipeline config, via `resource.version` or a `get` step's `version`. This is the permanent route; a config-pinned resource cannot be changed in the web UI, only by changing and resetting the pipeline config.
- In the web UI, on the resource version history page. This is for reactionary use, such as a broken upstream dependency. If a version is pinned in the UI and in config, the config pin takes precedence.

A pin on a resource propagates throughout the pipeline (a pin on a single `get` step is not shown on the resource page). With a `passed` constraint, the pinned version must have been used by the upstream job. In a two-job pipeline the first job builds with the pinned version, and when it succeeds the second job can trigger because that version passed.

**Unpinning** returns to the latest available version. If the most recent build used the old pin and the input has `trigger: true`, a new build is queued.

**Disabling** a version in the web UI, from the version history page, stops it being used to schedule builds for any job that takes the resource as input. It can be re-enabled. Use it for versions you know are broken or incompatible.

## Checked

2026-11-04. Pinning routes, precedence, passed behaviour, unpinning and disabling confirmed on the Resource Versions page.

Method: documentation only; no commands were run.
