---
id: computing-software.devops-ci-cd.concourse-ci.in-parallel-do-try-steps
name: in-parallel-do-try-steps
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [in-parallel, do-step, try-step, limit, fail-fast, build-matrix, steps]
level: practitioner
status: docs-checked
description: "Run steps concurrently with in_parallel (limit, fail_fast), group serial steps with do, and swallow non-critical failures with try, with the documented YAML for each."
sources:
  - https://concourse-ci.org/docs/steps/in-parallel/
  - https://concourse-ci.org/docs/steps/do/
  - https://concourse-ci.org/docs/steps/try/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**`in_parallel`** runs steps concurrently. If any sub-step fails or errors, the whole step does. It is the easiest speed-up, usually fetching all inputs together. It takes either a list or a config with `steps`, `limit` and `fail_fast`:

```yaml
- in_parallel:
    limit: 2
    fail_fast: false
    steps:
      - get: ci
      - get: repo
      - get: code
```

`limit` is a semaphore, default unlimited, so a growing set of tasks does not overload workers. `fail_fast` (default `false`) returns as soon as one sub-step fails, interrupting running steps and not scheduling pending ones. Because any failure fails the build, it suits build matrices, such as unit tests for windows, linux and darwin.

**`do`** performs steps serially, as if they were at the top level. Use it where a single step is required: under `try`, `across`, or a step hook.

**`try`** performs a step and masks any failure as success. Use it for side effects where failure should not fail the build, such as a flaky log upload:

```yaml
on_success:
  try:
    put: test-logs
    params:
      from: run-tests/*.log
```

`try` swallows the failure entirely, so avoid it around anything whose result matters.

## Checked

2026-11-04. Semantics, defaults and examples confirmed on the In Parallel, Do and Try step pages.

Method: documentation only; no commands were run.
