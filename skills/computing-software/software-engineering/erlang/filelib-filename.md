---
id: computing-software.software-engineering.erlang.filelib-filename
name: filelib-filename
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-files, filelib-filename]
level: practitioner
status: docs-checked
description: "Erlang filelib wildcard, ensure_dir, fold_files and path building with the filename module; code:priv_dir."
sources:
  - https://www.erlang.org/doc/apps/stdlib/filelib.html
  - https://www.erlang.org/doc/apps/stdlib/filename.html
  - https://www.erlang.org/doc/apps/kernel/code.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# filelib and filename
**Goal:** build portable paths and walk directories.

```erlang
Path = filename:join(["priv", "static", "app.js"]),
filename:basename(Path), filename:dirname(Path), filename:extension(Path),
ok = filelib:ensure_dir("out/logs/x.log"),     % creates the parent directories of the name
filelib:wildcard("src/**/*.erl"),
filelib:is_file(Path), filelib:is_dir("src"),
filelib:fold_files("src", ".*\\.erl$", true, fun(F, Acc) -> [F | Acc] end, []).
code:priv_dir(myapp).   % path to the priv directory of an application
```
- Build paths with `filename:join`; do not concatenate separators by hand.
- `filelib:ensure_dir/1` ensures that all parent directories of the given file or directory name exist, so pass a path whose last component is the file; it returns `ok` or `{error, Reason}`.
- In `wildcard/1`, `**` (two adjacent stars as a single pattern) matches all files and zero or more directories and subdirectories.
- `code:priv_dir/1` returns the path to the `priv` directory of an application (name given as an atom) or `{error, bad_name}`.

## Gotchas
- `ensure_dir("a/b")` creates `a` only; `b` is treated as the file name.

## Self-check
Create nested directories with `ensure_dir`, then list them with `wildcard`.

## Checked

2026-11-03. Confirmed in the `filelib`, `filename` and `code` module pages (`join`, `basename`, `dirname`, `extension`, `ensure_dir`, `wildcard` `**`, `fold_files/5`, `is_file`, `is_dir`, `priv_dir/1`). Removed: the "works inside releases" claim and the launch-method working-directory gotcha.
Method: documentation only; no commands were run.
