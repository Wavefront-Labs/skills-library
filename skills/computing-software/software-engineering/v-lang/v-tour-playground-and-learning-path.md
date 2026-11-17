---
id: computing-software.software-engineering.v-lang.v-tour-playground-and-learning-path
name: v-tour-playground-and-learning-path
category: computing-software
field: software-engineering
product: v-lang
tags: [v-tour-playground-and-learning-path, ecosystem-learning-and-stability, v tour, playground, learn v, examples, docs.vlang.io, discord, tutorial, vlib, awesome v, v-lang]
level: intro
status: draft
description: "Learn V with the docs, the V Tour, the online playground, examples folder, Discord and the vlib source as references."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# V Tour, playground and learning path

Goal: get productive in V efficiently.

- Read https://docs.vlang.io/ end to end once (about one evening); it is a single long page with runnable snippets.
- Try snippets without installing in the online playground (play.vlang.io).
- Study `examples/` in the vlang/v repo (hello, web server, gg games, tetris, json, concurrency) and `vlib/` source for idioms; `v doc os` shows APIs from the terminal.
- Ask: official Discord and GitHub discussions; search issues for the exact error; Stack Overflow tag `v` is small.
- Install: clone vlang/v and run `make` (or `make.bat`); then `v symlink`.
- Editor: VS Code extension "V" and `v-analyzer` LSP; Vim/Neovim and Sublime plugins exist.
- Practice order: strings/arrays/maps -> structs/methods -> option/result -> modules/tests -> concurrency -> interop.

Gotchas:
- Many blog posts target older syntax (`[attr]`, `go`, `vweb`); check dates.
- Docs track master; your installed version may differ.

Verify: run the tour's samples in a scratch directory.
