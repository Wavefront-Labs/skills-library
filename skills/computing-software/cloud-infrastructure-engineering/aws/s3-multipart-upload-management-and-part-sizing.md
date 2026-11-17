---
id: computing-software.cloud-infrastructure-engineering.aws.s3-multipart-upload-management-and-part-sizing
name: s3-multipart-upload-management-and-part-sizing
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, list-multipart-uploads, part-size, abort-multipart-upload, multipart-threshold, storage-lens]
level: practitioner
status: docs-checked
description: "Run multipart uploads well: part size limits and tuning, CLI multipart settings, listing and aborting stale uploads, lifecycle cleanup, and finding hidden upload costs."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity.html", "https://docs.aws.amazon.com/cli/latest/topic/s3-config.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-abort-incomplete-mpu-lifecycle-config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multipart upload management and part sizing

## 1. Limits
- Part size 5 MiB to 5 GiB (no minimum for the last part); part numbers 1 to 10,000, so max **10,000 parts**.
  The multipart limits table gives a maximum object size of 48.8 TiB (the upload guide says 50 TB); a single
  `PutObject` is limited to 5 GB. Older SDKs and tools may apply lower caps, so test before relying on it.
- So part size must be at least object size / 10,000: a 1 TiB file needs parts of at
  least ~105 MiB.
- AWS recommends multipart for objects of 100 MB or more; it is required above the 5 GB single-PUT limit.

## 2. CLI tuning (aws s3 cp/sync)
```bash
aws configure set default.s3.multipart_threshold 64MB
aws configure set default.s3.multipart_chunksize 64MB
aws configure set default.s3.max_concurrent_requests 20
aws configure set default.s3.preferred_transfer_client crt   # values: auto (default), classic, crt
```
Defaults are `multipart_threshold` 8MB, `multipart_chunksize` 8MB (minimum 5MB for uploads) and
`max_concurrent_requests` 10. The CLI adjusts a chunk size that does not fit S3 limits. `auto` uses the CRT
client when its criteria are met; `crt` forces it (falling back to `classic` for cases such as S3-to-S3 copies).

## 3. Low-level flow (when you need control)
```bash
UPLOAD_ID=$(aws s3api create-multipart-upload --bucket b --key big.bin --checksum-algorithm CRC32C --query UploadId --output text)
aws s3api upload-part --bucket b --key big.bin --part-number 1 --body part1 --upload-id $UPLOAD_ID --checksum-algorithm CRC32C
# ... collect ETag + ChecksumCRC32C for each part into parts.json
aws s3api complete-multipart-upload --bucket b --key big.bin --upload-id $UPLOAD_ID \
  --multipart-upload file://parts.json
```
Parts can be uploaded in any order, in parallel, and retried individually; S3 assembles them in ascending part-number order. With checksums, part numbers must be consecutive starting at 1. Keep your own list of part numbers and ETags for the complete call rather than using a listing.

## 4. Stale uploads cost money
Uploaded parts of incomplete multipart uploads are billed as storage but invisible to
`aws s3 ls` and most consoles views.
```bash
aws s3api list-multipart-uploads --bucket b \
  --query 'Uploads[].{key:Key,id:UploadId,started:Initiated}' --output table
aws s3api list-parts --bucket b --key big.bin --upload-id <id> --query 'sum(Parts[].Size)'
aws s3api abort-multipart-upload --bucket b --key big.bin --upload-id <id>
```
Prevent with a lifecycle rule on every bucket:
```json
{"Rules": [{"ID": "abort-mpu", "Status": "Enabled", "Filter": {},
  "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7}}]}
```
The Storage Lens free metric `Incomplete multipart upload bytes` (`IncompleteMultipartUploadStorageBytes`)
finds offenders across the organization.

## 5. Integrity
- Use additional checksums per part (CRC64NVME is the default algorithm, plus CRC32, CRC32C, SHA-1, SHA-256 and others);
  S3 validates each part and stores a composite (checksum of checksums) or full-object checksum.
- The ETag of a multipart object is a checksum of checksums and is not necessarily the MD5 of the data; do not compare it
  with `md5sum`.

## Gotchas
- Presigned multipart (browser uploads): presign each `UploadPart`; the client must be able to read each part's `ETag` response header.
- Stop an upload only after all part uploads have finished: part uploads in flight can still succeed after an abort
  and leave stored parts, so list again afterwards.
- Multipart uploads have no expiry; only completing, aborting or a lifecycle rule cleans them. Re-uploading a part number overwrites the earlier part.

## Verify
- [ ] Every bucket has an `AbortIncompleteMultipartUpload` rule (Config rule or script).
- [ ] Storage Lens shows incomplete multipart bytes near zero.
- [ ] A large test upload completes with a stored checksum (`head-object --checksum-mode ENABLED`).

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: multipart limits (qfacts table: 10,000 parts, 5 MiB to 5 GiB parts, 48.8 TiB max object), 5 GB single PUT, 100 MB recommendation, incomplete-upload billing and no expiry, `AbortIncompleteMultipartUpload` lifecycle rule, checksum behaviour and default CRC64NVME, consecutive part numbers with checksums, multipart ETag semantics, AWS CLI S3 settings and defaults, Storage Lens metric name. Removed unconfirmed CORS header detail.

Method: documentation only; no commands were run.
