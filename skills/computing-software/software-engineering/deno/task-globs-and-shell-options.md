---
id: computing-software.software-engineering.deno.task-globs-and-shell-options
name: task-globs-and-shell-options
category: computing-software
field: software-engineering
product: deno
tags: [task, glob, globstar, failglob, nullglob, pipefail, errexit]
level: advanced
status: docs-checked
description: "Glob expansion in deno task, the globstar node_modules trap, and shell options failglob, globstar, nullglob, pipefail and errexit."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/cli/task.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Globs work cross-platform (Deno 1.34+): `*`, `?`, `[`/`]`.

```sh
echo **/*.ts
echo data[0-9].csv
```

Caution: `globstar` is on by default, so `**` recurses into all descendant directories, including `node_modules`. A task like `deno check **/*.ts` can then hit `Argument list too long` or check unintended files. For `deno check` and `deno fmt`, run without glob arguments and use `exclude` in deno.json (`node_modules` is excluded by default), or disable recursion with `shopt -u globstar`.

Shell options (Deno 2.6.6+); `failglob` and `globstar` are on by default:

- `failglob`: unmatched globs error. Disable: `shopt -u failglob`.
- `globstar`: `**` matches zero or more directories. Disable: `shopt -u globstar`.
- `nullglob`: unmatched globs expand to nothing. Enable: `shopt -s nullglob`.
- `pipefail`: pipeline exit code is the last non-zero one. Enable: `set -o pipefail`.
- `errexit` (Deno 2.8+): a sequential list aborts on first non-zero exit. `set -e` / `set +e`.

```jsonc title="deno.jsonc"
{
  "tasks": {
    "task2": "shopt -u failglob && shopt -s nullglob && rm -rf *.ts",
    "task4": "set -o pipefail && cat missing.txt | echo 'hello'",
    "task5": "set -e; build_step_one; build_step_two; build_step_three"
  }
}
```

## Checked

2026-11-04. Confirmed against docs runtime/reference/cli/task.md (deno task): glob characters, Deno 1.34 glob support, globstar caution, shell options with defaults and version gates (2.6.6, errexit 2.8).

Method: documentation only; no commands were run.
