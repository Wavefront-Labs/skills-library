---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.s3-cors-configuration
name: s3-cors-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [allowedorigins, preflight, put-bucket-cors, cors]
level: practitioner
status: docs-checked
description: "Enable CORS for SeaweedFS S3: global -s3.allowedOrigins default and per-bucket put-bucket-cors rules, with priority, preflight and storage details."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/S3-CORS
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# s3 cors configuration

Quick global default:
```bash
weed server -s3 -s3.allowedOrigins=*
weed server -s3 -s3.allowedOrigins=https://app.example.com,https://admin.example.com
```
It applies to all buckets, allows GET, PUT, POST, DELETE and HEAD, and all headers.

Per bucket (highest priority):
```bash
aws --endpoint-url $S3_ENDPOINT s3api put-bucket-cors --bucket my-bucket --cors-configuration file://cors-config.json
aws --endpoint-url $S3_ENDPOINT s3api get-bucket-cors --bucket my-bucket
```
Priority: bucket-level CORS, then the global `-s3.allowedOrigins`, then no CORS headers. So set a permissive global default and tighten specific buckets.

Configurations persist in bucket metadata. CORS middleware adds the headers and answers `OPTIONS` preflight requests.

Do not list OPTIONS in AllowedMethods; it is handled automatically for preflight. A preflight that fails origin, method or header validation returns 403 Forbidden. Maximum 100 rules per bucket.

Test a preflight:
```bash
curl -i -X OPTIONS http://localhost:8333/my-bucket/file -H 'Origin: https://app.example.com' -H 'Access-Control-Request-Method: GET'
```

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki page S3 CORS: `-s3.allowedOrigins`, default methods and headers, priority order, persistence, preflight handling, 100-rule limit, example file name `cors-config.json`. Removed the `[cors.allowed_origins]` security.toml note and the `Access-Control-Allow-Origin` verify claim (neither is on the page).
Method: documentation only; no commands were run.
