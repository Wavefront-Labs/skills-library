---
id: computing-software.firmware-embedded-development.hardware-debugging.manufacturing-test-firmware
name: manufacturing-test-firmware
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [manufacturing-test, factory-test, end-of-line-test, test-jig, provisioning, pytest-embedded, hardware-debugging, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Design manufacturing test firmware and the jig host side: shell-driven tests, machine-readable results, pytest-embedded services, provisioning and traceability."
sources:
  - https://docs.espressif.com/projects/pytest-embedded/en/latest/
  - https://interrupt.memfault.com/blog/firmware-shell
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manufacturing test firmware

**Goal:** every board leaving the line has been functionally tested and provisioned in a fixed
cycle time, with results stored against its serial number.

## Device side: a command shell
Memfault's article describes the pattern: along the assembly line stations talk to the unit over
UART (works on Windows, Linux and macOS, no network needed); each station runs shell commands
and checks for a pass or fail response. Stations can also provision private keys into persistent
storage and write the serial number.
- Every command ends with a fixed `> OK` or `> FAIL,<code>` so a machine can parse it.
- Arguments, behaviour and output formats must not change between builds, or the station parsers
  break. Guard this with unit tests that assert the exact output, run in CI on every change.
- Production-like builds should carry only the commands the automated tests need; mark them with
  "do not change" comments.
- Lock the shell down before units ship (password, knock pattern, signed unlock phrase, or build
  without it).

## Host side: pytest-embedded
Espressif's pytest-embedded is a pytest plugin for embedded testing. A test uses a `Dut` fixture
and checks device output with `dut.expect(...)` (regex) or `dut.expect_exact(...)`. Extra services
are enabled with `pytest --embedded-services <list>`: serial (serial port utilities), esp
(target and port auto-detect by esptool), idf (app info and auto-flash for ESP-IDF), jtag
(openocd and gdb utilities), qemu, espemu, arduino, wokwi and nuttx. Install with
`pip install -U pytest-embedded~=2.0`.

## Design points (general practice, not from the sources)
Keep limits on the PC so they can change without reflashing; apply a timeout to every command;
store results keyed by serial with the firmware, jig software and limits versions; verify the jig
with known good and known bad samples; decide a retry policy and log every attempt.

## Verify
- [ ] A board with a missing component fails on the expected test.
- [ ] Results for every serial can be retrieved with all measurements.
- [ ] Output format tests fail if a command's output changes.

## Checked
Confirmed from the Memfault firmware shell article (assembly line use, OK/FAIL format, stability
tests, production command set, locking down) and the pytest-embedded 2.x documentation front page
(Dut fixture, expect calls, services list, install). Removed as unconfirmed: the Nordic source
(page unreadable), test image versus test mode trade-offs, protocol examples, RF test modes, the
measurement list, provisioning and debug lock steps, and cycle time figures.

Method: docs-checked 2026-11-09 against the Memfault firmware shell article and the pytest-embedded 2.x documentation front page.
