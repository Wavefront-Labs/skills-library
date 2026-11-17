---
id: computing-software.digital-forensics-incident-response.evidence-handling.live-versus-dead-box-acquisition-decision
name: live-versus-dead-box-acquisition-decision
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [live-vs-dead-acquisition, order-of-volatility, live-response, dfir]
level: advanced
status: docs-checked
description: "Decide when to collect from a running system before powering down, using the RFC 3227 order of volatility, shutdown risks and documentation duties."
sources: ["https://www.rfc-editor.org/rfc/rfc3227"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Live versus dead-box acquisition decision

**Goal:** decide what to collect from a running system before it is powered down, and record why, using the guidance in RFC 3227 (BCP 55).

## What the RFC says
- Proceed from the volatile to the less volatile. Its example order: registers and cache; routing table, ARP cache, process table, kernel statistics and memory; temporary file systems; disk; remote logging and monitoring data; physical configuration and network topology; archival media.
- Do not shut down until evidence collection is complete: much evidence may be lost, and the attacker may have altered startup or shutdown scripts or services to destroy evidence.
- Do not trust programs on the system. Run collection tools from protected media (read-only media, statically linked, prepared in advance for each OS you manage). The RFC warns that rootkits installed through loadable kernel modules may mean your tools do not show the full picture.
- Do not run programs that change access times on all files (the RFC names `tar` and `xcopy`).
- Removing external avenues for change is a collection step, but simply disconnecting or filtering the network may trigger "deadman switches" that wipe evidence.
- Collect first and analyse later. Make a bit-level copy of media, and do forensics on a copy of that copy, since analysis almost certainly alters access times.
- Minimise changes to the data while collecting, including file and directory access times.
- Record the system clock's drift from UTC and state for every timestamp whether it is UTC or local.

## Decision notes
The RFC does not give a single rule for pulling power. Treat the choice as a judgement you must be able to defend:
1. List what volatile evidence (memory, process table, network state) exists and what you would lose.
2. List the risks of staying live (tools you cannot trust, changes you make to the system) and the risks of shutting down (evidence loss, scripts run at shutdown).
3. Choose the order that preserves the most relevant evidence, within your site policy and with the right people involved (incident handling, law enforcement where needed).
4. Do the volatile collection first when you are allowed to touch the running system.

## Document
Record who decided and why, exact times, what was collected in what order, system clock drift, and each step you took. Notes should be dated, and signed where printed. Be ready to repeat your methods so that independent experts can test them.

## Verify
Your notes show that the order followed the order of volatility, or explain the specific reason it did not, and that every action on the live system is recorded.

## Checked
Confirmed against RFC 3227 (read in full): order of volatility, shutdown warning, untrusted programs and prepared tools, access-time cautions, deadman-switch warning, collection steps, bit-level copy advice, clock-drift recording and documentation duties. Removed unconfirmed content: pull-the-plug versus graceful shutdown rules, full-disk-encryption and memory-key recovery claims, cloud and VM snapshot advice, commands (`manage-bde`, `fdesetup`), and the NIST SP 800-86 source (only its abstract page was readable, so no claim relied on it).

Method: docs-only read of cited pages, 2026-11-09
