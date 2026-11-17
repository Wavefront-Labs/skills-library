---
id: computing-software.data-engineering.kestra.flow-checks
name: flow-checks
category: computing-software
field: data-engineering
product: kestra
tags: [checks, validation, block-execution, inputs, guard]
level: practitioner
status: docs-checked
description: "Guard Kestra executions with flow-level checks: when, message, style and behavior, how multiple checks combine, and the strict boolean rule."
sources:
  - https://kestra.io/docs/workflow-components/checks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Checks are assertions evaluated against inputs before an execution is created.

- `when` (required): Pebble expression that must be a boolean; can use inputs, KV pairs and other variables.
- `message` (required): shown in the Execute modal when false.
- `style`: `ERROR`, `SUCCESS`, `WARNING`, `INFO` (default `INFO`).
- `behavior`: `BLOCK_EXECUTION` (default; no execution), `FAIL_EXECUTION` (created as failed), `CREATE_EXECUTION` (created anyway).

```yaml
checks:
  - message: "Sorry, this flow can only be executed with 'Kestra'"
    when: "{{ (inputs.name | upper) == 'KESTRA' }}"
    style: ERROR
    behavior: BLOCK_EXECUTION
```

When several checks fail, the most restrictive behavior applies, in order: `BLOCK_EXECUTION`, `FAIL_EXECUTION`, `CREATE_EXECUTION`.

Caveats:

- The condition must be a real boolean `true`. The strings `"true"` or `"yes"`, numbers and other truthy values do not pass; use comparisons.
- If a condition cannot be evaluated (undefined variable, syntax error), the execution is hard-blocked with `BLOCK_EXECUTION` and `ERROR` style regardless of the declared values.

## Checked

2026-11-04. Confirmed against the Kestra checks page: when and message required, style values and INFO default, behavior values and BLOCK_EXECUTION default, most restrictive behavior wins, strict boolean rule, unevaluatable condition hard-blocks with ERROR style. Nothing removed.

Method: documentation only; no commands were run.
