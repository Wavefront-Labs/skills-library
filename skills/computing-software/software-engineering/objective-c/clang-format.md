---
id: computing-software.software-engineering.objective-c.clang-format
name: clang-format
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-style-lint, clang-format]
level: intro
status: docs-checked
description: "Configure .clang-format with Objective-C options, format with -i, and handle .h files that clang-format may guess as C++."
sources:
  - https://clang.llvm.org/docs/ClangFormat.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---


# clang-format
**Goal:** automatic consistent formatting.

```yaml
# .clang-format
BasedOnStyle: Google
ObjCBlockIndentWidth: 4
ObjCSpaceAfterProperty: true
ObjCSpaceBeforeProtocolList: true
```
```bash
clang-format -i --style=file Sources/main.m
clang-format --dump-config -style=llvm > .clang-format
clang-format --style=file --dry-run --Werror Sources/main.m
git clang-format
```
- Presets: LLVM, GNU, Google, Chromium, Microsoft, Mozilla, WebKit. `--style=file` is the default: the `.clang-format` file is searched in parent directories of the source file; if none is found it falls back to `--fallback-style` (default LLVM; `none` skips formatting). `file:<path>` names a file explicitly.
- `-i` edits in place; `--dry-run` (alias `-n`) does not change files; `--Werror` turns formatting warnings into errors; `--dump-config` prints the configuration; `--assume-filename` sets the name used to pick the language and find the config.
- `.m` and `.mm` files are Objective-C. Unrecognised file names are treated as C++.
- `// clang-format off` and `// clang-format on` bracket code left unformatted.
- Objective-C options exist: `ObjCBinPackProtocolList`, `ObjCBlockIndentWidth`, `ObjCBreakBeforeNestedBlockParam`, `ObjCSpaceAfterProperty`, `ObjCSpaceBeforeProtocolList`.
- `git clang-format` formats the lines that differ from a commit (the working tree against `HEAD` when no commit is given).

## Self-check
Run `clang-format --dry-run --Werror` over a file and confirm the exit status.

## Checked
2026-11-02. Confirmed against the ClangFormat page and the Clang-Format Style Options page: presets, `--style=file` search and fallback, flag meanings, file extensions, `// clang-format off`, Objective-C option names, `git clang-format`. Removed: `.h` language-detection and `Language: ObjC` section advice, ColumnLimit/IndentWidth example values, pre-commit and version-pinning advice (not stated).
Method: documentation only; no commands were run.
