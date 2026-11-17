---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.hardware-diagnostics-and-triage
name: hardware-diagnostics-and-triage
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, hardware, post-codes, beep-codes, memtest, dell-supportassist, hp-pc-hardware-diagnostics, lenovo-diagnostics, battery-health, bitlocker-recovery, swap-test, no-boot, no-post]
level: practitioner
status: draft
description: "Physical hardware triage: POST/beep codes, vendor diagnostics (Dell SupportAssist, HP PC Hardware Diagnostics), memory/disk stress tests, battery health, swap-testing method."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# hardware-diagnostics-and-triage

Goal: decide "software fault, needs a fix" vs "hardware fault, needs a
part/RMA" quickly, instead of reinstalling an OS three times on a machine
with a failing RAM stick.

## No-boot triage: before touching the OS at all
- **No power at all** (no fans, no lights): check the power source
  itself first — a different known-good outlet/cable/charger before
  opening the case; a surprising number of "dead laptop" tickets are a
  failed charging brick, not the machine.
- **Powers on, no display**: listen/watch for **POST (Power-On
  Self-Test)** signals — beep codes (pattern varies by BIOS vendor,
  check the motherboard/OEM manual for the exact sequence) or, on
  systems with them, diagnostic LEDs (Dell has colored LED sequences on
  some models, HP/Lenovo have their own). A consistent beep/LED pattern
  before the OS ever loads is hardware-level (RAM, GPU, motherboard) —
  don't troubleshoot a "corrupted Windows install" when it never got
  that far.
- **Boots partway, stops at a vendor logo or spinning indefinitely
  with no OS error**: this is the ambiguous zone — could be disk
  failure, boot-order misconfiguration, or an OS-level problem. Go to
  vendor diagnostics (below) before assuming OS corruption.

## Vendor pre-boot diagnostics (run these before OS-level troubleshooting)
- **Dell**: `SupportAssist` (OS-level) or the pre-boot diagnostics
  (F12 at boot → Diagnostics, or hold the diagnostic button on some
  models) runs hardware tests outside the OS — RAM, storage, battery,
  thermal — and gives a vendor error code useful for warranty claims.
- **HP**: `HP PC Hardware Diagnostics` (UEFI version, accessible via
  F2 at boot on many models, or downloadable bootable USB version) —
  same purpose, HP's own error/failure ID format.
- **Lenovo**: `Lenovo Diagnostics` (bootable, via Novo button or F10/F12
  depending on model).
- Running the vendor's own tool matters beyond convenience: the error
  codes it produces are usually required for a warranty/RMA claim —
  doing a generic `memtest86` pass instead and getting a clean result
  doesn't help if the vendor's own diagnostic (which may test more
  aggressively or differently) is what support actually asks for.

## Memory and storage stress testing
- `memtest86` (free, bootable) or `memtest86+` for RAM — run **multiple
  passes** (a single pass can miss intermittent errors); an overnight
  run (several hours) is standard practice for a machine with
  unexplained intermittent crashes/BSODs before ruling RAM out.
- Disk health: `CrystalDiskInfo` (Windows, reads SMART data) or
  `smartctl` (cross-platform) for SSD/HDD health attributes — a rising
  reallocated-sector count or a SMART "pre-fail" status on a drive
  explains intermittent read errors/freezes far better than continued
  OS-level troubleshooting will.
- Thermal: a machine that only crashes under load (gaming, video
  export, long builds) and never at idle is a strong thermal-throttling
  or failing-fan signal — check CPU/GPU temps under load (HWiNFO or
  similar) before assuming it's a software crash.

## Battery health (laptops)
- Windows: `powercfg /batteryreport` generates an HTML report showing
  design capacity vs full-charge capacity over time — a battery holding
  well under 80% of design capacity is a legitimate hardware-replacement
  case, not a "calibrate your battery" software fix.
- A battery reporting 0% or failing to charge at all while the laptop
  runs fine on AC power is almost always the battery itself or its
  connector, not a driver issue — swap-test (below) confirms quickly if
  spares exist.

## The swap-test method (fastest way to isolate without a full diagnostic suite)
- When unsure whether a fault is the machine, a peripheral, or a cable:
  swap **one variable at a time** with a known-good spare — same cable,
  different monitor; same monitor, different cable; same everything,
  different machine. This is literally the "change one variable" rule
  from `systematic-problem-isolation` applied to physical components,
  and it's usually faster than any diagnostic tool when a spare is on
  hand.
- Document which swap fixed it before reassembling — "it just started
  working" without noting which swap did it means re-diagnosing from
  scratch if the symptom returns.

## Gotchas
- A BIOS/UEFI update can fix hardware-adjacent issues that look like
  component failure (fan control bugs, false thermal shutdowns, battery
  reporting bugs) — check for a pending firmware update before ordering
  a replacement part.
- Intermittent faults that only occur under specific conditions (heat,
  vibration, a specific port) are the hardest to diagnose and the
  easiest to misdiagnose as software — if a clean OS reinstall doesn't
  resolve a recurring issue, stop reinstalling and go back to hardware
  diagnostics rather than repeating the same non-fix.
- Liquid/physical damage voids most standard warranties — note visible
  damage before starting any diagnostic, it changes both the
  troubleshooting approach (assume component damage, don't just swap
  parts and ship it back as a standard fault) and the support path.

## Verify
- Vendor pre-boot diagnostic passes clean (or returns the specific
  failure code used for the RMA/replacement decision), the component
  identified as faulty is confirmed by a swap test with a known-good
  spare, and the machine holds up under the same load/conditions that
  originally triggered the symptom, not just at idle immediately after
  the fix.
