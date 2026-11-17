---
id: computing-software.software-engineering.cpp.diagnosing-undefined-references-and-link-errors
name: diagnosing-undefined-references-and-link-errors
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-linking, cpp-ln-undefined, undefined-reference-debugging, linker-errors, link-order]
level: practitioner
status: docs-checked
description: "Diagnose undefined reference and multiple definition link errors with GNU ld options: link order, groups, trace-symbol, map files."
sources:
  - https://sourceware.org/binutils/docs/ld/Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing undefined references

```
/usr/bin/ld: main.o: in function `main': main.cpp:(.text+0x9): undefined reference to `Widget::draw() const'
```

## Procedure
1. Read the full symbol, including `const`, namespaces and parameter types. Check the function is actually defined in a source file that is part of the build target.
2. Find where the reference comes from: `-Wl,--trace-symbol=NAME` (or `-y NAME`) prints each linked file in which the symbol appears. Per the ld manual it is for an undefined symbol when you do not know where the reference comes from. On some systems an underscore must be prepended to the name.
3. Check link order for static archives. An archive is normally searched once, in command-line order. If a symbol in an archive is needed by an object in an archive that appears later on the command line, it cannot be resolved. List dependents before their dependencies.
4. For unavoidable circular references between archives, group them: `gcc -Wl,--start-group foo.a bar.a -Wl,--end-group`. The archives are searched repeatedly until no new undefined references appear. It has a significant performance cost, so use it only when needed.
5. Get a link map: `-Wl,-Map=out.map` writes the map file, useful to see which input sections were pulled in.

## Related ld options
- `-Wl,--no-undefined` (same as `-z defs`) reports unresolved references from regular object files even when creating a shared library, so missing symbols fail at link time. `-z undefs` reverts it.
- Multiple definitions are normally a fatal error; `--allow-multiple-definition` (`-z muldefs`) uses the first definition. Treat it as a workaround, not a fix.
- `--gc-sections` (off by default) discards unused input sections. Sections reachable from the entry symbol, symbols undefined on the command line and symbols referenced by dynamic objects are kept. Objects that only register themselves via static initialisers can be dropped if nothing references them.

## Verify
After the fix, the link succeeds with `-Wl,--no-undefined` for shared libraries.

## Checked
Read the GNU ld Options page. Kept: the archive search order and start/end-group behaviour, trace-symbol, Map, no-undefined, muldefs and gc-sections. Removed: nm, objdump, c++filt and ldd recipes, the typical-cause table (vtable, template, static member, MSVC LNK errors), the dual-ABI/_GLIBCXX_USE_CXX11_ABI guidance, `--whole-archive`/visibility advice and `-Wl,--verbose` (not on the page read; the gcc.gnu.org dual ABI page is unreadable).

Method: docs-checked 2026-11-09 against the GNU ld Options page (sourceware.org/binutils/docs/ld/Options.html).
