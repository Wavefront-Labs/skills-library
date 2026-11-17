---
id: computing-software.software-engineering.crystal.mutex-and-sync
name: mutex-and-sync
category: computing-software
field: software-engineering
product: crystal
tags: [mutex-and-sync, multithreading, mutex, synchronize, lock, race-condition, reentrant, thread-safe, sync, crystal]
level: practitioner
status: docs-checked
description: "Protect shared state with Mutex#synchronize, reentrancy options, and Crystal's sync structures."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mutex and Sync primitives

Goal: avoid data races.

```crystal
m = Mutex.new
count = 0
10.times { spawn { 1000.times { m.synchronize { count += 1 } } } }
```
- Protection types (`Sync::Type`): `Checked` (default; relock by the owner or unlock by a non-owner raises), `Reentrant` (owner may relock; lock count) and `Unchecked` (no checks; relock deadlocks). `Sync::Mutex.new(:reentrant)`; the old `Mutex.new(Mutex::Protection::Reentrant)` is a deprecated alias.
- `lock`/`unlock` manual; always unlock in `ensure`; `synchronize` does so for you.
- Since Crystal 1.20: `Sync::Mutex` (`Mutex` is a deprecated alias), `Sync::RWLock` (`read`/`write`), `Sync::Exclusive(T)` and `Sync::Shared(T)` which guard a value.
- Alternative to locks: confine state to one fiber and talk through a Channel.

Gotchas:
- Holding a lock across a blocking channel op can deadlock.
- A Mutex is per-object; copy of a struct containing one does not share.

Verify: a spec that runs the counter example and expects 10_000.

## Checked

Date 2026-11-03. Confirmed in the Mutex and Sync source: Mutex is an alias of Sync::Mutex deprecated as of Crystal 1.20, Mutex::Protection aliases Sync::Type (Unchecked, Checked, Reentrant, default :checked), synchronize, lock, unlock, Sync::RWLock read and write, Sync::Exclusive and Sync::Shared. Removed the preview_mt verification wording.

Method: documentation only; no commands were run.
