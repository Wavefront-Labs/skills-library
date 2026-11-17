---
id: computing-software.devops-ci-cd.nx.nx-gitignored-inputs
name: nx-gitignored-inputs
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, caching, inputs, includeignored, ultracache, continuous-tasks, e2e]
level: advanced
status: docs-checked
description: "Hash gitignored or generated files with includeIgnored, plus inputs:false on dependsOn and always:true for Ultracache, in Nx task inputs."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/inputs.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make generated or gitignored files affect the cache key, and control how e2e/server tasks hash.

By default filesets only see files not excluded by `.gitignore` and `.nxignore`. Add `includeIgnored: true` to match files on disk:

```jsonc
{ "inputs": [
  { "fileset": "{projectRoot}/generated/**/*.json", "includeIgnored": true },
  { "fileset": "!{projectRoot}/generated/**/*.local.json", "includeIgnored": true },
  { "fileset": "{workspaceRoot}/openapi.generated.json", "includeIgnored": true }
] }
```
Rules: globs must start with `{projectRoot}` or `{workspaceRoot}`; keep them narrow (matches are checked every run; `{workspaceRoot}/**` is allowed but covers every ignored file); a path may name a file that does not exist yet (key changes when it appears); `{projectRoot}` globs do not enter nested projects. A `!` negation with `includeIgnored` filters the other `includeIgnored` globs resolved with it (with `dependencies: true`, those carrying that flag); a negation with nothing to filter is a configuration error. Globs never walk `node_modules`, `.git`, `.nx/cache`, `.nx/workspace-data`, `.yarn/cache`, and `..` or absolute paths are errors.

Continuous dependencies: a task also hashes the declared inputs of every continuous dependency (e.g. the `serve` an `e2e` depends on). To depend on the server without hashing it, use `"inputs": false` on the `dependsOn` entry:

```jsonc
{ "targets": { "e2e": { "dependsOn": [{ "projects": "myapp", "target": "serve", "inputs": false }] } } }
```

Ultracache (CI): a task hashes from files it read on a recorded run, replacing declared filesets. Keep specific inputs with `"always": true`, e.g. `{ "input": "production", "projects": ["checkout"], "always": true }` (accepted on `fileset`, `json`, `input` forms). With `always`, a `projects` pattern matching nothing is an error. Opt out with `NX_CLOUD_USE_ULTRACACHE=false` or a target's `ultracache.mode: "warn"`.

## Checked

2026-11-07. Confirmed: includeIgnored rules, negation scoping, walk exclusions, inputs: false on dependsOn and always: true under Ultracache against the Inputs reference. Removed: an invented Verify step.

Method: documentation only; no commands were run.
