---
id: computing-software.firmware-embedded-development.hardware-debugging.openocd-configuration-files
name: openocd-configuration-files
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [openocd-config, openocd, interface-cfg, target-cfg, board-cfg, reset-config, event-handlers, adapter-serial, swd, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Write OpenOCD config files for a custom board: interface/target/board layering, adapter speed and serial, reset_config, reset-init hooks, flashing one-liners, and RTT."
sources:
  - https://openocd.org/doc/html/Config-File-Guidelines.html
  - https://openocd.org/doc/html/Reset-Configuration.html
  - https://openocd.org/doc/html/General-Commands.html
  - https://openocd.org/doc/html/Debug-Adapter-Configuration.html
  - https://openocd.org/doc/html/Server-Configuration.html
  - https://openocd.org/doc/html/Flash-Commands.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenOCD configuration files

**Goal:** a checked-in `board/myboard.cfg` so anyone can run `openocd -f board/myboard.cfg`
and get a reliable debug and flash connection.

## Layering (the official guideline)
- **interface**: the adapter (probe) config.
- **target**: the chip, its TAPs/DAP, flash banks and work area. Generic things inside target
  chips belong in target config files, not board files, so reuse the shipped ones.
- **board**: your wiring and policy, sourcing the other two.

Board config files run in the configuration stage: they cannot use TAPs or targets, so they
cannot write memory or access chip registers. That is done later in event handlers, of which the
target `reset-init` handler is one of the most important. Define those handlers last, after the
rest of the board configuration works.

## board/myboard.cfg (shape)
```tcl
source [find interface/<your-adapter>.cfg]
transport select swd
adapter speed 4000                 ;# kHz; lower it for long cables or flaky links
# adapter serial <probe-serial>    ;# pick one of several probes

source [find target/<your-chip>.cfg]

reset_config srst_only srst_nogate

$_TARGETNAME configure -event reset-init {
    # e.g. bring up clocks, then raise the adapter speed for faster flashing
    adapter speed 10000
}
```
- `reset_config` takes the signals that are connected (`none` is the default, `trst_only`,
  `srst_only`, `trst_and_srst`) plus gate flags: `srst_gates_jtag` (default) means asserting SRST
  gates the JTAG clock; `srst_nogate` means JTAG commands can be issued while SRST is active.
- Before the `reset-init` handler has set up the PLLs and clocking, you may need a low adapter
  speed; raise it after the handler makes the faster clock usable. `jtag_rclk` (adaptive clocking)
  is for cores and boards that support it.
- Server ports: `gdb port`, `telnet port` and `tcl port` take a port number; `gdb port pipe`
  makes the gdb server use stdin/stdout (then redirect logs with `log_output`).

## Common commands
```sh
openocd -f board/myboard.cfg -c "program build/app.elf verify reset exit"
openocd -f board/myboard.cfg -c "init; reset halt; flash erase_sector 0 0 last; shutdown"
```
`program filename [preverify] [verify] [reset] [exit] [offset]` flashes an image; a raw binary
needs the offset. `mdw addr [count]` displays 32-bit words; `reset init` halts the target and
runs the `reset-init` script. `flash erase_sector num first last` erases a bank range.

## RTT through OpenOCD
```tcl
rtt setup 0x20000000 2048          ;# address and size of the area to search for the control block
rtt start
rtt server start 9090 0            ;# TCP port and RTT channel
```
`rtt setup address size [ID]` also takes an optional control block ID string.

## Debugging the config
- Check the `debug_level` command and OpenOCD's log for the failing step.
- A too-high `adapter speed` is a common cause of flaky communication: lower it first.
- Check `openocd --version` against the manual you are reading: commands change between releases.

## Verify
- [ ] `openocd -f board/myboard.cfg` connects and reports the expected target.
- [ ] `program ... verify` passes on a board whose firmware enters deep sleep immediately.

## Checked
2026-10-31. Confirmed in the OpenOCD manual (Config File Guidelines, Reset Configuration, General
Commands, Debug Adapter Configuration, Server Configuration, Flash Commands): layering and
`reset-init` rules, `reset_config` signals and gate tokens, `adapter speed`, `adapter serial`, `jtag_rclk`,
`gdb port`/`tcl port`/`telnet port` and `pipe`, `program`, `mdw`, `flash erase_sector`, `reset init`,
`rtt setup`/`start`/`server start`, `debug_level`.
Removed: shipped interface/target file names, default port numbers, `connect_assert_srst`, the `gdb-attach` event,
the work area setting, the DBGMCU address, `-d3` log strings, vendor unlock commands, renamed-command history.
Method: documentation only; no commands were run.
