---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-kinesis-data-streams-integration
name: dynamodb-kinesis-data-streams-integration
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-kinesis-data-streams-integration, dynamodb-streams, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Stream table changes to Kinesis when you need longer retention or multiple consumers."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kinesis Data Streams integration

**Goal:** Stream table changes to Kinesis when you need longer retention or multiple consumers.

## Steps
- aws dynamodb enable-kinesis-streaming-destination --table-name Orders --stream-arn KINESIS_STREAM_ARN
- Kinesis offers longer retention than DynamoDB Streams; records may arrive out of order or duplicated, so use ApproximateCreationDateTime to order and deduplicate.
- Changes are billed by both Kinesis and DynamoDB.

## Gotcha
Duplicate records are possible; deduplicate downstream by key and timestamp.

## Verify
- [ ] describe-kinesis-streaming-destination shows ACTIVE and test writes appear in the Kinesis stream.

## Checked
Checked 2026-11-03 against the Kinesis streaming destination page and botocore (EnableKinesisStreamingDestination TableName, StreamArn): longer retention, possible out-of-order and duplicate records, ApproximateCreationDateTime and dual billing match. Removed the unsupported 365 day figure, the "per change data capture unit" wording and the unconfirmed claim about enabling DynamoDB Streams alongside (resolved by deletion).
Method: documentation only; no commands were run.
