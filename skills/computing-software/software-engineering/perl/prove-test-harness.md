---
id: computing-software.software-engineering.perl.prove-test-harness
name: prove-test-harness
category: computing-software
field: software-engineering
product: perl
tags: [perl, prove, tap-harness, test-harness, parallel-tests, harness-perl-switches, prove-test-harness]
level: practitioner
status: docs-checked
description: "Run suites with prove (-l, -r, -v, -j, --state), set the harness environment and read results."
sources: ["https://perldoc.perl.org/prove", "https://perldoc.perl.org/TAP::Harness"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# prove, TAP and running test suites

**Goal:** run and iterate on tests quickly.

```bash
prove -l t/                     # add lib/ to @INC, run t/*.t
prove -lr t                     # recurse into subdirectories
prove -lv t/basic.t             # verbose TAP of one file
prove -l -j4 t                  # four test files in parallel (tests must be independent)
prove -l --state=failed,save    # rerun only failed tests next time; --state=slow,save orders by duration
prove -b t                      # use blib/ after make
prove -I lib -I t/lib t
prove -Q -l t ; prove --timer   # quiet / show timings
prove -l xt/                    # author/extended tests directory
prove --formatter Name ...      # choose a result formatter class (see FORMATTERS in the prove docs)
prove -lm --merge t             # merge stderr into stdout
TEST_VERBOSE=1 make test        # raw test output through make
```

## Rules
- Exit status of `prove` is non-zero when any test fails; use it in CI.
- If no files or directories are given, `prove` runs `t/*.t`.
- `~/.proverc` and `./.proverc` are read before the command line; options go in the same form as on the command line. `--norc` skips them.
- `--state=save` writes `.prove` in the current directory; `--state=failed`, `hot` and `slow` select or order tests from that saved state.
- `--rules='seq=t/p*.t' --rules='par=**'` marks which files may not run in parallel under `-j`.
- Parallel runs share files and ports: allocate temp dirs and random ports.
- `PERL5LIB` directories are passed on as `-I` switches by `prove`; or use `-l` rather than editing `@INC` in tests.
- `-f` / `--failures` shows failed tests; `-v` prints all test lines.

## Self-check
- [ ] `prove -l t` exits 0 only when all pass, and `-j4` gives the same result as serial.

## Checked

2026-11-02. Checked against perldoc prove (option list: -l, -b, -r, -v, -j, -m, -Q, --timer, --formatter, --state, --rules, --norc; .proverc; default t/*.t; non-zero exit status on failure; PERL5LIB handling). Removed: the JUnit formatter module, HARNESS_PERL_SWITCHES coverage line, the AUTOMATED_TESTING / RELEASE_TESTING / AUTHOR_TESTING convention list, the 'Dubious, test returned 255' text, Test::TCP, perl -d, and the make test / Build test remark (not in the fetched pages).

Method: documentation only; no commands were run.
