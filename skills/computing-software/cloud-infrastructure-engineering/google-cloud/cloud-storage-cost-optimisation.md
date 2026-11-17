---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-storage-cost-optimisation
name: cloud-storage-cost-optimisation
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cost-optimisation, storage-cost-optimisation, autoclass, lifecycle-rules, storage-insights, soft-delete-cost]
level: practitioner
status: docs-checked
description: "Cut Cloud Storage cost: choose storage classes and minimum durations, write lifecycle rules, skip small objects, and control soft delete cost on temporary data."
sources: ["https://cloud.google.com/storage/docs/storage-classes", "https://cloud.google.com/storage/docs/lifecycle", "https://cloud.google.com/storage/docs/soft-delete#cost"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Storage cost optimisation

Prices are not kept here: see the Cloud Storage pricing page.

## Storage classes (storage classes page)
| Class | API name | Minimum duration | Retrieval fees |
|---|---|---|---|
| Standard | STANDARD | none | none |
| Nearline | NEARLINE | 30 days | yes |
| Coldline | COLDLINE | 90 days | yes |
| Archive | ARCHIVE | 365 days | yes |
- Rule of thumb from the page: Nearline for data read or modified about once a month or less; Coldline at most once a quarter; Archive less than once a year. Colder classes have lower at-rest cost but higher access and operation costs and slightly lower availability.
- A bucket's default class is Standard if you do not set one; changing the default does not affect existing objects. Change an existing object's class by rewriting it or with Object Lifecycle Management. Autoclass lets Cloud Storage manage transitions automatically.
- There is no minimum object size for any class.
- Legacy classes (Multi-Regional, Regional, DRA) exist; with Autoclass they count as different from Standard and objects move to Standard.

## Lifecycle rules (Object Lifecycle Management)
A rule has one action (`Delete`, `SetStorageClass`, `AbortIncompleteMultipartUpload`) and one or more conditions that must all match. Conditions include `age`, `createdBefore`, `daysSinceNoncurrentTime`, `isLive`, `matchesStorageClass`, `matchesPrefix`/`matchesSuffix`, `numNewerVersions`, `sizeAboveBytes`/`sizeBelowBytes`.
```json
{"lifecycle": {"rule": [
  {"action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
   "condition": {"age": 90, "matchesStorageClass": ["STANDARD", "NEARLINE", "REGIONAL", "DURABLE_REDUCED_AVAILABILITY"]}},
  {"action": {"type": "Delete"}, "condition": {"daysSinceNoncurrentTime": 30}},
  {"action": {"type": "AbortIncompleteMultipartUpload"}, "condition": {"age": 7}}
]}}
```
(The `REGIONAL` entry is for a regional bucket; use `MULTI_REGIONAL` instead in a multi-region or dual-region bucket. Using the wrong one is an error.)
- Valid class transitions only go colder: Standard to Nearline, Coldline or Archive; Nearline to Coldline or Archive; Coldline to Archive. An unlisted transition is accepted but never happens.
- `AbortIncompleteMultipartUpload` can only combine with `age`, `matchesPrefix` and `matchesSuffix`.
- `SetStorageClass` and `matchesStorageClass` cannot be used on a bucket with Autoclass enabled.
- If several rules match one object, Delete wins over SetStorageClass, and the class with the lowest at-rest price wins among SetStorageClass rules.
- Config changes can take up to 24 hours to take effect, and actions are asynchronous. Test on development data or a small prefix first.

## Lifecycle cost behaviour
- `SetStorageClass` is billed as a Class A operation at the destination class rate. For small objects this can outweigh the saving: exclude them with `sizeAboveBytes` (max 5 TiB) or delete them.
- Unlike a manual rewrite, a lifecycle class change has no inter-region replication, retrieval or early-deletion charge for the change itself, and time in the earlier class counts toward the new class's minimum duration. Deleting before the minimum duration still incurs early deletion charges. Page example: Nearline for 20 days, lifecycle to Coldline, deleted 60 days later gives a 10-day early-deletion charge; the same via rewrite gives a retrieval fee and a 30-day charge.
- At-rest storage cost is waived after an object becomes eligible for deletion only when soft delete is disabled, the rule is Delete with only `age` (optionally plus `matchesStorageClass`), and there is no hold.

## Soft delete cost
- Soft delete is on by default with a 7-day retention; you can set 7 to 90 days, and 0 disables it. A tag can change the default for new buckets.
- Soft-deleted objects keep accruing storage charges until retention ends. For buckets of temporary, high-churn data the page recommends storing them in buckets without soft delete, and renaming with `objects.move` rather than copying.
- Lifecycle rules do not act on soft-deleted objects. Lifecycle Delete of a live object makes it soft-deleted (or noncurrent if versioning is on). The Recommender API can suggest enabling or disabling soft delete from billing data.

## Verify
- [ ] Each lifecycle transition is one of the valid colder transitions, and the bucket is not on Autoclass.
- [ ] Temporary-data buckets have soft delete disabled deliberately.

## Checked
Confirmed 2026-11-08 against the storage classes, Object Lifecycle Management and soft delete pages. Removed claims the pages do not state: the billing-export SQL and Storage Insights guidance, Autoclass fee and small-object statements, "no retrieval fees" for Autoclass, regional relocation advice, the `gcloud storage buckets update` command, Pub/Sub polling advice, and the egress comparison.
Method: docs-only read of cited pages, 2026-11-08
