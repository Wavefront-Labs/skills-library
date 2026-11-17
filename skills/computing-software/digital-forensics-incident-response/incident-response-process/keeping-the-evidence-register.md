---
id: computing-software.digital-forensics-incident-response.incident-response-process.keeping-the-evidence-register
name: keeping-the-evidence-register
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [evidence-register, incident-documentation, chain-of-custody, case-tracking, dfir]
level: practitioner
status: draft
description: "Maintain a case evidence register: item numbering, fields per item, derived artefacts, hash records, storage location and reconciliation at closure."
sources: ["https://www.rfc-editor.org/rfc/rfc3227", "https://csrc.nist.gov/pubs/sp/800/86/final", "https://www.swgde.org/documents/published-complete-listing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Keeping the evidence register

**Goal:** one authoritative list of every evidence item in the case - physical media, images,
memory dumps, triage packages, log exports, cloud snapshots - so anyone can answer "what do we
have, where is it, and can we prove it is unaltered?"

## Numbering
- `<CASE>-<NNN>` for original items, `<CASE>-<NNN>.<n>` for derivatives (an image of item 003 is
  003.1, an export from that image 003.1.1). Never reuse numbers.

## Fields per item
| Field | Example |
|---|---|
| Item ID | IR2026-014-007 |
| Description | Memory image, host FIN-WS042 |
| Type | memory / disk image / triage / logs / cloud snapshot / physical |
| Source | hostname, serial, cloud resource ARN, account |
| Collected by / when (UTC) | name, 2026-10-12T14:03Z |
| Method / tool + version | WinPmem 4.0.rc1 via EDR live response |
| Hash (algorithm + value) | SHA-256 ... |
| Size | 32 GiB |
| Storage location | evidence NAS path / bucket + object key / locker shelf |
| Custody form ref | CoC-0007 |
| Notes | collected after attacker activity at 13:40 |

## Practice
- Register the item when collected, not at the end of the week.
- Record hashes as computed by the acquisition tool and re-verify on intake; note both.
- Remote collections: record the agent job ID / flow ID so the collection can be traced in tool logs.
- Working copies used for analysis are not separate items, but note which copy each analyst used.

## At closure
- Reconcile the register with storage: every item present, hashes re-verified, retention dates set.
- Record disposition (retained until date / destroyed by whom, when, method).

## Gotchas
- Spreadsheets on a shared drive the attacker can reach; keep the register in the case platform or offline store.
- Missing tool versions undermine later validation questions.

## Verify
A random item can be located and its hash re-verified in minutes, and the register matches storage at closure.
