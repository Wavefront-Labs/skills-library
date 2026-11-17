---
id: computing-software.devops-ci-cd.nx.nx-convert-to-inferred
name: nx-convert-to-inferred
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, inferred-tasks, convert-to-inferred, infer-targets, plugins, targetdefaults, atomizer]
level: advanced
status: docs-checked
description: "Migrate executor-based project.json targets to inferred tasks with infer-targets and convert-to-inferred generators; centralisation into targetDefaults and its skip conditions."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/kb/convert-to-inferred.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replace explicit executors with plugin-inferred tasks to cut `project.json` config, get cache settings inferred from tool config, and enable the Atomizer.

Steps:
1. `npx nx migrate latest` first (recommended).
2. All plugins at once: `npx nx g infer-targets` (detects every `convert-to-inferred` generator, runs the ones you choose; add `--project` to try one project).
3. One plugin: `nx g convert-to-inferred` and pick, or `nx g @nx/vite:convert-to-inferred --project demo`. Third-party plugins: choose "None of the above" and type the package, or use `nx g <plugin>:convert-to-inferred`. Official generators exist for e.g. `@nx/eslint`, `@nx/playwright`, `@nx/vite`.

What the generator does: registers the plugin in `nx.json` `plugins` (e.g. `"plugin": "@nx/vite/plugin"` with options like `buildTargetName`, `serveTargetName`; rename to change command names, `"serveTargetName": "dev"` gives `nx dev demo`), moves executor options into tool config files where applicable, trims `project.json` to deviations only, and removes executor uses (`@nx/vite:build`, `dev-server`, `preview-server`, `test`). Target and configuration names are kept. Targets now call the tool CLI directly (`vite build`), so tool flags pass through: `nx serve demo --cors --port 8888`. Vite keeps `options` such as `mode` and `configurations` in `project.json`.

Whole-workspace runs (no `--project`) lift identical config into `targetDefaults` scoped by `"filter": { "plugin": "@nx/vite/plugin" }`. Centralisation is skipped, with a warning and full per-project config kept, when: target identity is authored outside the plugin (`executor`/`command` in project.json, a package.json script or `nx.targets`); later plugins are registered after it; it would change which existing targetDefaults apply (exact names beat globs like `build-*`); or verification of equivalence fails. Two targets in one project mapping to the same plugin option: one is converted, rerun for the next (single-project mode errors).

Error `The nx plugin found a project inside <root> but did not infer a "<target>" target`: see the troubleshoot-convert-to-inferred page.

Atomizer plugins: `@nx/cypress`, `@nx/jest`, `@nx/gradle`, `@nx/playwright`; needs Nx Cloud connected and distribution in CI.

Verify: run each migrated target (vite: build/serve/test; playwright: e2e; eslint: lint) and `npx nx show project <name>`.

## Checked

2026-11-07. Confirmed: the migration commands, steps and the Verify the migration section against the Convert to inferred page. Removed: nothing; no claim failed.

Method: documentation only; no commands were run.
