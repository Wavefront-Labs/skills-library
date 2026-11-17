---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-iam-fine-grained-access
name: dynamodb-iam-fine-grained-access
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-iam-fine-grained-access, dynamodb-security, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Restrict users to their own items using IAM condition keys."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/specifying-conditions.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fine-grained access control

**Goal:** Restrict users to their own items using IAM condition keys.

## Steps
- Condition: "ForAllValues:StringEquals": {"dynamodb:LeadingKeys": ["${www.amazon.com:user_id}"]} limits access to partition keys equal to the caller's federated user id (the docs example uses Login with Amazon).
- dynamodb:Attributes restricts which attributes can be read or written; pair with dynamodb:Select SPECIFIC_ATTRIBUTES.
- Grant least privilege per action (GetItem, Query) and per resource ARN, including table/NAME/index/*.

## Gotcha
Forgetting the index ARN denies index queries; a wildcard table/* grants every table, far too broad.

## Verify
- [ ] The IAM policy simulator denies cross-user key reads and allows the user's own.

## Checked
Checked 2026-11-03 against the specifying-conditions page: dynamodb:LeadingKeys with ForAllValues, dynamodb:Attributes paired with dynamodb:Select SPECIFIC_ATTRIBUTES and the table/NAME/index/* ARN form match. Replaced the Cognito variable (not on the page) with the documented www.amazon.com:user_id example and removed the unconfirmed "use roles not access keys" line.
Method: documentation only; no commands were run.
