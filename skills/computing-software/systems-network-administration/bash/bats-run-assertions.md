---
id: computing-software.systems-network-administration.bash.bats-run-assertions
name: bats-run-assertions
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, bats-run-assertions, bats-run, shell-scripting]
level: practitioner
status: docs-checked
description: "Test shell commands in bats with run, $status, $output and $lines, plus bats-assert helper functions."
sources:
  - https://bats-core.readthedocs.io/en/stable/writing-tests.html
  - https://github.com/bats-core/bats-assert
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bats run, status and output
**Goal:** assert on exit code and output.
```bash
@test "prints usage on bad flag" {
  run ./script.sh --bogus
  [ "$status" -eq 2 ]
  [[ "$output" == *"usage:"* ]]
  [ "${lines[0]}" = "usage: script.sh [-v]" ]
}
@test "with bats-assert" {
  # load bats-support and bats-assert first (see the bats-assert README)
  run ./script.sh
  assert_success
  assert_output --partial "done"
}
run -127 nonexistent         # fail unless the exit status is 127
run ! ./script.sh --bogus    # fail if the command succeeds (expects 1-255)
```
- `run` saves the exit status in `$status` and the combined stdout and stderr in `$output`, then returns 0 itself, so assert on `$status` explicitly or give `run` an expected status (`-N`, or `!` for any nonzero).
- `${lines[@]}` holds the output lines; empty lines are left out unless you pass `run --keep-empty-lines`.
- `run --separate-stderr` splits stdout and stderr into `$output`/`$stderr` and `${lines[@]}`/`${stderr_lines[@]}`.
- `run` executes its command in a subshell, so variable changes it makes do not persist after it returns.
- Bats sets `set -e` for all tests, so `run -0 cmd` is equivalent to plain `cmd`; use `run ! cmd` (not `! cmd`) to test that a command failed.
- bats-assert depends on bats-support; `assert_success` and `assert_failure [status]` check the exit status, and `assert_output` checks `$output` (`--partial`, `--regexp`).
- Self-check: a deliberately wrong status makes the test fail.

## Checked
2026-11-08. Confirmed against the Bats writing-tests page (run, `$status`, `$output`, `$lines`, `-N` and `!`, `--separate-stderr`, `--keep-empty-lines`, subshell note, `set -e`) and the bats-assert README (assert_success, assert_failure, assert_output `--partial`/`--regexp`, bats-support dependency). Removed the version labels for `run -N` and `--separate-stderr`, the claim about bare `[[ ]]` in older bats, and the helper load paths, none of which the pages state.
Method: documentation only; no commands were run.
