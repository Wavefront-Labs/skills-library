---
id: computing-software.web-development.directus.flow-data-chain
name: flow-data-chain
category: computing-software
field: web-development
product: directus
tags: [data-chain, flow-variables, trigger-accountability, flows-env-allow-list]
level: practitioner
status: docs-checked
description: "Read and reference the Directus flow data chain: $trigger, $accountability, $env, $last and operation keys, using {{ }} variable syntax."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/06.flows/2.data-chain.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each flow run builds one JSON data chain. It starts with four keys:
- `$trigger`: data from the trigger (headers, payloads, tokens)
- `$accountability`: who or what started it (user, role, admin, app, ip, userAgent)
- `$env`: environment variables listed in `FLOWS_ENV_ALLOW_LIST`
- `$last`: output of the most recently executed operation

After each operation, its output is appended under its `<operationKey>`; if it generates nothing, `null`.

Reference values in operation options with double braces; dot notation and array indexes work, and hardcoded JSON can sit alongside:

```json
{
  "key0": "a hard-coded value",
  "key1": "{{ $trigger.payload }}",
  "key2": "{{ operationKey.payload.friend_list[0] }}"
}
```

Use Toggle to Raw Editor on an operation to bypass dropdowns and type raw values.

## Checked

2026-11-04: confirmed against the Directus docs Data Chain page: four starting keys, operation key appending with null, variable syntax, dot notation and array indexing, Toggle to Raw Editor. Removed the unsupported gotcha and verify lines.

Method: documentation only; no commands were run.
