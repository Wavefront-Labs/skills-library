---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-encryption-and-network
name: dynamodb-encryption-and-network
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-encryption-and-network, dynamodb-security, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Secure DynamoDB data at rest with KMS keys and share tables with resource-based policies."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/specifying-conditions.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encryption and network controls

**Goal:** Secure data at rest and in transit.

## Steps
- All tables are encrypted at rest and this cannot be disabled; choose an AWS owned key (default), an AWS managed key or a customer managed KMS key.
- Resource-based policies exist for tables, indexes and streams and support cross-account access.

## Gotcha
If DynamoDB loses access to a customer managed KMS key (for example the grant is revoked), it cannot protect or maintain the table; keep the key and its grants intact.

## Verify
- [ ] describe-table shows SSEDescription with the expected key type.

## Checked
Checked 2026-11-03 against the encryption at rest and resource-based policy pages: always-on encryption, the three key types, resource-based policies on tables, indexes and streams with cross-account support, and the effect of revoking KMS access match. Removed the VPC endpoint and CloudTrail data event steps and the aws/dynamodb key name (the pages read were stubs or silent on them) and resolved the cross-account "(confirm)". Description narrowed to match.
Method: documentation only; no commands were run.
