---
id: computing-software.web-development.storybook.vitest-addon-setup
name: vitest-addon-setup
category: computing-software
field: web-development
product: storybook
tags: [vitest-addon, storybook-test, browser-mode, playwright, component-tests]
level: practitioner
status: docs-checked
description: "Install the Vitest addon so stories run as component tests in Storybook, the terminal and CI."
sources:
  - https://storybook.js.org/docs/writing-tests/integrations/vitest-addon
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vitest addon setup

Goal: turn stories into component tests with Vitest browser mode.

Requirements:
- A Vite-based Storybook framework (for example `react-vite`, `vue3-vite`, `nextjs-vite`); Webpack projects must migrate to Vite first
- Vitest 3.0 or newer (installed for you if missing)
- Optional MSW 2.0 or newer
- Next.js 14.1+ only with `@storybook/nextjs-vite`

Automatic install:

```shell
npx storybook add @storybook/addon-vitest
```
It registers the addon, inspects Vite and Vitest config, creates or adjusts Vitest config with sensible defaults, sets up browser mode with Playwright Chromium and offers to install browser binaries (answer Yes; or run `playwright install` later).

Manual setup: configure Vite and Vitest, enable Vitest browser mode, install `@storybook/addon-vitest`, register it in `main.ts`, and add the `storybookTest` plugin to a Vitest project (use a separate test project if you already have Vitest tests).

Use: press Run tests in the sidebar testing widget, run a single story or group from the sidebar item menu, or toggle watch mode (eye icon). Status indicators appear on sidebar items.

CLI: `vitest --project=storybook` (the page suggests it as a `test-storybook` script). Stories are tested with a smoke test (it renders) and, if defined, the play function and its assertions. By default stories with the `test` tag run. The testing widget shows total, passed and failed counts, and pressing the failure number filters the sidebar to failing stories.

## Checked

Method: 2026-11-08 read docs/writing-tests/integrations/vitest-addon/index.mdx from the Storybook repo. Requirements, automatic install steps, manual setup, usage and CLI match the page; added how-it-works and widget details and removed a Verify step.
