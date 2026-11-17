---
id: computing-software.qa-testing-engineering.vitest.install-vitest
name: install-vitest
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [install-vitest, node-requirement, npx-vitest, vitest-gitignore]
level: intro
status: docs-checked
description: "Install Vitest with npm, yarn, pnpm, bun or deno, know the Vite and Node minimums, run it with npx, and git-ignore the .vitest artifacts directory."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install as a dev dependency:

```bash
npm install -D vitest
yarn add -D vitest vite
pnpm add -D vitest
bun add -D vitest
deno add -D vitest
```

Requirements per the guide: Vite >= v6.4.0 and Node >= v22.12.0.

Installing a copy of `vitest` in `package.json` is recommended. If you prefer to run it directly, `npx vitest` checks local project binaries first, then `$PATH`, then installs to a temporary location.

Vitest and third-party integrations can store generated artifacts in a `.vitest` directory. Add it to `.gitignore`:

```sh
# Vitest reports and artifacts
.vitest/
```

You can try Vitest with no install on StackBlitz (vitest.new); it runs in the browser.

With Bun as package manager use `bun run test`, not `bun test`, or Bun runs its own test runner.

## Checked

2026-11-04. Confirmed against guide/index.md: install commands per package manager, Vite >=6.4.0 and Node >=22.12.0, the `npx` lookup order, the `.vitest` artifacts directory and gitignore advice, StackBlitz, and the Bun warning.

Method: documentation only; no commands were run.
