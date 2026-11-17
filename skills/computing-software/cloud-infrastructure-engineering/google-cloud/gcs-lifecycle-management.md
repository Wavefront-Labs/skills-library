---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gcs-lifecycle-management
name: gcs-lifecycle-management
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-storage, gcs, object-lifecycle-management, lifecycle-rules, storage-classes, standard, nearline, coldline, archive, autoclass, setstorageclass, abortincompletemultipartupload, object-versioning, noncurrent-versions, numnewerversions, days-since-noncurrent-time, soft-delete, retention-policy, bucket-lock, object-holds, minimum-storage-duration, early-deletion, storage-insights, gcloud-storage]
level: practitioner
status: docs-checked
description: "Manage GCS object lifecycle: Autoclass vs explicit SetStorageClass rules, versioned-object cleanup, soft-delete cost, retention locks, and the minimum-duration and operation-cost traps."
sources: ["https://docs.cloud.google.com/storage/docs/lifecycle", "https://docs.cloud.google.com/storage/docs/storage-classes", "https://docs.cloud.google.com/storage/docs/autoclass", "https://docs.cloud.google.com/storage/docs/soft-delete", "https://docs.cloud.google.com/storage/docs/bucket-lock", "https://docs.cloud.google.com/sdk/gcloud/reference/storage/buckets/update"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GCS lifecycle management — classes, rules and the hidden bytes

**Goal:** each bucket either lets Autoclass tier it or carries explicit rules matched to
its access pattern, versioned and soft-deleted bytes stay bounded, and retention that
must hold is locked.

## 1. Classes are a property of each object, all online
| Class | Min. storage duration | Retrieval fee |
|---|---|---|
| Standard | — | none |
| Nearline | 30 days | per GB |
| Coldline | 90 days | higher per GB |
| Archive | 365 days | highest per GB |
Unlike S3 Glacier and Azure Archive, **no GCS class needs an offline restore step**: even
Archive data is available within milliseconds. Cost lives in retrieval and operation fees, and in early
deletion fees when an object is deleted before its class's minimum duration (time in the
original class counts toward the minimum). A lifecycle class change itself incurs no
retrieval or early-deletion fee, but a lifecycle `Delete` before the new class's minimum does.

## 2. Autoclass or explicit rules?
- **Autoclass** (per bucket): new objects start in Standard and move to Nearline after 30 days
  without access (the default terminal class); with the terminal class set to Archive they continue to Coldline
  after 90 days and Archive after 365 days without access. Reading an object's data moves it back to Standard.
  Retrieval and early-deletion fees generally do not apply, and Autoclass's own transitions incur no
  operation charges. There is a management fee and a one-time enablement charge, and objects under 128 KiB stay in
  Standard. Choose it when access is unpredictable.
- A bucket cannot combine Autoclass with lifecycle rules that use `SetStorageClass` or a `matchesStorageClass` condition (`Delete` rules are still allowed).
- **Explicit rules** when access is predictable (logs, backups) and you want Archive
  pricing from day N with no management fee.

## 3. Write rules
```json
{"lifecycle": {"rule": [
 {"action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
  "condition": {"age": 30, "matchesPrefix": ["logs/"], "matchesStorageClass": ["STANDARD"]}},
 {"action": {"type": "Delete"}, "condition": {"age": 400, "matchesPrefix": ["logs/"]}},
 {"action": {"type": "Delete"}, "condition": {"isLive": false, "daysSinceNoncurrentTime": 30}},
 {"action": {"type": "Delete"}, "condition": {"isLive": false, "numNewerVersions": 5}},
 {"action": {"type": "AbortIncompleteMultipartUpload"}, "condition": {"age": 7}}
]}}
```
Apply: `gcloud storage buckets update gs://<BUCKET> --lifecycle-file=lifecycle.json`
(clear with `--clear-lifecycle`). A rule has exactly one action.
- Conditions inside one rule are **AND**; across rules with the same action, meeting any one rule triggers it (**OR**).
- If an object matches both a Delete and a SetStorageClass rule, Delete wins; among
  class changes, the one moving the object to the class with the lowest at-rest price wins.
- `matchesStorageClass` stops rules re-acting on objects already moved and lets you chain
  Standard → Nearline → Coldline correctly.
- Other conditions: `matchesSuffix`, `createdBefore`, `customTimeBefore` /
  `daysSinceCustomTime` (set `Custom-Time` metadata to e.g. the business date of a record),
  `noncurrentTimeBefore`, `sizeAboveBytes` / `sizeBelowBytes`.
- `age` is measured from creation time; a lifecycle class change updates the modification time, not the creation time.

## 4. Versioning and soft delete
- With versioning on, a delete or overwrite makes the live version **noncurrent** and it
  is billed until a rule with `isLive: false` removes it. No noncurrent rule = unbounded growth.
- **Soft delete** is on by default for new buckets that support it (7-day retention; configurable 7 to 90 days, and 0 disables it). Soft-deleted data keeps incurring storage charges until its retention ends — on high-churn
  buckets this can exceed the live data. Set `--soft-delete-duration=0` where data is
  reproducible, keep it on for critical buckets.
- With versioning on, deleting a live object makes it noncurrent, and deleting a noncurrent object makes it soft-deleted.

## 5. Retention that must hold
- **Bucket retention policy**: objects can only be deleted or replaced once their age exceeds the retention period; **Bucket Lock** makes the policy permanent (it cannot be removed or reduced, though it can be increased, and the bucket cannot be deleted unless every object has met the retention period).
- **Object holds** (event-based or temporary) for legal hold on specific objects; the retention period restarts when an event-based hold is released.
- Lifecycle `Delete` on retained objects is deferred until retention expires.

## Gotchas
- Changes to a bucket's lifecycle configuration can take up to 24 hours to go into effect, and the old configuration may still run meanwhile.
- Each `SetStorageClass` transition is a Class A operation charged at the **destination**
  class rate (it does not rewrite the object); billions of small objects make tiering uneconomic — aggregate first.
- Changing a bucket's default storage class only affects new objects; existing objects are not changed.
- Check current Cloud Storage pricing for Autoclass management fees and soft-delete charges.

## Verify
- [ ] Each bucket is either Autoclass or has explicit rules, with a written reason.
- [ ] Every versioned bucket has `isLive: false` delete rules (age and/or count).
- [ ] Soft-delete duration set deliberately per bucket; Storage Insights/billing shows soft-deleted bytes bounded.
- [ ] `AbortIncompleteMultipartUpload` present on buckets receiving multipart uploads.
- [ ] Locked retention only where regulation requires it, recorded with the lock date.

## Checked
Checked 2026-10-24 against the Cloud Storage lifecycle, storage classes, Autoclass, soft delete and Bucket Lock documentation and the gcloud `storage buckets update` reference (docs.cloud.google.com). Confirmed minimum storage durations, the lifecycle actions and conditions used, AND/OR and conflict rules, the 24-hour propagation note, Autoclass transitions and restrictions, soft-delete defaults and range, retention and Bucket Lock behaviour, and the flags `--lifecycle-file`, `--clear-lifecycle` and `--soft-delete-duration`. Wrong claims fixed: when several class changes apply the lowest-priced class wins (not simply the colder one); Autoclass fees generally do not apply but a management fee does; soft-delete billing is not documented as the object class rate; the "all classes millisecond access" wording is narrowed to what the page states. Removed the early-deletion-on-rewrite claim and the dual-region and Turbo replication remark.
Method: documentation only; no commands were run.
