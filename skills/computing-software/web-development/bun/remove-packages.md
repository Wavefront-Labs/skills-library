---
id: computing-software.web-development.bun.remove-packages
name: remove-packages
category: computing-software
field: web-development
product: bun
tags: [bun-remove, uninstall-package, remove-filter]
level: intro
status: docs-checked
description: "Remove dependencies with bun remove (aliases rm, uninstall, r), including removal from every dependency group and from selected workspaces with --filter."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/remove.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
bun remove ts-node
bun rm ts-node            # aliases: rm, uninstall, r
bun remove zod --filter api
bun remove zod --filter '*'
```

Behaviour:
- Removes the package from every dependency group in `package.json` that lists it, and updates `bun.lock`.
- Deletes it from `node_modules` only after no other package depends on it.
- Without `--filter` (`-F`), only the current directory's package is affected.
- `--filter` uses the same patterns as `bun add --filter`; `'*'` removes the package from all workspace packages, and workspaces that do not list it are unchanged.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/remove.mdx: aliases, removal from every dependency group, node_modules deletion once unused, --filter behaviour and shared patterns with bun add. Removed a Verify line the remove page does not state.

Method: documentation only; no commands were run.
