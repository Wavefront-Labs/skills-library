---
id: computing-software.cloud-infrastructure-engineering.aws.s3-static-website-hosting-and-cors
name: s3-static-website-hosting-and-cors
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, static-website, website-hosting, cors, cloudfront, origin-access-control, spa]
level: practitioner
status: docs-checked
description: "Host static sites from S3 the right way (private bucket + CloudFront OAC vs website endpoint), SPA routing, redirects, and S3 CORS rules for browser uploads and fetches."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteEndpoints.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/how-to-page-redirect.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/cors.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/ManageCorsUsing.html", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 static website hosting and CORS

## 1. Two hosting models
| | S3 website endpoint | Private bucket + CloudFront (OAC) |
|---|---|---|
| Bucket | **public** read required | private, Block Public Access on |
| HTTPS | no (HTTP only) | yes, ACM cert, custom domain |
| Index/error docs, redirects | built-in | CloudFront default root object + functions/custom errors |
| Recommended | legacy / redirect-only buckets | **yes** |

The S3 website hosting page itself recommends AWS Amplify Hosting (CloudFront-backed) for hosting static content stored in S3. If the bucket uses SSE-KMS, anonymous website access does not work: serve it through CloudFront with OAC (OAI does not support SSE-KMS).

## 2. CloudFront + OAC
Bucket policy allowing only the distribution:
```json
{"Effect": "Allow", "Principal": {"Service": "cloudfront.amazonaws.com"},
 "Action": "s3:GetObject", "Resource": "arn:aws:s3:::site-bucket/*",
 "Condition": {"StringEquals": {"AWS:SourceArn": "arn:aws:cloudfront::<ACCOUNT_ID>:distribution/E123"}}}
```
- Origin = bucket REST endpoint (`site-bucket.s3.<REGION>.amazonaws.com`), not the website endpoint.
- Default root object `index.html`. **SPA routing**: custom error responses 403/404 →
  `/index.html` with 200 (OAC returns 403 for missing keys because `ListBucket` isn't granted).
  Subdirectory index files (`/docs/` → `/docs/index.html`) need a CloudFront Function URL rewrite.
- Deploy: `aws s3 sync dist/ s3://site-bucket --delete` then invalidate `/index.html` (hashed assets need no invalidation).

## 3. Website endpoint (when you need it)
```bash
aws s3 website s3://www-redirect --index-document index.html --error-document 404.html
aws s3api put-bucket-website --bucket example.com --website-configuration \
  '{"RedirectAllRequestsTo":{"HostName":"www.example.com","Protocol":"https"}}'
```
Good for apex → www redirects. Routing rules support prefix-based redirects (limit of 50 routing rules per website configuration).

## 4. CORS on the bucket
Needed when a browser on another origin calls S3 directly (presigned uploads, fetching JSON):
```bash
aws s3api put-bucket-cors --bucket uploads --cors-configuration '{"CORSRules":[{
  "AllowedOrigins":["https://app.example.com"],
  "AllowedMethods":["GET","PUT","POST"],
  "AllowedHeaders":["*"],
  "ExposeHeaders":["ETag"],
  "MaxAgeSeconds":3000}]}'
```
- `ExposeHeaders` lists the response headers browser scripts may read; include `ETag` if your upload code reads part ETags (for example browser multipart uploads).
- Behind CloudFront, also check how the distribution handles CORS headers (see the CloudFront documentation).

## Gotchas
- A failing preflight usually means no CORS rule matches the request's origin, method and headers (AllowedOrigins, AllowedMethods, AllowedHeaders).
- Website endpoints do not support HTTPS or access points (S3 documentation); use the bucket REST endpoint as the CloudFront origin when you use OAC.

## Verify
- [ ] `curl -I https://www.example.com/` 200 via CloudFront; direct S3 object URL returns 403.
- [ ] Deep link `/settings/profile` returns the SPA (200).
- [ ] Browser presigned PUT from app origin succeeds; from another origin fails preflight.

## Checked

Checked 2026-10-27 against the S3 User Guide pages Hosting a static website, Website endpoints, Configuring a redirect, CORS, and the CloudFront Developer Guide pages on restricting access to an S3 origin (OAC) and custom error responses.
Confirmed: website endpoints do not support HTTPS; AWS recommends Amplify Hosting for static content in S3; SSE-KMS buckets cannot serve anonymous website users, so CloudFront with OAC (not OAI) is required; CloudFront OAC bucket policy shape (service principal cloudfront.amazonaws.com, s3:GetObject, AWS:SourceArn condition); 50 routing rules per website configuration; CORS rule elements AllowedOrigins, AllowedMethods, AllowedHeaders, ExposeHeaders, MaxAgeSeconds; a missing key without s3:ListBucket returns 403 (GetObject API reference); put-bucket-website accepts RedirectAllRequestsTo. Removed the unconfirmed claims about exact origin scheme and port matching and ETag being mandatory.

Method: documentation only; no commands were run.
