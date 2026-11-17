---
id: computing-software.qa-testing-engineering.vitest.filter-files-names-lines
name: filter-files-names-lines
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [test-name-pattern, file-filter, line-number-filter, experimental-preparse]
level: intro
status: docs-checked
description: "Narrow a Vitest run by file path, by test name with -t, and by file:line, and pass a file with the name filter to avoid per-file overhead."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/filtering.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
File name: `vitest basic` runs files whose path contains `basic`.

Test name: `-t` / `--testNamePattern` takes a regex matched against the full name, the `describe` names and test name joined with `' > '` (for example `math > adds`).

```bash
vitest -t "handles empty input"
vitest utils -t "handles empty input"
```

Line number (Vitest 3+): needs the full filename, relative or absolute, with the extension.

```bash
vitest basic/foo.test.ts:10                       # ok
vitest basic/foo.test.ts:10 basic/foo.test.ts:25  # ok, space-separated
vitest foo:10                                     # no: partial name
vitest basic/foo.test.ts:10-25                    # no: ranges unsupported
```

Performance: `-t`, `--tags-filter`, `.only` and `.skip` apply per test file, so Vitest still runs each file to discover matches. Always pass a file path with the filter. Alternatively `--experimental.preParse` parses files to find test names without executing them.

## Checked

2026-11-04. Confirmed against guide/filtering.md: file-name filter, `-t` regex and the ` > ` joined full name, line-number rules and the accepted and rejected forms, the performance note and `--experimental.preParse`; and guide/cli.md for the Vitest 3 line-number feature.

Method: documentation only; no commands were run.
