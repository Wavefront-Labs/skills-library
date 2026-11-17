---
id: computing-software.systems-network-administration.bash.bats-setup-teardown
name: bats-setup-teardown
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, bats-setup-teardown, bats-fixtures, shell-scripting]
level: practitioner
status: docs-checked
description: "Use bats setup, teardown, setup_file and temporary directories to isolate shell tests."
sources:
  - https://bats-core.readthedocs.io/en/stable/writing-tests.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bats setup and teardown
**Goal:** every test starts clean.
```bash
setup_file()    { export SHARED=$(mktemp -d "${BATS_TMPDIR:-/tmp}/suite.XXXXXX"); }
teardown_file() { rm -rf "$SHARED"; }
setup() {
  cd "$BATS_TEST_TMPDIR" || exit 1          # temp dir unique to each test
  source "${BATS_TEST_DIRNAME}/../lib/util.sh"
}
teardown() { :; }
@test "creates the file" { make_file; [ -f out.txt ]; }
```
- `setup`/`teardown` run before and after each test; `setup_file`/`teardown_file` run once per file, before the first test's `setup` and after the last test's `teardown`. Variables exported in `setup_file` are visible to `setup`, the test, `teardown` and `teardown_file`.
- `setup_suite`/`teardown_suite` run once per test run and must live in a separate `setup_suite.bash` file.
- `BATS_TEST_DIRNAME` is the directory of the test file; `BATS_TEST_NAME` is the function name of the current test; `BATS_TMPDIR` is the base temp dir (`$TMPDIR`, else `/tmp`); `BATS_TEST_TMPDIR` is unique per test, `BATS_FILE_TMPDIR` per file, `BATS_SUITE_TMPDIR` per suite.
- `teardown` runs unconditionally after the test ends, but a nonzero return from it (including a failing last command) fails the test; failing commands inside `teardown` do not abort it because errexit is disabled there.
- `load helpers/common` sources a file relative to the current test file (an absolute path is used directly); `load` first looks for a name ending in `.bash`, which is deprecated, so give exact filenames.
- Self-check: `bats test/` passes with tests independent of order.

## Checked
2026-11-08. Confirmed against the Bats writing-tests page: setup/teardown hooks, setup_file/teardown_file and export visibility, setup_suite file rule, teardown failure behaviour, the BATS_* variables and the load argument resolution. Removed the unconfirmed `1.4+` version label for `BATS_TEST_TMPDIR` and the claim that a failing `setup` fails the test.
Method: documentation only; no commands were run.
