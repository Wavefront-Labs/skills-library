---
id: computing-software.firmware-embedded-development.hardware-debugging.bring-up-smoke-test-firmware
name: bring-up-smoke-test-firmware
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [board-bring-up, smoke-test, hardware-test-firmware, memory-test, address-test, moving-inversions, production-test-reuse, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Write bring-up firmware that exercises a new board's subsystems, with a RAM test plan (address, moving inversions, random, bit fade) borrowed from MemTest86."
sources:
  - https://www.memtest86.com/tech_individual-test-descr.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bring-up smoke test firmware

**Goal:** a separate, simple firmware that proves each hardware block works, isolating board faults
from application bugs, and reusable later in production test.

## Structure (general practice)
Build it as a console-driven menu so one test can be rerun on a probed board, print machine-readable
result lines for automation, and keep it independent of the application (minimal drivers, no RTOS)
so a broken subsystem cannot hang everything. Start with the simplest proof of life (an LED, then a
serial log) before testing anything that needs them. Record expected versus actual values, not just
pass or fail. Keep it in the repository and update it first for each hardware revision.

## Memory test plan
MemTest86's documented test sections give a proven ordering for a RAM test, arranged so errors are
found as fast as possible. Adapt the ideas to external RAM on the target (the tool itself is a PC
program):
1. **Address test, walking ones:** tests all address bits using a walking-ones address pattern.
2. **Address test, own address:** write each address with its own address, then check. This catches
   addressing errors the previous test missed.
3. **Moving inversions with all ones and zeros:** finds "hard" errors and some subtle ones quickly.
4. **Moving inversions with a walking 8 bit pattern:** better at detecting subtle errors in wide
   memory chips.
5. **Moving inversions with a random pattern and its complement:** effective for data sensitive
   errors; the sequence differs each pass, so more passes help.
6. **Moving inversions with a 32 bit pattern shifted per address:** 32 passes cover every pattern;
   effective but slow.
7. **Modulo-20 random pattern:** can reveal errors that moving inversions miss because of cache and
   buffering.
8. **Bit fade:** fill with all ones or all zeros, wait a few minutes, check for changed bits.
9. **Row hammer and DMA tests:** repeated access of rows in the same bank to find disturbance errors
   (relevant to DRAM from 2010 onward), and DMA based transfers to catch errors exposed by DMA access.

Notes from the page: enabling the cache interferes with the algorithm to some degree but makes the
test fast; the block-move test cannot say where an error occurred, only where the bad pattern was
found, so use address tests when you need to localise a fault.

## From bring-up to production
Reuse the same firmware with fixture control, serial number writing and a host script that logs
results by serial number.

## Verify
- [ ] Each test fails when its subsystem is deliberately broken (device removed, line shorted).
- [ ] The memory test detects a forced stuck bit and a forced address short.
- [ ] Full run time fits the production cycle time.

## Checked
Confirmed from the MemTest86 individual test descriptions page: the test sections, their algorithms
and the notes on cache, block move localisation, bit fade and row hammer. Removed as unconfirmed:
the numbered peripheral order (clock measurement, I2C scan, SPI ID reads, GPIO walk, ADC and DAC
checks) and the ST AN2586 source (page errors). The structure advice is general practice and not
sourced.

Method: docs-checked 2026-11-09 against the MemTest86 individual test descriptions page.
