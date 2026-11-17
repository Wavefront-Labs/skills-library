---
id: computing-software.cloud-infrastructure-engineering.vector.validate-configuration
name: validate-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [validate, configuration, exit-codes, healthchecks, ci, topology-checks, vector]
level: practitioner
status: docs-checked
description: "Check a config with vector validate before deploying and understand its three check groups."
sources:
  - https://vector.dev/docs/administration/validating/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vector validate` checks the configuration and exits: code 0 on success, 78 on failure.

```bash
vector validate /etc/vector/vector.yaml
vector validate /etc/vector/vector*.toml
```

Three groups of checks:

1. **Correctness:** every component has its required fields and fields have the proper types. Vector also warns about ignored fields, such as misspelled settings or fields from another enum variant, printing field paths without values. Fix them before a future release rejects them.
2. **Topology:** at least one source and one sink exist, every `inputs` list is non-empty, and inputs refer to valid upstream sources or transforms.
3. **Environment:** components have their prerequisites (for example data directories exist and are writable) and all sinks can reach their targets.

Flags:

- `--no-environment` disables the environment checks.
- `--skip-healthchecks` keeps the other environment checks but skips reachability, for example on a workstation that cannot reach the sinks. The configured `data_dir` must still be writable.

CI usage: run `vector validate --skip-healthchecks` in a pipeline, then deploy and rely on `--require-healthy` at runtime. Combine with `vector test` for behaviour.

Verify by introducing a typo in a field name and confirming the warning appears.

## Checked

2026-11-03. Read administration/validating. Confirmed: exit codes 0 and 78, correctness, ignored-fields, topology and environment checks, `--no-environment`, `--skip-healthchecks` and the writable `data_dir` note. The CI sequence is a suggestion built from these documented flags and `--require-healthy` from the CLI reference. Nothing removed.

Method: documentation only; no commands were run.
