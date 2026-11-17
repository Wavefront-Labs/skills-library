---
id: computing-software.qa-testing-engineering.vitest.browser-and-node-projects
name: browser-and-node-projects
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [browser-projects, mixed-test-types, unit-and-browser, browser-instances]
level: advanced
status: docs-checked
description: "Run Node unit tests and browser-mode tests in one Vitest run by defining separate projects, each with its own include patterns, name and browser config."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/browser/index.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/environment.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Environments (`node`, `jsdom`, `happy-dom`, `edge-runtime`) exist only for Node runs. Browser mode is a different runner, so mix them with projects:

```ts
import { defineConfig } from 'vitest/config'
import { playwright } from '@vitest/browser-playwright'

export default defineConfig({
  test: {
    projects: [
      {
        test: {
          name: 'unit',
          include: ['tests/unit/**/*.{test,spec}.ts'],
          environment: 'node',
        },
      },
      {
        test: {
          name: 'browser',
          include: ['tests/browser/**/*.{test,spec}.ts'],
          browser: {
            enabled: true,
            provider: playwright(),
            instances: [{ browser: 'chromium' }],
          },
        },
      },
    ],
  },
})
```

The file naming convention is up to you; the docs call the patterns just an example.

Run a single project with `vitest --project browser`.

In browser mode you cannot `vi.spyOn` module exports because the module namespace object is sealed; use `vi.mock(path, { spy: true })`.

## Checked

2026-11-04. Confirmed against guide/browser/index.md (projects example, provider and instances config, sealed namespace and `{ spy: true }`), guide/environment.md (environments exist only for Node runs; browser is not an environment) and guide/projects.md (`--project` filter).

Method: documentation only; no commands were run.
