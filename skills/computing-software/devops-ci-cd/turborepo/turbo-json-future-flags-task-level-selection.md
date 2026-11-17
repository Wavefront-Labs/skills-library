---
id: computing-software.devops-ci-cd.turborepo.turbo-json-future-flags-task-level-selection
name: turbo-json-future-flags-task-level-selection
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, futureflags, affectedusingtaskinputs, watchusingtaskinputs, filterusingtasks, stricttaskentrypointselection, task-level-inputs]
level: advanced
status: docs-checked
description: "Future flags that move --affected, turbo watch and --filter from package-level to task-level using inputs, plus strict task entrypoint selection."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`futureFlags` enables experimental behaviour that becomes default in future versions. **Root `turbo.json` only** (an error is thrown in Package Configurations), and flags that change behaviour can invalidate the task cache.

- **`affectedUsingTaskInputs`** (default `false`): `--affected` selects tasks whose declared `inputs` match changed files (task level) rather than all tasks in a changed package (package level). With `build` inputs `["$TURBO_DEFAULT$", "!README.md"]`, a README-only change does not run `build`. It also makes `turbo query`'s `affectedPackages` return packages that own affected tasks, and makes `turbo prune` retain packages needed by retained packages' tasks, following explicit `package#task` dependencies across toolchains.
- **`watchUsingTaskInputs`**: the same task-level behaviour for `turbo watch`: editing `README.md` does not re-run `build`, but editing `src/index.ts` does.
- **`filterUsingTasks`**: resolve `--filter` at the task level; git-range filters match changed files against `inputs`, and `...` traverses the Task Graph, for example `web#build -> schema#gen`.
- **`strictTaskEntrypointSelection`**: when at least one package can run a requested task, packages without a command are not entrypoints and their dependencies are not included merely because the task was requested. With `web` having `test` and `docs` not, `turbo run test` starts at `web#test` only. Missing tasks reached from retained tasks stay in the graph to preserve Transit Nodes and cache invalidation. Independent of `filterUsingTasks`.

For the first three: changes to `package.json`, `turbo.json`, `turbo.jsonc`, the lockfile or `globalDependencies` always select or re-run all tasks.

## Checked

2026-11-04. Read the `futureFlags` section of the configuration reference for `affectedUsingTaskInputs`, `watchUsingTaskInputs`, `filterUsingTasks` and `strictTaskEntrypointSelection` in full; defaults, examples and the root-config-files callout match. Removed the invented Verify step.

Method: documentation only; no commands were run.
