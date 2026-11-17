---
id: computing-software.firmware-embedded-development.platformio.custom-test-runners
name: custom-test-runners
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [pio-test, custom-test-runner, test-framework-custom, test-testing-command, simavr, renode, platformio, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Extend PlatformIO unit testing with custom test runners (Python TestRunnerBase subclasses) and test_testing_command to run tests in simulators or parse non-Unity output."
sources:
  - https://docs.platformio.org/en/latest/advanced/unit-testing/frameworks/custom/runner.html
  - https://docs.platformio.org/en/latest/advanced/unit-testing/frameworks/custom/api.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/test/test_testing_command.html
  - https://docs.platformio.org/en/latest/advanced/unit-testing/simulators/simavr.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom test runners

`pio test` normally builds each test folder with a test framework, uploads it, and parses the
framework's output. Two extension points change that: **where and how the test runs**
(`test_testing_command`) and **how results are produced and parsed** (a custom runner).

## Run tests in a simulator: test_testing_command
`test_testing_command` is a multiline option: each argument goes on its own line. Example for
SimAVR (the PlatformIO docs note it does not work on Windows for unit testing):
```ini
[env:uno]
platform = atmelavr
framework = arduino
board = uno
platform_packages =
    platformio/tool-simavr
test_speed = 9600
test_testing_command =
    ${platformio.packages_dir}/tool-simavr/bin/simavr
    -m
    atmega328p
    -f
    16000000L
    ${platformio.build_dir}/${this.__env__}/firmware.elf
```
Simulators need no upload stage, so run `pio test --without-uploading`. Renode (a
`platformio/tool-renode` package with `-e` commands that load the ELF and start) and QEMU are
documented the same way on the simulators pages. For the native platform the default command is
`${platformio.build_dir}/${this.__env__}/program`; extra arguments can be added in the option or
with `pio test --program-arg`.

## Custom framework and runner
```ini
[env:native]
platform = native
test_framework = custom
```
With `test_framework = custom`, PlatformIO looks for `test_custom_runner.py` in the running test
folder, then in parent folders up to the test directory root. It must define a `CustomTestRunner`
class that inherits `TestRunnerBase` or an existing runner:
```python
from platformio.public import TestCase, TestStatus, UnityTestRunner

class CustomTestRunner(UnityTestRunner):
    def stage_testing(self):
        # gather results from Serial, HTTP, sockets, ... and report them
        self.test_suite.add_case(
            TestCase(name="test_connectivity", status=TestStatus.PASSED, duration=1.34))
```
Overridable methods in the documented API: `setup()` (before `stage_building()`), `teardown()`
(after `stage_testing()`, even after an exception), `stage_building()`, `stage_uploading()`
(ignored on native), `stage_testing()`, `configure_build_env()`,
`on_testing_data_output(data)` and `on_testing_line_output(line)` (called for each line split from
the data). `TestStatus` has PASSED, FAILED, SKIPPED and ERRORED; `TestCase` takes `name`,
`status`, `message` (for failures), `stdout`, `duration` (seconds), `exception` and `source`
(a `TestCaseSource` with file and line).
Built-in frameworks (Unity, doctest, GoogleTest) exist; use a custom runner only when none fit.

## Typical uses
- Remote "board farm" runners: `stage_testing` connects to the farm over HTTP or TCP, collects
  results and records them with `add_case`.
- Hardware-in-the-loop: `setup` and `teardown` drive fixtures before and after the run.
- Parsing structured firmware output into individual test cases.

## Gotchas
- `test_testing_command` output is parsed like serial output: the program must print what the
  framework expects and then terminate, or the simulator runs forever.
- Runner files are executed by PlatformIO's Python; import only what PlatformIO provides
  (`platformio.public`) or vendor small helpers.
- Keep simulator versions pinned via `platform_packages`.

## Verify
- [ ] `pio test --without-uploading` runs in CI without hardware and a failing assert fails the job.
- [ ] A report option (`--junit-output-path` or `--json-output-path`) lists each case separately.
- [ ] Simulator run terminates on its own (no CI timeout).

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): custom runner, custom API,
`test_testing_command`, SimAVR and Renode pages, and `pio test` reference. Confirmed: runner
discovery rule, method names and call order, `TestCase` and `TestStatus` fields, multiline
argument format, `--without-uploading`, `--program-arg`, report options, SimAVR Windows
limitation. Removed as unconfirmed: the `self.test_suite.on_finish()` call, the HEAP_LEAK example
hook, the `renode-test` and `.resc` remark, and the statement that doctest and GoogleTest are
native-only.
Method: documentation only; no commands were run.
