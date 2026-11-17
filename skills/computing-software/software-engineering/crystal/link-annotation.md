---
id: computing-software.software-engineering.crystal.link-annotation
name: link-annotation
category: computing-software
field: software-engineering
product: crystal
tags: [link-annotation, c-bindings, link, ldflags, pkg-config, static-link, linking, framework, crystal]
level: practitioner
status: docs-checked
description: "Use the Link annotation on a lib with lib name, ldflags, pkg_config, framework, static, wasm_import_module and dll arguments to link a native library."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/c_bindings/lib.md
  - https://github.com/crystal-lang/crystal/blob/master/src/annotations.cr
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/codegen/link.cr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @[Link] and linking C libraries

Goal: link a native library.

```crystal
@[Link("pcre")]
lib LibPCRE
end
```
- `@[Link("pcre")]` passes `-lpcre` to the linker, but the compiler first tries `pkg-config`; it looks up a shared library.
- `@[Link(ldflags: "-lpcre")]` passes the flags to the linker unmodified. A common technique is a backtick command: ``@[Link(ldflags: "`pkg-config libpcre --libs`")]``.
- `@[Link(framework: "Cocoa")]` passes `-framework Cocoa` (macOS only).
- `@[Link("pcre", pkg_config: "libpcre")]` sets the pkg-config module name separately from the library name.
- Accepted arguments: `lib`, `ldflags`, `static`, `pkg_config`, `framework`, `wasm_import_module` and `dll` (the compiler rejects any other name). `static` takes a Bool; `dll: "gc.dll"` copies that DLL to built programs (name must end in `.dll`, no directory separators).
- The attribute can be omitted when the library is implicitly linked, as with libc.
- `CRYSTAL_LIBRARY_PATH` is the first lookup place for libraries to link; `--link-flags` adds linker flags at build time.

Gotchas:
- Static linking on glibc distributions is discouraged; use Alpine/musl (see release-static-cross).
- `pkg-config` must be available at build time for the pkg-config lookup.

Verify: build the program and confirm the linker finds the library.

## Checked

2026-11-03. Confirmed against the Crystal book "lib" page, the `Link` annotation docs in `annotations.cr` and the compiler's `link.cr` (argument names, types and checks), and the compiler manual (`--link-flags`, `CRYSTAL_LIBRARY_PATH`).
Removed: the `sqlite3_libversion` example, the `ldflags` search-path example with an invented `/opt` path, the `pkg_config: "libfoo >= 1.2"` version form, the conditional-`Link` macro form, "the linker needs the dev package", "library order matters" and `ldd` as a verify step.
Method: documentation only; no commands were run.
