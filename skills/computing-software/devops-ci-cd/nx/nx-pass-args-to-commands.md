---
id: computing-software.devops-ci-cd.nx.nx-pass-args-to-commands
name: nx-pass-args-to-commands
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, run-commands, args, targetdefaults, cli, inferred-tasks]
level: practitioner
status: docs-checked
description: "Forward extra arguments to the command behind an Nx task via project.json options, the args option, targetDefaults, or the CLI, and resolve name conflicts and precedence."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/kb/pass-args-to-commands.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give the tool behind an inferred or `nx:run-commands` task extra flags (example: `vite build` with `--assetsInlineLimit=2048 --assetsDir=static/assets`).

1. Per project, in `project.json` target `options`. Either individual options (Nx v18.1.1+) or `args`:

```json
"build": { "options": { "assetsInlineLimit": 2048, "assetsDir": "static/assets" } }
```
```json
"build": { "options": { "args": ["--assetsInlineLimit=2048", "--assetsDir=static/assets"] } }
```
`args` also accepts a single string. Precedence: an arg in `args` overrides an individual option of the same name (`"args": ["--assetsDir=static/assets"]` beats `"assetsDir": "different/path"`).

2. Workspace-wide, same shape under `targetDefaults.build.options` in `nx.json`. Caution: do not do this if same-named targets run different commands or executors; commands that do not expect those options may error.

3. One-off in the terminal:

```shell
nx build my-app --assetsInlineLimit=2048 --assetsDir=static/assets
nx build my-app --args="--assetsInlineLimit=2048 --assetsDir=static/assets"
```

Conflicts: an arg named like an Nx CLI option (`--configuration`) or an `nx:run-commands` option (`--env`) is consumed by Nx or the executor and is not forwarded. Use `--args` for those. You can pass the same name to both: `nx test mobile-e2e --configuration=ci --args="--configuration=ios.sim.release"` runs the `ci` configuration and gives `detox test` its own `--configuration`.

## Checked

2026-11-07. Confirmed: options vs args, precedence, targetDefaults caution, CLI forms and name conflicts against the Pass args to commands page. Removed: an invented Verify step.

Method: documentation only; no commands were run.
