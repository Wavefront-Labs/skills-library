---
id: computing-software.software-engineering.nim.nia-part1-fundamentals
name: nia-part1-fundamentals
category: computing-software
field: software-engineering
product: nim
tags: [nia-part1-fundamentals, nim-in-action-projects, nim-in-action, book, fundamentals, getting-started, learning-path, chat-app, reading-plan, nim]
level: intro
status: draft
description: "Map the book's first part (why Nim, getting started, language basics, parallelism, standard library) to the skills to practise."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
  - https://nim-lang.org/docs/lib.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nim in Action part 1: fundamentals chapters

Goal: follow the book's fundamentals with current Nim.

- Chapters (Part 1, "The basics of Nim"): why Nim, getting started (install, first programs, compile), the basics (types, control flow, procs, collections, modules), a chat application (sockets, async, threads, JSON message protocol), and the standard library tour.
- Book targets Nim 0.x/1.0: update when following: ORC/ARC replace the old GC, `threads` default on, `std/` import prefix, `result` unchanged, `async` unchanged, `parseopt` signature same.
- Exercise: build the book's chat server and client with `asyncnet` and `parseJson`, using `nimble init` and `nimble test`.
- Compare listing code against the current manual; mark sections that need modernizing (like `pragma` names and `GC_` calls).

Gotchas:
- Old tutorials use `{.noSideEffect.}` procs, `ptr`-heavy code and `--gc:boehm`, which differ in 2.x.
- `import os` style still works but `std/os` is preferred.

Verify: your chat client and server exchange messages across two terminals.
