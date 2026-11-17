---
id: computing-software.cloud-infrastructure-engineering.aws.cloudfront-keyvaluestore-with-functions
name: cloudfront-keyvaluestore-with-functions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudfront, keyvaluestore, cloudfront-functions, edge-redirects, feature-flags]
level: advanced
status: docs-checked
description: "Store redirect maps, feature flags and A/B config in CloudFront KeyValueStore and read them from CloudFront Functions without redeploying the function."
sources: ["https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/kvs-with-functions.html", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/functions-custom-methods.html", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cloudfront-limits.html", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/kvs-with-functions-create.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudFront KeyValueStore

## 1. Create and load
```bash
aws cloudfront create-key-value-store --name redirects \
  --import-source SourceType=S3,SourceARN=arn:aws:s3:::cfg-bucket/redirects.json
aws cloudfront describe-key-value-store --name redirects --query 'KeyValueStore.{arn:ARN,status:Status}'
```
The import file comes from S3 (you need `s3:GetObject` and `s3:GetBucketLocation` on the bucket); see the CloudFront guide's page on key-value data for the file format.

## 2. Use from a function (runtime `cloudfront-js-2.0`)
```javascript
import cf from 'cloudfront';
const kvsHandle = cf.kvs();
async function handler(event) {
  const uri = event.request.uri;
  if (await kvsHandle.exists(uri)) {
    const target = await kvsHandle.get(uri);
    return { statusCode: 301, statusDescription: 'Moved Permanently',
             headers: { location: { value: target } } };
  }
  return event.request;
}
```
Associate the KVS when creating/updating the function (`--function-config '{"Comment":"","Runtime":"cloudfront-js-2.0","KeyValueStoreAssociations":{"Quantity":1,"Items":[{"KeyValueStoreARN":"<ARN>"}]}}'`),
then publish.

## 3. Update data live
```bash
ETAG=$(aws cloudfront-keyvaluestore describe-key-value-store --kvs-arn <ARN> --query ETag --output text)
aws cloudfront-keyvaluestore put-key --kvs-arn <ARN> --key /spring --value /sale-spring --if-match $ETAG
```
The data is updated independently of the function code, so no function redeploy is needed.

## Limits
Quotas read on the CloudFront quotas page 2026-10-27: key up to 512 bytes, value up to 1 KB, store up to 5 MB, one KVS per function, up to 100 functions per store, 200 stores per account (adjustable), and up to 50 keys or 3 MB per update request. The KVS requires the CloudFront Functions JavaScript runtime 2.0. Reading is from CloudFront Functions only; key value store helper calls do not create CloudTrail data events.

## Verify
- [ ] `curl -sI https://d123.cloudfront.net/old` returns 301 to `/new`.
- [ ] An updated key value changes the response without publishing a new function version.

## Checked
2026-10-27. Documentation: Amazon CloudFront Developer Guide (KeyValueStore, helper methods, quotas, creating a key value store), read this date. Confirmed: JavaScript runtime 2.0 requirement, cf.kvs() with get() and exists() helpers (the draft passed an ID to cf.kvs and relied on exceptions), quota table values, S3 import permissions. Confirmed from the API models: create-key-value-store import-source SourceType S3, and cloudfront-keyvaluestore put-key parameters (KvsARN, Key, Value, IfMatch). Removed the unconfirmed import file format and propagation-time claim.
Method: documentation only; no commands were run.
