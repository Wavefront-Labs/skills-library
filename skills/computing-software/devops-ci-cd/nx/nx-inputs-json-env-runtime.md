---
id: computing-software.devops-ci-cd.nx.nx-inputs-json-env-runtime
name: nx-inputs-json-env-runtime
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, monorepo, inputs, env, runtime, workingdirectory, json-inputs]
level: practitioner
status: docs-checked
description: "Nx non-file inputs: json fields/excludeFields, env variables, runtime commands, workingDirectory relative or absolute."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/inputs.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add finer or non-file signals to a target's `inputs`.

JSON subset (edits to other fields no longer invalidate):
```jsonc
{ "json": "{projectRoot}/package.json" }                                   // whole file
{ "json": "{projectRoot}/package.json", "fields": ["dependencies"] }
{ "json": "{workspaceRoot}/tsconfig.base.json", "excludeFields": ["compilerOptions.paths"] }
```
- Path must start with `{workspaceRoot}` or `{projectRoot}`; may be a glob matching several files.
- Dot notation reaches nested values (`compilerOptions.target`); missing fields are skipped. If both are set, `fields` selects first, then `excludeFields` removes.
- The parsed content is hashed, so reformatting or key reordering does not invalidate. Files that are neither JSON nor JSONC fall back to raw hashing and field filters are ignored.

Environment variable: `{ "env": "API_KEY" }` hashes the value of `$API_KEY`.

Runtime command: `{ "runtime": "node --version" }` hashes the command output. It must work on every OS: avoid `.sh` and `.bat` scripts.

Working directory: `{ "workingDirectory": "relative" }` hashes the path from workspace root to cwd; `"absolute"` hashes the full path (invalidates when the repo is cloned to a different location, e.g. CI vs local).

Related automatic behaviour: command arguments are hashed too, except Nx-only flags such as `--parallel` and `--projects`; so `nx build myreactapp --prod` does not reuse `nx build myreactapp`. With a root `tsconfig.json`/`tsconfig.base.json`, Nx hashes `compilerOptions` plus only the path mappings relevant to the project.

## Checked

2026-11-07. Confirmed: json fields and excludeFields, env, runtime and workingDirectory inputs, and the tsconfig note against the Inputs reference. Removed: an invented Verify step.

Method: documentation only; no commands were run.
