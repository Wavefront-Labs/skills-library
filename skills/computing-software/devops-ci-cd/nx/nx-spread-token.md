---
id: computing-software.devops-ci-cd.nx.nx-spread-token
name: nx-spread-token
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, monorepo, spread-token, project-configuration, merge, inputs]
level: advanced
status: docs-checked
description: 'Use the Nx "..." spread token to extend inferred or default target config instead of replacing it: arrays, objects, supported levels, limits.'
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/project-configuration.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/nx-json.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add to a value from a lower-priority source (plugin inference, `targetDefaults`) without overwriting it.

By default each source overwrites the previous one per property. The spread token changes that.

Arrays: `"..."` is replaced by the base items at that position.
```json
"build": { "inputs": ["my-project-input", "..."] }
```
Base `["default", "^production"]` gives `["my-project-input", "default", "^production"]`. In `nx.json`, `"inputs": ["...", "{workspaceRoot}/babel.config.json"]` appends.

Objects: key `"..."` set to `true` spreads base properties at that position; keys after it override base values, keys before it can be overridden by base.
```json
"options": { "...": true, "assetsDir": "static/assets" }
```

Levels where it is resolved: target root; `inputs`, `outputs`, `dependsOn`, `syncGenerators`; `options`; `options[x]`; `configurations`; `configurations[x]`; `configurations[x][y]`; `ultracache`; `ultracache.ignoreReads` and `ignoreWrites`. Examples: `"configurations": { "prod": { "...": true, "sourceMap": false } }`, `"ultracache": { "...": true, "mode": "off" }`, `"readyWhen": { "...": true, "timeout": 1200000 }`.

Gotchas:
- Anything deeper than `options[x]` / `configurations[x][y]` is opaque: `options.webpack.plugins = { "...": true }` is ignored, while `options.webpack = { "...": true }` works.
- `tags` and `implicitDependencies` always merge across sources; the token is neither needed nor supported there.
- Same behaviour in `nx.json` target defaults as in `project.json`.

## Checked

2026-11-07. Confirmed against the Spread token section of the project configuration reference and the target defaults section of the nx.json reference: the "..." token merging inherited values, where spread is resolved, and the override rule for keys written after it. Removed: the invented Verify step.

Method: documentation only; no commands were run.
