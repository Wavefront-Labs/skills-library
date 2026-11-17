---
id: computing-software.web-development.storybook.test-coverage
name: test-coverage
category: computing-software
field: web-development
product: storybook
tags: [coverage, vitest-coverage, istanbul, v8-coverage, test-coverage]
level: practitioner
status: docs-checked
description: "Generate code coverage from story tests with the Vitest addon, CLI and CI."
sources:
  - https://storybook.js.org/docs/writing-tests/test-coverage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Test coverage

Goal: see which source lines your stories exercise.

Coverage is part of the Vitest addon. Install a provider: `@vitest/coverage-v8` (default) or `@vitest/coverage-istanbul`. Enable it by ticking the coverage checkbox in the testing widget; the summary appears after a run and the full report is served at `/coverage/index.html` of the running Storybook.

UI limits:
1. Coverage is computed from stories only, not other Vitest tests.
2. It covers all stories, not one story or a group.
3. It is not calculated while watch mode is on (enabling watch mode disables coverage).

CLI:

```shell
npx vitest --project=storybook --coverage
```
Reports go to the configured reports directory (`./coverage` by default) and only include story coverage. To include every test in the repo run `npx vitest --coverage`. Vitest IDE extensions also show coverage, including all tests.

CI: the page's GitHub Actions example runs the whole project's tests with `--coverage` (`yarn test --coverage`), because a coverage report is most accurate when it accounts for all tests, not just stories. It does not mention uploading artifacts.

Configuration (Vitest config):
- `coverage.provider` is `'v8'` by default or `'istanbul'`.
- Watermarks: `coverage.watermarks.statements` defaults to `[50, 80]`; the widget icon is red below the low value, orange between, green above the high value.
- In the Storybook UI these options are always ignored: `enabled`, `clean`, `cleanOnRerun`, `reportOnFailure`, `reporter`, `reportsDirectory`.
- The Vitest addon requires a Vite-based framework.

## Checked

Method: 2026-11-08 read docs/writing-tests/test-coverage.mdx from the Storybook repo. Setup, UI limits and CLI claims match; corrected the CI step (full test run, no artifact upload), added watermarks and ignored options, removed a Verify step. The CLI command line is derived from the page's `vitest --project=storybook` script plus `--coverage`; its snippet was not read.
