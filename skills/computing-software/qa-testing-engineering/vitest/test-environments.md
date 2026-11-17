---
id: computing-software.qa-testing-engineering.vitest.test-environments
name: test-environments
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [test-environment, jsdom, happy-dom, vitest-environment-comment]
level: practitioner
status: docs-checked
description: "Choose a Vitest environment (node, jsdom, happy-dom, edge-runtime), override it per file with a @vitest-environment comment, and build a custom environment."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/environment.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set `environment` in config; options go in `environmentOptions`. Built in: `node` (default), `jsdom`, `happy-dom` (faster, lacks some APIs), `edge-runtime`.

Per-file override with a control comment at the top:

```ts
// @vitest-environment jsdom
import { expect, test } from 'vitest'

test('has a window', () => {
  expect(typeof window).not.toBe('undefined')
})
```

If importing an external dependency fails with `unknown extension .css` under jsdom or happy-dom, add the whole import chain to `server.deps.inline`.

Custom environment: a package named `vitest-environment-<name>` or a path to a JS/TS file exporting an `Environment` object.

```ts
import type { Environment } from 'vitest/runtime'

export default <Environment>{
  name: 'custom',
  viteEnvironment: 'ssr',
  setup() {
    return { teardown() {} }
  },
}
```

`viteEnvironment` must be `ssr`, `client` or a custom Vite environment name. Add `setupVM()` only if you support `vmForks` or `vmThreads`. `builtinEnvironments` and `populateGlobal` come from `vitest/runtime`.

`browser` is not an environment in Vitest; to run part of your tests in Browser Mode, create a test project.

## Checked

2026-11-04. Confirmed against guide/environment.md: the four built-in environments and node default, `environmentOptions`, the `@vitest-environment` control comment, the `server.deps.inline` advice for `unknown extension .css`, the custom environment shape and `vitest-environment-<name>` naming, the `viteEnvironment` values, `setupVM` for the vm pools, and the `vitest/runtime` exports.

Method: documentation only; no commands were run.
