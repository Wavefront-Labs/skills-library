---
id: computing-software.software-engineering.deno.test-selection-and-affected
name: test-selection-and-affected
category: computing-software
field: software-engineering
product: deno
tags: [test, filter, changed, related, only, ignore, fail-fast, reporters]
level: practitioner
status: docs-checked
description: "Select tests by --filter, --changed and --related, by only/ignore in code, stop early with --fail-fast, and choose reporters including JUnit."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/test/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Filter by name; a string or a regex in forward slashes:

```sh
deno test --filter "my" tests/
deno test --filter "/test-*\d/" tests/
```

`test.include`/`test.exclude` in the config file control which files are collected.

Affected tests (one-shot runs, not a watch):

```sh
deno test --changed                 # working tree: staged, unstaged, untracked
deno test --changed=origin/main     # also commits since branching (merge-base)
deno test --related=src/util.ts     # tests importing a file, directly or transitively
```

Deno builds the module graph of the collected tests and keeps those reaching a changed or named file. Combine with a directory, `--filter` or include/exclude. Good for pre-commit hooks; CI that must verify everything should run the full suite (optionally with `--shard`).

In code:

```ts
Deno.test({
  name: "do macOS feature",
  ignore: Deno.build.os !== "darwin",
  fn() {},
});
Deno.test.ignore("my test", () => {});
Deno.test.only("my test", () => {});
```

If any test has `only`, the overall run always fails (a temporary debugging measure).

`deno test --fail-fast` stops after the first failure.

Reporters: default `pretty`; `--reporter=dot|junit|tap`. Write JUnit XML while keeping terminal output with `deno test --junit-path=./report.xml`.

## Checked

2026-11-04. Confirmed against docs runtime/test/index.md (Testing): --filter, test.include/exclude, --changed, --changed=ref, --related, ignore/only, --fail-fast, reporters and --junit-path.

Method: documentation only; no commands were run.
