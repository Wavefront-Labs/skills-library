---
id: computing-software.firmware-embedded-development.stm32.st-link-gdb-server-debug-configurations
name: st-link-gdb-server-debug-configurations
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-cube, st-link-gdb-server, stm32cubeide-debug, openocd-stlink, swo-trace, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Set up STM32CubeIDE and command-line debug with ST-LINK GDB server or OpenOCD: launch vs attach, reset modes, multiple probes, SWV/ITM printf and live expressions."
sources:
  - https://www.st.com/resource/en/user_manual/um2576-stm32cubeide-stlink-gdb-server-stmicroelectronics.pdf
  - https://www.st.com/resource/en/user_manual/um2609-stm32cubeide-user-guide-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ST-LINK GDB server debug configurations

## CubeIDE debug configuration
Debug Configurations > STM32 C/C++ Application > Debugger tab:
- **Debug probe**: ST-LINK (ST-LINK GDB server), ST-LINK (OpenOCD), or SEGGER J-Link.
- **Interface**: SWD; frequency 4000 kHz (drop to 1000 with long wires).
- **Reset behaviour**: "Connect under reset" for firmware that sleeps, disables SWD pins or
  crashes early; "Software system reset" default; "None" to attach to a running target.
- **ST-LINK S/N**: pin a serial number when several probes are connected.
- **Shared ST-LINK**: lets CubeProgrammer/CubeMonitor use the same probe concurrently.

## Attach to a running target (no reset)
Create a second configuration: Startup tab, uncheck "Download" and "Load symbols only" stays
on, reset behaviour "None". Useful for field units in a hung state.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Command line
```bash
ST-LINK_gdbserver -p 61234 -l 1 -d -s -cp <CubeProgrammer>/bin -m 0 -k
arm-none-eabi-gdb build/app.elf -ex "target remote :61234" -ex "monitor reset" -ex "load"
```
`-d` SWD, `-s` verify, `-m 0` core 0 (dual-core H7: `-m 1` for M4), `-k` keep running after
disconnect. OpenOCD alternative:
```bash
openocd -f interface/stlink.cfg -f target/stm32l4x.cfg
```

## SWV / ITM printf
Enable SWV in the debugger tab, set core clock exactly (HCLK), then:
```c
int _write(int f, char *p, int n) { for (int i = 0; i < n; i++) ITM_SendChar(p[i]); return n; }
```
Open SWV ITM Data Console, enable port 0, start trace. Needs SWO pin (PB3) and not available on
Cortex-M0/M0+ parts (use RTT or UART there).

## Live expressions and SFRs
Live Expressions update while running (background memory reads). SFR view decodes peripheral
registers from the SVD file; set breakpoints on register writes with data watchpoints.

## Problems
- "Target is not responding, retrying...": SWD pins remapped or core in low-power; use connect
  under reset.
- "Could not verify ST device": clone probe or non-ST chip; ST-LINK GDB server refuses.
- Breakpoints not hit after reset: set "Run to main" off and check optimisation (-O0/-Og for debug).

## Verify
- [ ] Debug starts on a board running low-power firmware (connect under reset).
- [ ] SWV printf output visible at the configured clock.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
