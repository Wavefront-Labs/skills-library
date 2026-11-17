---
id: computing-software.web-development.bun.test-coverage
name: test-coverage
category: computing-software
field: web-development
product: bun
tags: [code-coverage, coverage-threshold, lcov, coverage-ignore]
level: practitioner
status: docs-checked
description: "Collect coverage with bun test --coverage: lcov reports, bunfig thresholds that fail the run, path ignores, and which files are and are not tracked."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/test/code-coverage.mdx
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/bunfig.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
bun test --coverage
bun test --coverage --coverage-reporter=lcov     # writes coverage/lcov.info
```

```toml
[test]
coverage = true                                  # off by default
coverageThreshold = { lines = 0.9, functions = 0.9 }   # or a single number
coverageReporter = ["text", "lcov"]
coverageDir = "coverage"
coverageSkipTestFiles = false                    # false includes test files; set it explicitly
coveragePathIgnorePatterns = ["**/*.spec.ts", "src/utils/**"]
```

Behaviour:
- If line or function coverage falls below a threshold, `bun test --coverage` exits non-zero. Omitted keys in the object form default to 0.9.
- `statements` is accepted but not enforced.
- Outside `--parallel`, the threshold is checked only when the `text` reporter is enabled; with only `lcov` the run exits 0 regardless.

Gotchas:
- `node_modules` is excluded by default, as are files loaded by non-JS loaders (`.css`, `.txt`). The coverage page says test files are skipped by default but the bunfig page lists `coverageSkipTestFiles` as `false`, so set it explicitly.
- Only files that tests actually load are tracked; import a missing file in a test.
- `coverageIgnoreSourcemaps` is rarely useful; if used, add `// @bun` at the top of the source.
- Coverage measures execution, not assertion quality.

CI: `bun test --coverage --coverage-reporter=lcov` then upload `./coverage/lcov.info`.

## Checked

2026-11-04. Confirmed against the Bun docs pages test/code-coverage and runtime/bunfig: --coverage, lcov output to coverage/lcov.info, coverage/coverageDir/coverageReporter/coverageThreshold keys and defaults, 0.9 default for omitted threshold keys, statements not enforced, text-reporter-only threshold check, coveragePathIgnorePatterns globs, node_modules and non-JS loader exclusions, loaded-files-only tracking, coverageIgnoreSourcemaps with the // @bun note. The two pages disagree on the coverageSkipTestFiles default (true versus false), so the default claim was removed and the skill says to set it explicitly.
Method: documentation only; no commands were run.
