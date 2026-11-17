---
id: computing-software.systems-network-administration.nix.store-optimise-hardlinks
name: store-optimise-hardlinks
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, store-optimise, hard-links, deduplication, disk-space]
level: intro
status: docs-checked
description: "Shrink the Nix store by hard-linking identical files with nix-store --optimise, with the identity rules, expected savings and progress flags."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-store/optimise.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```
nix-store --optimise
```

It finds identical files in the store and hard-links them together; the manual says this typically shrinks the store by about 25-35%.

Rules:
- Only regular files and symlinks are hard-linked.
- Files are identical when their NAR serialisations match: for regular files, same contents and same executable permission; for symlinks, same target.
- When it finishes or is interrupted it prints a savings report to standard error.
- Add `-vv` or `-vvv` to see progress.

Example output from the manual:

```
541838819 bytes (516.74 MiB) freed by hard-linking 54143 files;
there are 114486 files with equal contents out of 215894 files in total
```

## Checked

2026-11-04: hard-link behaviour, 25-35% typical saving, identity rules, report on standard error, -vv/-vvv and the example output confirmed against the nix-store --optimise manual page. Removed the Verify line (du comparison), which the page does not state.

Method: documentation only; no commands were run.
