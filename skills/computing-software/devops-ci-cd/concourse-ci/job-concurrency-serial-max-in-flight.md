---
id: computing-software.devops-ci-cd.concourse-ci.job-concurrency-serial-max-in-flight
name: job-concurrency-serial-max-in-flight
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [job, serial, serial-groups, max-in-flight, concurrency, builds]
level: practitioner
status: docs-checked
description: "Control how many builds of a job run at once with serial, serial_groups and max_in_flight, and how groups of jobs share a lock within one pipeline."
sources:
  - https://concourse-ci.org/docs/jobs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default builds of a job run in parallel. Three job fields limit that.

- `serial: true` makes builds queue and run one at a time (default `false`).
- `serial_groups` is a list of arbitrary tag-like strings. Builds of this job and of other jobs sharing any tag are serialised. It only affects jobs in the same pipeline, and builds execute in order of creation across all jobs with common tags.
- `max_in_flight` caps the number of simultaneous builds. If `serial` or `serial_groups` is set they take precedence and force the value to 1.

Documented example:

```yaml
jobs:
  - name: job-a
    serial_groups:
      - some-tag
  - name: job-b
    serial_groups:
      - some-tag
      - some-other-tag
  - name: job-c
    serial_groups:
      - some-other-tag
```

Here `job-a` and `job-c` can run concurrently, but neither can run at the same time as `job-b`, since `job-b` shares one tag with each. Use this to keep deployment or database-migration jobs from overlapping while unrelated jobs run freely.

`job.interruptible` (default `false`) changes worker draining: normally a shutting-down worker waits for builds with containers on it, but with `interruptible: true` it will not wait on this job. Suited to self-deploying Concourse and long but low-importance jobs.

## Checked

2026-11-04. Field semantics, defaults, precedence and the three-job example confirmed on the Jobs page (job schema).

Method: documentation only; no commands were run.
