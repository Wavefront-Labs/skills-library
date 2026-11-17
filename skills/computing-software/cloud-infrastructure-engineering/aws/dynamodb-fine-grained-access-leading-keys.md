---
id: computing-software.cloud-infrastructure-engineering.aws.dynamodb-fine-grained-access-leading-keys
name: dynamodb-fine-grained-access-leading-keys
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dynamodb, leadingkeys, fine-grained-access-dynamodb, multi-tenant, iam-conditions]
level: advanced
status: docs-checked
description: "Restrict DynamoDB access per user or tenant with dynamodb:LeadingKeys, attribute-level conditions and principal tags, and close the Scan and index loopholes."
sources: ["https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/specifying-conditions.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_variables.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fine-grained access with dynamodb:LeadingKeys

## 1. Row-level: partition key must equal the caller's identity
```json
{"Effect":"Allow",
 "Action":["dynamodb:GetItem","dynamodb:Query","dynamodb:PutItem","dynamodb:UpdateItem","dynamodb:DeleteItem","dynamodb:BatchGetItem","dynamodb:BatchWriteItem"],
 "Resource":"arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/notes",
 "Condition":{"ForAllValues:StringEquals":{"dynamodb:LeadingKeys":["${aws:PrincipalTag/tenant}"]}}}
```
- `LeadingKeys` is the table's partition key; the key name is plural even for single-item actions and you must
  use the `ForAllValues` modifier, which also makes batch operations check every key.
- The partition key value must equal the substituted value exactly, so store the tenant identifier itself as
  the partition key (or put the tenant identifier in the tag value in the same format as the key).
- Policy variables need `"Version": "2012-10-17"`. `${aws:PrincipalTag/<key>}` is available for IAM users or
  roles that carry the tag (including session tags). The DynamoDB guide's examples use web identity variables such
  as `${www.amazon.com:user_id}`, `${graph.facebook.com:id}` and `${accounts.google.com:sub}`.

## 2. Column-level
```json
"Condition":{"ForAllValues:StringEquals":{"dynamodb:Attributes":["PK","SK","title","body"]},
             "StringEqualsIfExists":{"dynamodb:Select":"SPECIFIC_ATTRIBUTES","dynamodb:ReturnValues":["NONE","UPDATED_OLD","UPDATED_NEW"]}}
```
- `dynamodb:Attributes` lists the top-level attributes named in the request; it is checked on the request, not
  the response. Without a `ProjectionExpression`, all attributes are returned regardless of the policy, which is
  why `dynamodb:Select` must also be constrained.
- You must list every primary key and index key attribute for the table and any listed indexes, or DynamoDB
  cannot perform the action.
- Restrict `dynamodb:ReturnValues` on writes (exclude `ALL_OLD` and `ALL_NEW`). Do not grant `PutItem`,
  `DeleteItem` or `BatchWriteItem` with attribute restrictions: they replace the whole item.
- AWS recommends allow-based policies for DynamoDB; deny-based versions are hard to write correctly and can be
  invalidated by later API changes.

## 3. Loopholes
- **Scan** returns all items regardless of leading keys: do not grant it.
- **GSIs and LSIs**: grant only the index ARNs needed (`table/notes/index/byTenant`) and test each index with
  the tenant role, since index access is a separate resource ARN.
- Do not apply fine-grained conditions to the service principals or service-linked roles used for global table
  replication: that can interrupt replication.
- Contributor Insights publishes partition and sort key values to CloudWatch, so anyone with CloudWatch access can
  see keys of FGAC-protected tables.

## Verify
- [ ] Tenant A's role gets `AccessDenied` reading `TENANT#B` items via GetItem, Query, BatchGetItem and the GSI.

## Checked
Checked 2026-10-24 against the DynamoDB guide page "Using IAM policy conditions for fine-grained access
control", the IAM policy variables page and the global condition keys page. Confirmed: `dynamodb:LeadingKeys`
semantics and the mandatory `ForAllValues` modifier; `dynamodb:Attributes`, `dynamodb:Select` and
`dynamodb:ReturnValues` values; the `StringEqualsIfExists` pattern and the allow-list recommendation; Scan is not
covered by leading-key conditions; policy variables require version 2012-10-17; `aws:PrincipalTag` availability.
Removed unchecked claims: the Cognito identity pool variable, `StringLike` prefix matching, PartiQL action
conditions, transaction authorisation behaviour, and the statement that an index keyed differently bypasses
LeadingKeys. Added the requirement to list key attributes and the PutItem/DeleteItem caveat from the guide.
Method: documentation only; no commands were run.
