---
id: computing-software.software-engineering.d.d-module-declaration-imports
name: d-module-declaration-imports
category: computing-software
field: software-engineering
product: d
tags: [d-module-declaration-imports, modules-packages, module, import, selective-import, renamed-import, static-import, public-import, package-d, -i, d]
level: intro
status: docs-checked
description: "Organise D code in modules and packages: module statement, public/selective/renamed/static imports, package.d, local imports, name lookup and -I."
sources:
  - https://dlang.org/spec/module.html
  - https://dlang.org/dmd-linux.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module declarations, imports, selective and renamed imports

Goal: structure code and control names.

- Modules correspond one-to-one with source files; without a module declaration the name is the file name stripped of path and extension. The declaration must come first (only comments and `#line` may precede it).
- Imports: `import std.stdio;`, selective `import std.algorithm : map, filter;`, renamed `import io = std.stdio;` / `import std.string : toUp = toUpper;`, static `static import std.stdio;` (qualified only), `public import` re-exports. Imports are also allowed in local scopes; in function scope they take effect only after the import line.
- A package module's file name must be `package.d`; its module name is the package's fully qualified name, and it can be imported like any other module.
- `-I=directory` adds an import path; if a module is not found in any of them, the current working directory is searched.
- Symbol lookup stops at the first match; two symbols with the same name found in the same lookup phase are an ambiguity error. Locally imported symbols may hide symbols from outer scopes.
- Import cycles are allowed so long as neither, or only one, of the modules has static constructors or destructors; otherwise a runtime exception results.

Gotchas:
- `static` cannot be used with selective imports.
- `private` means accessible only within the same module, not the same directory.

Verify: `dmd -c -Isource source/app/main.d` resolves everything or reports missing module.

## Checked
Checked 2026-11-03 against the D spec Modules page (module declaration, public/static/renamed/selective imports, package modules, lookup, cycles) and the dmd command-line page (`-I`). Removed: the claim that module name should match the path, the `__MODULE__`/mixin-import line, the selective-import overload remark and the rdmd/dub remark (not on those pages).

Method: documentation only; no commands were run.
