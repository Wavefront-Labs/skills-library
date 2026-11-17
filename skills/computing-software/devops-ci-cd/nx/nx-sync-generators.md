---
id: computing-software.devops-ci-cd.nx.nx-sync-generators
name: nx-sync-generators
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, sync-generators, nx-sync, nx-json, ci, typescript-references]
level: practitioner
status: docs-checked
description: "Use Nx sync generators: task vs global, sync.applyChanges, disabledTaskSyncGenerators, globalGenerators, --skip-sync, nx sync and sync:check in CI."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/concepts/sync-generators.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep repo files (tsconfig references, CI scripts, formatting) in sync with the project graph.

Two kinds:
- Task sync generators: attached to a target through `syncGenerators` (like `dependsOn` for generators). Run before that task. Most are inferred by plugins, e.g. `@nx/js/typescript` registers `@nx/js:typescript-sync` on `build` and `typecheck`.
- Global sync generators: registered in `nx.json` under `sync.globalGenerators`; run only on `nx sync` or `nx sync:check`.

Find registered ones: `nx show project <name>` (see Sync Generators per target).

Behaviour:
- Developer machine: generator runs as `--dry-run`; if it would change files you are prompted to apply or skip. Silence the prompt in `nx.json`:
```json
{ "sync": { "applyChanges": true } }
```
`false` means developers must run `nx sync` manually before pushing, or CI fails.
- CI: dry run only; if files would change the task fails with the generator's message. Bypass with `--skip-sync` on the task, or opt a generator out:
```json
{ "sync": { "disabledTaskSyncGenerators": ["@nx/js:typescript-sync"] } }
```

Register your own on a target: `"syncGenerators": ["@my/plugin:my-sync"]` in the target config.

Commands:
```shell
nx sync          # run sync generators
nx sync:check    # use at the start of CI
```
Put `nx sync:check` at the start of CI so it fails fast, and `nx sync` in a pre-commit or pre-push hook.

## Checked

2026-11-07. Confirmed against Sync Generators: task versus global generators, syncGenerators on a target (like dependsOn for generators), nx.json sync.globalGenerators, nx show project for registered generators, @nx/js/typescript registering @nx/js:typescript-sync on build and typecheck, developer-machine dry run with prompt, sync.applyChanges true or false and the caution for false, CI dry run failing the task, --skip-sync, sync.disabledTaskSyncGenerators, and nx sync:check at the start of CI with nx sync in a pre-commit or pre-push hook. Removed: the gotcha about nx affected selection (not on the page), the unstated descriptions in the command comments, and the invented Verify step.

Method: documentation only; no commands were run.
