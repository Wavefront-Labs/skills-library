---
id: computing-software.qa-testing-engineering.vitest.rerun-last-failed-and-changed
name: rerun-last-failed-and-changed
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [last-failed, since-last-run, results-cache, affected-tests]
level: practitioner
status: docs-checked
description: "Rerun only failing or affected tests with --last-failed and the experimental --since-last-run, and know their cache requirement and blind spots."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--last-failed` runs only the tests that failed in the last run, read from the results cache. A file that failed outside a test (a `beforeAll` hook, collection) runs completely. Tests are selected by full name, so a renamed test waits for a run without the flag. With no failures Vitest prints `No failed tests found` and exits 1 unless `--passWithNoTests` is set. It combines with filters: `vitest run --last-failed -t login`. In watch mode only the first run is limited.

`--since-last-run` (experimental, 5.1.0) runs tests whose loaded files have a newer modification time than their last run, or were deleted. A test never run with the flag, or whose file failed last time, always runs.

```sh
vitest run --since-last-run
```

It enables `changed`, `experimental.recordDependencies` and the `mtime` provider, and requires `cache`; Vitest throws if the cache is disabled. Warnings: it reads file system mtimes, so a checkout setting old times is missed, and files a test did not load (a new `.env`, a new `__mocks__` file) are not detected. Run without the flag, or use `--clearCache`, to run everything.

## Checked

2026-11-04. Confirmed against guide/cli.md: `--last-failed` and `--since-last-run` behaviour, the experimental 5.1.0 tag, enabled options, the cache requirement, the warnings, `No failed tests found` with exit code 1, and the combination with `-t`.

Method: documentation only; no commands were run.
