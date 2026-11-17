---
id: computing-software.qa-testing-engineering.vitest.cli-run-and-watch
name: cli-run-and-watch
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [vitest-watch, vitest-dev-alias, ci-run-mode, filename-filter]
level: intro
status: docs-checked
description: "Use the vitest, vitest run, vitest watch and vitest dev commands: watch versus run mode, CI fallback, and the positional filename filter."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `vitest` starts in the current directory. It enters watch mode in a development environment and run mode in CI (or a non-interactive terminal) automatically.
- `vitest run` performs a single run without watch mode.
- `vitest watch` reruns tests when files change. It is the same as `vitest` without arguments, and falls back to `vitest run` in CI or when stdin is not a TTY.
- `vitest dev` is an alias of `vitest watch`.

A positional argument filters test files by path inclusion:

```bash
vitest foobar
```

The filter checks inclusion only; it supports neither regexp nor glob (unless your terminal expands it first).

Option syntax: camelCase and kebab-case both work (`--passWithNoTests`, `--pass-with-no-tests`); `--reporter dot` and `--reporter=dot` are equivalent; array options repeat the flag; booleans negate with `no-` (`--no-api`) or `=false`.

## Checked

2026-11-04. Confirmed against guide/cli.md: the vitest, run, watch and dev command descriptions, the CI and non-TTY fallback, the filename filter, and the option syntax tip.

Method: documentation only; no commands were run.
