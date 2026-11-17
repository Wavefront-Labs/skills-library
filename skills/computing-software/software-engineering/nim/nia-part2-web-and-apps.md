---
id: computing-software.software-engineering.nim.nia-part2-web-and-apps
name: nia-part2-web-and-apps
category: computing-software
field: software-engineering
product: nim
tags: [nia-part2-web-and-apps, nim-in-action-projects, nim-in-action, jester, web-app, wrapping-c, ffi, sqlite, project-based-learning, karax, nim]
level: practitioner
status: draft
description: "Map the book's applied projects (Wikipedia parser, web app with Jester, wrapping C libraries, packaging) to current tooling."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
  - https://nim-lang.org/docs/lib.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nim in Action part 2: web application and wrappers

Goal: reproduce the applied chapters today.

- Chapters: parsing (a Wikipedia page-count data processor with parseutils/files), a web application (Tweeter clone using Jester, sqlite via `db_connector`/`db_sqlite`, templates for HTML), interfacing with other languages (FFI, wrapping C, c2nim, JS), packages (writing and publishing nimble packages), metaprogramming (templates, macros, DSLs).
- Modern equivalents: Jester still works with Nim 2 (check compatibility), alternatives Prologue, Mummy, Happyx; database access moved to `nimble install db_connector` in Nim 2.x (`import db_connector/db_sqlite`).
- Replace the book's Twitter API dependencies with a local mock.
- Wrap a small C library by following the FFI chapters then compare with c2nim output.
- Publish a toy package as practice (see nimble topics).

Gotchas:
- `db_sqlite` was moved out of std in 2.0.
- Template engines (`karax`/`nimja`) differ from the book's old filters.

Verify: the web app serves a page backed by SQLite.
