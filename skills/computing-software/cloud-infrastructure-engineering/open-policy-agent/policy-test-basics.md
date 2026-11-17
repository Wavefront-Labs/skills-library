---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.policy-test-basics
name: policy-test-basics
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [opa-test, rego-tests, test-prefix, unit-testing, policy-testing]
level: intro
status: docs-checked
description: "Write and run Rego unit tests with opa test: the test_ prefix, the _test package convention, recursive discovery, and the PASS, FAIL, ERROR and SKIPPED outcomes."
sources:
  - https://www.openpolicyagent.org/docs/policy-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: prove a Rego policy behaves as intended before it ships.

A test is an ordinary rule whose name starts with `test_`. Put tests in a package suffixed `_test` (good practice, not required) and import the package under test:

```rego
package authz_test

import data.authz

test_post_allowed if {
    authz.allow with input as {"path": ["users"], "method": "POST"}
}

test_get_anonymous_denied if {
    not authz.allow with input as {"path": ["users"], "method": "GET"}
}
```

Save the policy and its tests in the same directory and run:

```
opa test . -v
```

`opa test` loads every file passed on the command line; given a directory it loads contents recursively. Use `--run` or `-r` with a re2 regex to select tests by name.

Outcomes:
- undefined or non-`true` result: `FAIL`
- runtime error such as divide by zero: `ERROR`
- rule prefixed `todo_`: `SKIPPED`
- anything else: `PASS`

The summary prints counts such as `PASS: 4/4`. A failing test prints the query trace, showing which `with` call failed, so break the policy deliberately once (delete a rule) and confirm the matching test turns `FAIL`; a test that cannot fail proves nothing.

Add `--format=json` when a CI step must parse results; each entry has `package`, `name`, `duration`, and `fail` or `error` fields.

## Checked

2026-11-04. Confirmed against the OPA docs Policy Testing page: Test Format (test_ prefix, _test package suffix is good practice not required), Test Discovery (recursive for directories), --run/-r with re2 syntax, Test Results (FAIL, ERROR, todo_ SKIPPED, PASS), the PASS: n/m summary, failing trace output and the JSON output format with package, name, duration, fail and error fields. The page also documents --fail-on-empty, which the skill does not mention. Nothing removed.

Method: documentation only; no commands were run.
