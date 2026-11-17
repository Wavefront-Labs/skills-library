---
id: computing-software.firmware-embedded-development.bootloader-development.flash-programming-constraints-and-wear
name: flash-programming-constraints-and-wear
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [bootloader, flash-programming, erase-before-write, sector-erase, page-erase, flash-endurance, write-protection, rdp, option-bytes, unlock-sequence, flash-busy-flag, cache-invalidation, icache, self-write, firmware-embedded-development]
level: advanced
status: draft
description: "Write a bootloader's flash-programming routine correctly: erase-before-write, sector/page granularity, the unlock sequence, write-protect/RDP option bytes, and cache invalidation after self-write."
sources:
  - https://www.st.com/resource/en/programming_manual/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Flash programming constraints in a bootloader

**Goal:** write a bootloader that programs the application image into flash
correctly on every attempt, including after a bad image, without corrupting
itself or hitting endurance limits it didn't plan for.

## Erase-before-write is not optional
NOR flash can only be written from 1→0 per bit by a program operation; going
0→1 requires an **erase**, which happens at sector/page granularity (never per
byte). Writing to an un-erased page produces the AND of old and new data, not
the new data — a classic "my bootloader writes garbage" bug that only shows up
when the target page already had content (second flash, not first). Always
erase the full sector/page range the image will occupy before programming it,
and erase in units the hardware defines (check the reference manual: STM32
sector sizes vary per bank/line, e.g. 16KB/64KB/128KB mixed within one chip).

## Unlock sequences and write protection
Flash controllers require an unlock sequence (magic key writes to an unlock
register) before the first erase/program after reset, and may need to be
unlocked again per operation depending on the family. Option bytes
(`RDP` — readout protection, `WRP` — write protection) can make sectors
permanently unwritable from software until a full option-byte erase (which on
some families also mass-erases the main flash as a side effect) — never set
RDP level 2 ("no debug ever again") on anything but a verified production image;
it usually can't be undone.

## Busy-wait and operation granularity
Flash program/erase operations take milliseconds and the controller sets a busy
flag (`FLASH->SR BSY` on STM32) during that time; code must poll it (or use the
completion interrupt) and must not attempt a second operation, or read from the
flash bank being written to, while busy — reading the active bank during a
program/erase operation returns undefined data on many parts (check if the
family supports read-while-write via a second bank; not all do).

## Self-write hazards
A bootloader erasing/reprogramming the flash region it itself executes from
reads undefined/stale instructions if it's running from that same bank — this
is why dual-bank parts let the bootloader run from bank 1 while writing bank 2,
and why single-bank parts need the bootloader to copy itself to RAM (or use a
small RAM-resident flash driver) before erasing anything in its own bank.
Confirm which case applies before writing the erase routine.

## Cache invalidation after programming
Parts with an instruction cache or prefetch buffer (many Cortex-M7, newer M4)
can execute stale cached instructions from a flash region just reprogrammed.
Invalidate the I-cache (and disable prefetch during the write if the errata
sheet says so) before jumping into newly written code — check the specific
MCU's errata; this is a documented silicon gotcha on more than one family, not
a theoretical concern.

## Endurance
NOR flash is typically rated for ~10,000 program/erase cycles per sector (varies
by part; check the datasheet, not the marketing one-pager). A bootloader that
re-flashes the same sector on every boot for a "scratch" area, or during
every failed update retry without backoff, exhausts that budget over a product's
field life — bound retry counts and/or rotate which physical sector is used.

## Verify
- [ ] Full sector/page range is erased before programming, confirmed against the reference manual's erase granularity for this exact part/bank.
- [ ] Unlock sequence runs before every program/erase session; option-byte changes are deliberate and reversible (RDP level checked twice).
- [ ] Code never reads from, or issues a second flash operation into, a bank currently busy with program/erase.
- [ ] If the bootloader writes its own execution bank, it runs from RAM (or another bank) while doing so.
- [ ] I-cache/prefetch invalidated after programming on parts known to need it; a freshly flashed image boots correctly on first try, repeatedly, across power cycles.
