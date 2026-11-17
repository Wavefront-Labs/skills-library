---
id: computing-software.cloud-infrastructure-engineering.google-cloud.firestore-and-datastore-mode
name: firestore-and-datastore-mode
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, firestore, datastore, firestore-native, datastore-mode, document-database, nosql, security-rules, composite-indexes, firestore-ttl, pitr-firestore, firestore-backups, firestore-export, named-databases, firestore-enterprise, mongodb-compatibility, hotspotting, 500-50-5-rule]
level: practitioner
status: docs-checked
description: "Operate Firestore (Native vs Datastore mode): named databases, indexes and TTL, Security Rules vs IAM, the 500/50/5 write ramp, PITR and scheduled backups."
sources: ["https://cloud.google.com/firestore/docs/firestore-or-datastore", "https://cloud.google.com/firestore/docs/best-practices", "https://cloud.google.com/firestore/docs/manage-databases", "https://cloud.google.com/firestore/docs/backups", "https://cloud.google.com/firestore/docs/pitr", "https://cloud.google.com/firestore/docs/ttl", "https://cloud.google.com/firestore/docs/concepts/index-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firestore and Datastore mode

**Goal:** a serverless document database with the mode, indexes, access model and backup policy chosen deliberately rather than by default.

## 1. Mode decision
Each database is either **Native** mode (`--type=firestore-native`) or **Datastore** mode (`--type=datastore-mode`); see "Choose between Native mode and Datastore mode" in the first source for the feature comparison (client SDKs, realtime updates, Security Rules versus IAM-only). Native mode is the choice when end-user apps talk to the database directly.

```bash
gcloud firestore databases create --database=orders --location=<LOCATION> --type=firestore-native \
  --delete-protection --enable-pitr
```
- `<LOCATION>` is a Firestore region or multi-region.
- The type can be changed with `gcloud firestore databases update --type=...`, but **only while the database is empty**.
- Named databases (other than `(default)`) let one project hold several databases.

## 2. Data model rules that prevent incidents
- **500/50/5**: start new collections at no more than 500 operations per second and increase traffic by 50 % every 5 minutes; avoid monotonically increasing keys or fields at high write rates, and keep traffic spread evenly across the key range.
- Single-field indexes are created automatically for each field; use index exemptions for large or unused fields. Array-contains and array-contains-any queries use array-element indexing (see the index overview page).
- **Composite indexes** serve multi-field queries; keep them as code and deploy them with your normal tooling.
- **TTL policy**: documents are deleted some time after the TTL timestamp (the TTL page says deletion typically occurs within 24 hours); see the TTL page for billing and the exact `gcloud firestore fields ttls` command.

## 3. Access control
- Native mode end-user access is governed by Security Rules; server SDKs with service account credentials use IAM.
- IAM roles include `roles/datastore.user`; for named databases an IAM condition on `resource.name` can scope a grant to one database (example in the manage-databases page).
- Firestore is a Google API: use VPC Service Controls rather than expecting private IPs.

## 4. Protect and recover
- **PITR** is off by default. When enabled it retains data for a 7-day window at one version per minute. Whether PITR is enabled or not, you can read documents at microsecond granularity within the past hour, no earlier than the database's `earliestVersionTime`. Recovery options include a stale read with a past timestamp or a database clone from a PITR timestamp (`--snapshot-time`, minute granularity, RFC 3339). Clone from PITR data: any minute in the last 7 days if PITR is enabled (less if enabled recently), else any minute in the past hour.
- **Scheduled backups** have a retention up to 14 weeks (`14w`); restoring creates a new database.
- Delete protection (`--delete-protection`) blocks `gcloud firestore databases delete` until it is disabled.

## Gotchas
- Missing composite indexes fail the query at runtime: test against real Firestore or the emulator with your index definitions loaded.
- Rules that allow broad reads on collections holding personal data are a common breach.
- Check the Firestore limits page for query limits (IN, array-contains-any, OR) before relying on a specific value.

## Verify
- [ ] The database's `describe` output shows the intended type and location.
- [ ] A scheduled backup exists; restore to a test database and spot-check a document.
- [ ] A load test ramps according to 500/50/5 with no latency spike.

## Checked
2026-10-31. Confirmed against the Firestore best-practices, manage-databases, backups, PITR, TTL and index-overview pages: 500/50/5 rule, `--type` values, `--delete-protection`, type change only when the database is empty, PITR 7-day window, one-minute granularity, one-hour microsecond reads and `earliestVersionTime`, 14-week backup retention, `roles/datastore.user` and the `resource.name` condition, TTL 24-hour wording.
Corrected: the old text said mode and location are immutable and that only export/import can change the mode; the manage-databases page says the type can be changed while the database is empty.
Removed as unconfirmed: example location codes, Enterprise/MongoDB edition note, the 1 MiB and one-write-per-second limits, the 30-value IN limit, read-cost and aggregation pricing statements, Key Visualizer/metric names, transaction limits, emulator and Firebase CLI commands, `bq load` and export details, and price/cost claims.
Method: documentation only; no commands were run.
