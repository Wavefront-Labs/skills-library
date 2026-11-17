---
id: computing-software.database-administration.cloud-nosql-databases.firestore-multi-region-and-databases
name: firestore-multi-region-and-databases
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-multi-region-and-databases, firestore-cost-capacity, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Select location and structure databases."
sources:
  - https://firebase.google.com/docs/firestore/locations
  - https://firebase.google.com/docs/firestore/quotas
  - https://firebase.google.com/docs/firestore/pricing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Locations, editions and multiple databases

**Goal:** Select location and structure databases.

## Steps
- Location is set at creation: regional or multi-region (for example nam5 or eur3); once provisioned it cannot be changed.
- The SLA uptime is 99.999% or more for multi-region and 99.99% or more for regional locations; see the pricing page for cost differences.
- On the Blaze plan you can create multiple databases per project (up to 100 by default), each with its own location; backup schedules are configured per database, and only one database per project gets the free quota.
- Firestore has Standard and Enterprise editions; some data types, TTL and index options differ by edition, so check the page for your edition.

## Gotcha
A location chosen for the wrong region adds permanent latency; plan before creating.

## Verify
- [ ] gcloud firestore databases describe --database=DATABASE_ID shows the expected locationId and type for each database.

## Checked

2026-11-03. Confirmed on the Firestore locations page (immutable location, nam5 and eur3, SLA percentages, multiple databases on Blaze), the quotas page (100 databases per project, one free database) and the PITR page (describe output fields locationId and type). Removed: the per-database rules and indexes claim, the cost claim and the MongoDB-compatibility availability claim.

Method: documentation only; no commands were run.
