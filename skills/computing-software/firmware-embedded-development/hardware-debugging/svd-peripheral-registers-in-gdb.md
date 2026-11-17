---
id: computing-software.firmware-embedded-development.hardware-debugging.svd-peripheral-registers-in-gdb
name: svd-peripheral-registers-in-gdb
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [pycortexmdebug, svd, cmsis-svd, svd-gdb, peripheral-registers, gdb-python, hardware-debugging, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Read peripheral registers by name in plain GDB using PyCortexMDebug and CMSIS SVD files: loading, svd command forms, hex formatting and read side effects."
sources:
  - https://github.com/bnahill/PyCortexMDebug
  - https://open-cmsis-pack.github.io/svd-spec/main/index.html
  - https://github.com/cmsis-svd/cmsis-svd-data
  - https://docs.memfault.com/docs/mcu/coredumps
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Peripheral registers with SVD in GDB

IDEs show a peripheral view from the vendor's CMSIS-SVD file. In command-line GDB, PyCortexMDebug
(a set of GDB/Python utilities for Cortex-M) gives the same with an `svd` command.

## What an SVD is
CMSIS-SVD is an XML description of a device's memory-mapped peripheral registers, fields and named
interrupts, comparable in detail to the reference manual. Silicon vendors maintain the files and
ship them in CMSIS Device Family Packs. The cmsis-svd-data repository aggregates SVDs from many
sources (under `data`, with each vendor's licence), including patched files.

## Setup
Clone the PyCortexMDebug repository and `source` its GDB script from your gdbinit (the README shows
`source /path/to/gdb.py`; check the repository for the current file name). It needs GDB with Python
support.
```gdb
# .gdbinit
source /path/to/gdb.py
svd_load STM32F407.svd
```
SVD files can be huge, so loading can take a second or two: load once in `.gdbinit`.

## Usage
```gdb
svd                       # list peripherals with descriptions
svd GPIOA                 # all registers of a peripheral, with values
svd GPIOA MODER           # all field values of one register, with descriptions
svd/x RCC CFGR            # hex formatting
```
Format modifiers: `/x` hex, `/o` octal, `/t` or `/b` binary, `/a` hex plus symbol resolution.
Tab completion works for nearly everything and `svd help` lists the rest. Field values are shown at
the lengths given in the SVD.

Without the plugin, read a register by address with `x/wx <address>` and decode it by hand.

## Caveats
- **Reading has side effects.** Some peripheral registers change value when read (the Memfault
  coredump guide warns about this too). Dumping a whole UART or SPI peripheral can read data
  registers and clear flags. Read single registers on live comms.
- Some parts need word-aligned reads of peripheral regions (the Memfault guide cites the nRF52840).
- SVD files are vendor-written and quirky; the PyCortexMDebug README asks for issues when a file does
  not parse. When a value looks impossible, cross-check with the reference manual.

## Verify
- [ ] `svd RCC CR` shows HSERDY/PLLRDY matching what clock init should have done.
- [ ] A field decoded by `svd` matches a manual `x/wx` read of the same register.

## Checked
Confirmed from the PyCortexMDebug README: svd_load, the svd command forms, format modifiers, the
huge-file note and the source line; from the SVD specification index and cmsis-svd-data README: what
an SVD is, who maintains it, the aggregation repository. Read side effects and word-aligned access
from the Memfault coredump page. Removed as unconfirmed: `svd set` field writes, the vendor
`.pack` zip layout, the `cmdebug/svd_gdb.py` path, disabled-clock reads as 0, the gdb-svd package
and IDE frontends, and the `-g3` struct-cast tip.

Method: docs-checked 2026-11-09 against the PyCortexMDebug README, the Open-CMSIS-SVD index, the cmsis-svd-data README and the Memfault coredump collection page.
