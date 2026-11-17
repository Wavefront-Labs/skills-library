---
id: computing-software.devops-ci-cd.nx.nx-run-tasks-cli
name: nx-run-tasks-cli
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, monorepo, run-many, affected, root-level-tasks, task-graph]
level: intro
status: docs-checked
description: "Run Nx tasks: single project, run-many with -t and -p, affected, root-level tasks with nx exec, and how the task graph decides parallelism."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/run-tasks.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/getting-started/how-nx-works.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/nx-json.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/cache-task-results.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right Nx command to run tasks and predict what runs in parallel.

Commands:
- One task: `npx nx test header` (target `test`, project `header`).
- Many projects: `npx nx run-many -t build lint test` (all projects); restrict with `-p header footer`.
- Parallel limit: `nx run-many -t test --parallel=5` (or `parallel` in `nx.json`).
- Only what a PR touches: `npx nx affected -t test` (see nx-affected-ci-base).

Task graph: each run builds a graph whose nodes are tasks like `myapp:build`. It comes from the project graph plus your `dependsOn` pipeline, not a mirror of it. `nx run-many -t test -p app1 app2 lib` yields three unconnected nodes, so all three run in parallel even though apps depend on `lib`; edges appear only when `dependsOn` adds them (nx-task-pipeline-dependson). `nx build web` includes only `web` and its dependency builds; `run-many -t build` adds every project. Different targets run concurrently when independent.

Task sources, lowest to highest precedence: plugin-inferred, `targetDefaults` in `nx.json`, project `package.json`/`project.json`. A `package.json` script becomes a task automatically.

Root-level tasks (to get caching for repo-wide scripts): in root `package.json` add `"nx": {}` plus the script, or in root `project.json` add a target with `"command"`. Then `npx nx docs`. To keep calling `npm run docs`, write the script as `nx exec -- node ./generateDocsSite.js`.

Gotchas:
- Commands that create the same task and args share a cache entry: `nx build myapp` and `nx run-many -t build -p myapp`; adding `--sourcemap` does not.
- In Nx 21, task output is shown in an interactive terminal UI.

To list every task Nx detected for a project and where each setting came from, run `nx show project my-project`.

## Checked

2026-11-07. Confirmed against Run Tasks and How Nx works: single task, run-many with -t and -p, affected, task graph behaviour (three unconnected nodes, dependsOn edges, independent tasks run concurrently), the three-source precedence order, root-level tasks (nx: {}, project.json command, nx exec), the Nx 21 terminal UI, and nx show project. The --parallel flag and nx.json parallel setting are confirmed on the nx.json reference, and the shared cache entry rule with --sourcemap on Cache Task Results, both added to sources. Removed: the wording "Nx 21+" (the page says Nx 21).

Method: documentation only; no commands were run.
