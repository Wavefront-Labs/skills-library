---
id: computing-software.devops-ci-cd.nx.nx-input-types
name: nx-input-types
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, caching, inputs, hashing, fileset, env, runtime, externaldependencies]
level: practitioner
status: docs-checked
description: "Reference of Nx task inputs forms that feed the cache hash: fileset globs, json fields, env, runtime, workingDirectory, externalDependencies and dependentTasksOutputFiles."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/inputs.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right `inputs` entry so the cache is invalidated exactly when it should be.

Nx always also hashes project configuration and command arguments (Nx-only flags such as `--parallel`, `--projects` are filtered out; `nx build app --prod` does not reuse `nx build app`).

Entry forms in a target's `inputs`:

- Source files: `"{projectRoot}/**/*.ts"`, `"!{projectRoot}/**/*.spec.ts"` (exclude), `"{workspaceRoot}/.gitignore"`. Globs must start with `{projectRoot}` or `{workspaceRoot}`; `{projectRoot}`/`{projectName}` may appear later. Object form: `{ "fileset": "..." }`. Use `/` on every OS; `\\` escapes glob characters (`{projectRoot}/app/\\(marketing\\)/**/*`). A path with no glob names that file, or that directory and everything under it.
- Dependencies: `^` prefix or `"dependencies": true`: `"^{projectRoot}/**/*.ts"`.
- JSON: `{ "json": "{projectRoot}/package.json", "fields": ["dependencies"] }` or `"excludeFields": ["compilerOptions.paths"]` (dot notation; `fields` applies first). Hashes parsed contents, so key order and formatting are irrelevant.
- Env: `{ "env": "API_KEY" }`.
- Runtime: `{ "runtime": "node --version" }`; avoid `.sh`/`.bat` for cross-platform.
- Working dir: `{ "workingDirectory": "relative" }` (path from workspace root) or `"absolute"` (also changes if the repo is cloned elsewhere).
- External deps: `{ "externalDependencies": ["eslint", "eslint-config-airbnb"] }`. Default when none listed: all workspace external dependencies are hashed (safe but over-invalidates, e.g. `eslint .`).
- Outputs of dependent tasks: `{ "dependentTasksOutputFiles": "**/*.d.ts", "transitive": true }`; globs match workspace-root-relative output paths.

Nested projects: `{projectRoot}/**/*` excludes files of nested projects; `{workspaceRoot}/packages/parent/**/*` includes them. Default behaviour with no `inputs`: all project files plus dependencies' files. Files in `.gitignore` are excluded (see nx-gitignored-inputs).

See nx-named-inputs for reuse.

## Checked

2026-11-07. Confirmed: every inputs form, the hashed project configuration and command arguments, the glob escape rules, external dependency default and dependentTasksOutputFiles against the Inputs reference. Removed: an invented Verify step. Thin: a single reference page; no other findings.

Method: documentation only; no commands were run.
