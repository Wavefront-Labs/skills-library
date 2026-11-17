---
id: computing-software.digital-forensics-incident-response.evidence-handling.remote-disk-acquisition-over-the-network
name: remote-disk-acquisition-over-the-network
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [remote-acquisition, disk-imaging, forensic-acquisition, live-response, dfir]
level: advanced
status: docs-checked
description: "Plan a remote disk acquisition: what vendor remote-access tools claim, dd operands that matter, and the RFC 3227 rules for integrity and documentation."
sources: ["https://www.f-response.com/", "https://man7.org/linux/man-pages/man1/dd.1.html", "https://www.rfc-editor.org/rfc/rfc3227"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote disk acquisition over the network

**Goal:** image a disk on a machine you cannot touch, keeping integrity and a defensible record.

## Approaches the cited pages support
- **Remote-access forensics software.** The F-Response site (vendor marketing, not a technical specification) describes software for accessing and collecting physical disks, logical volumes, physical memory, cloud servers and network shares over an IP network, with "direct, read-only access", and says any analysis software that reads a drive or share will work with it. Obtain the vendor's technical documentation before relying on any behaviour, and record the product and version.
- **Stream with dd.** dd copies a file according to operands: `if=` and `of=` (defaults to standard input and output), `bs=` (default 512 bytes), `count=`, `skip=`, `status=progress` for periodic statistics, and `conv=` flags. `conv=noerror` continues after read errors, and the man page describes `sync` as padding every input block with NULs; the page does not say how these affect forensic images, so test and record their use. A remote stream is a design choice you must justify; its transport, encryption and integrity checks are not covered by the cited pages.

## RFC 3227 rules that apply
- Follow the order of volatility and collect before analysing.
- Run collection tools you trust from protected media; a remote agent or shell relies on the target system, and the RFC warns that rootkits mean tools may not show a full picture.
- Make a bit-level copy of media, do analysis on a copy, and generate checksums (and signatures where feasible) without altering the evidence.
- Record clock drift, state whether times are UTC or local, keep detailed dated notes, and document each step so the method is reproducible.
- Respect privacy and legal constraints: collect only what you have a justification and authority to collect.

## Record
Source system and device identifier, whether the system was running, start and end times with time basis, exact commands or tool settings, tool versions, and the hashes you computed at each end.

## Verify
The record shows how integrity was checked at both ends, and that any live-system caveat is stated in the report.

## Checked
Confirmed against the F-Response home page (marketing claims only), the dd(1) man page (operands and conv flags, read) and RFC 3227 (read in full). Removed unconfirmed content: the method comparison table, ssh and netcat command lines, Velociraptor artefact names, compression and throttling advice, cloud snapshot advice, statements that live imaging produces a smear or that encrypted volumes stream as ciphertext, ddrescue-over-network advice, and the NIST SP 800-86 source (only its abstract page was readable).

Method: docs-only read of cited pages, 2026-11-09
