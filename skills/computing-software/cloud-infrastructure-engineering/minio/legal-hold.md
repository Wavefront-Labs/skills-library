---
id: computing-software.cloud-infrastructure-engineering.minio.legal-hold
name: legal-hold
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, legal-hold, mc-legalhold-set, put-object-legal-hold, indefinite-retention, worm, object-level-hold]
level: advanced
status: docs-checked
description: "Apply an indefinite legal hold to MinIO objects with mc legalhold set, who may lift it, and how it combines with GOVERNANCE and COMPLIANCE retention."
sources: ["https://github.com/minio/docs/blob/main/source/administration/object-management/object-retention.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO legal hold

Legal hold is indefinite WORM protection that complements retention modes.

```
mc legalhold set ALIAS/PATH
```
(The docs describe this command as toggling legal hold status on an object.)

## Rules
- Protects the object from writes by **all** users, including root.
- Only users with the `s3:PutObjectLegalHold` permission can set or lift it.
- Applies per object: placing a hold on a group of objects (such as a bucket's current contents) does not cover objects created afterwards.
- The object stays locked under a hold even after its GOVERNANCE or COMPLIANCE retention expires; it remains WORM until the hold is lifted *and* the rule expires.
- For GOVERNANCE-locked objects the hold blocks mutation even for users who could bypass governance retention.
- A hold can be placed on an object already under a retention lock. Someone with permission must explicitly lift it.

Also relevant: lifecycle expiry of non-current versions waits until legal holds are lifted. See `computing-software.cloud-infrastructure-engineering.minio.object-locking`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Object Retention page, Legal Hold and Enable Legal Hold Retention sections (object-retention.rst). Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
