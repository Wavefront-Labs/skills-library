---
id: computing-software.software-engineering.pnpm.production-install
name: production-install
category: computing-software
field: software-engineering
product: pnpm
tags: [production-install, offline-install, commit-lockfile, prefetch-store, no-registry-access]
level: intro
status: docs-checked
description: "Bootstrap a production environment with pnpm: commit the lockfile and run pnpm install, or copy the store and install offline when the registry is unreachable."
sources:
  - https://pnpm.io/production
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two ways to bootstrap a package in production.

1. Recommended: commit the lockfile, then run `pnpm install` in production. The dependency tree is rebuilt from the lockfile, so versions match what was committed.
2. Recommended only where external access to the registry is unavailable: commit the lockfile and also copy the package store to the production machine (the location is set with `storeDir`), then run:

```sh
pnpm install --offline
```

pnpm takes packages from the store and makes no registry requests.

To fill the store before the project source is copied (for example in a container build layer), run `pnpm fetch`. It reads the lockfile, not the package manifests.

Related skills: `computing-software.software-engineering.pnpm.install-frozen-lockfile`, `computing-software.software-engineering.pnpm.docker-build-recipes`.

## Checked

2026-11-04. Confirmed both bootstrap methods, the --offline behaviour and the pnpm fetch note against pnpm.io/production, and storeDir against pnpm.io/settings/store. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
