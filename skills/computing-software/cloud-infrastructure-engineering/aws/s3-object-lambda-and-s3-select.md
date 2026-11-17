---
id: computing-software.cloud-infrastructure-engineering.aws.s3-object-lambda-and-s3-select
name: s3-object-lambda-and-s3-select
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, object-lambda, s3-object-lambda, s3-select, select-object-content, writegetobjectresponse, redaction, on-the-fly-transform, access-points, athena, service-availability]
level: advanced
status: docs-checked
description: "Transform or filter S3 objects at read time: S3 Object Lambda access points with WriteGetObjectResponse, S3 Select queries, their new-customer closures and what replaces them."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/transforming-objects.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/amazons3-ol-change.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/olap-writing-lambda.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/olap-policies.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/selecting-content-from-objects.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 Object Lambda and S3 Select

**Goal:** callers get a transformed or filtered view of an object (PII redacted, image
resized, only matching CSV rows) without storing a second copy. First decide whether you
*can* still use these features: both have been closed to new customers.

## 0. Availability check
- **S3 Select** is no longer available to new customers; existing customers can continue to use it.
  For new work query the data with Athena or filter in the client.
- **S3 Object Lambda**, as of 7 November 2025, is available only to existing customers and select
  AWS Partner Network partners; AWS plans no new capabilities. The documented alternatives are the
  AWS Solution Dynamic Image Transformation for Amazon CloudFront, invoking Lambda through
  CloudFront, API Gateway or a function URL, or processing the data in the client application.
- Test in your account (`aws s3control list-access-points-for-object-lambda`, a
  `select-object-content` call) before designing around either.

## 1. S3 Object Lambda (existing users)
Pieces: a normal **supporting access point** → an **Object Lambda access point** naming a
Lambda per action (GetObject, HeadObject, ListObjects...).
```bash
aws s3control create-access-point --account-id <ACCOUNT_ID> --name raw-ap --bucket customer-data
aws s3control create-access-point-for-object-lambda --account-id <ACCOUNT_ID> --name redacted \
  --configuration '{"SupportingAccessPoint":"arn:aws:s3:<REGION>:<ACCOUNT_ID>:accesspoint/raw-ap",
    "TransformationConfigurations":[{"Actions":["GetObject"],
      "ContentTransformation":{"AwsLambda":{"FunctionArn":"arn:aws:lambda:<REGION>:<ACCOUNT_ID>:function:redact"}}}]}'
```
Function (Python):
```python
import boto3, urllib3
s3 = boto3.client("s3"); http = urllib3.PoolManager()
def handler(event, _):
    ctx = event["getObjectContext"]
    original = http.request("GET", ctx["inputS3Url"]).data        # presigned URL to the original
    body = redact(original)
    s3.write_get_object_response(RequestRoute=ctx["outputRoute"],
                                 RequestToken=ctx["outputToken"], Body=body)
    return {"status_code": 200}
```
- The function role needs `s3-object-lambda:WriteGetObjectResponse`; callers need
  `s3-object-lambda:GetObject` on the Object Lambda AP, and the supporting access point and bucket
  must also allow the underlying read.
- Callers use the Object Lambda AP ARN or alias as the bucket name in SDK calls.
- S3 Object Lambda allows up to 60 seconds to send a complete response (a shorter Lambda timeout
  or caller timeout shortens it); large objects need streaming and
  range handling (`event["userRequest"]["headers"]["Range"]`).

## 2. S3 Select (existing users)
```bash
aws s3api select-object-content --bucket logs --key 2026/10/16/app.csv.gz \
  --expression "SELECT s.user_id, s.status FROM S3Object s WHERE s.status = '500'" \
  --expression-type SQL \
  --input-serialization '{"CSV":{"FileHeaderInfo":"USE"},"CompressionType":"GZIP"}' \
  --output-serialization '{"JSON":{}}' out.json
```
Works on one object at a time (CSV, JSON, Parquet); no joins, no multi-object scan. For
anything across many objects, Athena is the tool anyway.

## Gotchas
- Each read runs your function; for repetitive access, CloudFront with the Object Lambda access
  point as origin is a documented pattern.
- Error handling: on failure call `write_get_object_response` with `StatusCode`/`ErrorCode`,
  otherwise the caller waits for the 60-second response limit.

## Verify
- [ ] `aws s3api get-object --bucket <OLAP_ARN> --key sample.json out.json` returns the redacted content; the raw AP returns the original.
- [ ] A caller without Object Lambda permission gets `AccessDenied`.
- [ ] Lambda errors surface as an S3 error to the caller within seconds.
- [ ] For new projects: design review records which replacement (Dynamic Image Transformation, Lambda behind CloudFront or API Gateway, client-side processing, Athena) was chosen and why.

## Checked

Checked 2026-10-27 against the S3 User Guide pages Transforming objects with S3 Object Lambda, Object Lambda availability change, Writing Lambda functions for Object Lambda, Object Lambda policies, Querying data in place with S3 Select, and the botocore s3 and s3control models.
Confirmed: Object Lambda available only to existing customers and select APN partners from 7 November 2025; documented alternatives; s3-object-lambda:WriteGetObjectResponse for the function and s3-object-lambda:GetObject on the access point; inputS3Url, outputRoute, outputToken, userRequest.headers in the event; StatusCode and ErrorCode on WriteGetObjectResponse; 60-second response window; S3 Select no longer available to new customers, one object at a time, CSV, JSON or Parquet, GZIP or BZIP2 for CSV and JSON, SelectObjectContent parameter shapes. The S3 Select closure date could not be read on a current page and was removed.

Method: documentation only; no commands were run.
