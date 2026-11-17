---
id: computing-software.digital-forensics-incident-response.evidence-handling.live-response-and-kape-triage-collection
name: live-response-and-kape-triage-collection
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [live-response, kape, triage-collection, targets, modules, volatile-data, velociraptor, osquery, remote-collection, incident-response, memory-acquisition, forensic-triage, dfir, at-scale-collection]
level: practitioner
status: draft
description: "Collect volatile and disk-based evidence from a running host fast with KAPE targets/modules or Velociraptor, in the right order, before a reboot or remote wipe destroys it."
sources: ["https://www.kroll.com/en/services/cyber-risk/incident-response-litigation-support/kroll-artifact-parser-extractor-kape", "https://docs.velociraptor.app/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Live response and KAPE triage collection

**Goal:** when a full forensic image of every affected host isn't feasible (hundreds
of endpoints, business can't tolerate downtime, evidence is volatile), collect the
subset that actually answers the investigative questions, fast, in the right order.
This sits inside the order-of-volatility sequencing from
computing-software.digital-forensics-incident-response.evidence-handling.forensic-acquisition-and-chain-of-custody
— live response is how you execute "disk artefacts" and "network state" steps at
speed and at scale, not a replacement for memory acquisition when memory matters.

## 1. Order on a single live host
1. Note system time vs a trusted time source (NTP) — every later timestamp correlates
   through this offset.
2. Volatile network/process state if not already captured (`netstat`, `tasklist`, or
   let the tool below do it) — this decays as connections close and processes exit.
3. Memory, if a compromise involving memory-resident malware or credential theft is
   suspected (see
   computing-software.digital-forensics-incident-response.volatility.memory-image-triage-with-volatility3)
   — do this before disk collection takes long enough that RAM contents shift
   meaningfully, and definitely before any reboot.
4. Disk-based triage artefacts (below).

## 2. KAPE: targets vs modules
KAPE has two independent jobs, often confused:
- **Targets** = *collection*. Copies specific files/paths matching curated definitions
  (`!SANS_Triage`, `KapeTriage`, or a custom `.tkape` file) — registry hives, EVTX,
  Prefetch, `$MFT`, browser artefacts, etc. — off the live/mounted system into an
  output folder, preserving original files untouched.
  ```
  kape.exe --tsource C: --tdest <OUTPUT_DRIVE>\out --target !SANS_Triage --vhdx case001
  ```
  `--vhdx` wraps the output in a VHDX container — convenient for chain-of-custody as a
  single hashable file, and directly mountable later.
- **Modules** = *processing*. Runs a parser (e.g. RECmd/RegRipper on the collected
  hives, Eric Zimmerman tools on Prefetch/MFT output) against already-collected data to
  produce CSVs. Modules operate on KAPE's own output, not the live system, so they can
  run later/elsewhere, including against output collected without ever running
  modules on the original host.
- Running `--target` and `--module` together in one invocation collects then
  immediately processes — convenient for a fast first look, but keep the raw
  **target** output as the evidence; the module CSVs are a derived/working product.

## 3. At scale: Velociraptor / osquery
Across many endpoints, KAPE per-host doesn't scale operationally. Velociraptor (VQL-based
hunts, agent-based, built for IR at scale) or osquery (SQL-style live queries against
OS state) push the same kind of targeted collection to hundreds of endpoints from a
central console, with built-in result aggregation — the collection logic (what
artefacts matter) is the same KAPE targets express, just executed differently at scale.
Use KAPE for single-host deep triage and incident scoping on a handful of hosts;
reach for Velociraptor/osquery once scoping says "check this IOC/artefact across the
whole estate."

## 4. Pitfalls
- Collecting from a **live** filesystem can miss locked files (an in-use hive or log) —
  KAPE's `--tsource` against a live `C:` drive uses raw volume access to read locked
  files, but confirm the tool version actually does this (older/misconfigured runs can
  silently skip a locked file and leave a gap you don't notice until later).
  **Unconfirmed in detail: exact locked-file handling varies by KAPE version — verify
  against the release notes for the version in use.**
- Live collection changes the live system's own artefacts (new Prefetch entry for
  `kape.exe`, EVTX logon/process-creation events for the collection tool itself,
  possibly new entries in `$MFT`/USN for staged output if written to the same volume).
  Write output to removable/network storage, never the source volume, and expect to
  explain the collection tool's own footprint if asked.

## Verify
- Hash the collection output (the VHDX/zip) immediately after collection, before
  transport.
- Spot-check that expected artefacts (a known-recent EVTX, the SYSTEM hive) are
  actually present and non-empty in the output before releasing the host.
- Record the exact target/module definition version used — target definitions update
  over time and what `!SANS_Triage` collects can change between KAPE releases.
