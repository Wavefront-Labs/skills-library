---
id: computing-software.qa-testing-engineering.vitest.coverage-include-exclude-ignore
name: coverage-include-exclude-ignore
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [coverage-include, coverage-exclude, ignore-hints, coverage-reporter]
level: practitioner
status: docs-checked
description: "Scope Vitest coverage with coverage.include and exclude to show uncovered files, ignore code with v8 or istanbul hints plus @preserve, and add custom reporters."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/coverage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the report lists only files imported during the run. To include untested source files, set `coverage.include`; trim with `coverage.exclude`.

```ts
export default defineConfig({
  test: {
    coverage: {
      include: ['src/**/*.{ts,tsx}'],
      exclude: ['**/utils/users.ts'],
    },
  },
})
```

Ignore hints (each provider has its own; TypeScript is transpiled by esbuild, which strips comments, so add `@preserve`):

```ts
/* v8 ignore next -- @preserve */
/* v8 ignore start -- @preserve */
/* v8 ignore stop -- @preserve */
/* v8 ignore if -- @preserve */
/* istanbul ignore if -- @preserve */
```

Also `v8 ignore else`, `v8 ignore file`, and `istanbul ignore start` / `stop`.

Reporters: `coverage.reporter` takes names, `[name, options]` tuples, or a custom reporter from a package or an absolute path. The HTML reporter has a `theme` option (`'light'`, `'dark'`, `'legacy'`) and shows in Vitest UI.

The docs warn that hints carrying `@preserve` may now be included in the final production build as well.

## Checked

2026-11-04. Confirmed against guide/coverage.md: default of only imported files, `coverage.include` and `exclude` examples, esbuild comment stripping and `@preserve`, the v8 and istanbul hint examples, custom reporters by package name or absolute path, HTML reporter `theme` values, Vitest UI integration. Changed one example hint to `istanbul ignore if`, which is the istanbul form the page shows.

Method: documentation only; no commands were run.
