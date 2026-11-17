---
id: computing-software.systems-network-administration.restic.repository-locks
name: repository-locks
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, locks, unlock, retry-lock, exclusive-lock, stale-lock]
level: practitioner
status: docs-checked
description: "Understand restic exclusive and non-exclusive locks, the 30-minute stale rule, --retry-lock and restic unlock after interrupted runs."
sources:
  - https://raw.githubusercontent.com/restic/restic/master/doc/design.rst
  - https://raw.githubusercontent.com/restic/restic/master/doc/077_troubleshooting.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repository locks

Locks are files in the `locks/` directory, each a JSON object with `time`, `exclusive`, `hostname`, `username`, `pid`, `uid` and `gid`.

## Two kinds

- Non-exclusive locks: many may coexist (for example several backups).
- Exclusive lock: at most one process can hold it, and no other locks may exist meanwhile. A client removing data must acquire it first.

## Creating a lock

When creating a lock, restic checks the existing locks, creates its own, waits, and checks again whether other locks appeared; depending on their types it either continues or fails. With `--retry-lock`, restic retries creating the lock periodically until it succeeds or the specified timeout expires.

## Stale locks

A lock is stale if its timestamp is older than 30 minutes. For a lock created on the same machine, even a younger lock is tested by sending a signal to its process; if that fails, restic assumes the process is dead and treats the lock as stale.

## Removing locks

Commands such as `backup` or `prune` can be interrupted at any point without damaging the repository, but you might have to run `restic unlock` manually afterwards.

## Checked

2026-11-08. Claims were read against: https://raw.githubusercontent.com/restic/restic/master/doc/design.rst, https://raw.githubusercontent.com/restic/restic/master/doc/077_troubleshooting.rst.

Method: documentation only; no commands were run.
