---
id: computing-software.devops-ci-cd.concourse-ci.build-scheduler-internals
name: build-scheduler-internals
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [scheduler, algorithm, passed-constraints, trigger, inputs, builds, build-tracker]
level: advanced
status: docs-checked
description: "Explain how Concourse schedules builds: the 10-second tick, the input-version algorithm, the new-version rule for trigger inputs, and the events that mark a job for scheduling."
sources:
  - https://concourse-ci.org/docs/internals/scheduler/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The build scheduler is a global component covering every job in a deployment. It ticks every 10 seconds by default, and with several ATCs only one scheduler runs per tick. Documentation applies to v6.0.0 and above.

**Algorithm.** A subcomponent that works out the input versions for a job's next build. It accounts for `version` and `passed` constraints on `get` steps, versions disabled in the web UI, and so on. It can fail to find a valid set of inputs; the error appears in the build page's preparation view. If it succeeds, the scheduler compares the trigger-able input versions with those of the previous build.

**Rule.** A new build is scheduled if any version computed for a `trigger: true` input has never been used in any previous build of that job for that same input. A version used by a build two months ago will not trigger again.

**On-demand scheduling.** The scheduler only schedules jobs that need it. A job is marked for scheduling by: a check detecting a new version; a `put` saving a new version; an upstream job finishing through `passed`; enabling or disabling, or pinning or unpinning, a version not yet used; setting the pipeline; updating a resource's resource config; manually triggering; rerunning a build; or multiple versions being available for a version-every constraint.

The scheduled build is then picked up by the build tracker, which runs it.

## Checked

2026-11-04. Interval, algorithm, scheduling rule and list of scheduling reasons confirmed on the Build Scheduler page.

Method: documentation only; no commands were run.
