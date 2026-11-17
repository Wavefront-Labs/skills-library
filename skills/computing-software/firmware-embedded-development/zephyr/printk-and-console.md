---
id: computing-software.firmware-embedded-development.zephyr.printk-and-console
name: printk-and-console
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-printk, zephyr-console, chosen-zephyr-console, uart-console, rtt-console, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Get console output from Zephyr: printk vs logging vs printf, selecting the console device with chosen zephyr,console, UART/RTT/USB CDC consoles, and console input."
sources:
  - https://docs.zephyrproject.org/latest/services/logging/index.html
  - https://docs.zephyrproject.org/latest/services/console.html
  - https://github.com/zephyrproject-rtos/zephyr/tree/main/snippets/cdc-acm-console
  - https://github.com/zephyrproject-rtos/zephyr/tree/main/snippets/rtt-console
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# printk and console

## Which output call
| Call | Use | Notes |
|---|---|---|
| `printk()` | early boot, quick debug | formatting via cbprintf; becomes a no-op with `CONFIG_PRINTK=n` |
| `LOG_INF()` etc. | normal diagnostics | levels, modules, deferred processing, backends |
| `printf()` | portable/libc code | goes to stdout -> console via libc hooks; heavier |

`CONFIG_LOG_PRINTK` (enabled by default) redirects printk to the logging subsystem, where each call is a
level-0 log entry that cannot be disabled; logging then manages the output so it does not interleave with log data. In
deferred mode printk output is delayed until the logging thread processes it.

## Selecting the console device
```dts
/ {
    chosen {
        zephyr,console = &uart0;
        zephyr,shell-uart = &uart0;
    };
};
```
```
CONFIG_SERIAL=y
CONFIG_CONSOLE=y
CONFIG_UART_CONSOLE=y
CONFIG_PRINTK=y
```

### RTT instead of UART
```
CONFIG_USE_SEGGER_RTT=y
CONFIG_RTT_CONSOLE=y
CONFIG_UART_CONSOLE=n
```
Or build with the snippet: `west build -S rtt-console` (it appends `CONFIG_USE_SEGGER_RTT`,
`CONFIG_CONSOLE` and `CONFIG_RTT_CONSOLE`).

### USB CDC ACM
```dts
&zephyr_udc0 { cdc_acm_uart0: cdc_acm_uart0 { compatible = "zephyr,cdc-acm-uart"; }; };
/ { chosen { zephyr,console = &cdc_acm_uart0; zephyr,shell-uart = &cdc_acm_uart0; }; };
```
Or simply `west build -S cdc-acm-console`: its overlay sets both chosen nodes and its Kconfig fragment enables
`CONFIG_SERIAL`, `CONFIG_CONSOLE`, `CONFIG_UART_CONSOLE`, `CONFIG_UART_LINE_CTRL` and the USB CDC ACM options.

## Formatting options
- `CONFIG_CBPRINTF_FP_SUPPORT=y` for floating point (default y if the target has an FPU; adds code size).
- `CONFIG_CBPRINTF_NANO=y` selects a much smaller but feature-limited formatter (instead of the default
  `CONFIG_CBPRINTF_COMPLETE`).
- Integer width: `CONFIG_CBPRINTF_FULL_INTEGRAL` (default) converts the full range of integer and pointer values;
  `CONFIG_CBPRINTF_REDUCED_INTEGRAL` handles only 32-bit values, saving stack.

## Console input
- Shell (`CONFIG_SHELL`) is the usual interactive interface.
- `CONFIG_CONSOLE_SUBSYS=y` plus a choice of `CONFIG_CONSOLE_GETCHAR=y` (`console_getchar()`) or
  `CONFIG_CONSOLE_GETLINE=y` (`console_getline()`); the choice needs `CONFIG_UART_CONSOLE` and a UART that supports
  interrupts.

## Gotchas
- No output at all: check `zephyr,console` points at an enabled UART with correct pinctrl, and
  baud rate (`current-speed` in DT) matches the terminal.
- printk in hot ISRs: at 115200 baud with 8N1 framing (10 bits per character) each character takes about 87 us of
  UART time, which will wreck timing if output is synchronous.
- `CONFIG_PRINTK=n` turns printk into a no-op; logging still works.

## Verify
- [ ] `chosen` console in `zephyr.dts` is the intended device.
- [ ] Release builds decide explicitly on printk/console (size and security).

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- `CONFIG_LOG_PRINTK` default and behaviour (doc: services/logging, Printk section); snippet contents for
  `rtt-console` and `cdc-acm-console` (`snippets/*/`); `CONFIG_CBPRINTF_*` options and defaults (`lib/os/Kconfig.cbprintf`);
  `CONFIG_CONSOLE_GETCHAR` / `GETLINE` choice and dependencies (`subsys/console/Kconfig`); `CONFIG_PRINTK` no-op
  (`include/zephyr/sys/printk.h`).
- 87 us per character is computed from 10 bits at 115200 baud.
- Removed: "synchronous, ISR-safe" for printk, "Don't combine with the shell on one UART", the nano "no 64-bit or FP"
  limits, and the `uart_line_ctrl_get` DTR advice (no source read for it).

Method: documentation only; no commands were run.
