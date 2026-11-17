---
id: computing-software.devops-ci-cd.nx.nx-inputs-includeignored
name: nx-inputs-includeignored
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, monorepo, inputs, includeignored, gitignore, generated-files]
level: advanced
status: docs-checked
description: "Hash gitignored or generated files in Nx task inputs with includeIgnored: fileset syntax, negation scoping, nested projects, walk limits."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/inputs.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make a generated or gitignored file (downloaded schema, generated client) invalidate the cache.

A normal fileset only sees files that `.gitignore` and `.nxignore` allow. Add `includeIgnored: true` to match files on disk regardless:
```jsonc
"inputs": [
  { "fileset": "{projectRoot}/generated/**/*.json", "includeIgnored": true },
  { "fileset": "!{projectRoot}/generated/**/*.local.json", "includeIgnored": true },
  { "fileset": "{workspaceRoot}/openapi.generated.json", "includeIgnored": true }
]
```
Rules:
- Every glob must start with `{projectRoot}` or `{workspaceRoot}`.
- Nx re-checks matches every run, so keep globs narrow. `{workspaceRoot}/**` is allowed but hashes every gitignored file in the workspace.
- A new matching file counts without config changes; a path may name a file that does not exist yet (key changes when it appears or disappears).
- Like `{projectRoot}`, globs do not enter nested projects: `{projectRoot}/**/*` on `packages/app` skips `packages/app/plugin`; `{projectRoot}/plugin/dist/**` or `{workspaceRoot}/dist/**` reach them.
- A `!` negation with `includeIgnored: true` filters every `includeIgnored` glob resolved with it. With `dependencies: true`, the flagged globs apply together to each dependency, through the whole dependency chain. A negation with nothing to filter is a configuration error.
- Globs never walk into `node_modules`, `.git`, `.nx/cache`, `.nx/workspace-data` or `.yarn/cache` unless they name a path inside; Vite/Vitest `*.timestamp-*.mjs` files are skipped. Symlinked files are read where they point; symlinked directories are not walked unless named. A glob using `..` or an absolute path is an error.
- Ultracache (nx-ultracache-target-config) replaces declared filesets, `includeIgnored` ones included, with the files read; add `"always": true` to keep an input.

## Checked

2026-11-07. Confirmed: includeIgnored syntax, narrow-glob advice, nested projects, negation scoping, walk exclusions, symlinks and Ultracache behaviour against the Inputs reference. Removed: an invented Verify step.

Method: documentation only; no commands were run.
