---
id: computing-software.qa-testing-engineering.vitest.cli-related-and-list
name: cli-related-and-list
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [vitest-related, lint-staged-vitest, vitest-list, files-only]
level: practitioner
status: docs-checked
description: "Run only tests covering given source files with vitest related, wire it into lint-staged with --run, and print matching tests with vitest list in JSON or files-only form."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vitest related <files>` runs only tests that cover the listed source files. It follows static imports but not dynamic ones such as `import(filepath)`. Paths are relative to the root.

```bash
vitest related /src/index.ts /src/hello-world.js
```

Under `lint-staged`, add `--run` so the command exits (watch mode is on by default):

```js
export default {
  '*.{js,ts}': 'vitest related --run',
}
```

`vitest list` inherits the `vitest` options and prints matching tests; it ignores `reporters`.

```bash
vitest list filename.spec.ts -t="some-test"
vitest list filename.spec.ts -t="some-test" --json=./file.json
vitest list --filesOnly
```

`--json` without a value prints JSON to stdout. Since Vitest 5, `list` parses files statically instead of running them; `--no-static-parse` runs them, and `--static-parse-concurrency` caps parsing concurrency (default `os.availableParallelism()`).

## Checked

2026-11-04. Confirmed against guide/cli.md, sections vitest related and vitest list: static versus dynamic imports, `--run` for lint-staged, `--json`, `--filesOnly`, Vitest 5 static parsing, `--no-static-parse`, `--static-parse-concurrency`.

Method: documentation only; no commands were run.
