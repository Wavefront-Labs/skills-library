---
id: computing-software.devops-ci-cd.concourse-ci.attempts-timeout-and-step-tags
name: attempts-timeout-and-step-tags
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [attempts, timeout, tags, retry, worker-selection, private-network, steps]
level: practitioner
status: docs-checked
description: "Retry flaky steps with attempts, bound them with timeout (which errors, not aborts), and route steps to workers with tags, including inheritance via do and in_parallel in v8.3.0+."
sources:
  - https://concourse-ci.org/docs/steps/modifier-and-hooks/attempts/
  - https://concourse-ci.org/docs/steps/modifier-and-hooks/timeout/
  - https://concourse-ci.org/docs/steps/modifier-and-hooks/tags/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**`attempts`** is the total number of tries before a step fails: `5` runs it up to five times. It retries on a Concourse error as well as a build failure. `attempts: 10` means one try plus up to nine retries.

**`timeout`** takes a duration such as `30m` or `1h30m`. When exceeded the step is interrupted with the same semantics as aborting the build, except the build is `errored`, not `aborted`, so human intervention and enforced timeouts can be told apart. That means `on_error` fires on timeout.

Combined, the timeout applies to each attempt:

```yaml
- task: flaky-tests
  file: flake/integration.yml
  timeout: 10m
  attempts: 3
```

This is deliberate: things usually either finish in a reasonable time or hang, so each attempt gets the allotted time rather than one hung attempt consuming everything.

**`tags`** match worker tags: with `[a, b]` only workers advertising both tags (and possibly others) run the step. From v8.3.0, `tags` on a `do` or `in_parallel` step are inherited by all child steps. Children can override with their own tags but cannot clear them, so split the plan if some steps must remain untagged.

```yaml
plan:
  - tags: ["private"]
    do:
      - get: my-repo
      - task: acceptance-tests
        file: my-repo/ci/acceptance.yml
```

Typical use is reaching a private cluster through on-premises workers.

## Checked

2026-11-04. Semantics and examples confirmed on the Attempts, Timeout and Tags modifier pages.

Method: documentation only; no commands were run.
