---
id: computing-software.software-engineering.crystal.spawn-fibers
name: spawn-fibers
category: computing-software
field: software-engineering
product: crystal
tags: [spawn-fibers, concurrency-fibers, spawn, fiber, green-thread, cooperative-scheduling, sleep, fiber-yield, event-loop, crystal]
level: practitioner
status: docs-checked
description: "Start lightweight fibers with spawn, understand cooperative scheduling, yielding at IO, sleep and Fiber.yield, and fiber names."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# spawn and fibers

Goal: run work concurrently.

- `spawn { work }` creates a fiber; `spawn(name: "w") { ... }` names it for debugging. Fibers are cheap: each has an 8 MiB stack reserved but only 4 KiB is allocated at first.
- Scheduling is cooperative: a fiber runs until it does IO, `sleep`, channel ops, `Fiber.yield` or finishes. CPU loops without yields starve others.
- Main fiber exiting ends the program even if others are running; wait with a Channel, `WaitGroup` or `sleep`.
- Fibers that wait for I/O are parked and the event loop resumes them when the I/O is ready.

Gotchas:
- `spawn` in a `while` loop shares the one loop variable (all fibers see its final value); pass it through `spawn` arguments or copy it to a local.

Verify: spawn N fibers that send results on a channel and receive N values.

## Checked

Date 2026-11-03. Confirmed in the Fiber source and the concurrency guide: 8 MiB stack with 4 KiB allocated at first, cooperative scheduling, Fiber.yield, the program exiting when the main fiber finishes, I/O waiting through the event loop, spawn name: keyword, and the shared loop variable example. Removed the unconfirmed exception-handling and blocking-C-call gotchas.

Method: documentation only; no commands were run.
