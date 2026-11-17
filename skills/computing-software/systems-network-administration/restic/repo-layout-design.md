---
id: computing-software.systems-network-administration.restic.repo-layout-design
name: repo-layout-design
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, repository-layout, design, snapshots, data, index, keys, locks]
level: advanced
status: docs-checked
description: "Read the restic repository layout: config, data, index, keys, locks and snapshots directories, storage IDs, and the write ordering rules."
sources:
  - https://raw.githubusercontent.com/restic/restic/master/doc/design.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repository layout

A repository contains a `config` file and the directories `data/`, `index/`, `keys/`, `locks/`, `snapshots/` and `tmp/`.

- `data/` holds pack files, sharded into subdirectories named by the first two hex characters of the pack ID, such as `data/21/2159dd...`.
- `config` is JSON with `version` (1 or 2), `id` (32 random bytes, hex) and `chunker_polynomial`.

## Storage IDs

A file's ID is the SHA-256 of its contents, written as lowercase hex. A prefix of an ID may be used instead of the complete filename. Files are write-once and never modified, so writes should be atomic.

## Ordering rules

- Write order: packs, then index, then snapshot.
- Read order: collect the snapshot list before loading the index, to avoid racing with new writes.
- Invariants: snapshots reference only existing trees; trees reference only existing blobs; indexes reference only valid blobs in existing packs.
- Removal needs an exclusive lock. Delete a pack from the index before deleting the file. A rewrite writes the new pack, updates the index, then deletes the old pack.

## Why it matters

Because files never change and writes follow the ordering above, a crash or interrupted connection still leaves a correct repository.

## Checked

2026-11-08. Claims were read against: https://raw.githubusercontent.com/restic/restic/master/doc/design.rst.

Method: documentation only; no commands were run.
