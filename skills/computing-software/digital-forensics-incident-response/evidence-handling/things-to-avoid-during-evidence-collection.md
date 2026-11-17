---
id: computing-software.digital-forensics-incident-response.evidence-handling.things-to-avoid-during-evidence-collection
name: things-to-avoid-during-evidence-collection
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [trusted-binaries, rfc-3227, order-of-volatility, evidence-collection, live-response, dfir]
level: practitioner
status: draft
description: "Avoid the collection mistakes RFC 3227 warns about: shutting down early, trusting system binaries, running tools that alter evidence, and losing timestamps."
sources: ["https://www.rfc-editor.org/rfc/rfc3227", "https://csrc.nist.gov/pubs/sp/800/86/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Things to avoid during evidence collection

**Goal:** do not destroy or contaminate evidence while collecting it. RFC 3227 section 2.2
lists the core mistakes; SP 800-86 adds detail.

## RFC 3227 "things to avoid", applied
- **Do not shut down until collection is done.** Shutdown loses memory, network state,
  running processes, mounted encrypted volumes; some malware deletes itself on shutdown.
- **Do not trust programs on the system.** Run tools from your own trusted, write-protected
  media (statically linked on Linux; signed known-good on Windows). An attacker may have
  replaced `ps`, `netstat`, `ls` (user-mode rootkits) or hooked APIs.
- **Do not run programs that modify access times of all files** (e.g. `tar` or `xcopy` across
  the filesystem, AV full scans) before imaging.
- **Do not take actions that the attacker could notice and react to** (e.g. pinging their
  C2, disconnecting one host) without a plan; "tripwires" may wipe the system on disconnect.

## Further common mistakes
- Installing analysis tools onto the evidence drive (overwrites unallocated space). Write
  outputs to external media or a network share.
- Logging in interactively with a domain admin to an attacker-controlled host (credential
  theft risk). Use remote tools with non-reusable credentials (e.g. EDR, restricted admin).
- Letting IT "clean up" first: AV quarantine, reimaging, log rotation, password resets.
- Opening files in their native application (updates metadata, executes macros).
- Forgetting to note the system clock offset vs true time.

## Practice
Use a written checklist per platform; record every command and its time, so any change you
caused is explainable.

## Verify
Review your collection log: every tool ran from external media, outputs went off-host, and
any unavoidable change (e.g. loading a memory driver) is documented with its time.
