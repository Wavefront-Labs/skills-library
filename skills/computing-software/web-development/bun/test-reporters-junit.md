---
id: computing-software.web-development.bun.test-reporters-junit
name: test-reporters-junit
category: computing-software
field: web-development
product: bun
tags: [junit-reporter, dots-reporter, ci-annotations, reporter-outfile]
level: intro
status: docs-checked
description: "Choose bun test reporters: default, dots and JUnit XML with flat or nested suites, bunfig settings, GitHub Actions annotations and JUnit report quirks."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/test/reporters.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
bun test --dots                                  # or --reporter=dots
bun test --reporter=junit --reporter-outfile=./junit.xml
bun test --reporter=junit --reporter-outfile=./junit.xml --reporter-junit-suites=flat
```

```toml
[test.reporter]
junit = "path/to/junit.xml"
junitSuites = "flat"       # default "nested"
```

- GitHub Actions: Bun detects the environment and emits annotations with no extra configuration.
- Flat suites prefix each test name with its describe blocks.
- Retried tests: earlier attempts appear as `<flakyFailure>` (eventual pass) or `<rerunFailure>` (final fail) in one `<testcase>`.
- JUnit `<properties>` include CI run info (`GITHUB_RUN_ID`, `GITHUB_REPOSITORY`...), commit SHA and hostname.

Gotchas:
- Console output is unchanged with JUnit; the XML is written only at the end of the run, creating missing folders.
- Every test file gets a `<testsuite>`, even with no tests.
- Uncaught exceptions or unhandled rejections get `uncaught="true"`; load-time errors show as a failed `(unhandled error)` testcase.
- With `--parallel`, crashes appear as `(worker crashed)`, `(aborted)` or `(interrupted)` testcases.
- JUnit lacks per-test stdout/stderr and precise timestamps.

## Checked

2026-11-04. Confirmed against the Bun docs page test/reporters: --dots and --reporter=dots, --reporter=junit with --reporter-outfile, [test.reporter] junit and junitSuites keys (nested default, flat), flat name prefixing, flakyFailure and rerunFailure for retried tests, properties from CI environment variables and hostname, uncaught=true, (unhandled error), (worker crashed), (aborted), (interrupted), a testsuite per file, GitHub Actions annotations, and the stdout/timestamp limitations. Nothing removed.
Method: documentation only; no commands were run.
