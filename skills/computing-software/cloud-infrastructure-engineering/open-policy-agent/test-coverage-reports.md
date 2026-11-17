---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.test-coverage-reports
name: test-coverage-reports
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [coverage, opa-test, not-covered, coverage-runs, rule-indexing]
level: practitioner
status: docs-checked
description: "Produce and read opa test --coverage JSON reports, including what not_covered lines mean and the index_excluded and early_exit annotations."
sources:
  - https://www.openpolicyagent.org/docs/policy-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: find policy lines no test exercises.

```
opa test --coverage --format=json example.rego example_test.rego
```

The JSON has a `files` object keyed by file name. Each file lists `covered` and `not_covered` ranges (`start.row`, `end.row`), plus `covered_lines`, `not_covered_lines` and a `coverage` percentage; the top level repeats the totals across all files. Test files appear in the report too, so their own coverage counts toward the overall figure.

Reading an uncovered line:
- on a rule head: the body was never true in any test
- on an expression: it was never evaluated

Not every gap is a missing test. Evaluation-time optimisations can skip a path: rule indexing may exclude it, or an early exit may stop once a result is known. To tell these apart, not-covered ranges can carry a `kinds` array:
- `index_excluded`: the rule indexer excluded the path without trying it
- `early_exit`: an early-exit optimisation skipped it

These come from supplementary evaluation passes controlled by `--coverage-runs`, available on both `opa test` and `opa eval`. Both kinds run by default; passing an empty list disables the extra passes and the annotations.

Workflow: run coverage, ignore ranges annotated with a `kinds` value unless the path matters, then write a case for each remaining rule head. Delete one test, rerun, and confirm the matching rule line moves to `not_covered`.

## Checked

The coverage command, the JSON report shape, the not-covered meaning, the kinds annotations and the --coverage-runs behaviour were confirmed against the Coverage section of the Policy Testing page. The workflow paragraph is practice advice.

Method: docs-checked 2026-11-09 against the OPA docs policy-testing page (docs/docs/policy-testing.md in the OPA repository, full file read).
