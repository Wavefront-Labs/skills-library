---
id: computing-software.firmware-embedded-development.hardware-debugging.field-crash-reporting-pipeline
name: field-crash-reporting-pipeline
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [crash-reporting, coredump, memfault, build-id, symbolication, fleet-diagnostics, minidump, hardware-debugging, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Build a field crash reporting pipeline: capture compact coredumps, embed a GNU build ID, upload on next connect, symbolicate against archived ELFs and dedupe by signature."
sources:
  - https://interrupt.memfault.com/blog/cortex-m-hardfault-debug
  - https://docs.memfault.com/docs/mcu/coredumps
  - https://sourceware.org/binutils/docs/ld/Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Field crash reporting pipelines

**Goal:** every crash in the fleet arrives as a symbolicated backtrace grouped with its duplicates,
so you fix the top crash, not the one someone happened to see.

## 1. Identify the exact build
- Link with `--build-id` (GNU ld option, pass as `-Wl,--build-id` through gcc). The `md5`, `sha1`
  and `xx` styles give an identifier that is the same for an identical output file and almost
  certainly unique among non-identical ones. It is not a checksum of the contents, and it stays
  the same if other tools modify the linked file later.
- Archive every released ELF (CI artefact store keyed by build ID). Without it, symbolication
  is impossible. The Memfault coredump format carries a build ID block and a software version block.

## 2. Capture on-device
- Memfault's coredump guidance: snapshot state into storage that survives a reboot (RAM-backed
  port, internal flash, external NOR, eMMC), then reboot at the end of saving.
- Saving all of RAM gives the best debugging, but storage may be too small or RAM may hold sensitive
  data. Choose regions instead (stack top, selected globals placed in named linker sections,
  peripheral registers). Some peripheral registers change value when read, so avoid capturing those
  where the read would hurt the running system.
- Capture the fault status registers (CFSR, HFSR, MMFAR at 0xE000ED34, BFAR at 0xE000ED38) so the
  fault can be classified; MMFAR and BFAR are only meaningful when their valid bits are set.
- If saving fails (storage already occupied by an unuploaded dump, write failure), fall back to a
  minimal record such as PC and LR.

## 3. Upload
- Send the dump on next connect (chunked), delete only after server acknowledgement, and rate-limit
  so a crash loop cannot drain the battery or data plan.
- Include a reboot counter so the backend can see crash loops.

## 4. Process
- Symbolicate against the archived ELF matching the build ID (Memfault, or your own tooling).
- Signature = top N symbolicated frames (function names, not addresses) plus the fault type.
- Group, count and track by firmware version; alert on new signatures after a release.

## Gotchas
- Stripped release builds still need the unstripped ELF archived under the same build ID.
- Dumps can contain user data: treat them as personal data where relevant (encrypt in transit,
  set a retention policy).
- Code that runs in the fault path must not depend on the RTOS or on interrupt-driven drivers.

## Verify
- [ ] A deliberately induced fault on a test device shows up symbolicated within minutes.
- [ ] Two crashes at the same site from different builds group under one signature.

## Checked
Confirmed: ld `--build-id` styles and behaviour (ld Options page); coredump storage, region choice,
read-side-effect warning, fallback trace event and build ID block (Memfault coredump page); MMFAR and
BFAR addresses and valid bits (Memfault HardFault post). Removed as unconfirmed: the `KEEP` linker
snippet, `sha1` as the default style, `addr2line` command, the LR bit 0 note, noinit-RAM and
1-4 KB stack-slice specifics.

Method: docs-checked 2026-11-09 against the ld Options page, the Memfault coredump collection page and the Memfault Cortex-M HardFault post, all fetched and searched for the claims kept.
