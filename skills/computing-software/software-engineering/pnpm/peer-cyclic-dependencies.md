---
id: computing-software.software-engineering.pnpm.peer-cyclic-dependencies
name: peer-cyclic-dependencies
category: computing-software
field: software-engineering
product: pnpm
tags: [cyclic-dependencies, cycle-cutting, deterministic-lockfile, peer-cycles, package-id-order]
level: sme
status: docs-checked
description: "pnpm v12 cuts dependency cycles at a fixed place ordered by package ID so peer resolution inside cycles is path-independent and the lockfile is byte-identical across installs."
sources:
  - https://pnpm.io/how-peers-are-resolved
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
pnpm v12 only (from v12.0.0-rc.5).

Problem: when package `a` depends on `b` and `b` depends back on `a`, and a package inside the cycle has peer dependencies, there is no single point higher in the graph to resolve them from, because entering the cycle at `a` or at `b` gives different parents.

Behaviour: pnpm orders the packages forming a cycle by package ID and cuts the closing edges at the same point regardless of where the walk enters. The cut edge is still a real dependency, resolved against an occurrence of its target at project level, but the walk never travels around the cycle. Peers of packages inside a cycle resolve to the nearest match along that order.

Consequences:
- The lockfile is a function of the dependency graph alone: repeated installs, reordered `packages` globs in `pnpm-workspace.yaml` and reordered `package.json` entries give a byte-identical lockfile.
- Cycle-heavy graphs get smaller lockfiles, since a cyclic package no longer gets a peer variant per path.
- Existing lockfiles keep working: `--frozen-lockfile` installs use them unchanged. The first install that re-resolves re-keys the cyclic packages' peer variants once, a one-time lockfile diff.

Not to be confused with workspace project cycles (see `computing-software.software-engineering.pnpm.workspace-setup`).

## Checked

2026-11-04. Confirmed against pnpm.io/how-peers-are-resolved (Cyclic dependencies): v12.0.0-rc.5 scope, fixed-place cycle cutting by package ID, deterministic lockfile, smaller lockfiles, frozen-lockfile compatibility and one-time re-key. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
