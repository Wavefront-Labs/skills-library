---
id: computing-software.qa-testing-engineering.vitest.coverage-providers
name: coverage-providers
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [coverage, v8-coverage, istanbul-coverage, coverage-provider]
level: intro
status: docs-checked
description: "Turn on Vitest coverage with --coverage, choose between the v8 (default) and istanbul providers, and install @vitest/coverage-v8 or @vitest/coverage-istanbul."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/coverage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```json
{ "scripts": { "test": "vitest", "coverage": "vitest run --coverage" } }
```

Or `test.coverage.enabled: true` in config. Select the provider with `test.coverage.provider` (`'v8'` or `'istanbul'`). Vitest prompts to install the package, or install manually: `npm i -D @vitest/coverage-v8` or `@vitest/coverage-istanbul`.

v8 (default):
- native, no pre-instrumentation, faster and lower memory
- since 3.2.0 it uses AST-based remapping, giving reports as accurate as istanbul
- needs a V8 runtime (Node, Deno, Chromium); does not work on Firefox, Bun or runtimes without profiler coverage such as Cloudflare Workers
- can be slower when loading very many modules, since V8 cannot limit collection to specific modules

istanbul:
- instruments source code, so it runs on any JavaScript runtime
- slower and heavier in memory, but can limit instrumentation to specific files

A custom provider: `provider: 'custom'` plus `customProviderModule`.

In agent environments Vitest sets `skipFull: true` on the text reporter and adds `text-summary` automatically.

Reports go through `coverage.reporter`; see the include/exclude skill for scope.

## Checked

2026-11-04. Confirmed against guide/coverage.md: `--coverage` and `coverage.enabled`, provider choice and v8 default, install packages and the install prompt, v8 and istanbul pros and cons, v3.2.0 AST remapping, runtime support, custom provider, agent-environment reporter changes.

Method: documentation only; no commands were run.
