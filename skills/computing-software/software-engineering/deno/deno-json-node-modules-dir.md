---
id: computing-software.software-engineering.deno.deno-json-node-modules-dir
name: deno-json-node-modules-dir
category: computing-software
field: software-engineering
product: deno
tags: [deno-json, node-modules, nodemodulesdir, jsr-deps, package-json, workspaces]
level: practitioner
status: docs-checked
description: "Choosing nodeModulesDir none, auto or manual, its package.json-dependent defaults, workspace-root rule, and jsrDepsInNodeModules."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/deno_json.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```json title="deno.json"
{
  "nodeModulesDir": "auto"
}
```

| Value | Behaviour |
| --- | --- |
| `"none"` | No local `node_modules`; use the global cache in `$DENO_DIR`, kept up to date by Deno. |
| `"auto"` | Local `node_modules`, created and kept up to date by Deno. |
| `"manual"` | Local `node_modules`; you keep it current, e.g. with `deno install` or `npm install`. |

Defaults when unset: `"none"` if there is no `package.json` in the project directory, `"manual"` if there is.

In workspaces the setting works only in the workspace root; specifying it in members gives warnings. `"manual"` is applied automatically only if there is a `package.json` in the workspace root.

`jsrDepsInNodeModules` (off by default) installs `jsr:` dependencies via JSR's npm compatibility registry when a `node_modules` directory is in use. `jsr:@david/dax` becomes `npm:@jsr/david__dax`, served from `https://npm.jsr.io`:

```jsonc title="deno.json"
{
  "jsrDepsInNodeModules": true
}
```

## Checked

2026-11-04. Confirmed against the Deno configuration file (deno.json) reference: the three `nodeModulesDir` values, the package.json-dependent defaults, the workspace-root rule, `jsrDepsInNodeModules` and its npm rewrite. Nothing removed.

Method: documentation only; no commands were run.
