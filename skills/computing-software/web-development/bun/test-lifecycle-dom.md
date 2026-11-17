---
id: computing-software.web-development.bun.test-lifecycle-dom
name: test-lifecycle-dom
category: computing-software
field: web-development
product: bun
tags: [test-hooks, around-each, happy-dom, dom-testing]
level: practitioner
status: docs-checked
description: "Set up bun test lifecycle hooks (including aroundEach and global preload setup) and a DOM environment with happy-dom or jsdom for component tests."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/test/lifecycle.mdx
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/test/dom.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hooks: `beforeAll`/`afterAll` (once per scope), `beforeEach`/`afterEach`, `onTestFinished`, `aroundEach`/`aroundAll` (wrap tests; receive `runTest`, do setup, await it, do teardown). Global setup: put hooks in `setup.ts` and run `bun test --preload ./setup.ts` or set `preload` under `[test]`.

Order: outer `beforeAll`, inner `beforeAll`, outer `beforeEach`, inner `beforeEach`, test, then reverse for after hooks. First-registered `around` hook is outermost.

Gotchas:
- If `beforeAll` throws, every test in its scope is skipped; log and rethrow.
- A test fails if an `around` hook throws or never calls `runTest()`.
- `onTestFinished` is not supported in concurrent tests; use `test.serial`.

DOM:

```bash
bun add -d happy-dom
bun test --environment=happy-dom
```
or `[test] environment = "happy-dom"` (also `jsdom`; default `node` has no DOM). Per file: `// @vitest-environment happy-dom` overrides the project setting. Alternative: `GlobalRegistrator.register()` from `@happy-dom/global-registrator` in a file listed in `preload`.

- Add `/// <reference lib="dom" />` if `document` has a type error.
- Clean up in `afterEach` (RTL `cleanup()`, reset `document.body.innerHTML`).
- Under `--isolate`, arrays that jsdom's own code creates belong to another realm, so `instanceof Array` can fail; use `Array.isArray()`.

## Checked

2026-11-04. Confirmed against the Bun docs pages test/lifecycle and test/dom: hook list, nesting order, aroundEach/aroundAll behaviour and failure rules, onTestFinished limit with concurrent tests, preload setup, beforeAll error rule, environment option in bunfig and --environment, the @vitest-environment comment, happy-dom global-registrator preload, dom reference directive, and the isolate cross-realm array note. Narrowed the instanceof Array gotcha to arrays created by jsdom's own code, as the page states.
Method: documentation only; no commands were run.
