---
id: computing-software.devops-ci-cd.concourse-ci.build-log-retention
name: build-log-retention
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [build-logs, retention, database-size, days-to-retain, builds-to-retain, web-node]
level: practitioner
status: docs-checked
description: "Configure build log retention on the web node with default and max env vars for build count and days, how pipelines can override defaults, and how mixed policies combine."
sources:
  - https://concourse-ci.org/docs/operation/tuning/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Concourse never deletes pipeline build logs, so the database grows without bound until you opt in. Retention is set on the web node with four environment variables, by count and/or by age:

- `CONCOURSE_DEFAULT_BUILD_LOGS_TO_RETAIN`: how many logs to keep per job by default. At `10`, a job with more than ten builds has the extra logs deleted. Users can override it in their pipelines.
- `CONCOURSE_MAX_BUILD_LOGS_TO_RETAIN`: the count ceiling. Users cannot override it.
- `CONCOURSE_DEFAULT_DAYS_TO_RETAIN_BUILD_LOGS`: delete logs older than this many days. Users can override it.
- `CONCOURSE_MAX_DAYS_TO_RETAIN_BUILD_LOGS`: the age ceiling, which users cannot override.

With a mixed policy (both count and days), a build's logs are only reaped if it is older than the `DAYS_TO_RETAIN` value. So a job with many builds still keeps all logs younger than the day limit.

## Checked

2026-11-04. All four variables and the mixed-policy rule confirmed on the Performance Tuning page, Build Logs section. Removed two advisory paragraphs the page does not state.

Method: documentation only; no commands were run.
