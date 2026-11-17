---
id: computing-software.web-development.svelte.testing-vitest
name: testing-vitest
category: computing-software
field: web-development
product: svelte
tags: [vitest-setup, svelte-unit-testing, effect-root-testing, jsdom-component-test, testing-library-svelte]
level: practitioner
status: docs-checked
description: "Test Svelte with Vitest: browser resolve conditions, runes in .svelte.test.js files, $effect.root with flushSync, and component tests with mount, jsdom and Testing Library."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/07-misc/02-testing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Setup: `npm install -D vitest`, import `defineConfig` from `'vitest/config'`, and make Vitest use browser entry points:

```js
resolve: process.env.VITEST ? { conditions: ['browser'] } : undefined
```

Unit tests of `.svelte.js`/`.svelte.ts` modules work like normal. Test files can use runes if the filename includes `.svelte` (e.g. `multiplier.svelte.test.js`).

Effects: wrap the test in `$effect.root` and use `flushSync()` to run pending effects synchronously:

```js
const cleanup = $effect.root(() => {
  let count = $state(0);
  let log = logger(() => count);
  flushSync();
  expect(log).toEqual([0]);
  count = 1;
  flushSync();
  expect(log).toEqual([0, 1]);
});
cleanup();
```

Components: consider testing extracted logic instead. Install jsdom and set `test: { environment: 'jsdom' }` (or `// @vitest-environment jsdom` per file). Then `mount(Component, { target: document.body, props })`, click, `flushSync()`, assert, and `unmount(component)`.

`@testing-library/svelte` streamlines this: `render(Component)`, `screen.getByRole('button')`, `await user.click(button)`. For two-way bindings, context or snippet props, create a wrapper component for the test.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Svelte testing page: Vitest setup, browser resolve conditions, runes in .svelte test files, $effect.root with flushSync, jsdom component tests with mount/unmount and Testing Library, wrapper-component advice. Nothing removed.
