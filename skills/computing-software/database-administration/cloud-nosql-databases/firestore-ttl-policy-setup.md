---
id: computing-software.database-administration.cloud-nosql-databases.firestore-ttl-policy-setup
name: firestore-ttl-policy-setup
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-ttl-policy-setup, firestore-ttl, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Delete expired documents automatically."
sources:
  - https://firebase.google.com/docs/firestore/ttl
  - https://firebase.google.com/docs/firestore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TTL policy setup

**Goal:** Delete expired documents automatically.

## Steps
- Add a timestamp field such as expireAt and create a policy: gcloud firestore fields ttls update expireAt --collection-group=sessions --enable-ttl
- Add --expiration-offset=7d to delay deletion after the timestamp; enabling a policy takes at least ten minutes. Only one field per collection group can be the TTL field.
- Documents are typically deleted within 24 hours after expiry, not at the exact time, and expired documents still appear in queries until deleted.
- TTL deletes count toward document delete costs and call snapshot listeners and Cloud Firestore triggers like normal deletes.
- TTL does not delete subcollections of the document; delete them explicitly.

## Gotcha
The field must hold a date and time value (Standard edition); any other type, or no value, disables TTL for that document.

## Verify
- [ ] A document with a past expireAt disappears within the documented window (gcloud firestore fields ttls list shows the policy state).

## Checked

2026-11-03. Confirmed on the Manage data retention with TTL policies page (gcloud firestore fields ttls update and list, --enable-ttl, --expiration-offset, 24 hour typical delay, one TTL field per collection group, ten minute enablement, subcollections not deleted, delete billing, listeners and triggers fire, value types) and the Usage and limits page.

Method: documentation only; no commands were run.
