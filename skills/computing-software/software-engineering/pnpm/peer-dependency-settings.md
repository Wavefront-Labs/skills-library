---
id: computing-software.software-engineering.pnpm.peer-dependency-settings
name: peer-dependency-settings
category: computing-software
field: software-engineering
product: pnpm
tags: [auto-install-peers, auto-install-peers-from-highest-match, dedupe-peer-dependents, dedupe-peers, add-missing-peer-types, strict-peer-dependencies, resolve-peers-from-workspace-root, peer-dependency-rules]
level: practitioner
status: docs-checked
description: "Tune pnpm peer resolution: autoInstallPeers, highest-match conflicts, dedupePeerDependents, dedupePeers, addMissingPeerTypes, strictPeerDependencies, peerDependencyRules."
sources:
  - https://pnpm.io/settings/peer-dependencies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Settings in `pnpm-workspace.yaml`:

- `autoInstallPeers` (default true): missing non-optional peers are installed at the highest version satisfying the range. Conflicting ranges (`react@^16` vs `^17`) install nothing and print a warning. A missing optional peer is installed only if the workspace already has a satisfying version, even from another project's `devDependencies`.
- `autoInstallPeersFromHighestMatch` (false): join conflicting ranges with `||` and install the highest match.
- `dedupePeerDependents` (true): projects share one instance of a package when their peer sets do not conflict (for example one project lacks an optional peer that the other has).
- `dedupePeers` (false): suffixes use `name@version` instead of full dep paths, removing nested suffixes like `(foo@1.0.0(bar@2.0.0))`.
- `addMissingPeerTypes` (false, v12.12.0): each peer also makes the matching `@types` package an optional peer. Changes the lockfile.
- `strictPeerDependencies` (false): fail on a missing or invalid peer.
- `resolvePeersFromWorkspaceRoot` (true): root dependencies resolve peers of every project.

`peerDependencyRules` (`ignoreMissing`, `allowedVersions`, `allowAny`) is deprecated and only silences warnings. To change the declared range use `overrides` with `:peer`, e.g. `"button@2>react:peer": "16 || 17"`.

Related: `computing-software.software-engineering.pnpm.how-peers-are-resolved`.

## Checked

2026-11-04. Confirmed defaults, conflict and optional-peer behaviour, dedupe semantics, the v12.12.0 gate on addMissingPeerTypes and the peerDependencyRules deprecation against pnpm.io/settings/peer-dependencies. Swapped the :peer override example for the page's own. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
