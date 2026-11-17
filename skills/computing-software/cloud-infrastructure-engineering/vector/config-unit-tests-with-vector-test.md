---
id: computing-software.cloud-infrastructure-engineering.vector.config-unit-tests-with-vector-test
name: config-unit-tests-with-vector-test
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [unit-tests, vector-test, vrl-assertions, no-outputs-from, insert-at, extract-from, vector]
level: advanced
status: docs-checked
description: "Write tests blocks that insert sample events into a transform and assert on the output with VRL."
sources:
  - https://vector.dev/docs/reference/configuration/unit-tests/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Run tests with `vector test /etc/vector/vector.yaml`; several files are treated as one configuration, so tests can live in a separate file. The command is described as experimental.

Each test has a `name`, `inputs` and `outputs`:

```yaml
tests:
  - name: "add_metadata sets id"
    inputs:
      - insert_at: add_metadata
        type: log
        log_fields:
          message: "successful transaction"
    outputs:
      - extract_from: add_metadata
        conditions:
          - type: vrl
            source: |
              assert!(is_string(.id))
              assert_eq!(.message, "successful transaction")
```

Input types are `log`, `metric`, `raw` and `vrl`. `insert_at` names the transform the event is injected into, so you mock sources and test a subset of the pipeline. Alternatives to `log_fields`: `value` for a raw string, `metric` for metric fields, `source` for a VRL program that builds the event.

Assertions: VRL `assert` (boolean) and `assert_eq`, each with an optional message. Use the bang form `assert!` so the program aborts on failure. Hyphenated field names need quotes.

To check that nothing comes out (a filter, or a remap that aborts), use `no_outputs_from: [log_filter]` at test level.

Verify by temporarily breaking an assertion and watching `vector test` fail with the message.

## Checked

2026-11-03. Read reference/configuration/unit-tests and reference/cli. Confirmed: `vector test` is described as experimental, multiple files are one configuration, input types `vrl`, `log`, `raw` and `metric`, `insert_at`, `extract_from`, `log_fields`, `value`, `metric`, `source`, VRL `assert` and `assert_eq` with the bang form recommended, and the root-level `no_outputs_from`. Nothing removed.

Method: documentation only; no commands were run.
