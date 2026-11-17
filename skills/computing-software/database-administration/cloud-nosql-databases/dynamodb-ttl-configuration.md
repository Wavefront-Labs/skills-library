---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-ttl-configuration
name: dynamodb-ttl-configuration
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-ttl-configuration, dynamodb-ttl, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Expire items automatically at no write cost."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TTL configuration and expiry

**Goal:** Expire items automatically at no write cost.

## Steps
- aws dynamodb update-time-to-live --table-name Sessions --time-to-live-specification Enabled=true,AttributeName=expiresAt
- The attribute must be type Number holding epoch seconds.
- Deletion typically happens within a few days of expiry; expired items may still appear in reads until then.
- Filter in queries with FilterExpression expiresAt > :now to hide pending-deletion items.

## Gotcha
Expiry is not immediate, so never rely on TTL for exact-time deletion; always filter on the timestamp as well.

## Verify
- [ ] describe-time-to-live shows ENABLED and a sample item with a past expiresAt disappears within the expected window.

## Checked
Checked 2026-11-03 against the TTL page and botocore UpdateTimeToLive (Enabled, AttributeName): Number type, epoch seconds, deletion typically within a few days, expired items still readable and hidden by a filter, and no write cost all match. Removed the "within 48 hours" figure and the unconfirmed claim that millisecond values never expire; the gotcha now states the documented delay instead.
Method: documentation only; no commands were run.
