---
id: computing-software.cloud-infrastructure-engineering.aws.s3-performance-multipart-and-presigned-urls
name: s3-performance-multipart-and-presigned-urls
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, s3-performance, multipart-upload, presigned-url, presigned-urls, presigned-post, transfer-acceleration, byte-range-fetch, prefix-parallelism, request-rate, 503-slowdown, s3-express-one-zone, crt, s3-transfer-manager, cloudfront-signed-url, checksum, sha256, etag, upload-part]
level: practitioner
status: docs-checked
description: "Make S3 fast and safely shareable: multipart upload sizing and cleanup, prefix-parallel request scaling, byte-range GETs, Transfer Acceleration, and presigned URL/POST with correct expiry."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-guidelines.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/transfer-acceleration.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity.html", "https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-HTTPPOSTConstructPolicy.html", "https://docs.aws.amazon.com/cli/latest/topic/s3-config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 performance, multipart upload and presigned URLs

**Goal:** uploads and downloads that saturate the network instead of a single TCP
stream, request patterns that do not trip `503 SlowDown`, and time-limited URLs that
let a browser or partner move an object without any AWS credentials.

## 1. Request-rate scaling
S3 gives **≥ 3,500 PUT/COPY/POST/DELETE and 5,500 GET/HEAD per second per prefix**, and
partitions prefixes automatically as load grows. Rules that follow:
- There is no limit on prefixes per bucket: spread hot traffic across prefixes (10 prefixes can scale reads to
  55,000 requests per second). Scaling is gradual, not instantaneous; while S3 scales you may see
  `503 Slow Down` — retry with backoff (the SDKs retry 503s automatically).
- Parallelism is the whole game: issue many concurrent requests over separate connections; S3 has no limit on the
  number of connections to a bucket. Large objects need multipart upload or byte-range GETs.
- Put compute in the same Region; the S3 docs say this reduces latency and data transfer costs.
- Latency-critical small objects: the S3 documentation points to **S3 Express One Zone** directory buckets
  (single-digit millisecond access, data stored in one AZ) and to CloudFront or ElastiCache caching.

## 2. Multipart upload
Required for > 5 GB (single PUT limit), recommended from 100 MB. Limits: 10,000 parts,
5 MiB-5 GiB per part (no minimum for the last part), maximum object size 48.8 TiB (the upload guide says 50 TB).
```bash
# CLI does it automatically above multipart_threshold
aws configure set default.s3.multipart_threshold 64MB
aws configure set default.s3.multipart_chunksize 64MB
aws configure set default.s3.max_concurrent_requests 32
aws configure set default.s3.preferred_transfer_client crt   # AWS CRT client (values: auto, classic, crt)
aws s3 cp big.bin s3://bucket/key
```
Manual API sequence (what SDK transfer managers do): `CreateMultipartUpload` →
N × `UploadPart` (parallel, each returns an ETag) → `CompleteMultipartUpload` with the
ordered `{PartNumber, ETag}` list. An unfinished upload **bills for stored parts
until it is completed or stopped** (multipart uploads do not expire) — every bucket needs a lifecycle `AbortIncompleteMultipartUpload`
(`DaysAfterInitiation: 7`), and `aws s3api list-multipart-uploads --bucket b` shows debris.

Part size: the object size divided by 10,000 is the floor (5 MiB parts on a 50 GB file would need
about 10,000 parts); smaller parts recover from failures faster, larger parts mean fewer requests, so size parts
to your network and retry needs. Python: `boto3.s3.transfer.TransferConfig(multipart_chunksize=64*2**20, max_concurrency=16)`
passed to `upload_file`.

Integrity: send `--checksum-algorithm SHA256` (or another supported algorithm; CRC64NVME is the default) so S3 verifies
each part and stores a checksum; multipart ETags are a checksum of checksums and **not necessarily** the MD5 of the
object, so do not compare them to local hashes.

## 3. Downloads
- **Byte-range GET** (`Range: bytes=0-104857599`) in parallel for large objects: higher aggregate throughput and
  cheaper retries. Objects uploaded with multipart upload are best fetched in the same part sizes or aligned to part boundaries
  (`GET ?partNumber=N` addresses a part). The SDK Transfer Manager uses byte-range requests where appropriate.
- `GetObject` from Glacier Flexible Retrieval and Deep Archive fails with `InvalidObjectState` until restored.
- For higher transfer rates over a single connection or lower latency, AWS suggests CloudFront or ElastiCache in front of S3.

## 4. Transfer Acceleration
`aws s3api put-bucket-accelerate-configuration --bucket b --accelerate-configuration Status=Enabled`
then endpoint `bucket.s3-accelerate.amazonaws.com` (dual-stack: `bucket.s3-accelerate.dualstack.amazonaws.com`; CLI: `--endpoint-url` or
`configure set default.s3.use_accelerate_endpoint true`). Data enters at CloudFront edge locations and is routed to S3 over an
optimized network path; it suits regular transfers of gigabytes to terabytes over long distances. Additional data transfer
charges might apply, and it can take up to 20 minutes after enabling before speeds improve. The S3 Transfer Acceleration Speed Comparison tool shows
whether it helps for your location. Requirements: virtual-hosted-style requests and a DNS-compliant bucket name with no periods;
supported only in certain Regions (see the Transfer Acceleration page).

## 5. Presigned URLs
A presigned URL embeds a SigV4 signature made with **your** credentials; whoever holds
it can perform that one operation on that one key until expiry, with your permissions.
```bash
aws s3 presign s3://bucket/report.pdf --expires-in 900      # GET, 15 min
```
```python
s3 = boto3.client("s3", region_name="eu-west-1", config=Config(signature_version="s3v4"))
url = s3.generate_presigned_url("put_object",
        Params={"Bucket": "b", "Key": "uploads/u1/photo.jpg", "ContentType": "image/jpeg"},
        ExpiresIn=600)
# client: PUT url with the same Content-Type header, body = file bytes
```
Rules that matter:
- Expiry caps: 7 days with IAM user keys (SigV4); with **temporary credentials (roles, STS) the URL
  dies when the credentials expire**, even if you asked for longer. Lambda-generated URLs therefore live at most as long as the function role's credentials.
- Every request parameter signed must be sent identically (HTTP method, headers such as `Content-Type`, query string); a mismatch is
  `SignatureDoesNotMatch`. For browser uploads configure CORS on the bucket.
- Use **presigned POST** when you need POST policy conditions such as `content-length-range`, a key prefix (`starts-with $key uploads/u1/`), or fixed
  metadata: `s3.generate_presigned_post(Bucket, Key, Conditions=[["content-length-range", 0, 10_000_000], {"Content-Type": "image/jpeg"}], ExpiresIn=600)` returns `url` + form `fields` for a multipart/form-data POST.
- The URL is limited by the permissions of the principal that created it; if that principal lacks the permission (or a bucket policy denies it), the request returns `403`.
- Large browser uploads: presign each `UploadPart` (`generate_presigned_url("upload_part", Params={..., "UploadId", "PartNumber"})`)
  and complete server-side.
- Use Signature Version 4 (`signature_version='s3v4'` in boto3, which the botocore documentation recommends) and the bucket's Region.
- For links that must outlive the signing credentials, use IAM user credentials (up to 7 days) or CloudFront signed URLs or cookies rather than role-signed S3 URLs.

## Gotchas
- For SSE-KMS objects the signing principal needs the relevant KMS permissions (`kms:Decrypt` to read, `kms:GenerateDataKey` to write).
- Keep clocks NTP-synchronised; even small drifts can invalidate signatures.
- Bucket policies with `aws:SecureTransport` deny `http://` presigned URLs; always generate `https`.
- A presigned URL leaks in logs and referrers; keep expiry short and never embed in
  cacheable HTML without the expiry matching the cache TTL.

## Verify
- [ ] A multi-GB `aws s3 cp` with the CRT client shows higher throughput than the classic client on your instance type.
- [ ] `list-multipart-uploads` empty and lifecycle abort rule present on every bucket.
- [ ] Presigned PUT works from a browser (CORS) and returns `403` after expiry; a POST with `content-length-range` rejects an oversized file.
- [ ] A sustained high-rate load test shows `503 Slow Down` only while S3 scales, then clean.
- [ ] Objects uploaded with `--checksum-algorithm SHA256` show `ChecksumSHA256` in `head-object --checksum-mode ENABLED`.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: request rates (3,500 / 5,500 per prefix, 10 prefixes = 55,000 reads/s), gradual scaling and 503 Slow Down, parallel connections, byte-range and part-aligned GETs, same-Region guidance, multipart limits (48.8 TiB table value, 5 GB single PUT), checksum defaults, AWS CLI settings, Transfer Acceleration requirements and endpoints, presigned URL credential rules and FAQ causes, boto3 SigV4 recommendation, POST policy condition format (botocore `generate_presigned_post`). Removed unconfirmed throughput-per-connection figures, Express One Zone naming, CORS header lists, redirect behaviour and acceleration-gain claims.

Method: documentation only; no commands were run.
