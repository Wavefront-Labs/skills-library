---
id: computing-software.devops-ci-cd.concourse-ci.build-reruns-and-caveats
name: build-reruns-and-caveats
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [rerun-build, builds, passed-constraints, scheduler, rerun, inputs]
level: practitioner
status: docs-checked
description: "Understand reruns: same input versions, numbering like 3.1, ordering after the original, effect on passed constraints, and the caveat that reruns use the current job config."
sources:
  - https://concourse-ci.org/docs/builds/
  - https://concourse-ci.org/docs/internals/checker/
  - https://concourse-ci.org/docs/jobs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rerunning builds a new build from the exact input versions of an earlier one, through the web UI build page or `fly rerun-build`.

The rerun is named after the original with a rerun number: the first rerun of build `3` is `3.1`. Rerun builds are ordered chronologically after the original, not as a new latest build. The scheduler uses that same order when resolving `passed` constraints on a job that has reruns, so versions that made it through a rerun do not become the latest versions. Instead they behave as if the original build had succeeded at its place in history. In short, a rerun acts as though it replaces the original failed build.

**Caveat.** The page calls the implementation an early iteration: a rerun uses the current state of the job config, not the plan the original build ran with. If `job.plan` changed in a backwards-incompatible way the rerun may error. For example, if a new input was added, there is no version for it because the original build did not use it.

Reruns make no resource checks when they start, per the checker rules. They can be turned off per job with `disable_reruns: true`. Treat a rerun as safe for transient failures (a flaky test, an outage) and re-trigger a fresh build if the pipeline has changed since.

## Checked

2026-11-04. Naming, ordering and caveats confirmed on the Builds page, Rerunning a Build; no-check rule on the Resource Checker page; disable_reruns on the Jobs page.

Method: documentation only; no commands were run.
