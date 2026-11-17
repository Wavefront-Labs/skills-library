---
id: computing-software.web-development.storybook.mocking-modules-sb-mock
name: mocking-modules-sb-mock
category: computing-software
field: web-development
product: storybook
tags: [sb-mock, automock, mock-modules, spy-only, module-mocking]
level: advanced
status: docs-checked
description: "Automock local modules and packages with sb.mock in the preview file, as spy-only or fully mocked."
sources:
  - https://storybook.js.org/docs/writing-stories/mocking-data-and-modules/mocking-modules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mock modules with sb.mock

Goal: control a component's module dependencies in stories and tests.

Register modules in `.storybook/preview.*` only (not in stories):

```ts
import { sb } from 'storybook/test';

// spy-only: original behavior kept, calls recorded
sb.mock(import('../lib/session.ts'), { spy: true });
sb.mock(import('uuid'), { spy: true });
// fully automocked: exports replaced by mock functions
sb.mock(import('../lib/analytics.ts'));
```

Rules:
- Local module paths must not use an alias or subpath import (`@/lib/...`, `#lib/...`), must be relative to the preview file, and must include the file extension.
- Packages in `node_modules` can be mocked too; for deeper imports register that path (for example `lodash-es/add`).
- Wrapping the path in `import()` gives TypeScript resolution.
- `spy: true` is recommended for most cases; omitting it (or `false`) replaces every export with a Vitest mock function.
- Fully automocked modules are still evaluated along with their dependencies, so side effects of the module still run.
- With the Webpack builder, only `node_modules` packages with ESM entry points can be automocked.
- A third option is a mock file: for a local module, a file in a `__mocks__` directory next to it; for a `node_modules` package, a file in a root `__mocks__` directory. Mock files must be JavaScript using ESM and export the same named exports. `sb.mock` looks for a mock file before automocking.

Then change behavior per story (for example in `beforeEach`) and assert calls in `play`. The mocked functions are Vitest mock functions (`mockReturnValue`, `mockResolvedValue`, `mockImplementation`). There is no `sb.unmock()` and `sb.mock()` takes no factory function, since mocking is resolved at build time.

## Checked

Method: 2026-11-08 compared against the Storybook docs source mdx for Mocking modules (writing-stories/mocking-data-and-modules/mocking-modules). Registration rules, spy-only versus full automock, side-effect warning, Webpack ESM limit and deeper import path claims match the page. Corrected the mock-file bullet to the page's `__mocks__` locations, added the no-factory and no-unmock limits, and dropped an unsupported "Verify" step.
