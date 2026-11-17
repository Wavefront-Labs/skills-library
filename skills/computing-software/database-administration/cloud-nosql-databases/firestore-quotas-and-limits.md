---
id: computing-software.database-administration.cloud-nosql-databases.firestore-quotas-and-limits
name: firestore-quotas-and-limits
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-quotas-and-limits, firestore-limits-hotspots, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Design inside Firestore limits."
sources:
  - https://firebase.google.com/docs/firestore/quotas
  - https://firebase.google.com/docs/firestore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quotas and limits

**Goal:** Design inside Firestore limits.

## Steps
- Document 1 MiB (1,048,576 bytes); field value 1 MiB - 89 bytes; document and collection IDs at most 1,500 bytes; API request 10 MiB.
- Index entries per document 40,000; composite indexes per database 200 without billing enabled and 1000 with billing; indexed field values over 1500 bytes are truncated.
- Subcollection depth 100; map and array depth 20; transaction time limit 270 seconds with a 60-second idle expiry; 500 field transformations per document in one commit or transaction; 100 databases per project.
- Free quota (one free database per project): 1 GiB stored data, 50,000 reads, 20,000 writes and 20,000 deletes per day, 10 GiB outbound transfer per month; TTL deletes, PITR, backups, restores and clones have no free usage.

## Gotcha
Quotas and limits change; confirm on the current quotas page.

## Verify
- [ ] Design notes list each limit relevant to the model and the expected headroom.

## Checked

2026-11-03. Confirmed against the Usage and limits page, last updated 2026-10-28. Removed: the 1 write per second per document figure and the 500-operation batch and transaction write limits, which the page does not list.

Method: documentation only; no commands were run.
