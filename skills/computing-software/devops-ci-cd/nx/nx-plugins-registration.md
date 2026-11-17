---
id: computing-software.devops-ci-cd.nx.nx-plugins-registration
name: nx-plugins-registration
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, monorepo, plugins, nx-add, include, exclude, plugin-order]
level: practitioner
status: docs-checked
description: "Register Nx plugins in nx.json: nx add, options, ordering and merge rules, include/exclude globs with negation, pluginsConfig."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/nx-json.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/nx-plugins.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add a plugin so Nx infers tasks from tool config, and scope it to the right projects.

Add: `nx add @nx/vite` installs the version matching your Nx (for `@nx/*`) and registers it in `nx.json`:
```json
{ "plugins": [
  "@my-org/graph-plugin",
  { "plugin": "@nx/vite/plugin",
    "options": { "buildTargetName": "build", "devTargetName": "dev", "previewTargetName": "preview" } } ] }
```
A plugin with no options may be a plain string. `options` mostly set the names of inferred tasks. Plugins can also add projects/dependencies to the graph (e.g. `@nx/gradle`).

Order: plugins are processed in array order; if several create the same task name (e.g. `build` from Vite and webpack), the one listed last wins. Compatible targets (same executor and command) merge property by property with later values winning; incompatible ones are replaced entirely.

Scope with `include` / `exclude` globs, matched against the config file the plugin reads (e.g. `jest.config.ts`):
```jsonc
{ "plugin": "@nx/jest/plugin",
  "include": ["packages/**/*"],
  "exclude": ["**/*-e2e/**/*", "!**/toolkit-workspace-e2e/**/*"] }
```
Patterns are processed in order and the last matching one decides; `!` removes from the match set, a non-`!` pattern adds; if the first pattern is a negation, all files match initially.

Workspace-wide plugin options live in `pluginsConfig`, keyed by package: `"pluginsConfig": { "@nx/js": { "projectsAffectedByDependencyUpdates": "auto" } }` (nx-affected-explain-legacy).

To see a project's tasks and which plugin or file set each value: `nx show project <name> --web`.

## Checked

2026-11-07. Confirmed: nx add, plugin registration shape, plugin order and merge rules, include/exclude with negation and pluginsConfig against nx.json reference and Nx plugins pages. Removed: an invented Verify step (replaced by the page's nx show project statement) and loosened the negation wording to the page's last-match rule.

Method: documentation only; no commands were run.
