---
id: computing-software.qa-testing-engineering.vitest.filter-by-tags-expression
name: filter-by-tags-expression
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [tags-filter, tag-expression, tag-wildcard, matches-tags]
level: practitioner
status: docs-checked
description: "Select tests with --tags-filter expressions using and, or, not, wildcards and parentheses, combine multiple flags, and check the filter at runtime with TestRunner.matchesTags."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/test-tags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Operators: `and`/`&&`, `or`/`||`, `not`/`!`, `*` wildcard, `()` grouping. Precedence: not, then and, then or.

```shell
vitest --tags-filter="frontend && !flaky"
vitest --tags-filter="(unit || e2e) && !slow"
vitest --tags-filter="unit/*"
vitest --tags-filter="unit || e2e" --tags-filter="!slow"
```

Multiple `--tags-filter` flags combine with AND. In Vitest UI, start the filter text with `tag:`. Programmatically pass `tagsFilter` to `startVitest`/`createVitest`, or `testTagsFilter` when creating a specification.

Skip expensive setup when no relevant test is scheduled:

```ts
import { beforeAll, TestRunner } from 'vitest'

beforeAll(async () => {
  if (TestRunner.matchesTags(['db'])) await seedDatabase()
})
```

`matchesTags` returns true if the current filter would include a test with those tags, and always true when no filter is active.

Tags suit cross-cutting categories; use projects when categories need different isolation, pool or environment.

## Checked

2026-11-04. Confirmed against guide/test-tags.md: operators and precedence, wildcard, parentheses, multiple flags combined with AND, `tag:` prefix in Vitest UI, `tagsFilter` and `testTagsFilter`, `TestRunner.matchesTags` behaviour.

Method: documentation only; no commands were run.
