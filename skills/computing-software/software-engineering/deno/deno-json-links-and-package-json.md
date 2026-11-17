---
id: computing-software.software-engineering.deno.deno-json-links-and-package-json
name: deno-json-links-and-package-json
category: computing-software
field: software-engineering
product: deno
tags: [deno-json, links, local-override, prefer-package-json, globs, dependencies]
level: advanced
status: docs-checked
description: "Override dependencies with local packages via the links field (like npm link, with globs) and route deno add/install/remove to package.json with preferPackageJson."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/deno_json.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`links` in deno.json replaces dependencies with local packages on disk, similar to `npm link`:

```json title="deno.json"
{
  "links": [
    "../some-package"
  ]
}
```

It helps with dependency bug fixes, private local libraries and compatibility issues. The linked package need not be published; it just needs the right package name and metadata in its `deno.json` or `package.json`.

Entries can be globs (relative paths or `file://` URLs), and a `!` prefix excludes matches:

```json title="deno.json"
{
  "links": [
    "../packages/*",
    "!../packages/internal-only"
  ]
}
```

`preferPackageJson` makes dependency commands write to `package.json` instead:

```jsonc title="deno.json"
{
  "preferPackageJson": true
}
```

`deno add`, `deno install <pkg>` and `deno remove` then target `package.json`, creating one if absent. It is equivalent to passing `--package-json` every time. Deno warns when `imports` or `scopes` remain in deno.json, since those dependencies should move to `package.json`.

## Checked

2026-11-04. Confirmed against the Deno configuration file (deno.json) reference: `links` purpose and example, globs with `file://` URLs and `!` exclusion, `preferPackageJson` behaviour. Nothing removed.

Method: documentation only; no commands were run.
