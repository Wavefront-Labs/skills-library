---
id: computing-software.qa-testing-engineering.vitest.browser-mode-setup
name: browser-mode-setup
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [browser-mode, vitest-init-browser, playwright-provider, webdriverio-provider]
level: practitioner
status: docs-checked
description: "Set up Vitest browser mode: vitest init browser, choose a provider (playwright, webdriverio, preview), enable it with at least one instance, and know the default port."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/browser/index.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/debugging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Quick start: `npx vitest init browser` installs dependencies and creates browser configuration.

Manual install, one provider package:
- `@vitest/browser-playwright` (the docs recommend starting with Playwright if you use none of these tools, because it supports parallel execution)
- `@vitest/browser-webdriverio`
- `@vitest/browser-preview` (for previewing only; it simulates events instead of using Chrome DevTools Protocol)

To run in CI you need `playwright` or `webdriverio` installed.

```ts
import { defineConfig } from 'vitest/config'
import { playwright } from '@vitest/browser-playwright'

export default defineConfig({
  test: {
    browser: {
      provider: playwright(),
      enabled: true,
      instances: [{ browser: 'chromium' }], // at least one instance is required
    },
  },
})
```

- Add your framework's Vite plugin to `plugins` (react, vue, svelte, solid and others).
- Vitest uses port 23315 for the browser server so it does not clash with a dev server; change it with the `api` option.
- Debug with `--inspect-brk --browser --no-file-parallelism`.

`browser` is not an environment; to run part of your tests in Node and part in a browser, use projects (see browser-and-node-projects).

## Checked

2026-11-04. Confirmed against guide/browser/index.md (`vitest init browser`, provider packages, config, instance requirement, port 23315 and the `api` option, CI needing playwright or webdriverio) and guide/debugging.md (`--inspect-brk --browser --no-file-parallelism`).

Method: documentation only; no commands were run.
