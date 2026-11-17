---
id: computing-software.devops-ci-cd.concourse-ci.fly-job-management-commands
name: fly-job-management-commands
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [fly, trigger-job, rerun-build, pause-job, unpause-job, clear-task-cache, jobs]
level: practitioner
status: docs-checked
description: "Operate jobs with fly: list jobs, trigger with --watch, rerun a build with the same inputs, pause and unpause a job, and clear a task cache by step or cache path."
sources:
  - https://concourse-ci.org/docs/jobs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Job commands on the Jobs page, all taking a target `-t example` and a `pipeline/job` value:

- `fly -t example jobs -p my-pipeline` lists the jobs.
- `fly -t example trigger-job --job my-pipeline/my-job` queues a build; add `--watch` to follow it. The `+` button in the web UI does the same.
- `fly -t example rerun-build --job my-pipeline/my-job --build 4 --watch` queues a new build with exactly the same input versions as build 4. The page's own code block for this command repeats its description text instead of the command, so take the syntax from the `--watch` example.
- `fly -t example pause-job --job my-pipeline/my-job` stops pending builds from being scheduled. Builds in flight still run and new pending builds are still created.
- `fly -t example unpause-job --job my-pipeline/my-job` resumes scheduling.
- `fly -t example clear-task-cache --job my-pipeline/my-job --step my-step-name` invalidates the caches immediately; they are garbage collected asynchronously and later builds start with empty caches. Add `--cache-path go/pkg` to clear only one path; without it, all caches for that step are cleared.

Clearing a task cache is the standard answer when a `caches:` entry has been poisoned by a bad dependency download or stale build output. Pausing a job is the safe way to hold a deploy while leaving in-flight builds alone.

For instanced pipelines the `--job` value takes the form `group/var1:value1/job`.

## Checked

2026-11-04. Command syntax and behaviour confirmed on the Jobs page (Managing Jobs); the rerun-build code block anomaly was observed in the source text.

Method: documentation only; no commands were run.
