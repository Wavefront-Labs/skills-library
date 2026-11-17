---
id: computing-software.devops-ci-cd.concourse-ci.step-hooks-and-failure-handling
name: step-hooks-and-failure-handling
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [hooks, on-success, on-failure, on-error, on-abort, ensure, build-status]
level: practitioner
status: docs-checked
description: "Choose between on_success, on_failure, on_error, on_abort and ensure, including what each triggers on, that hooks do not recover a failure, and a lock-release pattern."
sources:
  - https://concourse-ci.org/docs/steps/modifier-and-hooks/ensure/
  - https://concourse-ci.org/docs/steps/modifier-and-hooks/on-success/
  - https://concourse-ci.org/docs/steps/modifier-and-hooks/on-failure/
  - https://concourse-ci.org/docs/steps/modifier-and-hooks/on-error/
  - https://concourse-ci.org/docs/steps/modifier-and-hooks/on-abort/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hooks attach a step to a parent step.

- `on_success`: runs if the parent succeeds. It is equivalent to just listing the next step; it exists so it can sit beside an `on_failure`.
- `on_failure`: runs if the parent fails. It does not recover the failure, so the parent still fails even if the hook succeeds.
- `on_error`: runs when the parent terminates abnormally in a way not handled by `on_abort` or `on_failure`, from configuration mistakes and temporary worker network problems to exceeding a `timeout`.
- `on_abort`: runs if the build is aborted while the parent was running and was terminated.
- `ensure`: runs after the parent regardless of success, failure or error, and also if the build was aborted and the parent interrupted. If the parent succeeds and the ensured step fails, the overall step fails.

```yaml
plan:
  - put: some-lock
    params:
      acquire: true
  - task: integration
    file: foo/integration.yml
    ensure:
      put: some-lock
      params:
        release: some-lock
```

Notification example from the docs: wrap `get` and `task` in `do` and put `on_error: put: slack` on the `do`, so the hook covers both steps.

## Checked

Checked 2026-11-09 against the raw docs source of the Ensure, On Success, On Failure, On Error and On Abort hook pages (all read in full). Removed the unconfirmed claims that the same hooks exist at job level and that a hook takes only one step.

Method: docs-checked 2026-11-09 against concourse docs hook pages (github.com/concourse/docs source); documentation only, no commands were run.
