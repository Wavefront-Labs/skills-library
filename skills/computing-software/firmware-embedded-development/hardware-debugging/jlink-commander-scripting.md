---
id: computing-software.firmware-embedded-development.hardware-debugging.jlink-commander-scripting
name: jlink-commander-scripting
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [jlink-commander, segger-jlink, jlinkexe, command-file, production-programming, loadfile, mem32, swd, j-link, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Script SEGGER J-Link Commander for flashing and register pokes: command-line options, command files, loadfile, verifybin, memory access, probe selection and exit codes."
sources:
  - https://wiki.segger.com/J-Link_Commander
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# J-Link Commander scripting

**Goal:** repeatable, non-interactive flash/erase/inspect operations with a J-Link probe for
bench scripts, test fixtures and CI. Commander is mainly an interactive tool, but it can be automated.

## Invocation
```sh
JLink.exe -device CC2538SF53 -if JTAG -speed 4000 -jtagconf -1,-1 -autoconnect 1 -CommandFile flash.jlink
```
(`JLink.exe` on Windows; the Linux binary is `JLinkExe`.) Options from the wiki table:
- Batch: `-AutoConnect 1` connects automatically, `-CommandFile <path>` runs a command file, `-ExitOnError 1` exits on
  error, `-NoGui 1` suppresses GUI dialogs.
- Probe selection: `-USB <SerialNo / Nickname>` (from V7.92d) when several probes are on one PC; `-IP <...>` for TCP/IP.
- Device: `-Device`, `-If`, `-Speed`, `-JLinkScriptFile <path>`, and `-JTAGConf <IRPre>,<DRPre>` (`-1,-1` auto-detects).
- Misc: `-Log <path>`, `-RTTTelnetPort <port>`.

A command file is one command per line, as if typed in the terminal. A file can also configure the connection itself:
```
device CC2538SF53
si JTAG
speed 4000
jtagconf -1,-1
connect
```
A probe can also be chosen by putting `SelectEmuBySN <SN>` as the first command in the file.

## Flash example
```
r
h
loadfile build/app.hex
verifybin build/app.bin 0x08000000
r
g
exit
```
- `loadfile <file> [<addr>] [noreset|reset]` programs .bin, .elf, .hex, .mot, .s, .s19, .s37 and .srec files.
  The address is only used for .bin (0x0 if omitted). It verifies by default.
  Examples: `loadfile MyData.bin 0x08000000`, `loadfile MyData.hex 0 noreset`.
- `verifybin <file> <addr>` only reads memory and compares it to the file. It does no flash or QSPI initialisation,
  and a preceding `loadfile` does not guarantee it works for external flash, because `loadfile` restores controller
  state when it finishes.
- `exit` closes the target and probe connection and quits.

## Useful commands
| Command | Effect |
|---|---|
| `r`, `h`, `g`, `s` | reset, halt, go, step |
| `erase [<SAddr> <EAddr>] [noreset\|reset]` | erase flash (range) of the selected device |
| `mem32`, `mem8`, `mem16`, `mem` | read memory |
| `w4`, `w1`, `w2`, `w8` | write 32/8/16/64-bit items |
| `regs` | display CPU registers |
| `savebin <file> <addr> <numbytes>` | save target memory to a binary file |
| `setpc`, `setbp` | set PC, set breakpoint |
| `sleep <ms>` | wait, for command scripts |
| `exec <command string>` | run a J-Link Command String, e.g. `exec SupplyPower = 1` |
| `rsettype <n>` | change reset strategy, e.g. `RSetType 3` |
| `eoe 1` | toggle exit on error |

Note: in the license command list, `erase` means erase all custom licenses on the probe; it is not the flash erase.

## Exit codes
The Commander return value is read from `ERRORLEVEL` on Windows. The wiki shows an invalid interface parameter
(`-if InvalidInterfaceParameter`) giving 1, and a normal start giving 0. Check the code in your own script and test
with a wrong `-device` name, since the wiki does not list every failure case.

## Gotchas
- Pin the J-Link software version and re-run your script when upgrading, since output text can differ.
- `-JLinkScriptFile` is a separate J-Link script mechanism, selected per run.

## Verify
- [ ] Script returns exit code 0 on success and non-zero with a wrong `-device` name.
- [ ] `verifybin` passes; device boots after the final `r`/`g`.

## Checked
Method: docs-checked 2026-11-09 against the SEGGER wiki J-Link Commander page (command table, command specifics, options table, batch processing and return value sections read). The UM08001 PDF source was dropped (not read). Removed unconfirmed claims: `qc`, `-SelectEmuBySN` as a command-line option, `-speed adaptive`, `unlock kinetis`, nrfjprog and nrfutil recovery, `exec SetRTTAddr`, J-Flash project command line, `Verify failed` log text, "script waits without qc".
