---
id: computing-software.software-engineering.pnpm.run-script-environment
name: run-script-environment
category: computing-software
field: software-engineering
product: pnpm
tags: [npm-lifecycle-event, script-env-vars, init-cwd, pnpm-script-src-dir, npm-package-vars, report-summary, run-dry-run]
level: practitioner
status: docs-checked
description: "Know the environment pnpm sets for scripts (npm_lifecycle_event, INIT_CWD, npm_package_*), plus recursive run flags: --parallel, --stream, --resume-from, --dry-run."
sources:
  - https://pnpm.io/cli/run
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Variables pnpm creates for scripts: `npm_command` (`run-script` for `pnpm run`), `npm_lifecycle_event`, `npm_lifecycle_script`, `npm_package_json`, `npm_package_*` (name, version, config, engines, bin; e.g. `npm_package_config_port`), `npm_config_user_agent`, `npm_execpath`, `npm_node_execpath` and `NODE`, `INIT_CWD` (where pnpm was started), `PNPM_SCRIPT_SRC_DIR` (the package whose script runs), and `FORCE_COLOR=1` when pnpm itself prints output in color (existing values are kept).

Recursive run (`pnpm -r run build`):
- Uses a dependency-aware task graph configured by the `tasks` setting; `--no-sort` and `--parallel` drop that ordering.
- A package lacking the script is skipped; if none has it, the command fails.
- `--parallel`: no concurrency or topological limits, prefixed streaming output.
- `--stream`: interleave output with directory prefix; `--aggregate-output`: print each result when finished (append-only reporter); `--reporter-hide-prefix` for raw output such as GitHub annotations.
- `--resume-from <name>`: continue at a package.
- `--dry-run [--json]`: print the resolved task graph without running (recursive only).
- `--report-summary`: write `pnpm-exec-summary.json` with `status` passed, queued, running, skipped or failure.

## Checked

2026-11-04. Confirmed the script environment variable list, recursive run options, --dry-run and --json, and the --report-summary status values against pnpm.io/cli/run. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
