---
id: computing-software.devops-ci-cd.concourse-ci.resource-checker-internals
name: resource-checker-internals
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [checker, lidar, check-every, webhook-token, resource-checking, versions]
level: advanced
status: docs-checked
description: "Know when Concourse checks resources: the lidar scanner interval, check_every as a lower bound, the four trigger criteria, checks at build start, and webhook-only operation."
sources:
  - https://concourse-ci.org/docs/internals/checker/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Resource Checker (internally `lidar`) runs on an interval, default 10 seconds, set by `CONCOURSE_LIDAR_SCANNER_INTERVAL` on the web node. Each tick it looks for resources that have passed their own `resource.check_every`, which defaults to one minute and can be changed globally with `CONCOURSE_RESOURCE_CHECKING_INTERVAL`. Because the checker only ticks periodically, `check_every` is a lower bound between checks, not an exact schedule.

A resource is scheduled for a check when any of these hold:
- it is both an input and a trigger for a job and its `check_every` has elapsed
- it has not returned a version yet
- it has never been checked
- it errored the last time it was checked

Before v8.2.0 the checker considered any job input, whether or not it triggered the job, which caused more checks than needed.

Setting `resource.webhook_token` lets the external service tell Concourse when to check, but periodic checking continues. To rely on webhooks alone, set `check_every` to `never`.

When a job starts, checks may be created first: a manually triggered job checks all its inputs regardless of `check_every`; an automatically triggered job checks inputs past their `check_every`; a re-run of a previous build makes no checks. Inputs with a `passed` constraint are never checked, since a check could not find versions that job could use.

A check runs the resource type's `check` script. Versions are sets of key-value strings chosen by the resource: `git` uses commit SHAs, `registry-image` uses digest and tag.

## Checked

2026-11-04. Intervals, env vars, criteria, build-start rules and version examples confirmed on the Resource Checker page.

Method: documentation only; no commands were run.
