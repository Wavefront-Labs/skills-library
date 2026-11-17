---
id: computing-software.data-engineering.kestra.flow-inputs
name: flow-inputs
category: computing-software
field: data-engineering
product: kestra
tags: [inputs, validation, input-types, select, secret, nested-inputs]
level: practitioner
status: docs-checked
description: "Declare typed, validated Kestra flow inputs: properties, available types, min/max/regex validators, nested inputs, and the common caveats."
sources:
  - https://kestra.io/docs/workflow-components/inputs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Inputs are typed parameters passed at execution time, referenced as `{{ inputs.name }}`. A missing required or invalid input means no execution is created.

Properties: `id`, `type`, `required` (default `true`), `defaults`, `prefill`, `displayName`, `description`, `validator` (regex), `expression`, `dependsOn`, `autoSelectFirst`.

Types: `STRING`, `EMAIL`, `URI`, `SECRET`, `INT`, `FLOAT`, `BOOL`, `DURATION`, `DATETIME`, `DATE`, `TIME`, `SELECT`, `MULTISELECT`, `JSON`, `ION`, `YAML`, `ARRAY` (needs `itemType`), `FILE`, `FORM`.

```yaml
inputs:
  - id: age
    type: INT
    min: 18
    max: 64
  - id: username
    type: STRING
    validator: ^[a-z0-9_]{3,20}$
  - id: db.host
    type: STRING
    defaults: localhost
```

Reference nested inputs as `{{ inputs.db.host }}`.

Caveats:

- Quote `yes`/`no` in `SELECT` values; YAML may parse them as booleans.
- Use bracket notation for hyphenated ids: `{{ inputs['my-file'] }}`.
- `SECRET` requires an encryption key.
- A `FORM` cannot contain another `FORM`.
- Local `file:///` paths must be listed under `kestra.local-files.allowed-paths`.

## Checked

2026-11-04. Confirmed against the Kestra inputs page: invalid inputs prevent execution creation, property list and required default true, type list, min/max/validator examples, nested dotted ids, yes/no quoting, bracket notation, SECRET needs an encryption key, FORM cannot nest, kestra.local-files.allowed-paths, ARRAY needs itemType. Nothing removed.

Method: documentation only; no commands were run.
