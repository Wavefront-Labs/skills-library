---
id: computing-software.software-engineering.zig.learning-resources
name: learning-resources
category: computing-software
field: software-engineering
product: zig
tags: [zig, learning-resources, zig-ecosystem, langref, zig-std-docs, ziglings, release-notes, zig-guide]
level: intro
status: draft
description: "Navigate Zig official documentation, std docs, zig.guide, Ziglings exercises and release notes, and know how to check version relevance."
sources:
  - https://ziglang.org/learn/overview/
  - https://zig.guide/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Official docs and learning resources
**Goal:** find authoritative, version-correct information fast.

- Language Reference: `ziglang.org/documentation/<version>/` (per release) and `/master/`. Authoritative for syntax and builtins.
- Standard library docs: `ziglang.org/documentation/<version>/std/` or locally `zig std` (served from your installed compiler, so always matches your version).
- Learn pages: `ziglang.org/learn/` (overview, build system guide, style guide).
- `zig.guide`: tutorial site (versioned; check which Zig it targets).
- Release notes per version: list every breaking change with migration hints; read before upgrading.
- Ziglings: community exercise set (small programs to fix) for practice.
- Source code: the standard library source (`lib/std` in your install) is the most reliable documentation; read `std.mem.Allocator`, `std.ArrayList` and tests.
- Community: Ziggit forum, Zig Discord and Zig Software Foundation resources; Zig Showtime talks.
- Version check: any snippet using `@intCast(u8, x)` (type first), `std.io.getStdOut()` or `callconv(.C)` should be cross-checked against your compiler.
- Compiler errors are good: "note: ..." lines often show the fix.

## Gotchas
- Search results mix many Zig versions; add the version to your query.
- `master` docs describe unreleased behavior that your release compiler lacks.

## Self-check
Open `zig std` locally, find `std.mem.Allocator`, and read its `create` doc comment.
