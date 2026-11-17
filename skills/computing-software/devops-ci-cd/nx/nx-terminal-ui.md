---
id: computing-software.devops-ci-cd.nx.nx-terminal-ui
name: nx-terminal-ui
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, tui, terminal-ui, nx-json, output]
level: intro
status: docs-checked
description: "Enable, disable and configure the Nx Terminal UI: --tui and --no-tui flags, NX_TUI, tui.enabled and tui.autoExit in nx.json."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/kb/terminal-ui.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/environment-variables.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control the interactive Terminal UI (TUI) that shows parallel task results (Nx 21+).

Defaults: enabled automatically for `nx run`, `nx run-many` and `nx affected` when the terminal and environment support it; never used in CI. The Nx 21 initial release disabled it on Windows (per the guide; check current status for your version).

Ways to turn it on or off:
- `nx run-many -t build --no-tui` / `--tui`
- `NX_TUI=false` (or `true`) in the environment
- `nx.json`:

```json
{ "tui": { "enabled": false } }
```

Auto-exit (`tui.autoExit`): default is exit 3 seconds after all tasks finish.
- a number: seconds to wait before exiting
- `false`: stay open until you press ctrl+c
- `true`: exit immediately when tasks finish

```json
{ "tui": { "autoExit": 3 } }
```
`NX_TUI_AUTO_EXIT` (true, false or seconds) is the environment equivalent.

Usage: entirely keyboard driven; press `?` for the shortcut list. You can show or hide up to 2 tasks at a time, filter the task list, and interact with tasks that prompt for input.

## Checked

2026-11-07. Confirmed against Terminal UI and the environment variables reference: Nx 21 introduction, default for nx run, run-many and affected when supported, not used in CI, the Windows note for the initial Nx 21 release, --tui and --no-tui, NX_TUI, tui.enabled, tui.autoExit values (number, false, true) with the 3 second default, NX_TUI_AUTO_EXIT, keyboard control with ? for shortcuts, hiding and showing up to 2 tasks, filtering and interactive tasks. Removed: the precedence ordering (the page lists the options without ranking them) and the invented Verify step.

Method: documentation only; no commands were run.
