---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.object-key-design
name: object-key-design
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, storage-selection, object-key-design, s3-prefixes, request-rate, partitioned-prefixes, hive-partitioning, object-naming]
level: practitioner
status: docs-checked
description: "Design object storage keys for scale: S3 per-prefix request rates, Cloud Storage key-range hotspotting and ramp-up, Azure hash prefixes and block sizes."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html", "https://cloud.google.com/storage/docs/request-rate", "https://learn.microsoft.com/azure/storage/blobs/storage-performance-checklist"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object storage key design and request rates

## Request-rate facts
- **S3**: at least 3,500 PUT/COPY/POST/DELETE and 5,500 GET/HEAD requests per second **per partitioned prefix**.
  There is no limit on the number of prefixes in a bucket, so parallelising across 10 prefixes can reach about 55,000
  reads per second. Scaling is gradual, not instant; while it happens you may see 503 (Slow Down) errors that fade
  when scaling completes. SSE-KMS workloads are also bound by AWS KMS request rates.
- **Cloud Storage**: a bucket starts with roughly 1,000 object writes (upload, update, delete) and 5,000 object reads
  (including listing and metadata reads) per second, and autoscales by spreading load across servers. Detecting and
  redistributing load takes on the order of minutes. There is also a smaller limit for repeated writes to the same
  object name. Buckets with hierarchical namespace start with up to 8 times the QPS.
- **Azure Blob**: the targets are targets, not hard limits, and some can be raised; clients near them may be
  throttled. Upload blob or block sizes above 256 KiB to activate high-throughput block blobs, whose ingest is not
  affected by partition naming. With small block sizes, put a hash (three digits) or a seconds value as early as
  possible in the partition key.

## Design rules
1. **Cloud Storage keeps a lexicographic index of keys**, so sequential names (numbers, timestamps) keep shifting load to
   a new index range and slow autoscaling. Add a hash before the sequence or timestamp. The page's example prefixes the
   first 6 hex characters of the MD5 of the name; a 1-character random hex prefix (16 values) is enough to scale from
   5,000/1,000 up to roughly 80,000/16,000 reads/writes per second.
2. Randomness after a common prefix only helps under that prefix. If you write under a new timestamp prefix each hour,
   the write rate resets every hour; make new prefixes evenly distributed across the key range instead.
3. For bulk uploads or deletes where you cannot rename, reorder the work: spread it across many prefixes and pick
   folders and files in random order.
4. Ramp up gradually: if you expect to exceed 1,000 writes or 5,000 reads per second on a bucket (or a new key range)
   that has been quiet for days, start near the threshold and increase no faster than doubling every 20 minutes. Retry
   408, 429 and 5xx with exponential backoff.

## Gotchas
- Listing counts as a read request on Cloud Storage, so heavy listing uses the same request budget as reads.
- A bucket's 503/429 errors during a sudden burst are the scaling signal, not an outage: ramp, back off, retry.

## Verify
- [ ] Load test at the target rate without sustained 503/429 errors, starting from a cold bucket and a new key range.

## Checked
2026-11-08. Confirmed against the S3 "optimizing performance" page, the Cloud Storage request rate and access
distribution page and the Azure Blob performance checklist (all read in full): S3 3,500/5,500 per prefix and 503 Slow
Down, Cloud Storage 1,000/5,000 initial rates, 20-minute doubling, key index hotspotting, hash prefix example,
16-value prefix scaling, hourly-prefix reset, bulk reordering, 8x hierarchical namespace, Azure 256 KiB and hash prefix
advice. Removed as not on these pages: Azure partitioning by account+container+blob name and timestamp hot partitions,
Hive-style partition layout, 128 MB-1 GB file sizes, content-hash asset names, LIST billing, rename = copy+delete and
pre-warming through support.
Method: documentation only; no commands were run.
