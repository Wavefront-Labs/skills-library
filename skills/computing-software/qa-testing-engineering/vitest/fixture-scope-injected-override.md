---
id: computing-software.qa-testing-engineering.vitest.fixture-scope-injected-override
name: fixture-scope-injected-override
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [fixture-scope, injected-fixture, test-override, worker-scope]
level: advanced
status: docs-checked
description: "Set Vitest fixture scope to test, file or worker, follow the scope access rules, inject values from project config, and override fixtures with test.override."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/test-context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`scope` takes `'test'` (default), `'file'` or `'worker'`. A worker fixture can use only worker fixtures; a file fixture can use worker and file ones; a test fixture can use everything.

```ts
export const test = baseTest
  .extend('config', { scope: 'worker' }, () => loadConfig())
  .extend('database', { scope: 'file' }, async ({ config }, { onCleanup }) => {
    const db = await connect(config)
    onCleanup(() => db.close())
    return db
  })
  .extend('baseUrl', { injected: true }, () => '/default')
```

In the object syntax, group fixtures under `$worker`, `$file` and `$test` keys to type scopes.

`injected: true` makes the default overridable from the project `provide` config.

Override for a suite and its children with `test.override` (4.1.0; `test.scoped` is deprecated):

```ts
describe('staging', () => {
  test.override('config', { port: 8080, host: 'api.example.com' })
  // or object form: test.override({ config: {...} })
})
```

Limits: `override` cannot add new fixtures, cannot change `scope` or `auto`, and non-test-scope fixtures cannot be overridden inside `describe` blocks. `override` returns the test API, so calls chain.

## Checked

2026-11-04. Confirmed against guide/test-context.md: the three scopes and the scope hierarchy table, `$worker`, `$file` and `$test` typing keys, `injected: true` with project `provide`, `test.override` (4.1.0) in builder and object forms, its limits, chaining, and `test.scoped` being deprecated.

Method: documentation only; no commands were run.
