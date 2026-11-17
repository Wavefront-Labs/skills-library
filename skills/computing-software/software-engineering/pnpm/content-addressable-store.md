---
id: computing-software.software-engineering.pnpm.content-addressable-store
name: content-addressable-store
category: computing-software
field: software-engineering
product: pnpm
tags: [content-addressable-store, hard-links, disk-space, install-stages]
level: intro
status: docs-checked
description: "Explain how pnpm saves disk space and installs fast: a single content-addressable store, hard links or clones into node_modules, and a pipelined three-stage install."
sources:
  - https://pnpm.io/motivation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
pnpm keeps every package file once in a content-addressable store and links it into each project, instead of copying a dependency per project.

- Different versions of one package share unchanged files: if a new version changes 1 of 100 files, only 1 new file enters the store.
- Files are hard-linked or cloned (copy-on-write) from the store, using no extra disk space. Files are copied only when the filesystem supports neither. Tune with the `packageImportMethod` setting (see `computing-software.software-engineering.pnpm.node-modules-settings`).

Install runs in three stages:
1. Resolve dependencies and fetch them to the store.
2. Compute the `node_modules` directory structure.
3. Link the remaining dependencies from the store.

Each package advances to the next stage as soon as it is ready, without waiting for the others, which is faster than resolve-all, fetch-all, write-all.

## Checked

2026-11-04. Confirmed against pnpm.io/motivation and pnpm.io/settings/node-modules (packageImportMethod): shared file storage, 1-of-100 files example, hard-link or clone behaviour, three install stages and per-package progression. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
