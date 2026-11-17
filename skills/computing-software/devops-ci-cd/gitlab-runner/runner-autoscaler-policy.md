---
id: computing-software.devops-ci-cd.gitlab-runner.runner-autoscaler-policy
name: runner-autoscaler-policy
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [autoscaler-policy, idle-count, idle-time, scale-factor, periods]
level: sme
status: docs-checked
description: "Keep warm instances with [[runners.autoscaler.policy]] idle settings and schedules."
sources: ["https://docs.gitlab.com/runner/configuration/advanced-configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Autoscaler policies

Policies keep instances ready ahead of demand. Each `[[runners.autoscaler.policy]]` entry may set:
- `idle_count`: target idle capacity immediately available for jobs (counts jobs, not machines).
- `idle_time`: how long an idle instance lives before removal.
- `scale_factor`: idle capacity on top of `idle_count`, as a factor of current in-use capacity; default `0.0`.
- `periods`: unix-cron strings for when the policy is enabled; default `* * * * *`.

With periods you can run a larger idle pool in working hours and a smaller one at night.

With `preemptive_mode` on, jobs are requested only when an instance is confirmed available, so they start almost immediately. With it off, jobs are requested first and the system then finds or provisions capacity.

## Checked

2026-11-03. Confirmed against policy settings on Advanced configuration. Corrected idle_count/scale_factor/preemptive_mode wording and removed the unsupported failure claim.

Method: documentation only; no commands were run.
