---
id: computing-software.digital-forensics-incident-response.evidence-handling.keeping-an-evidence-collection-log
name: keeping-an-evidence-collection-log
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [collection-log, rfc-3227, contemporaneous-notes, evidence-collection, dfir]
level: practitioner
status: docs-checked
description: "Keep a contemporaneous log of every evidence collection step per RFC 3227: who, when, UTC or local time, clock drift, tools and chain of custody."
sources: ["https://www.rfc-editor.org/rfc/rfc3227"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keeping an evidence collection log

RFC 3227 says collection methods should be transparent and reproducible, and that you should be prepared to reproduce precisely the methods you used and have them tested by independent experts. The collection log is the record that makes that possible.

## What the RFC asks you to record
- Detailed notes with dates and times, ideally with an automatic transcript (it names the Unix `script` program). The transcript file must not be written to media that is part of the evidence. Notes and print-outs should be signed and dated.
- The difference between the system clock and UTC, and for each timestamp whether UTC or local time is used. Record the extent of the system's clock drift during collection.
- Which systems were involved and where the evidence is, and the order of volatility followed for each.
- Each collection step, and anything else you questioned as possible evidence.
- The people involved: who was there, what they were doing, what they observed and how they reacted.
- Checksums and, where feasible, cryptographic signatures of the collected evidence, generated without altering the evidence.
- Chain of custody: where, when and by whom evidence was discovered, collected, handled and examined; who had custody and when; how it was stored; and, for each transfer, when and how it occurred (including shipping numbers).
- The tools used, with the means to testify to their authenticity and reliability.

## Suggested layout
One row per action with these fields: entry number, time with UTC or local stated, examiner, host or item, action, tool and where it came from, exact command, output file and media, hash, observed clock offset, observations and deviations. The RFC does not prescribe a layout; this arrangement covers its list above.

## Practice
1. Start the log before touching the system and record the state you find.
2. Record exact command lines rather than descriptions.
3. Log mistakes and deviations; do not rewrite earlier entries, add a correcting entry.
4. Keep logs and transcripts on separate media from the evidence. Keep access to evidence restricted and documented so unauthorised access can be detected.
5. Reference tool-generated logs from your log rather than retyping them.

## Verify
Another examiner could follow the log to repeat each step, and each collected item has a recorded time basis, clock offset, hash and custody trail.

## Checked
Confirmed against RFC 3227 (read in full): transparency and reproducibility, notes and transcripts, UTC and clock-drift recording, collection steps, people involved, checksums, chain of custody, archive access and tools. Removed unconfirmed content: the NIST SP 800-86 and SWGDE sources (the NIST page showed only an abstract and the SWGDE page is a document listing; no claim relied on either), the worked examples naming specific tools and versions, `Start-Transcript`, and the advice about KAPE and Velociraptor logs.

Method: docs-only read of cited pages, 2026-11-09
