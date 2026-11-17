---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.test-failure-diagnosis-flags
name: test-failure-diagnosis-flags
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [var-values, fail-on-empty, opa-test, ci-gate, rego-tests]
level: practitioner
status: docs-checked
description: "Use opa test --var-values to see why an assertion failed, --run to filter, --fail-on-empty to stop silent no-test CI passes, and todo_ to skip."
sources:
  - https://www.openpolicyagent.org/docs/policy-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make failing tests explain themselves and keep CI honest.

`--var-values` enriches the report with the failing expression and the value of each variable or reference in it:

```
opa test . --var-values
```

For `"read" in authz.allowed_actions(user) with data.actions as p` the report draws each sub-term with its value (`["write"]`, `"jane"`, the `p` object), so you see which user and which data combination broke the assertion.

Filter by name with a re2 regex:

```
opa test . --run 'test_get_.*'
```

A misspelt name or an accidental empty selection still exits successfully. Add `--fail-on-empty` so the run fails instead. This is also useful in CI pipelines to ensure tests were actually executed.

Placeholders: prefix a test with `todo_` and it is reported as `SKIPPED` rather than failing:

```rego
todo_test_missing_implementation if {
    example.allow with data.roles as ["not", "implemented"]
}
```

Result classes: `FAIL` for undefined or non-true results, `ERROR` for runtime errors such as `div: divide by zero` (the message and line are printed under the test). Machine-readable output comes from `--format=json`.

Checklist for a pipeline step: `opa test . --fail-on-empty --var-values`, then break one rule deliberately and confirm the step goes red.

## Checked

The --var-values report, --run, --fail-on-empty, the todo_ prefix and the result classes were confirmed against the Policy Testing page.

Method: docs-checked 2026-11-09 against the OPA docs policy-testing page (docs/docs/policy-testing.md in the OPA repository, full file read).
