---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-failure-handling
name: woodpecker-failure-handling
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [failure, ignore, cancel]
level: practitioner
status: docs-checked
description: "Let a Woodpecker step fail without failing the pipeline, or cancel the pipeline on failure."
sources: ["https://woodpecker-ci.org/docs/usage/workflow-syntax", "https://woodpecker-ci.org/docs/usage/services"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker step failure handling

By default a failing step stops the workflow and the pipeline reports failure. The `failure` key changes this per step.

```yaml
steps:
  - name: lint
    image: golang
    commands:
      - go vet ./...
    failure: ignore
```

Values:

- `failure: fail` is the default behaviour.
- `failure: ignore` reports the step as failed but still runs the following steps, and the workflow status is not affected. Use it for non-blocking checks such as linting.
- `failure: cancel` cancels the whole pipeline once the step fails.

The same key works on services. A service that does not shut down cleanly is sent SIGTERM and then SIGKILL; add `failure: ignore` when you do not care how it exits.

To run a step because something failed (for example a notification), use a `when` block with a `status` filter instead of `failure`. Steps normally run only while the workflow has succeeded so far, which equals `status: [success]`:

```yaml
- name: notify
  image: alpine
  when:
    - status: [success, failure]
```

`failure` controls whether a step's result counts; `status` controls whether a step runs after earlier failures.

## Checked

2026-11-03. Confirmed against: workflow-syntax (failure, status) and services (SIGTERM then SIGKILL, failure: ignore). Removed: nothing.

Method: documentation only; no commands were run.
