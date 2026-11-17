---
id: computing-software.software-engineering.deno.deno-json-fmt-options
name: deno-json-fmt-options
category: computing-software
field: software-engineering
product: deno
tags: [deno-json, fmt, formatter, indent-width, line-width, trailing-commas]
level: practitioner
status: docs-checked
description: "Configuring the deno fmt formatter in deno.json: include/exclude, key options with defaults, and the separate json.trailingCommas setting."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/deno_json.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `fmt` field configures `deno fmt`:

```json title="deno.json"
{
  "fmt": {
    "useTabs": true,
    "lineWidth": 80,
    "indentWidth": 4,
    "semiColons": true,
    "singleQuote": true,
    "proseWrap": "preserve",
    "include": ["src/"],
    "exclude": ["src/testdata/", "src/fixtures/**/*.ts"]
  }
}
```

Defaults and values for some options:

| Option | Default | Values |
| --- | --- | --- |
| `indentWidth` | `2` | a number |
| `lineWidth` | `80` | a number |
| `proseWrap` | `always` | `always`, `never`, `preserve` |
| `semiColons` | `true` | `true`, `false` |
| `singleQuote` | `false` | `true`, `false` |
| `trailingCommas` | `always` | `always`, `never` |
| `useTabs` | `false` | `true`, `false` |
| `newLineKind` | `lf` | `auto`, `crlf`, `lf`, `system` |
| `quoteProps` | `asNeeded` | `asNeeded`, `consistent`, `preserve` |

Others include `bracePosition`, `nextControlFlowPosition`, `operatorPosition`, `singleBodyPosition`, `sortNamedExports`, `sortNamedImports`, `spaceAround`, `useBraces`, `jsx.*` options and `typeLiteral.separatorKind`.

`json.trailingCommas` (default `never`; also `always`, `maintain`, `jsonc`) controls JSON and JSONC separately from `trailingCommas`, which applies to JS and TS. `jsonc` adds trailing commas in `.jsonc` files only.

## Checked

2026-11-04. Confirmed against the Deno configuration file (deno.json) reference: the example fmt block, the defaults and possible values table, the other option names, and the `json.trailingCommas` note. Nothing removed.

Method: documentation only; no commands were run.
