---
id: computing-software.devops-ci-cd.nx.nx-named-inputs
name: nx-named-inputs
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, caching, namedinputs, production, sharedglobals, inputs]
level: practitioner
status: docs-checked
description: "Define and reuse namedInputs (default, production, sharedGlobals) in nx.json or project config and reference them with ^ or projects/dependencies object forms."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/inputs.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: name reusable input sets once and reference them from target `inputs`, like variables.

Define workspace-wide in `nx.json`, or per project in `project.json`/`package.json` (a project-level set with the same name overrides the workspace one for that project). Generated workspaces follow this convention:

```jsonc
{ "namedInputs": {
  "default": ["{projectRoot}/**/*", "sharedGlobals"],
  "production": ["default", "!{projectRoot}/jest.config.ts"],
  "sharedGlobals": []
} }
```

- `default`: everything in the project plus shared globals, so tasks re-run whenever anything relevant changes.
- `sharedGlobals`: things always hashed (OS, Node version).
- `production`: `default` minus files that do not affect end-user behaviour (tests, lint config). Prefer "everything except known exclusions".

Use them in a target. `^` applies a named input to project dependencies:

```jsonc
{ "targets": { "test": { "inputs": ["default", "^production", "{projectRoot}/jest.config.js"] } } }
```
Tests hash all project files plus only production files of dependencies.

Object forms:
- `{ "input": "production", "projects": "mylib" }` or `["mylib", "myapp"]`: that project's named input.
- `"production"` equals `{ "input": "production" }`; `"^production"` equals `{ "input": "production", "dependencies": true }`.
- `{ "input": "production", "projects": "myapp", "dependencies": true }` covers the dependencies of myapp only (not myapp), so pair it with the plain form to include both.

Disambiguation: after `^`, a value starting with `{projectRoot}` or `{workspaceRoot}` is a dependency fileset; anything else is a named input reference.

## Checked

2026-11-07. Confirmed: default, production and sharedGlobals conventions, ^ and projects/dependencies object forms and the ^ disambiguation note against the Inputs reference. Removed: an invented Verify step.

Method: documentation only; no commands were run.
