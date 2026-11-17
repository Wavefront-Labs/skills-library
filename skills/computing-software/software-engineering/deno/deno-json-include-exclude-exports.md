---
id: computing-software.software-engineering.deno.deno-json-include-exclude-exports
name: deno-json-include-exclude-exports
category: computing-software
field: software-engineering
product: deno
tags: [deno-json, include, exclude, negated-glob, exports, publish, gitignore]
level: practitioner
status: docs-checked
description: "Precedence of include/exclude in deno.json, un-excluding with negated globs, top-level exclude, overriding .gitignore for publish, and the exports field."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/deno_json.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Many configs (`lint`, `fmt`, ...) take `include` and `exclude`. `exclude` has higher precedence and wins when a path matches both. In Deno 1.41.2+, un-exclude a path with a negated glob after the general exclude:

```jsonc
{
  "fmt": {
    "exclude": [
      "fixtures",
      "!fixtures/scripts"
    ]
  }
}
```

A top-level `exclude` applies to all subcommands and the LSP; un-exclude per command:

```jsonc
{
  "fmt": { "exclude": ["!dist"] },
  "exclude": ["dist/"]
}
```

`deno publish` honours `.gitignore`. Opt out with a negated exclude, or list paths in `include`:

```jsonc title="deno.json"
{
  "publish": {
    "exclude": ["!dist/"]
  }
}
```

`exports` defines the public paths of your package:

```json title="deno.json"
{
  "exports": {
    "./module1": "./src/module1.ts",
    "./module2": "./src/module2.ts",
    ".": "./src/mod.ts"
  }
}
```

A string value (`"exports": "./src/mod.ts"`) sets just the default entry point. Other files stay private.

## Checked

2026-11-04. Confirmed against the Deno configuration file (deno.json) reference: exclude precedence, negated globs from Deno 1.41.2, top-level exclude, publish and .gitignore override, `exports` forms. Nothing removed.

Method: documentation only; no commands were run.
