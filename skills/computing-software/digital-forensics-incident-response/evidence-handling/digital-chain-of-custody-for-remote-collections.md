---
id: computing-software.digital-forensics-incident-response.evidence-handling.digital-chain-of-custody-for-remote-collections
name: digital-chain-of-custody-for-remote-collections
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [digital-chain-of-custody, chain-of-custody, remote-acquisition, cloud-evidence, dfir]
level: advanced
status: draft
description: "Maintain chain of custody when evidence is collected remotely or from cloud APIs: tool logs, hashes at source, transfer integrity and custody records without physical media."
sources: ["https://www.rfc-editor.org/rfc/rfc3227", "https://www.iso.org/standard/44381.html", "https://docs.velociraptor.app/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Digital chain of custody for remote collections

**Goal:** most enterprise evidence is now collected over the network (EDR, Velociraptor, KAPE to
S3) or from cloud APIs. There is no bag to seal; custody must be shown through logs and hashes.

## Record at collection
- Tool, version, and job identifier (Velociraptor flow ID, EDR live-response session ID, KAPE
  console log, cloud request ID).
- Who initiated it (named account, not a shared admin), from where, at what UTC time.
- Source identity: hostname plus a stable ID (agent client ID, cloud instance ID, disk serial via WMI).
- Hash computed **at the source** where the tool supports it (Velociraptor uploads record SHA-256
  and MD5; KAPE writes a hash of each copied file in its copy log).

## Transfer integrity
- TLS transport plus a hash recomputed on arrival; mismatch = re-collect.
- Upload destinations write-only for the collector credential (S3 bucket policy denying delete,
  object lock in compliance mode for high-stakes cases).
- Cloud snapshots: record snapshot ID, source volume ID, the account it was shared to, and CloudTrail event IDs for `CreateSnapshot`/`ModifySnapshotAttribute`.

## Custody record
- A custody entry per item stating each hand-off between systems and people: collected (agent) ->
  server -> evidence store -> analyst working copy.
- Keep tool audit logs (Velociraptor server audit, EDR audit trail) as exhibits; export them at case closure.

## Gotchas
- Shared service accounts destroy attribution of who collected what.
- Velociraptor/EDR data retention may delete original uploads; copy to the evidence store and hash.
- Time zones: tools log in UTC or server local time; record which.

## Verify
For any item you can show, from tool logs alone, who collected it, from which system, when, and that its hash never changed.
