---
id: computing-software.cloud-infrastructure-engineering.garage.s3-compatibility-high-level
name: s3-compatibility-high-level
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [s3-compatibility, signature-v4, presigned-urls, bucket-versioning]
level: practitioner
status: docs-checked
description: "Know which S3 features Garage supports: SigV4, path and vhost styles, presigned URLs and SSE-C, but not SigV2 or versioning."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/s3-compatibility/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The compatibility page's high-level table for Garage:

- Signature v4: implemented. Signature v2 (deprecated): missing.
- Path-style URLs (`host.tld/bucket/key`) and vhost-style URLs (`bucket.host.tld/key`): both implemented.
- Presigned URLs: implemented.
- SSE-C encryption: implemented.
- Bucket versioning: missing.

Any endpoint Garage does not implement returns `501 Not Implemented`, and some `x-amz-` headers are unsupported.

Core endpoints implemented include CreateBucket, DeleteBucket, GetBucketLocation, HeadBucket, ListBuckets, HeadObject, CopyObject, DeleteObject, DeleteObjects, GetObject, ListObjects, ListObjectsV2, PostObject and PutObject. The page notes ListObjects is implemented, though exactly what `encoding-type=url` covers is under-specified so encoding bugs are possible; URL-encoded fields match those in ListObjectsV2.

All multipart endpoints are implemented: CreateMultipartUpload, UploadPart, UploadPartCopy, ListParts, ListMultipartUpload, CompleteMultipartUpload, AbortMultipartUpload.

The comparison with other platforms is informational and may be outdated; the page's disclaimer says to run your own tests before any serious decision. Minio is absent because it publishes no public S3 compatibility list.

Per this table, tools that need signature v2 or bucket versioning are not served by Garage; `GetBucketVersioning` is a stub that always reports versioning not enabled.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): S3 Compatibility status. Confirmed on the S3 compatibility page: the high-level table rows for Garage, 501 for missing endpoints, the core and multipart endpoint lists, the ListObjects encoding note, and the disclaimer. Removed: the unsupported 'practical takeaway' inference and a duplicated disclaimer line.

Method: documentation only; no commands were run.
