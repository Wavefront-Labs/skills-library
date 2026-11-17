---
id: computing-software.software-engineering.zig.fetch-dependency
name: fetch-dependency
category: computing-software
field: software-engineering
product: zig
tags: [zig, fetch-dependency, zig-package-manager, zig-fetch, b-dependency, dep-module, dep-artifact, lazy-dependency]
level: practitioner
status: docs-checked
description: "Add a dependency with zig fetch --save, then consume it in build.zig with b.dependency, dep.module and dep.artifact."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/doc/build.zig.zon.md
  - https://github.com/ziglang/zig/blob/0.15.1/lib/init/build.zig.zon
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Build.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zig fetch and b.dependency
**Goal:** add, pin and use a package.

```bash
zig fetch --save https://github.com/org/repo/archive/refs/tags/v1.0.0.tar.gz
```
Adds the dependency (with its hash) to `build.zig.zon`; the key is the package's `name` field unless you choose another.
```zig
const dep = b.dependency("repo", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("repo", dep.module("repo"));    // module exported by the dep's build.zig via b.addModule
exe.root_module.linkLibrary(dep.artifact("repo_c"));       // library built by the dep (Compile.linkLibrary also exists)
const data = dep.path("assets/x.dat");                     // LazyPath into the package
```
- The `hash` is the source of truth; the `url` is just a mirror. Prefer tagged or commit-pinned URLs.
- `zig build --fetch` fetches all dependencies recursively; afterwards `zig build` needs no internet connection.
- The second argument to `b.dependency` is an args struct passed to the dependency's build script.
- Lazy deps: set `.lazy = true` in the manifest and call `b.lazyDependency("x", .{})`, which returns `?*Dependency` (null while the dependency is not yet fetched; return from your build function in that case). It also works on non-lazy dependencies.
- Vendoring: use `.path = "vendor/x"` (relative to the build root; not hashed).

## Gotchas
- The dependency name in `.zon` and in `b.dependency("...")` must match.
- `dep.module(name)` takes the name the dependency registered with `b.addModule(name, ...)`, and `dep.artifact(name)` the name of its compiled artifact.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: `b.dependency`, `b.lazyDependency` (`?*Dependency`), `Dependency.module`/`artifact`/`path`, `Module.linkLibrary`, and the `.zon` `url`/`hash`/`path`/`lazy` rules plus `zig fetch --save` and `zig build --fetch` comments in doc/build.zig.zon.md and lib/init. Removed: git `--save=name` form, `zig env`, private-repo advice.

Method: documentation only; no commands were run.

## Self-check
Fetch a tiny package, import its module, call one function, and check `build.zig.zon` contains a `.hash`.
