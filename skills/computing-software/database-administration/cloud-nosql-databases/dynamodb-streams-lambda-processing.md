---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-streams-lambda-processing
name: dynamodb-streams-lambda-processing
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-streams-lambda-processing, dynamodb-streams, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Process change records reliably with a Lambda event source mapping."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html
  - https://docs.aws.amazon.com/lambda/latest/dg/services-ddb-params.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streams with Lambda processing

**Goal:** Process change records reliably with a Lambda event source mapping.

## Steps
- Enable with StreamSpecification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES (KEYS_ONLY, NEW_IMAGE, OLD_IMAGE also exist).
- Records are ordered per item key and retained for 24 hours.
- Event source mapping settings: BatchSize (default 100, max 10,000), ParallelizationFactor (1-10), BisectBatchOnFunctionError, MaximumRetryAttempts, MaximumRecordAgeInSeconds, and an on-failure SQS or SNS destination.
- Make handlers idempotent; Lambda processes each event at least once. Use TRIM_HORIZON as the starting position if missing events at mapping creation matters.

## Gotcha
MaximumRetryAttempts defaults to -1 (infinite), so a poison record is retried until it expires from the stream (24 hours) unless you set retry limits and a failure destination.

## Verify
- [ ] Writing an item triggers the function once; a forced failure lands in the on-failure destination and the shard continues.

## Checked
Checked 2026-11-03 against the Lambda DynamoDB event source and parameters pages and the Streams page: 24 hour retention, per-item ordering, view types, the parameter defaults and limits, SQS/SNS destinations and at-least-once processing match. Added the infinite-retry default to the gotcha and the TRIM_HORIZON note (LATEST can miss events during mapping creation or update).
Method: documentation only; no commands were run.
