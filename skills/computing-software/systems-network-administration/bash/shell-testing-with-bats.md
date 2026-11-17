---
id: computing-software.systems-network-administration.bash.shell-testing-with-bats
name: shell-testing-with-bats
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-bats, shell-testing, bats-core, test-doubles, shell-unit-tests]
level: advanced
status: draft
description: "Unit-test shell scripts with bats-core: run, assertions, setup/teardown and stubbing commands."
sources: ["https://www.gnu.org/software/bash/manual/", "https://pubs.opengroup.org/onlinepubs/9799919799/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing shell with bats

- bats-core runs `*.bats` files: `@test "adds numbers" { run ./calc 1 2; [ "$status" -eq 0 ]; [ "$output" = "3" ]; }`. `run` captures `$status`, `$output`, `${lines[@]}` and never aborts the test; `run -1 cmd` asserts a specific status in recent versions.
- Helpers: `bats-support`, `bats-assert` (`assert_success`, `assert_output --partial`), `bats-file`. Load with `load 'test_helper/bats-support/load'`.
- `setup()`/`teardown()` per test, `setup_file()`/`teardown_file()` per file; use `$BATS_TEST_TMPDIR` for isolated temp dirs.
- Make scripts testable: put logic in functions, guard `main` with `[[ ${BASH_SOURCE[0]} == "$0" ]] && main "$@"` so the file can be `source`d by tests.
- Stub external commands by prepending a fake bin directory to PATH containing scripts that record their arguments.
- Run: `bats test/` or `bats --tap`, `--jobs N` for parallel; in CI add ShellCheck.
- Each test body runs with `set -e` semantics; a failing command fails the test.
