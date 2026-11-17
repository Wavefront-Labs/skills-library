---
id: computing-software.cloud-infrastructure-engineering.garage.s3-unimplemented-endpoints
name: s3-unimplemented-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [s3-not-implemented, bucket-policy, object-lock, bucket-acl]
level: advanced
status: docs-checked
description: "List the S3 endpoint groups Garage marks missing so you can screen applications before migrating."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/s3-compatibility/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/known-issues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Per the compatibility table, Garage marks these S3 areas as Missing, returning 501:

- Bucket policy: DeleteBucketPolicy, GetBucketPolicy, GetBucketPolicyStatus, PutBucketPolicy.
- ACLs: PutBucketAcl, GetObjectAcl, PutObjectAcl (GetBucketAcl is only partial: it reports the read/write/owner permissions of the current key).
- Versioning: ListObjectVersions, PutBucketVersioning (GetBucketVersioning is a stub that always reports versioning not enabled).
- Replication: Delete, Get and PutBucketReplication.
- Object lock: GetObjectLegalHold, PutObjectLegalHold, GetObjectRetention, PutObjectRetention, GetObjectLockConfiguration, PutObjectLockConfiguration.
- Bucket encryption: Delete, Get and PutBucketEncryption.
- Notifications: Get and PutBucketNotificationConfiguration.
- Tagging: bucket and object tagging endpoints such as GetBucketTagging and GetObjectTagging.

Implemented website and CORS endpoints: DeleteBucketWebsite, GetBucketWebsite, PutBucketWebsite, and Delete, Get and PutBucketCors. `PutBucketWebsite` lacks `RedirectAllRequestsTo`. Lifecycle endpoints such as DeleteBucketLifecycle are implemented.

The known-issues page says conditional writes, WORM and object locking are structurally impossible to implement in Garage because it has no consensus algorithm, which is a core design choice; it describes only a semi-working, unsafe implementation as possible.

The table was first published on 2022-02-07 and updated on 2022-05-25 to add undocumented Ceph endpoints.

Practical takeaway: before moving an application onto Garage, compare the S3 calls it issues with this list, because every unimplemented call fails with 501 rather than being ignored.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): S3 Compatibility status, Known issues. Confirmed on the S3 compatibility page: all endpoint groups listed, the website and CORS and lifecycle endpoints, the `RedirectAllRequestsTo` note, the two history dates, and 501 for missing endpoints. Confirmed on the known-issues page: the no-consensus explanation. Removed: the Quick Start sentence (not cited). Added: the GetBucketAcl partial and GetBucketVersioning stub notes.

Method: documentation only; no commands were run.
