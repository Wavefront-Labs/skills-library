---
id: computing-software.software-engineering.pnpm.scripts-lifecycle-and-processes
name: scripts-lifecycle-and-processes
category: computing-software
field: software-engineering
product: pnpm
tags: [hidden-scripts, lifecycle-scripts, dev-preinstall, leftover-processes, script-name-conflicts, pnpm-pm-builtin, prepare-script]
level: practitioner
status: docs-checked
description: "Understand pnpm script behaviour: hidden dot scripts, install lifecycle order, pnpm:devPreinstall, processes left running, and scripts that shadow built-in commands."
sources:
  - https://pnpm.io/scripts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```json
{
  "scripts": {
    ".helper": "echo hidden",
    "build": "pnpm run .helper && tsc"
  }
}
```

- Names starting with `.` are hidden: not runnable with `pnpm run`, not listed, callable from other scripts only.
- `pnpm install` runs per workspace project, in order: `preinstall`, `install`, `postinstall`, `preprepare`, `prepare`, `postprepare`. With `--prod` or when installing specific packages, only `preinstall`, `install`, `postinstall`. `pre`/`post` of other scripts depend on `enablePrePostScripts`.
- `pnpm:devPreinstall` runs when `pnpm install` runs in the project itself (also CI), before any dependency is installed, never when installed as a dependency, and only if set in the root project's `package.json`.
- A process a script, `pnpm exec` or `pnpm dlx` starts and leaves running keeps running after pnpm exits, even after failure or Ctrl+C. pnpm ends what it started only when pnpm itself is killed or crashes (Windows: all except `CREATE_BREAKAWAY_FROM_JOB`; Unix: scripts in their own process group, which is every script of a parallel run and every script without a terminal), or when a script fails in a recursive or parallel run, unless `--no-bail`.
- Built-ins that yield to user scripts of the same name: `clean` (alias `purge`), `setup`, `deploy`, `rebuild` (alias `rb`), `tasks`. Force the built-in with `pnpm pm <name>`.

Related: `computing-software.software-engineering.pnpm.run-script-environment` for the variables scripts see.

## Checked

2026-11-04. Confirmed hidden scripts, the install lifecycle order with and without --prod, pnpm:devPreinstall, the leftover-process rules and the built-in name conflict list against pnpm.io/scripts. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
