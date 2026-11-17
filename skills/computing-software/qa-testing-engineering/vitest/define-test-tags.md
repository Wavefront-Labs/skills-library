---
id: computing-software.qa-testing-engineering.vitest.define-test-tags
name: define-test-tags
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [test-tags, tags-config, strict-tags, tag-priority]
level: practitioner
status: docs-checked
description: "Define Vitest tags in config with shared timeout and retry options, resolve conflicts by priority, apply tags to tests and suites, and type the allowed names."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/test-tags.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/projects.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tags (Vitest 4.1+) must be defined in config; an undefined tag throws unless `strictTags` is disabled.

```ts
export default defineConfig({
  test: {
    tags: [
      { name: 'db', description: 'Tests for database queries.', timeout: 60_000 },
      { name: 'flaky', retry: process.env.CI ? 3 : 0, timeout: 30_000, priority: 1 },
    ],
  },
})
```

Use them on tests or suites (suite tags are inherited):

```ts
test('renders homepage', { tags: ['frontend'] }, () => {})
describe('API', { tags: ['backend'] }, () => {})
```

Conflicts: lower `priority` wins, then order in the test's `tags` array. Options on the test itself always win; options set to `undefined` are ignored. A project's own `tags` replace the inherited array.

A JSDoc `@module-tag name` at file top tags every test in the file, even if written beside one test.

Type-check names by augmenting `TestTags` with `tags: 'frontend' | 'db'`. List them with `vitest --list-tags` (or `--list-tags=json`). Names cannot be `and`, `or`, `not` or contain spaces or `( ) & | ! *`.

## Checked

2026-11-04. Confirmed against guide/test-tags.md (version 4.1.0, config definition and `strictTags`, priority resolution, test-level options winning, `undefined` ignored, suite inheritance, `@module-tag`, `TestTags` augmentation, `--list-tags`, reserved names) and guide/projects.md (project `tags` replace the inherited array).

Method: documentation only; no commands were run.
