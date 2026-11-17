---
id: computing-software.software-engineering.erlang.dialyzer-usage
name: dialyzer-usage
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-dialyzer, dialyzer-usage]
level: advanced
status: docs-checked
description: "Dialyzer: building a PLT, running via rebar3 dialyzer, warning flags, success typing and suppressing with -dialyzer."
sources:
  - https://www.erlang.org/doc/apps/dialyzer/dialyzer.html
  - https://rebar3.org/docs/commands/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running Dialyzer, PLTs and warnings
**Goal:** run Dialyzer in CI with a cached PLT.

```
dialyzer --build_plt --apps erts kernel stdlib crypto --output_plt .plt   # standalone
dialyzer --plt .plt -Wunmatched_returns -Werror_handling -Wunderspecs ebin
rebar3 dialyzer                                                         # builds and keeps up to date a PLT
```
- Dialyzer bases its analysis on success typings, giving sound warnings without false positives. It starts from debug-compiled BEAM code or from source, so compile with `debug_info`.
- Exit status: 0 no problems and no warnings, 1 problems found during analysis, 2 no problems but warnings were emitted.
- `--add_to_plt` extends an existing PLT, `--check_plt` checks it for consistency and rebuilds if needed, `--no_check_plt` skips the check, `--plt_info` prints PLT information. `--incremental` uses incremental PLTs, which are not compatible with classic ones.
- `rebar.config` options live in a `dialyzer` proplist: `warnings`, `plt_extra_apps`, `plt_apps` (`top_level_deps` or `all_deps`), `plt_location`, `base_plt_apps`, `base_plt_location` (default global, under the home cache directory), `incremental`. Example: `{dialyzer, [{warnings, [unmatched_returns, error_handling]}, {plt_extra_apps, [ssl]}]}.`
- Rebar3 PLT files are named with prefix and OTP release (`<prefix>_<otp_release>_plt`); one base PLT is created per OTP version and used to build project PLTs. `rebar3 dialyzer` options: `--incremental`, `--update-plt`, `--succ-typings`.
- Suppress narrowly in source: `-dialyzer({nowarn_function, f/1}).` or `-dialyzer({[no_return, no_match], [g/0, h/0]}).`; fix the code first.

## Gotchas
- `-Wunderspecs` and similar extra flags can be noisy; warning flags can differ between OTP releases, so check `dialyzer --help` for your version.
- Warnings are only emitted for files analysed in that run.

## Self-check
Run `rebar3 dialyzer` twice and compare timings.

## Checked
Method: docs-checked 2026-11-09 against https://www.erlang.org/doc/apps/dialyzer/dialyzer.html (command-line, warning and -dialyzer attribute sections read) and the dialyzer section of https://rebar3.org/docs/commands/. Dropped the CI cache advice, which neither page states.
