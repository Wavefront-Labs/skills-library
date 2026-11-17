---
id: computing-software.digital-forensics-incident-response.evidence-handling.macos-memory-acquisition-constraints
name: macos-memory-acquisition-constraints
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [macos-memory-acquisition, memory-acquisition, macos-forensics, sip, apple-silicon, dfir]
level: advanced
status: draft
description: "Understand macOS memory acquisition constraints: SIP and kernel extension limits, Apple Silicon, commercial tools, and what to collect instead when RAM is unattainable."
sources: ["https://support.apple.com/guide/security/welcome/web", "https://www.sans.org/cyber-security-courses/mac-and-ios-forensic-analysis-and-incident-response/", "https://github.com/tclahr/uac"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macOS memory acquisition constraints

**Goal:** know when full RAM capture of a Mac is realistic and what to collect otherwise.

## The constraints
- **System Integrity Protection (SIP)** and kernel extension policy block unsigned kernel
  extensions; open-source tools (OSXPmem/MacPmem) relied on kexts and stopped working on
  recent macOS without disabling security features.
- **Apple Silicon (M1+)**: kexts are deprecated and require reduced security mode set in
  recoveryOS (needs physical access, reboot, and user authentication), which destroys the
  memory you wanted.
- Commercial tools have historically offered limited support; check the current vendor
  matrix for the exact macOS version and chip before promising RAM capture.
- Volatility 3 mac plugins need a matching kernel ISF.

## What to collect instead (live, with admin)
- Process listing with full arguments and code signing: `ps auxww`, `lsof -nP`,
  `codesign -dvvv <path>` for suspicious binaries.
- Network: `lsof -i -nP`, `netstat -anv`.
- Per-process memory of a specific process (not full RAM): `lldb`/`gcore` require
  disabling protections for many processes; often impossible for platform binaries.
- Unified logs: `log collect --output /Volumes/EVID/system.logarchive` (captures recent
  logs including process launches).
- Triage collection: UAC (`./uac -p ir_triage /Volumes/EVID`) or Aftermath; collect
  `/private/var/db/` databases, LaunchAgents/Daemons, TCC.db, quarantine events.
- sysdiagnose (`sudo sysdiagnose -f /Volumes/EVID`) bundles many live-state artefacts.

## Gotchas
- Do not disable SIP on an evidence system; it reboots and modifies the system.
- FileVault plus Apple Silicon: imaging the disk later requires credentials; do a live
  logical collection while unlocked.

## Verify
Notes record macOS version, chip, SIP status (`csrutil status`), the reasoning for the
chosen collection, and hashes of everything collected.
