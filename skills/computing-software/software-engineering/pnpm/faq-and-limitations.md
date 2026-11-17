---
id: computing-software.software-engineering.pnpm.faq-and-limitations
name: faq-and-limitations
category: computing-software
field: software-engineering
product: pnpm
tags: [faq, hard-links-disk-usage, windows-junctions, cross-drive-store, btrfs-reflinks, undeclared-dependency-fix, npm-lockfile-ignored, binstubs-shell-files]
level: practitioner
status: docs-checked
description: "Answer common pnpm questions: hard-link disk usage, Windows junctions, store on another drive, undeclared dependencies missing, ignored npm lockfiles, shell binstubs."
sources:
  - https://pnpm.io/faq
  - https://pnpm.io/limitations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- Disk use: `node_modules` files are hard links to the store, the same bytes addressed twice, so they are counted once on disk.
- Windows: without Developer Mode or admin rights pnpm uses junctions instead of symlinks. Packages are stored flatly, so no deep nesting.
- Store on a different drive or filesystem than the project: packages are copied, not linked. With `storeDir` set, put the store on the project's disk. Without it, pnpm uses `<pnpm home>/store` when it can hardlink there, else `.pnpm-store` at the filesystem mount point, else `<project>/node_modules/.pnpm-store`. Btrfs subvolumes use reflinks.
- A project fails with "Cannot find module": a dependency uses a package it never declared (a flat `node_modules` hid it). Fix options: `nodeLinker: hoisted`; add the package to your own `package.json`; add it with `packageExtensions`; or use a `readPackage` hook in `.pnpmfile.mjs`, then re-run `pnpm install` (no need to delete the lockfile).
- `package-lock.json` and `npm-shrinkwrap.json` are ignored. Run `pnpm import` first to keep versions npm resolved.
- Files in `node_modules/.bin` are always shell files, not symlinks to JS; reference the original file if a JS file is needed.

## Checked

2026-11-04. Confirmed against pnpm.io/faq and pnpm.io/limitations: hard-link disk accounting, Windows junction fallback, flat storage, cross-filesystem copying and store location order, Btrfs reflinks, missing-dependency fixes (nodeLinker hoisted, add dependency, packageExtensions, readPackage), lockfile ignoring and pnpm import, binstubs. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
