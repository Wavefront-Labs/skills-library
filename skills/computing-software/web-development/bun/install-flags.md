---
id: computing-software.web-development.bun.install-flags
name: install-flags
category: computing-software
field: web-development
product: bun
tags: [bun-install, production, dry-run, omit, backend, offline]
level: practitioner
status: docs-checked
description: "Choose the right bun install flags: production, omit, dry-run, offline, prefer-offline, force, no-cache, backend and concurrent-scripts, with their gotchas."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/install.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Common flags:

```bash
bun install --production            # skips devDependencies, implies --frozen-lockfile
bun install --omit dev --omit peer  # repeatable: dev, peer, optional
bun install --dry-run               # resolve only; no lockfile, scripts or package.json changes
bun install --offline               # no network; an uncached required dependency is an error
bun install --prefer-offline        # use cached metadata of any age
bun install --force                 # refetch registry metadata
bun install --no-cache              # skip manifest cache for one run
bun install --backend symlink       # hardlink|clonefile|clonefile_each_dir|copyfile|symlink
bun install --concurrent-scripts 8
```

Gotchas:
- `--production` does not remove devDependencies already in `node_modules`; run `bun prune --production`.
- Manifests are cached for 5 minutes. `bun update <pkg>` moves a locked package; `--force` does not.
- With `--backend symlink`, Node.js does not resolve dependencies' node_modules unless each dependency has its own node_modules folder or you pass `--preserve-symlinks`.
- `--concurrent-scripts` defaults to twice the CPU count.
- `--production=true` is an error for `bun update`.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/install.mdx: --production, --omit, --dry-run, --offline, --prefer-offline, --force, --no-cache, backend names, concurrent-scripts default, 5-minute manifest cache, bun update behaviour. Removed a Verify line; tightened offline and symlink wording.

Method: documentation only; no commands were run.
