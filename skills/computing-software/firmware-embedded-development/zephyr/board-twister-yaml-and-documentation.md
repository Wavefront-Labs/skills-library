---
id: computing-software.firmware-embedded-development.zephyr.board-twister-yaml-and-documentation
name: board-twister-yaml-and-documentation
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [board-twister-yaml, board-yaml, twister-supported, board-documentation, board-index-rst, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Write a Zephyr board's twister YAML (identifier, ram, flash, toolchain, supported features) and its docs page so twister filters tests correctly and the board is documented."
sources:
  - https://docs.zephyrproject.org/latest/develop/twister/index.html
  - https://docs.zephyrproject.org/latest/hardware/porting/board_porting.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/schemas/twister/platform-schema.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/templates/board.tmpl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Board twister YAML and documentation

## `<board_target>.yaml` (one per board target)
`boards/acme/widget/widget_nrf52840.yaml` (name = normalized board target):
```yaml
identifier: widget/nrf52840          # must equal the board target string
name: ACME Widget (nRF52840)
type: mcu                            # mcu, qemu, sim, native, unit
arch: arm
ram: 256                             # KB (default 128 if omitted)
flash: 1024                          # KB (default 512 if omitted)
toolchain:
  - zephyr
  - gnuarmemb
supported:                           # features tests can require via depends_on
  - gpio
  - i2c
  - spi
  - pwm
  - adc
  - watchdog
  - counter
  - ble
testing:
  default: true                      # include in default twister runs
  ignore_tags:
    - net
vendor: acme
```
Twister uses it to:
- skip tests whose `depends_on` features aren't in `supported`,
- skip tests needing more RAM/flash than declared (`min_ram`, `min_flash` are compared with the
  board metadata),
- filter out instances whose toolchain is not in the board's `toolchain` list (the list says which
  toolchains may build the board; `--force-toolchain` disables the check),
- treat the board as a default board (`testing.default: true`): tested with the highest priority
  and covered when twister is invoked without extra arguments.

`twister: false` makes twister ignore the platform entirely. `testing.ignore_tags` and
`only_tags` filter tests by tag, and `testing.timeout_multiplier` stretches scenario timeouts for
slow boards.

## Features: be truthful
List only features with working drivers and DT nodes enabled by default. Over-claiming causes
false failures in CI; under-claiming hides coverage. Features are single words or `class:variant`
(e.g. `arduino_i2c`, `usb_device`, `netif:eth`); a test scenario can depend on `eth` or on `netif`
to run on any board with a networking interface.

## Documentation
`boards/acme/widget/doc/index.rst` (Zephyr 4.x can use a `.. zephyr:board::` directive):
```rst
.. zephyr:board:: widget

Overview
********
Short description, photo (``doc/widget.webp``: named after the board, WebP, at most 600 px).

Hardware
********
.. zephyr:board-supported-hw::

Programming and Debugging
*************************
.. zephyr:board-supported-runners::

Flashing
========
.. zephyr-app-commands::
   :zephyr-app: samples/hello_world
   :board: widget/nrf52840
   :goals: flash
```
Include pin mapping (LEDs, buttons, connectors), default console, how to enter bootloader, and
known limitations.

## Verify
- [ ] `twister -p widget/nrf52840 -T tests/drivers/gpio --dry-run` (or `--cmake-only`) selects tests.
- [ ] `identifier` matches the board target exactly.
- [ ] The board page renders with its supported-hardware and runners tables, if upstreaming (they need hardware-feature generation enabled in the docs build).

## Checked

Checked 2026-10-25 against the Zephyr source (main, post-4.4; latest release v4.4.2): doc/develop/twister/index.rst, scripts/schemas/twister/platform-schema.yaml, scripts/pylib/twister/twisterlib/environment.py, doc/templates/board.tmpl, doc/contribute/documentation/guidelines.rst and doc/hardware/porting/board_porting.rst.
Confirmed: board YAML keys `identifier`, `name`, `type` (mcu, qemu, sim, unit, native), `arch`, `ram`/`flash` (KB, defaults 128 and 512), `toolchain`, `supported` (`class:variant` form), `vendor`, `twister`, `testing.default`/`ignore_tags`/`only_tags`/`timeout_multiplier`; scenario keys `depends_on`, `min_ram`, `min_flash`; twister options `-p`, `-T`, `--dry-run`/`-y`, `--cmake-only`; `.. zephyr:board::`, `zephyr:board-supported-hw` and `zephyr:board-supported-runners` directives (the latter two need hardware-feature generation); board picture in WebP named after the board; the `zephyr-app-commands` directive.

Method: documentation only; no commands were run.
