---
id: computing-software.firmware-embedded-development.zephyr.twister-hardware-map
name: twister-hardware-map
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [twister, twister-hardware-map, device-testing, hil-testing, fixtures, generate-hardware-map, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Run Zephyr twister tests on real boards: generating and editing a hardware map, probe IDs and serial ports, fixtures, flash options and multi-board CI runs."
sources:
  - https://docs.zephyrproject.org/latest/develop/twister/index.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/schemas/twister/hwmap-schema.yaml
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Twister hardware map

Twister can flash each test image to a real board, read its console and parse results.
A hardware map tells it which boards are attached and how to reach them.

## Single board, quick
```bash
west twister --device-testing --device-serial /dev/ttyACM0 \
    -p nucleo_l476rg -T tests/kernel/semaphore
```

## Generate a map
```bash
west twister --generate-hardware-map map.yml
```
Detects connected probes (J-Link, ST-Link, CMSIS-DAP...) and fills in what it can. Edit it:
```yaml
- connected: true
  id: 0672FF485550755187034646        # probe serial number
  platform: nucleo_l476rg
  product: STM32 STLink
  runner: openocd
  serial: /dev/serial/by-id/usb-STMicroelectronics_STM32_STLink_0672FF48-if02
  baud: 115200
  fixtures:
    - i2c_eeprom                        # what's wired to this board
- connected: true
  id: 000683123456
  platform: nrf52840dk/nrf52840
  runner: nrfjprog
  serial: /dev/serial/by-id/usb-SEGGER_J-Link_000683123456-if00
```
Prefer stable device paths such as `/dev/serial/by-id/...` over `/dev/ttyACM*`, whose numbering can
change. Entries marked `unknown` in a generated map must be filled in by hand.

## Run against the map
```bash
west twister --device-testing --hardware-map map.yml \
    -T tests/drivers -p nucleo_l476rg -p nrf52840dk/nrf52840
```
Twister schedules builds in parallel and runs each image on a matching connected board.
Useful flags:
- `--west-flash="--erase"` passes comma-separated runner options to `west flash`.
- `--device-flash-timeout 120` for slow flashers (default 60 seconds); `--device-flash-with-test`
  when flashing also runs the test.
- `--retry-failed 2` retries failing tests, to separate flaky hardware from real failures.
- Map keys (hardware map schema in `scripts/schemas/twister/hwmap-schema.yaml`): `pre_script`,
  `post_script`, `post_flash_script` (for power-cycle or relay scripts), `runner_params` (extra
  args for the west runner), `probe_id` (overrides `id` for an external J-Link), `notes`,
  `serial_pty`, `baud` (only needed if not 115200) and `run_with_fixture_only`. Per-board flash
  timeouts are documented as `flash-timeout` / `flash-with-test` (the schema spells them with
  underscores; check your release).
- `--flash-command` for a custom flash script (called with `--build-dir` and `--board-id`).
- The docs list hardware-map support for boards using the pyocd, nrfjprog, jlink, openocd or
  dediprog runners.

## Fixtures
A test that needs external wiring declares it:
```yaml
tests:
  drivers.eeprom.at24:
    harness: ztest
    harness_config:
      fixture: i2c_eeprom
```
With `--device-testing`, fixtures in the map are matched to the tests requesting them, so the test
runs on boards that list that fixture. `run_with_fixture_only: true` reserves a board for
fixture-dependent tests. `--fixture name` (`-X`) adds a fixture to all boards of the run; a
`:config` suffix on a fixture name is not part of the match.

## Gotchas
- A board in a bad state (locked flash, wrong boot mode) fails every test; add a pre_script
  that does a recovery erase or power cycle.
- Console output must reach the configured serial port (check `zephyr,console` chosen node).
- USB hubs drop devices under load; powered hubs, and `connected: false` to take one out.

## Verify
- [ ] Map uses persistent serial paths and correct probe IDs (compare with a fresh `--generate-hardware-map` run).
- [ ] Nightly CI runs device tests and publishes JUnit results.
- [ ] Fixture-dependent tests skip on boards without the fixture.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed the device-testing options, hardware-map generation and example fields, runner support list, fixtures and run_with_fixture_only (twister page, doc/develop/twister/index.rst), and the map keys pre_script/post_script/post_flash_script, probe_id, runner_params plus the --retry-failed, --fixture and --device-flash-timeout options (scripts/schemas/twister/hwmap-schema.yaml and twisterlib/environment.py). The old twister doc URL moved; sources updated. Removed unconfirmed third-party probe-tool commands and the claim that tests skip rather than fail.
Method: documentation only; no commands were run.
