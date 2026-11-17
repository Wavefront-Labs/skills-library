---
id: computing-software.software-engineering.pnpm.how-peers-are-resolved
name: how-peers-are-resolved
category: computing-software
field: software-engineering
product: pnpm
tags: [peer-dependencies, peer-resolution, peer-variants, duplicate-package-copies, lockfile-peer-keys]
level: advanced
status: docs-checked
description: "Understand how pnpm resolves peer dependencies from higher in the graph, why a package is hard-linked once per peer set, and how variants appear in node_modules/.pnpm."
sources:
  - https://pnpm.io/how-peers-are-resolved
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In one project a package version normally has exactly one set of dependencies. The exception is a package with peer dependencies: peers come from dependencies installed higher in the graph, so `foo@1.0.0` with peers `bar` and `baz` can end up with different sets when two parents provide different `baz` versions.

pnpm then hard-links `foo@1.0.0` once per distinct set:

```text
node_modules/.pnpm/foo@1.0.0_bar@1.0.0_baz@1.0.0/node_modules/{foo,bar,baz,...}
node_modules/.pnpm/foo@1.0.0_bar@1.0.0_baz@1.1.0/node_modules/{foo,bar,baz,...}
```

Symlinks target the right copy, so Node's resolver finds the correct peers. Lockfile keys: `foo@1.0.0(bar@1.0.0)(baz@1.0.0)` and `foo@1.0.0(bar@1.0.0)(baz@1.1.0)`.

Transitive case: if `a@1.0.0` depends on `b@1.0.0`, which has peer `c@^1` that `a` does not provide, `b`'s peer resolves from `a`'s parent and `a` itself gets one copy per distinct `c` (`a@1.0.0_c@1.0.0`, `a@1.0.0_c@1.1.0`).

Duplicates caused by peers are expected, not a bug. Settings that change this: `dedupePeers`, `dedupePeerDependents`, `autoInstallPeers` (see `computing-software.software-engineering.pnpm.peer-dependency-settings`).

## Checked

2026-11-04. Confirmed against pnpm.io/how-peers-are-resolved: peer variants per dependency set, directory naming, lockfile key format, transitive a/b/c case, related settings. Removed: the generic closing Check line (pnpm why was not on the page).
Method: documentation only; no commands were run.
