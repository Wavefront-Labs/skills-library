---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.ram-fault-isolation
name: ram-fault-isolation
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, ram-diagnostics, memory, memtest86, windows-memory-diagnostic, bsod, hardware-diagnostics]
level: practitioner
status: draft
description: "Isolate faulty RAM: the symptoms and stop codes that point to memory, Windows Memory Diagnostic and MemTest86 runs, stick-and-slot swapping, XMP and soldered-RAM gotchas."
sources:
  - "https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/bug-check-0x1a--memory-management"
  - "https://www.memtest86.com/"
  - "https://learn.microsoft.com/en-us/windows-hardware/drivers/whea/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ram-fault-isolation

## When to suspect RAM
- Random BSODs with varying stop codes, especially MEMORY_MANAGEMENT (0x1A),
  PAGE_FAULT_IN_NONPAGED_AREA (0x50), IRQL_NOT_LESS_OR_EQUAL (0x0A).
- Corrupted files after copies, installs failing with CRC errors, apps crashing at random.
- No POST with a memory beep/LED code; WHEA-Logger events naming memory on ECC systems.

## Test
1. Quick: `mdsched.exe` > Restart now. After boot, result is in the System log, source
   MemoryDiagnostics-Results. Default pass catches gross faults only; use Extended for a
   real test.
2. Thorough: boot MemTest86 from USB and run at least 4 full passes (overnight for
   intermittent faults). Any error is a fail; there is no acceptable error count.
3. Vendor diagnostics (Dell ePSA/SupportAssist pre-boot, HP PC Hardware Diagnostics UEFI,
   Lenovo Diagnostics) give a failure code the vendor accepts for warranty.

## Isolate the stick or slot
- Test one module at a time in the first slot; then move a known-good module across slots
  to separate a bad stick from a bad slot/board.
- Reseat and clean contacts first; oxidised or partly seated modules cause most "faults".
- Mixed kits (different speeds, ranks, vendors) can fail together and pass alone; replace
  as a matched set.

## Gotchas
- XMP/EXPO overclock profiles cause instability that looks like bad RAM; test at default
  JEDEC speed before replacing anything.
- Many thin laptops have soldered RAM; a memory fault means a board replacement under
  warranty, so log the vendor diagnostic code.
- Passing tests do not prove RAM is fine if crashes continue; move to drivers, storage and
  power next.

## Verify
After replacement, 4+ MemTest86 passes with zero errors and no new crash dumps or WHEA
memory events for a week of normal use.
