---
id: computing-software.devops-ci-cd.nx.nx-inputs-filesets
name: nx-inputs-filesets
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, monorepo, inputs, fileset, glob, caching, hashing]
level: practitioner
status: docs-checked
description: "Write Nx file-set inputs: {projectRoot}/{workspaceRoot} globs, ! exclusion, ^ dependency prefix, object form, glob escaping, nested-project behaviour."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/inputs.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control which source files invalidate a task's cache with `inputs`.

```jsonc
"inputs": [
  "{projectRoot}/**/*",            // all project files
  "{workspaceRoot}/.gitignore",    // one workspace file
  "!{projectRoot}/**/*.spec.ts",   // exclude
  "^{projectRoot}/**/*.ts"         // .ts files of dependency projects
]
```
Rules:
- Every glob must start with `{projectRoot}` or `{workspaceRoot}`. `{workspaceRoot}` only at the start; `{projectRoot}` and `{projectName}` may be interpolated later in the path.
- `!` excludes; `^` applies the entry to dependency projects (e.g. `^{workspaceRoot}/tools/**/*` applied per dependency).
- Object form: `{ "fileset": "{projectRoot}/**/*.ts", "dependencies": true }`.
- A path with no glob names that file or the directory and everything under it: `{projectRoot}/src`, `{projectRoot}/src/` and `{projectRoot}/src/**/*` are equivalent.
- Use `/` on every OS. `\` escapes the next character, so write `{projectRoot}/app/\\(marketing\\)/**/*` (JSON needs `\\`). A Windows-style `{projectRoot}\src\**` matches nothing.
- Nested projects: `{projectRoot}/**/*` excludes files owned by nested projects; `{workspaceRoot}/packages/parent/**/*` includes them.
- `^production` (no brace token after `^`) is a named-input reference, not a fileset; see nx-named-inputs.
- Default when unset: all files in the project plus its dependencies. Safe but may rerun more than needed.
- Files in `.gitignore`/`.nxignore` are excluded unless `includeIgnored` is set (nx-inputs-includeignored).

## Checked

2026-11-07. Confirmed: fileset globs, !, ^, object form, directory paths, escaping and nested project tokens against the Inputs reference. Removed: an invented Verify step.

Method: documentation only; no commands were run.
