---
id: computing-software.software-engineering.v-lang.v-module-search-paths-and-vmodules
name: v-module-search-paths-and-vmodules
category: computing-software
field: software-engineering
product: v-lang
tags: [v-module-search-paths-and-vmodules, v-mod-and-module-search, vmodules, module path, search path, local module, symlink, v-lang]
level: practitioner
status: draft
description: "Understand where V resolves imports: project root, ~/.vmodules and VMODULES, and how to manage local development modules."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Module search paths and VMODULES

Goal: debug "module not found".

- Resolution order: relative to the current module root, then the `VMODULES` environment path (default is a `.vmodules` folder in your home directory), then V's own `vlib`.
- `v install author.mod` places it under `.vmodules/author/mod`; import as `import author.mod`.
- Develop a library locally: symlink or clone it into the `.vmodules` tree, or use `-path` (compiler flag for module lookup; confirm with `v help build`).
- Print config: `v -v` or `v doctor` summarises paths and versions (`v doctor` exists in recent versions).
- Clear caches with `v wipe-cache` if stale builds appear.

Gotchas:
- A directory without v.mod inside `.vmodules` may fail to resolve.
- Different names for the folder and `module` line cause confusing errors.

Verify: `v doctor` shows the VMODULES location and the import compiles.
