---
id: computing-software.cryptography-implementation.key-management.data-key-caching-and-kms-quotas
name: data-key-caching-and-kms-quotas
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, kms, cloud-kms, data-key-caching, kms-quotas, throttling, aws-encryption-sdk, envelope-encryption, s3-bucket-keys]
level: advanced
status: verified
description: "Stay within KMS request quotas: data key caching with max age/messages/bytes limits, S3 Bucket Keys, hierarchical keyrings, backoff on ThrottlingException, and quota monitoring."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/requests-per-second.html", "https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/data-key-caching.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-key.html", "https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/use-hierarchical-keyring.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data key caching and KMS quotas

Calling KMS for every record works in development and fails in production:
AWS KMS cryptographic operations share a per-account, per-region request
quota that varies by Region and KMS key type: for symmetric encryption keys and HMAC keys (one shared
quota) the default is 10,000 requests per second, more in some Regions (20,000 or 100,000); RSA, ECC and ML-DSA
keys each have a much lower shared quota (1,000 per second in the quota table). Throttling counts requests from
all principals in the Region, including AWS services acting for you. All quotas except the CloudHSM key store
quota are adjustable. Exceeding it returns
`ThrottlingException`, and every service sharing the account suffers.

## Reduce calls

1. **Envelope encryption done right**: one `GenerateDataKey` per object/batch,
   not per field. Encrypt many fields of a record with one DEK.
2. **Data key caching** (AWS Encryption SDK caching CMM, or your own):
   reuse a plaintext DEK for a bounded number of encryptions.

```python
import aws_encryption_sdk
from aws_encryption_sdk.caches.local import LocalCryptoMaterialsCache
cache = LocalCryptoMaterialsCache(capacity=100)
cmm = aws_encryption_sdk.CachingCryptoMaterialsManager(
    master_key_provider=kms_provider, cache=cache,
    max_age=300.0,                      # seconds
    max_messages_encrypted=10_000,
    max_bytes_encrypted=100 * 1024**2)
```
   `max_age` is required; `max_messages_encrypted` defaults to 2^32 and `max_bytes_encrypted` to 2^63-1, so set
   all three explicitly (signature checked against aws-encryption-sdk 4.0.7). Caching widens the blast radius of one DEK and keeps
   plaintext keys in memory longer - a deliberate trade.
3. **Hierarchical keyring** (AWS ESDK / DB Encryption SDK): branch keys stored
   in DynamoDB, unwrapped by KMS occasionally, then used locally to derive
   per-item keys - very low KMS call rates for high-volume workloads.
4. **S3 Bucket Keys**: SSE-KMS with `BucketKeyEnabled=true` makes S3 use a
   bucket-level data key, cutting KMS request costs by up to 99 percent (AWS's figure). Note
   S3 Bucket Keys use the bucket ARN, not the object ARN, as the encryption context, so key or IAM policies that
   match the object ARN stop working; update them first.
5. **Decrypt caching**: cache unwrapped DEKs by wrapped-key bytes (LRU, TTL)
   on the read path.

## Handle throttling

- AWS SDKs retry with exponential backoff by default; tune max attempts and
  add jitter for bursty batch jobs.
- Spread batch re-encryption jobs over time; request a quota increase
  (Service Quotas console) ahead of migrations.

## Monitor

CloudWatch `AWS/Usage` metrics for KMS (`CallCount` by operation) against
quota, alarms at 70-80%; GCP `cloudkms.googleapis.com` quota metrics
(`crypto requests per minute`).

## Verify

- [ ] Load test at peak volume shows KMS calls well under quota.
- [ ] Cache limits (age, messages, bytes) set and documented.
- [ ] Alarm on KMS usage vs quota and on ThrottlingException counts.
