---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.data-driven-test-cases
name: data-driven-test-cases
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [parameterized-tests, table-tests, test-cases, yaml-fixtures, rego-tests]
level: practitioner
status: docs-checked
description: "Write parameterised Rego tests with case names in the rule head, load cases from JSON or YAML data files, and nest case dimensions."
sources:
  - https://www.openpolicyagent.org/docs/policy-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run one test body over many named cases and see which case failed.

Declare case names as variables in the test rule head reference, then enumerate with `some`:

```rego
package example_test

test_concat[note] if {
    some note, tc in {
        "empty + empty": {"a": [], "b": [], "exp": []},
        "empty + filled": {"a": [], "b": [1, 2], "exp": [1, 2]},
    }

    act := array.concat(tc.a, tc.b)
    act == tc.exp
}
```

`opa test` lists each case under the rule: `empty + empty: PASS`. A failing case marks the whole rule `FAIL`.

Cases do not have to be inline Rego. Put them in a YAML or JSON data file and pass both files:

```yaml
test_cases:
  empty + empty:
    a: []
    b: []
    exp: []
```

```rego
import data.test_cases

test_concat[note] if {
    some note, tc in test_cases
    act := array.concat(tc.a, tc.b)
    act == tc.exp
}
```

```
opa test file_example_test.rego file_example_test.yaml
```

Nest dimensions by adding more variables to the head, for example `test_sign_token[note][alg]`, and iterate a second `some alg in [...]`. The report indents results by level, so a failure shows as `claims: FAIL` then `HS333: FAIL`.

Keep the expected value in the data, never recomputed from the same logic as the policy.

## Checked

2026-11-04. Confirmed against the OPA docs Policy Testing page, Parameterized Tests and Data-driven Testing: case names in the rule head reference with some, loading cases from YAML/JSON data files (opa test file_example_test.rego file_example_test.yaml), nested case names such as test_sign_token[note][alg], and the indented FAIL/PASS report. Nothing removed.

Method: documentation only; no commands were run.
