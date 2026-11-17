---
id: computing-software.web-development.storybook.install-storybook
name: install-storybook
category: computing-software
field: web-development
product: storybook
tags: [install, create-storybook, setup, cli, getting-started]
level: intro
status: docs-checked
description: "Install Storybook in an existing project with the create command and choose features or project type."
sources:
  - https://storybook.js.org/docs/get-started/install
  - https://storybook.js.org/docs/api/cli-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install Storybook

Goal: add Storybook to an existing app with one command.

Run from the project root:

```shell
npm create storybook@latest
```

With yarn use `yarn create storybook@latest`. With pnpm 10 or later use `pnpm --allow-build=esbuild create storybook@latest`, because pnpm blocks esbuild's postinstall script until approved. Storybook detects your package manager; force one with `--package-manager`.

Choose features with the flag, for example `--features docs test a11y`. If auto-detection of the project fails, pass `--type` explicitly.

Requirements (Node, package manager and framework versions) change between releases and the published page and the main-branch docs disagreed when read. Check the install page for the current list before installing.

`storybook init` still works for backwards compatibility, but `create storybook` is the documented route.

Verify: the dev server starts and the example stories appear in the sidebar.

## Checked
Date: 2026-11-04. Read the Install page and CLI options page (storybookjs/storybook main branch docs, commit e4ec607) and compared the install page with the live site.
Confirmed: create command forms, pnpm esbuild note, `--features`, `--package-manager`, `--type`, `init` kept for compatibility.
Conflict: the requirements list differs between the published page and the main branch docs, so the numbers were removed. Also removed `--install-typescript`, the `ai` feature, `--yes` and the default port, which the pages read did not confirm.
Method: documentation only; no commands were run.
