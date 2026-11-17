---
id: computing-software.software-engineering.pnpm.pm-builtin-vs-script
name: pm-builtin-vs-script
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-pm, script-override, builtin-command, script-override-in-workspace-root, pnpm-clean]
level: practitioner
status: docs-checked
description: "Resolve clashes between package.json scripts and pnpm built-in commands: which commands a script overrides, pnpm pm <command>, and ERR_PNPM_SCRIPT_OVERRIDE_IN_WORKSPACE_ROOT."
sources:
  - https://pnpm.io/cli/pm
  - https://pnpm.io/cli/run
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`pnpm pm <command>` always runs the built-in command, bypassing a same-named script.

Commands that run a same-named script when one exists: `clean` (alias `purge`), `rebuild` (alias `rb`), `deploy`, `setup`, `tasks`. An alias looks up its own script name: `pnpm rb` runs a script called `rb`, not `rebuild`.

```json
{ "scripts": { "clean": "rm -rf dist" } }
```

```sh
pnpm clean          # runs the script
pnpm run clean      # same
pnpm pm clean       # built-in pnpm clean
```

In a workspace, running one of these from a subdirectory fails with `ERR_PNPM_SCRIPT_OVERRIDE_IN_WORKSPACE_ROOT` if the root `package.json` has a script of that name. Run `pnpm pm <command>` for the built-in, or `pnpm run <command>` from the workspace root for the script.

Related shorthand rule: `pnpm <script>` works only when the script name is not a pnpm command; built-in commands win, except those listed above.

## Checked

2026-11-04. Confirmed the override command list, alias rule, example and ERR_PNPM_SCRIPT_OVERRIDE_IN_WORKSPACE_ROOT against pnpm.io/cli/pm, and the shorthand rule against pnpm.io/cli/run. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
