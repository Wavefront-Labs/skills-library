---
id: computing-software.firmware-embedded-development.zephyr.code-coverage-with-gcov
name: code-coverage-with-gcov
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [twister, gcov-coverage, coverage-report, gcovr, config-coverage, coverage-dump, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Measure Zephyr test coverage with twister and gcov on native_sim and on hardware (console dump), generate gcovr/lcov reports and filter them to your code."
sources:
  - https://docs.zephyrproject.org/latest/develop/test/coverage.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/pylib/twister/twisterlib/environment.py
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/pylib/twister/twisterlib/coverage.py
  - https://gcovr.com/en/stable/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Code coverage with gcov

## On native_sim (easy path)
```bash
west twister --coverage -p native_sim -T tests/ --coverage-tool gcovr
```
`--coverage` implies enabling coverage collection. The report is `twister-out/coverage/index.html`
and, with the default `gcovr` tool, the collected data is in `twister-out/coverage.json`.
`--coverage-tool` (`gcovr` default, or `lcov`) and `--coverage-formats` (comma-separated, no
spaces) choose the output: gcovr supports html, xml, csv, txt, coveralls and sonarqube (default
html); lcov supports html and lcov (default html,lcov). Unit tests use `-p unit_testing`.

Single app by hand (the documented flow; needs lcov 1.14 or newer, or gcovr 4.2 or newer):
```bash
west build -b native_sim app -- -DCONFIG_COVERAGE=y
./build/zephyr/zephyr.exe            # press Ctrl+C to exit; gcda/gcno data is written
lcov --capture --directory ./ --output-file lcov.info -q --rc lcov_branch_coverage=1
genhtml lcov.info --output-directory lcov_html -q --ignore-errors source --branch-coverage --highlight --legend
```

## On QEMU and embedded targets
```
CONFIG_COVERAGE=y
CONFIG_COVERAGE_DUMP=y      # dumps gcov data over the console
```
On target, gcov keeps its profiling data in RAM, so support is limited by RAM and is currently
enabled only for QEMU emulation of embedded targets; a board opts in by selecting
`CONFIG_HAS_COVERAGE_SUPPORT` in its `Kconfig.board`. Capture the console output into a log,
run `python3 scripts/gen_gcov_files.py -i log.log` to produce the `.gcda`/`.gcno` files, then
run `gcovr -r $ZEPHYR_BASE . --html -o coverage-report/coverage.html --html-details
--gcov-executable <gcov from the SDK>`. Small devices may crash when coverage is enabled on
larger tests. Run coverage on native_sim and keep target runs for target-specific code.
`--coverage-platform <board>` selects the platforms to report on (default: those chosen with
`--platform`).

## Filtering
Zephyr kernel and drivers pollute the numbers. Filter to your code:
```bash
gcovr -r . --filter 'app/src/' --filter 'modules/acme/' --exclude '.*tests/.*' ...
```
or use `--coverage-basedir` in twister (it defaults to `$ZEPHYR_BASE`; pass it when the
application lives outside the Zephyr repository). Report line **and** branch coverage; branch
coverage is what finds untested error paths. If your tree has symlinks, either make
`ZEPHYR_BASE` a real path or use `--coverage-tool lcov`, because gcovr filters assume resolved paths.

## Making it useful
- Publish Cobertura XML to the CI system for per-PR diffs; gate on "no drop" for changed
  files rather than an absolute percentage.
- Error-handling paths are the usual holes: use emulators with error injection (see
  driver-emulators-for-testing).
- Coverage proves code ran, not that it was checked. Pair with meaningful assertions.

## Verify
- [ ] CI produces an HTML report filtered to project code on every PR.
- [ ] Branch coverage tracked for safety- or security-relevant modules.
- [ ] Any QEMU or target coverage run fits in RAM with instrumentation.

## Checked

Checked 2026-10-25 against the Zephyr source (main, post-4.4; latest release v4.4.2): doc/develop/test/coverage.rst, scripts/pylib/twister/twisterlib/environment.py and coverage.py, plus the gcovr filter documentation (`-f/--filter`, `-e/--exclude`).
Confirmed: `west twister --coverage -p native_sim -T ...`, `twister-out/coverage/index.html` and `twister-out/coverage.json`; `--coverage-tool` (lcov, gcovr), `--coverage-formats` lists, `--coverage-basedir`, `--coverage-platform`; `CONFIG_COVERAGE`, `CONFIG_COVERAGE_DUMP`, `CONFIG_HAS_COVERAGE_SUPPORT`; `scripts/gen_gcov_files.py -i`; the native_sim lcov/genhtml flow and its minimum versions; the symlink note; gcovr `--filter`/`--exclude`.

Method: documentation only; no commands were run.
