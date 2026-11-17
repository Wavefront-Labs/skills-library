---
id: computing-software.web-development.bun.test-run-flags
name: test-run-flags
category: computing-software
field: web-development
product: bun
tags: [bun-test, test-discovery, test-name-pattern, flaky-tests]
level: intro
status: docs-checked
description: "Run bun test: file discovery and filters, name patterns, timeout, bail, retry, randomize and seed, rerun-each, concurrency and type-checking."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/test/index.mdx
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/test/discovery.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Discovery: recursively finds `*.test.*`, `*_test.*`, `*.spec.*`, `*_spec.*` (js, jsx, ts, tsx, mjs, cjs, mts, cts). It skips `node_modules` and hidden directories. Set `[test] root = "src"` in `bunfig.toml` to limit scanning.

```bash
bun test utils                          # substring filter, NOT a glob
bun test ./test/specific-file.test.ts   # exact file needs ./ or /
bun test --files-from list.txt          # one path per line; a filter alongside is an error
bun test -t "Math operations"           # regex on describe-prefixed test name
bun test --timeout 10000 --bail=3
bun test --retry 3 --rerun-each 20
bun test --randomize                    # prints seed
bun test --seed 123456                  # implies --randomize
bun test --concurrent --max-concurrency 4
bun test --check                        # type-check first; errors exit 1, no tests run
bun test --preload ./setup.ts --watch
```

- Default timeout 5000 ms; `--bail` alone stops after the first failure; `--max-concurrency` defaults to 20.
- `test.serial` opts a test out of `--concurrent`.

Gotchas:
- Without `--parallel` all files share one global, so state can leak between files.
- A test passing on a retry counts as passing.
- Without `--check` types are not verified.
- With `CLAUDECODE=1`, `REPL_ID=1` or `AGENT=1`, output shows only failures and summary.

## Checked

2026-11-04. Confirmed against the Bun docs pages test/index and test/discovery: discovery patterns and exclusions, substring filters, ./ prefix, --files-from, -t matching on describe-prefixed names, root in bunfig, timeout default 5000, --bail, --retry, --rerun-each, --randomize and --seed, --concurrent, --max-concurrency default 20, test.serial, --check exit code 1, agent environment variables. Reworded the --files-from note (the page says a filter on the command line is an error, extra paths are allowed).
Method: documentation only; no commands were run.
