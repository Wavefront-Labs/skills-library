---
id: computing-software.software-engineering.zig.publish-package
name: publish-package
category: computing-software
field: software-engineering
product: zig
tags: [zig, publish-package, zig-package-manager, package-release, exposing-module, semver-zig, package-index]
level: advanced
status: docs-checked
description: "Prepare a Zig library for consumption: expose modules, set paths, tag releases, document and list it in package indexes."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/doc/build.zig.zon.md
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing and versioning a Zig package
**Goal:** make your library fetchable.

- Expose modules from `build.zig` with `b.addModule("name", .{ .root_source_file = ... })`.
- `build.zig.zon` fields: `name` (enum literal, valid bare identifier, at most 32 bytes, no need to include "zig"), `fingerprint`, `version` (semver string, at most 32 bytes), `minimum_zig_version` (optional semver), `dependencies`, and `paths` (required list of files and directories included in the package, relative to the build root; `""` means the build root).
- `fingerprint` together with `name` is the globally unique package identity. The toolchain generates it when the package is created and it never changes; regenerate it only for a fork of a maintained project (delete the field and run `zig build`). Changing `name` or `fingerprint` therefore makes it a different package.
- `minimum_zig_version` is advisory only in 0.15.1: the compiler does not act on it.
- Only files listed in `paths` are used to compute the package `hash`, so list everything the package needs (sources, `build.zig`, `build.zig.zon`, `LICENSE`).
- Consumers add your package with `zig fetch --save <url>`; the `name` field is the default key in their `dependencies` table. A dependency with a `path` is found relative to the build root and its hash is not computed.
- `lazy = true` on a dependency means it is fetched only if used.

## Self-check
In a scratch project, run `zig fetch --save` with your tarball URL and call an exported function from a test.

## Checked
2026-11-02. Confirmed in `doc/build.zig.zon.md` at tag 0.15.1 (name, fingerprint, version, minimum_zig_version, dependencies, lazy, paths) and `lib/std/Build.zig` (`addModule`).
Removed: tag/tarball URL pattern, README table advice, "no official registry" and community index names, semver-for-API advice, `zig build examples` step.
Method: documentation only; no commands were run.
