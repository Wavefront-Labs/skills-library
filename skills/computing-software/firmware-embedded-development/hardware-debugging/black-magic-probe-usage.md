---
id: computing-software.firmware-embedded-development.hardware-debugging.black-magic-probe-usage
name: black-magic-probe-usage
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [black-magic-probe, bmp, gdb-server-on-probe, swdp-scan, jtag-scan, bmp-uart, hardware-debugging, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Debug with a Black Magic Probe: connect GDB to its serial port, scan with auto_scan, swd_scan or jtag_scan, attach, load, compare-sections, tpwr and connect_rst."
sources:
  - https://black-magic.org/docs/usage/gdb-commands/
  - https://black-magic.org/docs/intro/getting-started/
  - https://github.com/blackmagic-debug/blackmagic
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Black Magic Probe

The probe presents a GDB remote server over USB CDC-ACM serial; you use a normal GDB for your target architecture.

## Ports
The probe enumerates a pair of CDC-ACM devices. The first is the GDB server, the second a USB-to-UART adapter. On Linux they appear as ttyACM devices (the guide assumes the project's udev rules are installed, giving `/dev/ttyBmpGdb`); on macOS use the `cu.` device, not the `tty.` one, which freezes GDB when it opens it; on Windows you get two COM ports, and COM10 and above need the `\\.\` prefix.

## Session
```gdb
(gdb) target extended-remote /dev/ttyBmpGdb
(gdb) monitor auto_scan        # or monitor jtag_scan / monitor swd_scan
(gdb) attach 1
(gdb) load
(gdb) compare-sections
(gdb) start                    # or run
```
- `target extended-remote <port>` only connects GDB to the probe; it performs no JTAG/SWD action and does not attach to the target.
- Scan commands detach any currently connected target. `attach <n>` takes an id from the scan output and does not reset the target; `run` or `start` do.
- `load` transfers the binary; if linked at Flash addresses the Flash is erased and programmed. `compare-sections` checks a CRC32 of target memory against the binary's sections.
- `start` halts at `main`; `run` lets the target run until interrupted (Ctrl-C or SIGINT).
- `set mem inaccessible-by-default off` lets GDB reach memory-mapped IO outside the known memory map. Put frequent commands in `.gdbinit`.
- `detach` and `kill` disconnect from the target; `kill` also resets the target on detach.

## Monitor commands (from `monitor help`)
`version`, `jtag_scan`, `swdp_scan` (the docs' help text name), `auto_scan`, `frequency` (sets minimum high and low times), `targets`, `halt_timeout`, `connect_rst enable|disable` (connect under reset), `reset` (pulses nRST, disconnects target), `tdi_low_reset`, `traceswo`, `heapinfo`. The list is context sensitive: for example STM32 targets add `monitor erase_mass` only after a scan finds the target. Commands take plain integers, not units (`halt_timeout 5000`).

## Power and firmware update
- VCC is off by default on UART and JTAG/SWD to avoid conflicts between power sources. `monitor tpwr enable` makes the probe a power source; on a v2 probe it also powers the voltage translator when Vtarget is not connected.
- Getting-started notes: on Windows 10, installing the WinUSB driver via Zadig exposes the probe's DFU interface so `dfu-util` can upgrade the probe firmware (not needed if you are only using the probe).

## Verify
- The scan output shows the exact target driver name.
- `compare-sections` reports no inconsistencies.

## Checked
2026-11-08. Confirmed against the Black Magic GDB commands page and Getting Started page (the old URLs redirect to the /docs/ paths now cited). The GitHub repository link was not read. Removed (not stated on these pages): macOS port names with serial suffixes, the batch-mode one-liner, `bmputil-cli`, the dfu-util command line and addresses, RTT and its v1.10 requirement, SWO Manchester detail, claims about ST-LINK/BluePill builds, the "No flash memory" gotcha, and the incorrect statement that detach leaves cores running (the docs say `kill` resets the target). Corrected `swd_scan` to the documented `swdp_scan` while noting the getting-started page also uses `swd_scan`.
Method: documentation only; no commands were run.
