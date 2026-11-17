---
id: computing-software.cybersecurity-defensive.cloud-security.cloudtrail-lake-data-events
name: cloudtrail-lake-data-events
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloudtrail-lake, cloudtrail-data-events, s3-data-events, event-data-store, advanced-event-selectors, cloud-logging]
level: practitioner
status: docs-checked
description: "Use CloudTrail data events and Lake: advanced event selectors for S3 data events, event data stores, Trino SQL queries, retention and cost; Lake closed to new customers."
sources: ["https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake.html", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/query-limitations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudTrail Lake and data events

**Availability:** the Lake pages state CloudTrail Lake is closed to new customers from 31 May 2026; existing customers continue as normal. New builds should plan a trail-plus-Athena alternative.

## Data events
- Trails and event data stores do **not** log data events by default, and they cost extra. Data events (data plane) are high volume.
- Basic selectors support only S3 objects, Lambda functions and DynamoDB tables; other resource types (150+) need **advanced event selectors**.
- Selector fields include `eventCategory`, `resources.type`, `resources.ARN`, `eventName`, `eventSource`, `eventType`, `readOnly` (omit to log reads and writes), `sessionCredentialFromConsole`, `userIdentity.arn`. Operators: Equals, NotEquals, StartsWith, EndsWith, NotStartsWith, NotEndsWith; no wildcards. Max 500 values across selectors on an event data store.
- S3 example (trailing slash needed because object ARNs extend the bucket ARN):
```json
[{"Name": "S3EventSelector",
  "FieldSelectors": [
    {"Field": "eventCategory", "Equals": ["Data"]},
    {"Field": "resources.type", "Equals": ["AWS::S3::Object"]},
    {"Field": "resources.ARN", "StartsWith": ["arn:aws:s3:::prod-customer-data/"]}]}]
```
Add a `readOnly` field selector to log only reads or only writes.
- Logging all S3 data events to a bucket that is itself in scope creates a loop; set `RecursiveLogging` to false on the trail or deliver to another account's bucket.
- Two copies of an event (for example two trails) are charged twice.

## CloudTrail Lake
- Event data stores (EDS) are immutable, queryable collections (stored as ORC). Retention up to 3,653 days with one-year extendable pricing, or up to 2,557 days with seven-year pricing.
- An EDS holds one event category: CloudTrail events (management, data, network activity), Insights, Config configuration items, Audit Manager evidence, or events from outside AWS via integrations.
- Organisation event data stores cover multiple accounts and Regions. Trail events can be copied to an EDS. Cross-account access via an EDS resource policy; optional customer KMS key (cannot be changed later).
- Federate an EDS to Glue Data Catalog to query with Athena.
- Events typically arrive about 5 minutes after the API call, not guaranteed.

## Querying
Only SELECT is allowed, with Trino SELECT syntax and functions; the EDS ID goes in FROM. UNION, EXCEPT, INTERSECT and JOINs work across event data stores. Queries are billed by data scanned; results are viewable for 7 days or can be saved to S3.
```sql
SELECT eventTime, userIdentity.arn, sourceIPAddress, eventName, element_at(requestParameters,'key') AS objkey
FROM <eds-id>
WHERE eventSource = 's3.amazonaws.com' AND eventName = 'GetObject'
  AND element_at(requestParameters,'bucketName') = 'prod-customer-data'
  AND eventTime > '2026-10-01 00:00:00'
ORDER BY eventTime
```
Aggregate by principal and IP to find bulk downloads.

## Verify
- [ ] Data events captured for crown-jewel buckets.
- [ ] Saved investigation queries in the IR runbook.

## Checked
Method: 2026-11-08 read the cloudtrail-lake and query-limitations pages in full and the data-events page up to its first 100,000 characters (the last ~14k characters unread). Added the closed-to-new-customers notice and exact retention figures; removed unsupported claims: read-vs-write cost advice, S3 server access log comparison, Secrets Manager remark, and the 5-15 minute test window. The query example is illustrative and not taken from the pages; other claims unchanged.
