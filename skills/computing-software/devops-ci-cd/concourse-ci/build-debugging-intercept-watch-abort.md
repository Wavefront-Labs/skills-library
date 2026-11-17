---
id: computing-software.devops-ci-cd.concourse-ci.build-debugging-intercept-watch-abort
name: build-debugging-intercept-watch-abort
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [fly, intercept, hijack, watch, builds, abort-build, debugging, containers]
level: practitioner
status: docs-checked
description: "Debug builds with fly intercept (by step, job, check container), watch logs from the CLI, list builds with filters, abort builds, and know when failed containers are kept."
sources:
  - https://concourse-ci.org/docs/builds/
  - https://concourse-ci.org/docs/internals/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A build is a job's plan, a resource check, or a one-off `fly execute`. Containers and volumes go away after a successful build. A failed build's are kept for debugging: for a job's build until its next build starts, and for a one-off build removed immediately, so intercept while it runs.

`fly intercept` opens a shell in a container:

```shell
fly -t example intercept -j some-pipeline/some-job -b some-build -s some-step
fly -t example intercept --check some-pipeline/some-resource
fly -t example intercept ps auxf
```

`--build` defaults to the job's latest build; one-off builds are reached by build ID. Omitting `--step` lets you choose. Ambiguous matches open a prompt. A trailing command is allowed, so `watch fly intercept ps auxf` follows the current build. The original working directory and environment, including task `params`, are reused. On Windows workers run `fly -t example intercept powershell`. The web load balancer needs TCP or SSL forwarding for this to work.

`fly -t example builds` lists recent builds (50 by default); `-j pipeline/job`, `-c 100`, `--since` and `--until` (format `yyyy-mm-dd HH:mm:ss`) filter.

`fly -t example watch --job my-pipeline/tests --build 52` shows archived or streaming logs; with no `--build` it takes the latest. Unlike `fly execute`, killing `fly watch` does not abort the build. Use `--ignore-event-parsing-errors` for an `unknown event type` mismatch between fly and web.

`fly -t example abort-build --job my-pipeline/my-job --build 3` cancels a build.

## Checked

2026-11-04. Retention of containers, intercept flags, builds filters, watch and abort confirmed on the Builds page; TCP forwarding note on the Internals page.

Method: documentation only; no commands were run.
