---
id: computing-software.devops-ci-cd.nx.nx-target-defaults
name: nx-target-defaults
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-json, targetdefaults, filter, spread-token, cache, executors]
level: advanced
status: docs-checked
description: "Configure nx.json targetDefaults: key types, filtered array form, override and priority rules, atomizer globs, the spread token and common cache/inputs/outputs defaults."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/nx-json.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set target configuration once for many projects.

`targetDefaults` is keyed by target name (`test`), a glob over target names (`e2e-ci--*`), or an executor (`@nx/js:tsc`). A value is a plain object, or an ordered array of entries each with an optional `filter`:

```json
{ "targetDefaults": { "test": [
  { "cache": true },
  { "filter": { "plugin": "@nx/vitest" }, "inputs": ["default", "^production"] },
  { "filter": { "projects": ["tag:dotnet"] }, "options": { "configuration": "Release" } }
] } }
```

Filter fields: `plugin` (targets inferred by that plugin), `projects` (names, globs, directories, `tag:foo`, `!foo`), `executor`. Array entries apply in order; later overrides earlier; an unfiltered entry is a catch-all baseline. Any other field is a normal target property (`cache`, `inputs`, `outputs`, `dependsOn`, `options`, `configurations`). Tokens `{workspaceRoot}` and `{projectRoot}` work in values.

Precedence: defaults apply after plugin inference but before `project.json`/`package.json`, and they replace (not merge) inferred values. Both a name key and an executor key can match `build` with `@nx/js:tsc`; only the more specific executor key applies, so put the full config there. `cache` resolves from the applying key too; a name-key `"cache": true` leaves the target uncached when an executor key wins. An executor key hits every target using it, so exclude continuous targets (a target cannot be both cacheable and continuous).

Merging: `inputs` set on a target replaces the default's (`projectJson.inputs || targetDefaults.inputs`). Named inputs from nx.json and project config are merged. Use the spread token to extend instead: in arrays `"inputs": ["...", "{workspaceRoot}/babel.config.json"]`; in objects `"options": { "...": true, "assetsDir": "static/assets" }` (keys after `...` override base).

Atomizer targets (e.g. `e2e-ci--test/my/test.spec.ts`): use `"e2e-ci--**/**"` (names can contain `/`); `e2e-ci-*` only if no slash.

Cautions: do not set `options` on a shared name when same-named targets run different commands. Disabling cache on a target breaks distributed execution for it and its dependents.

## Checked

2026-11-07. Confirmed against the Target defaults section of the nx.json reference and the project configuration reference: targetDefaults keyed by target name, how defaults merge with project-level target configuration, and the spread token for combining. Removed: the invented Verify step.

Method: documentation only; no commands were run.
