---
id: computing-software.software-engineering.ruby.ruby-fibers-scheduler
name: ruby-fibers-scheduler
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-concurrency, fibers-scheduler]
level: advanced
status: docs-checked
description: "Understand Fibers and the non-blocking Fiber scheduler interface (3.0) used by async libraries."
sources: ["https://docs.ruby-lang.org/en/master/Fiber.html", "https://docs.ruby-lang.org/en/master/Enumerator.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fibers and Fiber scheduler
- Fibers are light-weight cooperative concurrency primitives: code blocks that can be paused (`Fiber.yield`) and resumed.
- With `Fiber.set_scheduler`, a non-blocking fiber (`Fiber.new(blocking: false)`, the default) that performs a blocking operation such as `sleep` or waiting for I/O yields control to the scheduler; with no scheduler set, blocking and non-blocking fibers behave the same.
- Ruby ships no scheduler implementation of its own; you supply one.
- External enumeration with `Enumerator#next` runs the enumerator in a different Fiber.
Verify: run concurrent sleeps in a scheduler and measure total time.

## Checked
2026-11-02. Confirmed against: Fiber and Enumerator pages. Removed or softened (not stated on those pages): version tag, async gem, Queue claims.
Method: documentation only; no commands were run.
