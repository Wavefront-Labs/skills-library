---
id: computing-software.database-administration.supabase.storage-s3-compatibility
name: storage-s3-compatibility
category: computing-software
field: database-administration
product: supabase
tags: [storage, s3, s3-protocol, multipart, sigv4]
level: advanced
status: docs-checked
description: "Supabase Storage S3 protocol support: SigV4 presigned URLs, implemented operations, multipart uploads and unsupported features like versioning."
sources:
  - https://supabase.com/docs/guides/storage/s3/compatibility
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know what S3 clients can and cannot do against Supabase Storage.

Enable the S3 connection via the S3 protocol on the Storage Settings page. Presigned URLs use query parameters and expect AWS Signature Version 4.

Implemented:
- Bucket: ListBuckets, HeadBucket, CreateBucket, DeleteBucket, GetBucketLocation.
- Object: HeadObject, ListObjects, ListObjectsV2, GetObject, PutObject, DeleteObject, DeleteObjects, CopyObject, ListParts.
- Multipart: ListMultipartUploads, CreateMultipartUpload, UploadPart, UploadPartCopy, CompleteMultipartUpload, AbortMultipartUpload.

Partial: CopyObject supports the metadata-directive header with a caveat; several query parameters such as ListObjects `delimiter` and `marker` are supported.

Not implemented:
- Bucket: DeleteBucketCors, GetBucketEncryption, GetBucketLifecycleConfiguration, GetBucketCors, PutBucketCors, PutBucketLifecycleConfiguration.
- Versioning: not supported; deleted objects are permanently removed.
- Request features the page marks unsupported: ACL headers, SSE-C and other server-side encryption headers, Request Payer, expected-owner headers, Object Locking, Tagging, website redirects, Content-MD5, the x-amz-mfa header on deletes, x-amz-storage-class on CreateMultipartUpload and checksum algorithm headers on CopyObject and PutBucketCors.

Plan around the gaps: no versioning means deletes are final, and lifecycle or CORS bucket configuration cannot be driven through the S3 API.

## Checked

Confirmed against the compatibility page: SigV4 query-string presigning, enabling the S3 connection in Storage settings, the lists of implemented and unimplemented bucket and object operations, multipart operations, no versioning. The generic feature line was rewritten to name only the operations where the page marks each feature unsupported (checksums and storage class were over-generalised).

Method: docs-checked 2026-11-09 against the Supabase docs source for guides/storage/s3/compatibility (apps/docs/content on GitHub master), read in full.
