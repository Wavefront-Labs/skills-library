---
id: computing-software.firmware-embedded-development.zephyr.twister-pytest-harness
name: twister-pytest-harness
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [twister-pytest, pytest-twister-harness, harness-pytest, dut-fixture, shell-fixture, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Write host-side pytest tests that twister runs against a Zephyr device or simulator: harness pytest config, the dut and shell fixtures, and MCUmgr or serial interaction."
sources:
  - https://docs.zephyrproject.org/latest/develop/twister/pytest.html
  - https://docs.zephyrproject.org/latest/develop/twister/harness/pytest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Twister pytest harness

Use when the test logic belongs on the host: sending shell commands, checking output sequences,
power cycling, DFU over serial, talking to the device with a Python library.

## testcase.yaml
```yaml
tests:
  app.shell.pytest:
    harness: pytest
    harness_config:
      pytest_root:
        - "pytest/test_shell.py"
      pytest_args: ["-k=test_boot_banner"]
    platform_allow:
      - native_sim
      - nrf52840dk/nrf52840
    integration_platforms:
      - native_sim
```
Twister discovers, builds and reports as usual, then delegates execution to pytest as a
subprocess, passing build directory and device details in a YAML config file, and reads pytest's
`results.xml`. The `pytest-twister-harness` plugin lives in the Zephyr tree
(`scripts/pylib/pytest-twister-harness`): twister adds it to `PYTHONPATH` and appends
`-p twister_harness.plugin` to the pytest call, so nothing needs installing (use
`--allow-installed-plugin` to prefer an installed copy). `pytest_root` defaults to a `pytest`
directory next to the sources.

## Test file
```python
# pytest/test_shell.py
import logging
from twister_harness import DeviceAdapter, Shell

logger = logging.getLogger(__name__)

def test_boot_banner(dut: DeviceAdapter):
    dut.readlines_until(regex=r"Booting Zephyr OS", timeout=10)

def test_version_command(shell: Shell):
    lines = shell.exec_command("app version")
    assert any("1.4." in l for l in lines), lines

def test_led_toggle(shell: Shell):
    shell.exec_command("led on 0")
    lines = shell.exec_command("led status 0")
    assert "on" in "".join(lines)
```
- `dut`: `DeviceAdapter` that launches the device (flash, serial connect) with `launch`, `close`,
  `readline`, `readlines`, `readlines_until` and `write`; works across `native`, `qemu` and
  `hardware` device types.
- `shell`: `Shell` that calls `wait_for_prompt` first, then offers `exec_command` and
  `get_filtered_output`.
- `unlaunched_dut`: like `dut` but you call `launch()` yourself.
- `mcumgr`: wraps the `mcumgr` command-line tool (must be on PATH) for image upload tests.
- Multi-device: `duts`, `shells`, `unlaunched_duts` (hardware and `native_sim`; not QEMU).
- Custom fixtures in `conftest.py` next to the test. `pytest_dut_scope` (`function` default,
  or `class`, `module`, `package`, `session`) sets how long `dut` and `shell` are shared.

## Running
```bash
./scripts/twister -T app/tests -p native_sim
./scripts/twister -T app/tests --device-testing --hardware-map map.yaml
./scripts/twister -T app/tests -p native_sim --pytest-args='-k test_boot_banner'
```
`--pytest-args` extends `pytest_args` from the YAML file and wins on conflicts.

## Re-running pytest without rebuilding
Run twister again with `--test-only`, or run once with `-vv`, copy the logged
`Running pytest command: ...` line, or call pytest directly using the config twister wrote
(`twister_pytest_config.yaml` in the test's build directory):
```bash
export PYTHONPATH=$ZEPHYR_BASE/scripts/pylib/pytest-twister-harness/src
pytest -s -v -p twister_harness.plugin --twister-config=<build dir>/twister_pytest_config.yaml
```

## Gotchas
- The `shell` fixture waits for the shell prompt, so shell tests need the shell enabled in the
  app (for example `CONFIG_SHELL=y`).
- Logging backends printing to the same UART can interleave with shell output; route logs
  elsewhere in test builds.
- Keep timeouts generous for real hardware (flash + boot).

## Verify
- [ ] Same test passes on `native_sim` and on at least one real board.
- [ ] Failures show the device log in the twister report.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed the pytest integration flow, plugin PYTHONPATH and -p twister_harness.plugin handling, --allow-installed-plugin, pytest_root/pytest_args/pytest_dut_scope, fixtures dut/shell/mcumgr/unlaunched_dut and multi-DUT fixtures, DeviceAdapter and Shell methods, --pytest-args precedence, and the re-run recipe (doc/develop/twister/pytest.rst and harness/pytest.rst). Wrong in the draft: the plugin is not installed via requirements, the --twister-harness/--device-type invocation and clear_buffer method are not documented, and the uart:~$ default prompt and handler.log paths were unconfirmed (removed). Old doc URLs under develop/test moved to develop/twister.
Method: documentation only; no commands were run.
