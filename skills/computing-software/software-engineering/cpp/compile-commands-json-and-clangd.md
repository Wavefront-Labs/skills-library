---
id: computing-software.software-engineering.cpp.compile-commands-json-and-clangd
name: compile-commands-json-and-clangd
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, compile-commands-json, clangd, language-server, cmake, bear, clang-tidy, editor-tooling, cpp-tooling]
level: practitioner
status: docs-checked
description: "Generate compile_commands.json (CMake, Bear, Meson, Bazel) and configure clangd with .clangd for accurate C++ code completion, navigation and inline clang-tidy diagnostics."
sources: ["https://clang.llvm.org/docs/JSONCompilationDatabase.html", "https://clangd.llvm.org/installation", "https://clangd.llvm.org/config", "https://clangd.llvm.org/guides/system-headers", "https://cmake.org/cmake/help/latest/variable/CMAKE_EXPORT_COMPILE_COMMANDS.html", "https://github.com/rizsotto/Bear"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# compile_commands.json and clangd

**Goal:** every C/C++ tool (clangd, clang-tidy, cppcheck, IWYU, CodeChecker) sees the exact flags
each file is compiled with, so completion, navigation and diagnostics are correct.

## What it is
A JSON array with one entry per translation unit: `directory`, `file`, and `command` or
`arguments`. Tools find it by walking up from the source file (or via `-p <dir>`).

## Generating it
| Build system | How |
|---|---|
| CMake (Ninja/Makefile generators) | `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` or `"CMAKE_EXPORT_COMPILE_COMMANDS": true` in presets; writes `build/compile_commands.json` |
| Ninja (any) | `ninja -t compdb > compile_commands.json` |
| Make / custom scripts | `bear -- make -j8` (intercepts compiler calls) |
| Bazel | `hedronvision/bazel-compile-commands-extractor` |
CMake honours `CMAKE_EXPORT_COMPILE_COMMANDS` only for the Makefile and Ninja generators (it is ignored on others, including Visual Studio), so use a Ninja preset for tooling; it also does not work well with unity builds.
Symlink or copy to the repo root (`ln -s build/compile_commands.json .`) or tell clangd where it is.

## clangd setup
Install clangd (LLVM release or package manager; use a version >= your compiler's language level),
then the editor plugin (VS Code "clangd" extension; disable Microsoft C/C++ IntelliSense to avoid
duplicate engines; the clangd docs say the Microsoft C/C++ extension must not be installed). Project config `.clangd` (YAML) at the repo root:
```yaml
CompileFlags:
  CompilationDatabase: build/            # where compile_commands.json lives
  Add: [-Wall, -Wextra]
Diagnostics:
  ClangTidy:
    Add: [modernize-*, bugprone-*, performance-*]
    Remove: [modernize-use-trailing-return-type]
  UnusedIncludes: Strict
  MissingIncludes: Strict
Index:
  Background: Build
InlayHints:
  ParameterNames: Yes
  DeducedTypes: Yes
```
Useful command-line flags (set in the editor): `--background-index`, `--clang-tidy`, `--compile-commands-dir=<path>`,
`--query-driver=/usr/bin/g++*,/opt/arm/bin/*` (lets clangd ask a GCC
or cross compiler for its system include paths - essential for embedded toolchains).

## Common problems
- **Headers show errors**: headers have no entry; clangd infers flags from a nearby source file.
  Ensure each header is included by at least one compiled TU, or add flags with `If: PathMatch:` blocks.
- **Flags clang rejects** (for example from a GCC build): remove them in `CompileFlags: Remove`.
- **Wrong standard library**: add `--query-driver` or `-isystem` paths; check with clangd's
  "Show AST/Compile command" or log (`clangd --check=src/file.cpp` prints what it does).
- **Stale database** after adding files: re-run the CMake configure step (Ninja regenerates automatically on rebuild).
- Generated sources (protobuf) must exist: build once before indexing.

## Also feeds
`clang-tidy -p build file.cpp`, `run-clang-tidy -p build`, `include-what-you-use` via
`iwyu_tool.py -p build`, `cppcheck --project=build/compile_commands.json`.

## Verify
- [ ] `clangd --check=<a source file>` reports no errors for a known-good file.
- [ ] Go-to-definition works into third-party headers.
- [ ] CI tools (clang-tidy) consume the same database.

## Checked

Date: 2026-10-25. Documentation: clangd site sources (llvm/clangd-www config.md, installation.md, faq.md, guides/system-headers.md) and CMake CMAKE_EXPORT_COMPILE_COMMANDS (Kitware/CMake, head 2026-10-25), Ninja manual.

Confirmed: `.clangd` keys CompileFlags.CompilationDatabase, Diagnostics.ClangTidy Add/Remove, UnusedIncludes and MissingIncludes (`Strict`), Index.Background (`Build` default or `Skip`), InlayHints ParameterNames and DeducedTypes; `--background-index`, `--clang-tidy`, `--compile-commands-dir`, `--query-driver` and `--check` (clangd 12+); Bear and the Bazel extractor are named in the installation page; `ninja -t compdb`; the CMake generator limitation.
Removed as unconfirmed: the Meson and MSBuild rows, the GCC-only flag list, and the `--header-insertion=iwyu` value.

Method: documentation only; no commands were run.
