---
id: computing-software.software-engineering.deno.import-map-imports-field
name: import-map-imports-field
category: computing-software
field: software-engineering
product: deno
tags: [import-map, imports, bare-specifiers, path-mapping, scopes, trailing-slash]
level: practitioner
status: docs-checked
description: "Using the deno.json imports field to map bare specifiers, files and directories, scopes for per-path versions, and the trailing-slash difference from --import-map."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/deno_json.md
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/modules.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `imports` field maps bare specifiers to URLs or paths:

```json title="deno.json"
{
  "imports": {
    "@std/assert": "jsr:@std/assert@^1.0.0",
    "chalk": "npm:chalk@5"
  }
}
```

A `"dependencies"` field in `package.json` also works, but requires running `deno install`.

Custom path mappings: an exact key maps to a file, a key ending in `/` maps to a directory.

```jsonc title="deno.jsonc"
{
  "imports": {
    // Map to an exact file
    "foo": "./some/long/path/foo.ts",
    // Map to a directory, usage: "bar/file.ts"
    "bar/": "./some/folder/bar/"
  }
}
```

`"@/": "./"` makes `import { MyUtil } from "@/util.ts"` resolve relative to the import map.

`scopes` override mappings for modules under a path prefix, e.g. two dependencies needing different versions:

```json title="deno.json"
{
  "scopes": {
    "./legacy/": {
      "@std/assert": "jsr:@std/assert@^0.224.0"
    }
  }
}
```

Standard import maps (`--import-map` or the `importMap` field) need both `"@std/async"` and `"@std/async/": "jsr:/@std/async@^1.0.0/"` entries. The `imports` field in deno.json extends the standard: only the specifier without the trailing `/` is needed.

## Checked

2026-11-04: confirmed against the Deno docs Configuration file page (Dependencies, Custom path mappings, Scoped mappings) and the Modules page (imports versus --import-map trailing-slash section): imports mapping, package.json dependencies needing deno install, path mappings, @/ example, scopes example, trailing slash requirement.

Method: documentation only; no commands were run.
