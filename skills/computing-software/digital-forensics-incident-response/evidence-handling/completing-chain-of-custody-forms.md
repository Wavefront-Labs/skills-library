---
id: computing-software.digital-forensics-incident-response.evidence-handling.completing-chain-of-custody-forms
name: completing-chain-of-custody-forms
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [chain-of-custody-form, chain-of-custody, evidence-log, documentation, iso-27037, dfir]
level: practitioner
status: draft
description: "Complete chain-of-custody forms and the master evidence log correctly: required fields, every transfer signed, digital-only evidence, and common defects."
sources: ["https://www.rfc-editor.org/rfc/rfc3227", "https://www.nist.gov/document/sample-chain-custody-formdocx", "https://www.iso.org/standard/44381.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Completing chain-of-custody forms

**Goal:** an unbroken, documented record of who had each item of evidence from collection
to disposal (RFC 3227 4.1; ISO/IEC 27037; NIST sample chain of custody form).

## Master evidence log (one per case)
Evidence ID, description (make/model/serial or file name), source (custodian, location),
collected by, date/time (UTC), method/tool, hash(es) at acquisition, storage location,
current custodian, status (in storage, in analysis, returned, destroyed).

## Per-item chain-of-custody form
Header: case number, evidence ID, description, serial numbers, hashes, where and how
seized/acquired, by whom.
Transfer table, one row per hand-over:
| Date/time | Released by (name, signature) | Received by (name, signature) | Purpose | Location |
Every row needs **both** signatures. Gaps (an item sitting on a desk overnight unrecorded)
are what opposing counsel looks for.

## Digital-only evidence (images, log exports, cloud data)
- Same discipline: evidence ID, hash at creation, storage path, access log of the evidence
  store, and transfers recorded (copying to an analyst workstation is a transfer of a
  working copy; the master stays put).
- Cloud exports: record the API/console used, account, query, time and hash of export file.

## Common defects
Missing time zone, illegible names without printed version, hash recorded but algorithm not
named, evidence ID mismatch between label and form, corrections with whiteout (strike
through once, initial and date instead).

## Verify
Pick any item: you can account for every hour from acquisition to now with a signed entry,
and the current hash matches the acquisition hash.
