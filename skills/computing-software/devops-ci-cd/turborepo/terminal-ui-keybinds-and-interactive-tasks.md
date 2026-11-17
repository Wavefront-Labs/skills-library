---
id: computing-software.devops-ci-cd.turborepo.terminal-ui-keybinds-and-interactive-tasks
name: terminal-ui-keybinds-and-interactive-tasks
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, terminal-ui, tui, keybinds, interactive-tasks, task-list, log-scrolling, drizzle-migrations]
level: practitioner
status: docs-checked
description: "Navigate the Turborepo terminal UI with keybinds, pin tasks, scroll logs, and type input into tasks marked interactive."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/developing-applications.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Turborepo's terminal UI gives an interactive view over tasks.

**Customising the view**
- `m`: toggle a popup listing keybinds.
- Up/down arrows or `j`/`k`: select the next/previous task in the task list.
- `p`: toggle selection pinning for the selected task.
- `h`: toggle visibility of the task list.
- `c`: when logs are highlighted, copy the selection to the system clipboard.
- `u`/`d`: scroll logs up and down.

**Interacting with tasks.** Some tools accept typed input, for example Drizzle ORM's interactive migrations or Jest's filtering and re-running of test suites. You can interact with tasks that are marked as interactive (the `interactive` key in the configuration reference):
- `i`: begin interacting.
- `Ctrl+z`: stop interacting.

The docs describe `"persistent": true` as a signal for the terminal UI to treat a task as long-running and interactive.

## Checked

2026-11-04. Read the "Using the terminal UI" section and the `persistent` bullet of the Developing applications page: both keybind tables and the Drizzle/Jest examples match. Removed the unsupported pointer to a `ui` setting and the invented Verify step.

Method: documentation only; no commands were run.
