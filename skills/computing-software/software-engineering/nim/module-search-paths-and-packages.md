---
id: computing-software.software-engineering.nim.module-search-paths-and-packages
name: module-search-paths-and-packages
category: computing-software
field: software-engineering
product: nim
tags: [module-search-paths-and-packages, modules, module-path, search-path, nimblepath, path, std-import, project-layout, nim]
level: practitioner
status: docs-checked
description: "How the Nim compiler finds imported modules: the search path, --path, path substitutions, nimble packages in pkgs2, nimblePath, nimbledeps, src layout, and nim dump."
sources:
  - https://nim-lang.org/docs/nimc.html
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/folder-structure.md
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/create-packages.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module search paths and --path

Goal: have imports resolve without hacks.

- The compiler keeps a global search path (PATH) used to find imported modules and include files; more than one match is an ambiguity error. Before PATH is used, the current directory is checked for the file. In the guide's example, with `$lib/x.nim` and `$lib/bar/x.nim` both on PATH, `$lib/x.nim` wins as the first match.
- Add directories with `-p` / `--path:PATH`. Path options support `$nim`, `$lib`, `$home`/`~`, `$config` (directory of the module being compiled), `$projectname`, `$projectpath`/`$projectdir`, `$nimcache`.
- Nimble installs libraries into `$nimbleDir/pkgs2` (default `$HOME/.nimble`), and the compiler finds them through its `nimblePath` feature, so `import modulename` works without setup. The compiler cannot read `.nimble` files or resolve dependencies and can only use the latest version of a package; when Nimble builds your package it feeds the exact path of each dependency to the compiler.
- Custom `$nimbleDir`: pass `--nimblePath:PATH` to Nim (for example `nim c --nimblePath:nimbledeps/pkgs2 main.nim`) or set `nimblePath = "$project/nimbledeps/pkgs2"` in a config file. If a `nimbledeps` directory exists next to the .nimble file, Nimble uses it as `$nimbleDir`.
- Recommended layout: `foobar.nimble`, `src/foobar.nim` (imported as `foobar`), `src/foobar/utils.nim` (imported as `foobar/utils`), `tests/`; the .nimble file needs `srcDir = "src"`. `nimble setup` writes a `nimble.paths` file for the compiler.
- `nim dump` (or `nim --dump.format:json`) shows the defined conditionals and search paths.

Gotchas:
- A local file with the same name as a module that is on PATH is found first, because the current directory is checked before PATH.

Verify: `nim dump` lists your source directory.

## Checked

2026-11-03. Confirmed in the Nim compiler guide (search path handling, `--path`, substitutions, `dump`), the Nimble guide "folder structure" (pkgs2, nimbledeps, `--nimblePath`, compiler limits) and "Creating Nimble packages" (layout, `srcDir`). Removed: the stdlib `std/` prefix advice, `tests/config.nims` path recipe, "paths in nim.cfg are relative to the config file", the older `pkgs` directory remark, and `json.nim` shadowing example.
Method: documentation only; no commands were run.
