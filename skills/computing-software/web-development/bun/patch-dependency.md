---
id: computing-software.web-development.bun.patch-dependency
name: patch-dependency
category: computing-software
field: web-development
product: bun
tags: [bun-patch, patched-dependencies, patch-commit]
level: advanced
status: docs-checked
description: "Patch a third-party package in place with bun patch and bun patch --commit, store patch files, remove a patch, and avoid corrupting the global cache."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/patch.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
bun patch react                   # prepare (or react@17.0.2, or node_modules/react)
# edit files in node_modules/react, then:
bun patch --commit react          # writes patches/, updates package.json and lockfile
bun patch --commit react --patches-dir=mypatches
bun patch --commit react --dry-run
```

`bun patch-commit <pkg>` is a pnpm-compatible alias for `--commit`.

Remove a patch: revert your edits in `node_modules/react` and run `bun patch --commit react`, or delete the `patchedDependencies` entry and the patch file, then `bun install`.

Gotchas:
- Always run `bun patch <pkg>` before editing; otherwise you may modify Bun's global cache because `node_modules` can link to it.
- Only the root `package.json` is read for `patchedDependencies`; a workspace declaring it triggers a warning.
- If the commit cannot apply (or a security scanner refuses the install), your edits, `package.json` and lockfile stay unchanged.
- If a listed patch file is missing, `bun install` fails; fix with `bun patch --commit <pkg>` while the package is still patched in `node_modules`, or delete the entry.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/patch.mdx: bun patch forms, --commit, --patches-dir, --dry-run, patch-commit alias, removal steps, root-only patchedDependencies, global-cache warning, failed-commit and missing-patch-file behaviour.

Method: documentation only; no commands were run.
