---
id: computing-software.cloud-infrastructure-engineering.aws.s3-presigned-url-expiry-and-signature-errors
name: s3-presigned-url-expiry-and-signature-errors
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, presigned-url-expiry, presigned-urls, sigv4, signaturedoesnotmatch]
level: practitioner
status: docs-checked
description: "Set realistic S3 presigned URL lifetimes (7-day SigV4 cap, temporary credential expiry) and fix Request has expired and SignatureDoesNotMatch errors."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html", "https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-query-string-auth.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Presigned URL expiry and SigV4 errors

## 1. How long a URL really lives
The URL is valid until the **earlier** of:
- `X-Amz-Expires` (max 604,800 s = 7 days for SigV4, with the AWS CLI or SDKs), and
- expiry of the credentials that signed it.
| Signed with | Practical max |
|---|---|
| IAM user access keys (SigV4) | 7 days |
| IAM role or STS credentials | until the credentials expire (AssumeRole defaults to 1 hour; EC2 instance profile credentials last typically about 6 hours) |
| S3 console | 1 minute to 12 hours |
A URL made by Lambda for 7 days dies when Lambda's role credentials expire. For long-lived links use IAM user
credentials (tightly scoped) or CloudFront signed URLs.

## 2. Generate
```bash
aws s3 presign s3://reports/2026/q3.pdf --expires-in 3600 --region eu-west-1
```
SDK: generate with Signature Version 4 for the bucket's Region.

## 3. Errors
| Error | Cause |
|---|---|
| `SignatureDoesNotMatch` | request parameters differ between signing and use (HTTP method, headers, query string), clock not NTP-synchronised, a proxy that rewrites headers or the query string |
| `AccessDenied` / 403 | the creating principal lacks permission for the operation, or the bucket policy explicitly denies it |
| `AccessDenied` with `HeadersNotSigned: if-range` | `Range` is signed but `If-Range` is not; add `If-Range` to `X-Amz-SignedHeaders` |
| `ExpiredToken` | the credentials used to generate the URL are no longer valid; refresh them and regenerate |
A presigned URL stops working at the earlier of its expiry and the signing credentials' expiry; S3 checks expiry when the HTTP request arrives (a download already in progress continues).

## 4. Restrict
A bucket policy Deny with `"NumericGreaterThan": {"s3:signatureAge": "600000"}` rejects presigned requests whose signature is older than 10 minutes (the value is in milliseconds).
Network-path restrictions (`aws:SourceIp`, `aws:SourceVpc`, `aws:SourceVpce`) also apply to presigned requests.

## Verify
- [ ] A GET request to a presigned GET URL succeeds now and returns 403 after expiry (a `HEAD` request needs a URL signed for `HEAD`).

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: credential-type expiry rules and the 7-day / 12-hour (console) limits, `ExpiredToken` and `SignatureDoesNotMatch` guidance, `HeadersNotSigned: if-range`, `s3:signatureAge` example (milliseconds), network-path conditions. Removed unconfirmed exact error strings, the `s3:authType` claim and a verification step that used a HEAD request against a GET-signed URL.

Method: documentation only; no commands were run.
