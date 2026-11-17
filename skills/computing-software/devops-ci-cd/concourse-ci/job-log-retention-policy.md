---
id: computing-software.devops-ci-cd.concourse-ci.job-log-retention-policy
name: job-log-retention-policy
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [job, build-log-retention, days, builds, minimum-succeeded-builds, logs]
level: practitioner
status: docs-checked
description: "Set a per-job build_log_retention policy with days, builds and minimum_succeeded_builds, including how the three limits combine and the documented worked example."
sources:
  - https://concourse-ci.org/docs/jobs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`job.build_log_retention` limits how long logs are kept for a job that runs often. If omitted, logs are kept forever unless global retention is configured on the web node. Builds outside the policy have their logs reaped. The fields:

- `days`: keep logs for builds finished within this many days.
- `builds`: keep logs for the last N builds.
- `minimum_succeeded_builds`: keep at least this many successful build logs that would otherwise be reaped. It requires `builds` to be an integer above 0. Default 0.

When both `days` and `builds` are set, a build's logs are only reaped if it is older than `days`. All policies work independently:

```yaml
jobs:
  - name: smoke-tests
    build_log_retention:
      days: 2
      builds: 1000
      minimum_succeeded_builds: 1
    plan:
      - get: 10m
      - task: smoke-tests
```

Here, if more than 1000 builds finish in two days, all are kept because of `days`; if 1000 builds span more than two days they are kept because of `builds`; and if all failed, `minimum_succeeded_builds` keeps one successful log.

The page's own illustration of `minimum_succeeded_builds`: with `builds: 5`, `minimum_succeeded_builds: 1` and history 7(f) 6(f) 5(f) 4(f) 3(f) 2(f) 1(s), builds 2 and 3 are reaped, because five logs are retained plus at least one success.

Operators can also set global defaults and maxima; see the build log retention skill.

## Checked

2026-11-04. Field definitions, combination rule and both examples confirmed on the Jobs page, build_log_retention section.

Method: documentation only; no commands were run.
