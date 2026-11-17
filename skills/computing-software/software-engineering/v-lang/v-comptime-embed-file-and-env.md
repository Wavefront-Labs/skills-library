---
id: computing-software.software-engineering.v-lang.v-comptime-embed-file-and-env
name: v-comptime-embed-file-and-env
category: computing-software
field: software-engineering
product: v-lang
tags: [v-comptime-embed-file-and-env, compile-time-programming, embed-file, env, tmpl, compile-error, compile-warn, v-lang]
level: advanced
status: docs-checked
description: "Ship files in the V binary with $embed_file (-prod embeds fully), read build env vars with $env, take -d defines with $d, render $tmpl, and use $compile_error."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Embedding files and compile-time helpers

Goal: bake data into the executable.

- `$embed_file('v.png')` embeds a file; paths can be absolute or relative to the source file, and may use `@VEXEROOT`, `@VMODROOT`, `@DIR`, `$d` and `$env`. The result is `EmbedFileData`: use `.to_string()` or `.data()`; `.len` is the size.
- In a normal development build only the file path is stored and the file is loaded the first time `.data()` runs. The whole file is embedded only in `-prod` builds (and portable `-os cross` C output). A dev build panics where that file is missing; use `-prod` for anything you distribute.
- Compression: `$embed_file('x.css', .zlib)` works with `-prod`; zlib is the only compression type. The docs note compressing already-compressed assets (png, zip) usually gains little.
- Discarding the `$embed_file` result as a statement is an error.
- `$env('ENV_VAR')` brings a build-time environment variable into the program; it also works in top-level `#flag` and `#include` statements.
- `$d('ident', default)` reads `-d ident=value` defines; `-d ident` means `-d ident=true`. Defaults must be pure literals: `false`, an integer, a float or a string. Example: `v -d my_i64=4096 -d my_string="V rocks" run .`.
- `$tmpl('path/to/template.txt')` renders a template file using local variables with `@name`, `@for ... @end` syntax; see vlib/v/TEMPLATES.md in the vlang/v repo.
- `$compile_error('msg')` and `$compile_warn('msg')` take a string literal and show a custom error or warning at compile time, typically inside a `$if` branch; top-level ones in imported modules fire even if no function is called.

Gotchas:
- Embedded files increase executable size.

## Checked

Confirmed against the "Compile time ... $embed_file / $tmpl / $env / $d / $compile_error" subsections of doc/docs.md in the vlang/v repository, read 2026-11-08. Removed: the `.to_string()`-vs-`data()` text/binary advice beyond the docs, `@[compress]` wording, and the docs.vlang.io and modules.vlang.io sources.
Method: docs-only read of cited pages, 2026-11-08
