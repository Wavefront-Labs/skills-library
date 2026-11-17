---
id: computing-software.qa-testing-engineering.vitest.junit-json-html-files
name: junit-json-html-files
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [junit-reporter, json-reporter, output-file, html-reporter]
level: practitioner
status: docs-checked
description: "Write Vitest json, junit and html output to files: default .vitest paths, outputFile as string or per-reporter map, and the stdout option and its pitfalls."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/reporters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default locations:
- `json` writes `.vitest/json/output.json`
- `junit` writes `.vitest/junit/output.xml`
- `html` writes `.vitest/index.html` (option `outputDir`)

Override `json` and `junit` with `outputFile`:

```bash
npx vitest --reporter=json --outputFile=./test-output.json
```

```ts
export default defineConfig({
  test: {
    reporters: ['junit', 'json', 'verbose'],
    outputFile: {
      junit: './junit-report.xml',
      json: './json-report.json',
    },
  },
})
```

A reporter option wins over the top-level setting: `[['json', { outputFile: './out.json' }]]`.

Print to the terminal instead of a file with `[['json', { stdout: true }]]` (ignored when `outputFile` is set).

With `stdout` the JSON or XML can be interleaved with other output (`process.stdout.write` in tests, global setup logs) and become unparsable. Use file output when a tool consumes the data.

Add `.vitest/` to `.gitignore`.

## Checked

2026-11-04. Confirmed against guide/reporters.md: default output paths for json, junit and html, `outputFile` as CLI, string or per-reporter map, the reporter option taking precedence, `stdout` and its interleaving warning, and `outputDir` for html. The gitignore line is from guide/index.md, which is not cited here.

Method: documentation only; no commands were run.
