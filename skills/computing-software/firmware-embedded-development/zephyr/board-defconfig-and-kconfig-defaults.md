---
id: computing-software.firmware-embedded-development.zephyr.board-defconfig-and-kconfig-defaults
name: board-defconfig-and-kconfig-defaults
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [board-porting, board-defconfig, kconfig-defconfig, board-kconfig, soc-selection, default-console, board-init-hooks, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Set board-level Kconfig in Zephyr correctly: what belongs in <board>_defconfig vs Kconfig.defconfig vs the app, enabling console/GPIO/pinctrl, and board init code."
sources:
  - https://docs.zephyrproject.org/latest/hardware/porting/board_porting.html#write-kconfig-files
  - https://docs.zephyrproject.org/latest/build/kconfig/setting.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/platform/hooks.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Board defconfig and Kconfig defaults

**Goal:** a board that boots `hello_world` with console and basic drivers, without forcing
choices on applications that should be theirs.

## Three places, three meanings
| File | Content | Overridable by app? |
|---|---|---|
| `<board_target>_defconfig` | mandatory settings for the UART, console and similar, merged as a Kconfig fragment | yes: a symbol also assigned in the application configuration takes the application's value |
| `Kconfig.defconfig` | board-specific default values for options defined elsewhere, wrapped in `if BOARD_<NAME>` / `endif`; may nest conditions such as `if NETWORKING` | yes, they are defaults (use it for invisible symbols, which `.conf` assignments cannot change) |
| `Kconfig.<board>` | selects the SoC and SoC-related settings; must not select anything outside the reusable board and SoC trees | no |
| `Kconfig` | board-specific new symbols (with a prompt); not for changing the default of an existing symbol | n/a |

Keep the defconfig to what the board needs to **boot and print** (the porting guide's example
is `CONFIG_GPIO`, `CONFIG_CONSOLE`, `CONFIG_UART_CONSOLE`, `CONFIG_SERIAL`) and leave optional
subsystems to applications. Enable on-board devices in devicetree with `status = "okay"`;
driver Kconfig symbols commonly default on through `DT_HAS_<COMPAT>_ENABLED` dependencies.

## Example
```
# sensor_node_defconfig
CONFIG_GPIO=y
CONFIG_CONSOLE=y
CONFIG_UART_CONSOLE=y
CONFIG_SERIAL=y
```
```
# Kconfig.defconfig
if BOARD_SENSOR_NODE
config BT_CTLR
	default BT
endif
```

## Board init code
Hooks for early board setup (power switches, LED defaults): implement `board_early_init_hook()`
(runs before the kernel starts, with `CONFIG_BOARD_EARLY_INIT_HOOK=y`) or `board_late_init_hook()`
(after the kernel starts, with `CONFIG_BOARD_LATE_INIT_HOOK=y`), declared in
`zephyr/platform/hooks.h`. Prefer devicetree-driven regulators (`regulator-fixed` supports
`regulator-boot-on`) over custom C when possible.

## Gotchas
- An assignment whose dependencies are not satisfied is ignored and Kconfig prints a warning;
  check `build/zephyr/.config` and the warnings (`KCONFIG_WARNING_AS_ERROR` turns all Kconfig
  warnings into errors).
- Keep application policy out of board files.

## Verify
- [ ] `west build -p -b sensor_node samples/hello_world` prints on the console.
- [ ] `samples/basic/blinky` works with only devicetree aliases set.
- [ ] Twister runs the board's default test set without Kconfig warnings.

## Checked

Checked 2026-10-25 against the Zephyr documentation source (main, post-4.4; latest release v4.4.2): doc/hardware/porting/board_porting.rst, doc/build/kconfig/setting.rst, include/zephyr/platform/hooks.h and dts/bindings/regulator/regulator-fixed.yaml.
Confirmed: roles of `<board>_defconfig`, `Kconfig.defconfig` (`if BOARD_...` wrapper, nested conditions), `Kconfig.<board>` (selects the SoC) and `Kconfig`; application configuration overriding the board defconfig; unmet-dependency assignments produce a warning; `KCONFIG_WARNING_AS_ERROR`; `board_early_init_hook()`/`board_late_init_hook()` and `CONFIG_BOARD_EARLY_INIT_HOOK`/`CONFIG_BOARD_LATE_INIT_HOOK`; `regulator-boot-on` on `regulator-fixed`.

Method: documentation only; no commands were run.
