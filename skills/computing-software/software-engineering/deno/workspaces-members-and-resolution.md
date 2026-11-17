---
id: computing-software.software-engineering.deno.workspaces-members-and-resolution
name: workspaces-members-and-resolution
category: computing-software
field: software-engineering
product: deno
tags: [workspaces, monorepo, members, patterns, exports, containerization]
level: practitioner
status: docs-checked
description: "Set up a Deno workspace: root workspace array, member name/version/exports, glob and exclusion patterns, resolution rules and Docker copy layout."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/workspaces.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A workspace is a root `deno.json` listing member directories. Members import each other by bare package name and inherit the root `imports`.

```json title="deno.json"
{ "workspace": ["./add", "./subtract"] }
```

```json title="add/deno.json"
{ "name": "@scope/add", "version": "0.1.0", "exports": "./mod.ts" }
```

```ts title="subtract/mod.ts"
import { add } from "@scope/add";
```

Several entry points: `"exports": { ".": "./mod.ts", "./foo": "./foo.ts", "./other": "./dir/other.ts" }`.

Patterns (Deno 2.1+): `some-dir/*` and `other-dir/*/*`; `**` matches recursively; a leading `!` excludes, e.g. `"!packages/internal"`, `"!packages/*/fixtures"`.

Resolution: Deno looks for a parent root deno.json, checks its `workspace` array, matches the package name, then resolves through `exports`. Nested workspaces are not supported.

Docker: copy the root config and every member the app depends on.

```dockerfile
COPY deno.json /app/deno.json
COPY project-a/ /app/project-a/
COPY project-b/ /app/project-b/
```

## Checked

2026-11-04: confirmed against the Deno docs Workspaces and monorepos page: workspace array, member name/version/exports, path patterns (2.1), recursive and exclusion patterns, resolution steps, containerization note, nested workspaces unsupported.

Method: documentation only; no commands were run.
