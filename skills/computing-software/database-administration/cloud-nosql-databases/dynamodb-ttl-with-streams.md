---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-ttl-with-streams
name: dynamodb-ttl-with-streams
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-ttl-with-streams, dynamodb-ttl, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Archive or react to expired items using the stream record that TTL produces."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TTL deletions and streams

**Goal:** Archive or react to expired items using the stream record that TTL produces.

## Steps
- TTL deletes appear in DynamoDB Streams with userIdentity.principalId = dynamodb.amazonaws.com and type Service.
- Lambda event filter: {"userIdentity":{"type":["Service"],"principalId":["dynamodb.amazonaws.com"]}} archives only TTL deletes to S3 or Firehose.
- TTL deletes consume no write capacity on the source table; on global tables (2019.11.21) the replicated delete is billed on the replicas.
- The record includes the old item only if the view type has OLD_IMAGE.

## Gotcha
Use NEW_AND_OLD_IMAGES or OLD_IMAGE or the archive will have no item content.

## Verify
- [ ] An expired test item results in one filtered Lambda invocation and an archived object.

## Checked
Checked 2026-11-03 against the TTL page: TTL deletes appear in Streams with userIdentity type Service and principalId dynamodb.amazonaws.com, the filter pattern, no write cost on the source and replicated-delete billing on global table replicas match. Resolved the "(confirm)" marker. View-type behaviour follows the Streams page (OLD_IMAGE needed for item content).
Method: documentation only; no commands were run.
