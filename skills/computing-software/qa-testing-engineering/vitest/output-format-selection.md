---
id: computing-software.qa-testing-engineering.vitest.output-format-selection
name: output-format-selection
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [reporters, verbose-reporter, github-actions-reporter, config-defaults-reporters]
level: intro
status: docs-checked
description: "Pick Vitest reporters with --reporter or config, know the auto-selected defaults, pass reporter options, and combine several without losing the defaults."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/reporters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
npx vitest --reporter=verbose
npx vitest --reporter=json --reporter=default
```

```ts
import { configDefaults, defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    reporters: [
      'json',
      ...configDefaults.reporters,
      ['junit', { suiteName: 'UI tests' }],
    ],
  },
})
```

Defaults when `reporters` is not set:
- `default` in a normal terminal run
- `minimal` when an AI coding agent is detected
- `github-actions` added when `process.env.GITHUB_ACTIONS === 'true'`

A configured list replaces the defaults, so spread `configDefaults.reporters` to keep them.

Details:
- `default` shows a summary; disable with `['default', { summary: false }]`. With one file, or a failure, it prints the test tree.
- `verbose` prints every finished test; with `--includeTaskLocation` it adds locations. It is the only terminal reporter that shows annotations on passing tests.
- Reporter-specific options go in a `[name, options]` tuple.

Several reporters can run together. By default the `json`, `junit` and `html` reporters write files under `.vitest/` and the others print to the terminal.

## Checked

2026-11-04. Confirmed against guide/reporters.md: `--reporter` and `reporters`, the three auto-selected defaults, replacement by a configured list and `configDefaults.reporters`, `[name, options]` tuples, the junit `suiteName` option, the default reporter summary option and tree output, the verbose reporter behaviour and its annotation note, and the file outputs of json, junit and html. Removed: a generic combining-reporters gotcha.

Method: documentation only; no commands were run.
