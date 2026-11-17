---
id: computing-software.digital-forensics-incident-response.volatility.rootkit-and-kernel-memory-analysis
name: rootkit-and-kernel-memory-analysis
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [rootkit, kernel-memory, ssdt-hooking, driver-scan, callback-scanning, hidden-process, psscan-vs-pslist, dkom, direct-kernel-object-manipulation, modscan, ssdt, volatility3, windows-kernel, dfir]
level: sme
status: docs-checked
description: "Hunt kernel-level rootkits in a memory image with Volatility 3: compare pslist vs psscan for hidden processes, scan drivers/modules, and check kernel callback tables for hooks."
sources: ["https://volatility3.readthedocs.io/", "https://github.com/volatilityfoundation/volatility3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rootkit and kernel memory analysis

**Goal:** detect malware that hides itself from the normal enumeration APIs
(Task Manager, `tasklist`, even some EDR agents that trust those same APIs) by
tampering with kernel structures — the one class of threat where memory-image
analysis finds something a live, running system genuinely cannot show you about
itself. Builds on
computing-software.digital-forensics-incident-response.volatility.memory-image-triage-with-volatility3's
baseline process/network triage.

## 1. The core technique: scan vs list, compared
Volatility offers two fundamentally different ways to enumerate processes:
- **List-walking** (`windows.pslist`) follows the kernel's own doubly-linked list of
  `EPROCESS` structures — exactly what live enumeration APIs do, and exactly what a
  rootkit using **DKOM (Direct Kernel Object Manipulation)** defeats by unlinking its
  process's entry from that list.
- **Pool/signature scanning** (`windows.psscan`) scans physical memory for the
  `EPROCESS` structure's pool tag/signature directly, independent of the linked list
  — finds a process even if it's been unlinked from pslist's view, because the
  structure itself is still sitting in memory.
**A process present in `psscan` but absent from `pslist` is the single strongest,
most specific rootkit indicator available in memory forensics.** Run both on every
case where rootkit activity is even plausible, not just when something else already
looks wrong — DKOM hiding leaves no other symptom by design.
- The same list-vs-scan contrast applies to other object types: `windows.netscan`
  (scan-based) vs relying on a process's own handle table for network state,
  `windows.modules` vs `windows.modscan` for kernel drivers — a driver present in
  `modscan` but missing from the kernel's own loaded-module list is the DKOM
  equivalent for drivers.

## 2. Driver and module inspection
```
vol -f mem.dmp windows.modules          # kernel's own loaded-module list
vol -f mem.dmp windows.modscan           # pool-scan for driver objects, catches unlinked ones
vol -f mem.dmp windows.driverscan        # pool-scan for driver objects
```
An unsigned or unknown-named driver loaded outside the usual Windows/vendor driver set
is worth pulling and reversing (see
computing-software.digital-forensics-incident-response.malware-analysis.advanced-static-analysis-disassembly-and-unpacking) —
kernel-mode code can do far more damage/concealment than a user-mode process, and a
rootkit driver is often small and purpose-built, easier to fully reverse than a large
user-mode payload.

## 3. Kernel callback and hook scanning
```
vol -f mem.dmp windows.ssdt               # (where supported) system call table entries
vol -f mem.dmp windows.callbacks          # kernel callbacks and notification routines, including registry and bugcheck callbacks
```
Legitimate AV/EDR products *also* register kernel callbacks and sometimes hook the
SSDT (older/32-bit-era AV in particular) — a callback pointing into an unexpected or
unsigned module is the actual signal, not the mere presence of callbacks/hooks.
Resolve each callback's target address to a module (`windows.modules` output) and
treat anything resolving outside a known, signed module as worth pulling and
reversing. Double-check an SSDT anomaly is not a symbol-table misread before
reporting it.

## 4. Symbol tables matter even more here
Kernel-structure analysis is more sensitive to an exact-build symbol table match than
user-mode process analysis — a slightly mismatched table can misinterpret kernel
structure offsets entirely, producing plausible-looking but wrong output (a phantom
"hidden process" that's actually a parsing error, or a real hidden process missed
because the scan silently failed on that structure). Always confirm Volatility
resolved symbols cleanly for the target build (no ISF/symbol warnings in the output)
before trusting a rootkit finding, and corroborate a kernel-level finding with a
second independent signal (e.g. a psscan-only process also having an active network
connection in `netscan`, or a suspicious driver's file also showing up in disk-side
triage) before reporting it as confirmed.

## Verify
- Confirm `pslist` vs `psscan` (and `modules` vs `modscan`) were both run and
  diffed on every case where rootkit/DKOM activity is plausible.
- Confirm symbol-table resolution was clean for the exact build before trusting any
  kernel-structure-dependent plugin output.
- Corroborate a flagged hidden process/driver/callback with at least one independent
  signal before treating it as confirmed rather than a parsing artifact.

Unconfirmed: this is SME-level, fast-moving territory — exact plugin availability and
behaviour (ssdt/callbacks support) varies by Volatility 3 version and Windows build;
verify plugin support for the specific target OS version before relying on a negative
result (no callbacks/hooks found) as conclusive.

## Checked

- Confirmed: all plugin names exist with the described purposes (callbacks lists kernel notification routines, registry and bugcheck callbacks).

Method: docs-checked 2026-11-09 against volatility3 develop source plugins/windows/{pslist,psscan,modules,modscan,driverscan,ssdt,callbacks}.py (MITRE source was unreadable and was dropped). Removed the PatchGuard claim and unconfirmed driverscan device-object detail; rootkit-hunting heuristics (pslist vs psscan diff, AV callbacks) are practitioner guidance.
