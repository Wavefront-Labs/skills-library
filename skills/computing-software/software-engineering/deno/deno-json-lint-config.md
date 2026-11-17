---
id: computing-software.software-engineering.deno.deno-json-lint-config
name: deno-json-lint-config
category: computing-software
field: software-engineering
product: deno
tags: [deno-json, lint, rules, tags, recommended, include-exclude]
level: intro
status: docs-checked
description: "Configure deno lint from deno.json: file include/exclude and the rules block with tags, include and exclude."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/deno_json.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `lint` field controls which files `deno lint` checks and which rules apply:

```json title="deno.json"
{
  "lint": {
    "include": ["src/"],
    "exclude": ["src/testdata/", "src/fixtures/**/*.ts"],
    "rules": {
      "tags": ["recommended"],
      "include": ["ban-untagged-todo"],
      "exclude": ["no-unused-vars"]
    }
  }
}
```

This lints only `src/`, skips `src/testdata/` and TypeScript files in `src/fixtures/`, applies the recommended rule tag, adds `ban-untagged-todo` and removes `no-unused-vars`.

A full list of rules is on the lint rules page of the Deno docs.

## Checked

2026-11-04. Confirmed against the Deno configuration file (deno.json) reference: the lint example and its explanation. Nothing removed.

Method: documentation only; no commands were run.
