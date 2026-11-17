---
id: computing-software.software-engineering.zig.libraries-frameworks
name: libraries-frameworks
category: computing-software
field: software-engineering
product: zig
tags: [zig, libraries-frameworks, zig-ecosystem, zap, httpz, zig-clap, raylib-zig, mach, libxev, ecosystem]
level: practitioner
status: draft
description: "Orient in the Zig ecosystem: web servers, CLI parsing, GUI and game bindings, databases and projects written in Zig, with a vetting checklist."
sources:
  - https://ziglang.org/learn/overview/
  - https://zig.guide/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Notable libraries, frameworks and real-world projects
**Goal:** find and judge libraries (all names are community projects; check current maintenance, unconfirmed).

- Web/network: `httpz` (http.zig), `zap` (facil.io wrapper), `libxev` (cross-platform event loop), std.http for basics.
- CLI: `zig-clap`, `zig-cli`.
- Graphics/games: `raylib` bindings (`raylib-zig`), `sokol-zig`, SDL3 bindings, `mach` engine, `zgui` (Dear ImGui), `zgpu`.
- Data/formats: `zig-sqlite` or direct C sqlite via build.zig, `zig-toml`, protobuf and msgpack packages, `zlib`/`zstd` wrappers via the C-build pattern.
- Embedded: MicroZig.
- Projects written in Zig that are good code to read: Bun (JS runtime), TigerBeetle (database), Ghostty (terminal), River (Wayland compositor), the Zig compiler itself (self-hosted).
- Discovery: `awesome-zig` lists and package indexes such as zigistry; search the forge by topic `zig-package`.

Vetting checklist:
1. Does it state the Zig version it supports, and does CI use it?
2. Is `build.zig.zon` clean (minimum version, paths, fingerprint)?
3. Tests present, `zig build test` passes on your version?
4. Last commit date and issue activity; is there a branch per Zig release?
5. Dependencies pinned by hash; any C code vendored?
6. License compatible.

## Gotchas
- A library for an older Zig will fail on newer compilers due to API churn; budget migration time or pin the compiler.
- Prefer small libraries you can vendor and read.

## Self-check
Pick one library, add it with `zig fetch --save`, build, and run its example on your compiler.
