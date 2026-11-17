---
id: computing-software.digital-forensics-incident-response.log-analysis.s3-data-events-and-server-access-logs
name: s3-data-events-and-server-access-logs
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [s3-data-events, aws, cloudtrail, s3-server-access-logs, dfir]
level: practitioner
status: docs-checked
description: "Prove S3 object access with CloudTrail data events and S3 server access logs: what each records, what is off by default, and requester attribution."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/cloudtrail-logging-s3-info.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/LogFormat.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 data events and server access logs

By default CloudTrail logs S3 bucket-level calls from the last 90 days (for example `CreateBucket`, `DeleteBucket`, `PutBucketPolicy`, `PutBucketAcl`) but not requests made to objects. To show what was read or downloaded you need one of the sources below.

| Source | Records | Notes |
|---|---|---|
| CloudTrail data events | Object-level API calls such as `GetObject`, `PutObject`, `CopyObject`, `DeleteObject`, `DeleteObjects`, `HeadObject`, `ListObjects` | Not logged by default; additional charges apply; not shown in CloudTrail Event history, so query the logs |
| S3 server access logs | Per request: requester, remote IP, operation, key, bytes sent, HTTP status | Must be enabled on the bucket before the incident |

If neither was enabled before the incident, object reads cannot be shown from these sources: say so and look for indirect signals in other sources.

## CloudTrail data events
- Choose the resource type (`resources.type` `AWS::S3::Object` for S3 objects) in a trail or event data store, via console, CLI or API. Advanced event selectors can filter on `eventName`, `readOnly` and `resources.ARN` to cut volume.
- A `DeleteObjects` event record includes both the `DeleteObjects` event and a `DeleteObject` event for each object deleted; this extra visibility can be excluded in selectors, so check your configuration.
- `PutObjectRetention` is recorded with eventName `PutObjectLockRetention`.
- Cross-account: CloudTrail always delivers object-level logs to the requester, and also to the bucket owner even if the owner lacks permission for the operation or does not own the object.

## Server access log fields
- **Requester:** the canonical user ID, or `-` for unauthenticated requests; for an IAM user it gives the IAM user name with the account; for an assumed role it gives the role.
- **Remote IP:** the apparent IP; intermediate proxies and firewalls can obscure the real one.
- **Operation:** declared as `REST.HTTP_method.resource_type`, `WEBSITE.…`, `SOAP.…`, `BATCH.DELETE.OBJECT` or `S3.action.resource_type`.
- **Bytes Sent:** response bytes excluding HTTP overhead, or `-` if zero.
- A copy produces two records (a GET and a PUT portion).

## Attribution
- A `-` requester means an unauthenticated request; check the bucket's public access settings and the CloudTrail record for presigned URL use.
- Correlate the access key in the CloudTrail `useridentity` block with key-creation and leak timelines.

## Verify
Totals of objects and bytes accessed by the attacker identity are computed from the logs and stated with the coverage window.

## Checked
Confirmed against the S3 "Amazon S3 CloudTrail events" page (data events off by default and chargeable, resource types, selectors, DeleteObjects behaviour, 90-day bucket-level history, cross-account delivery) and the S3 server access log format page (Requester, Remote IP, Operation, Bytes Sent, copy records). Removed unconfirmed content: the Athena query and the Athena page (not read), "best-effort delivery with hours of delay", billing and GuardDuty signals, `BytesDownloaded` metrics, user-agent tool names, and the claim that anonymous requests prove a presigned URL or public bucket.

Method: docs-only read of cited pages, 2026-11-09
