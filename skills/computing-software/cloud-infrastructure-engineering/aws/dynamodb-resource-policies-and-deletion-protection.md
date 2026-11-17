---
id: computing-software.cloud-infrastructure-engineering.aws.dynamodb-resource-policies-and-deletion-protection
name: dynamodb-resource-policies-and-deletion-protection
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dynamodb, dynamodb-resource-policy, deletion-protection, cross-account, data-protection]
level: advanced
status: docs-checked
description: "Attach DynamoDB resource-based policies to tables and streams for cross-account access and guardrails, and turn on deletion protection for critical tables."
sources: ["https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/access-control-resource-based.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/rbac-auth-iam-id-based-policies-DDB.html", "https://github.com/boto/botocore/blob/develop/botocore/data/dynamodb/2012-08-10/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource-based policies and deletion protection

## 1. Resource policy on a table
```bash
cat > policy.json <<'J'
{"Version":"2012-10-17","Statement":[
 {"Sid":"ReportingRead","Effect":"Allow","Principal":{"AWS":"arn:aws:iam::<REPORTING_ACCOUNT_ID>:role/reporter"},
  "Action":["dynamodb:GetItem","dynamodb:Query","dynamodb:DescribeTable"],
  "Resource":["arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/orders","arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/orders/index/*"]}]}
J
aws dynamodb put-resource-policy --resource-arn arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/orders --policy file://policy.json
aws dynamodb get-resource-policy --resource-arn arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/orders
```
- Resource-based policies are supported on tables, indexes and streams. The policy on a table covers its
  indexes (list index ARNs in `Resource`); a stream takes its own policy on the stream ARN. Maximum policy size
  is 20 KB, and whitespace counts.
- Same account: a resource-based policy alone is sufficient. Cross-account: access must be allowed in both the
  caller's identity-based policy and the resource-based policy.
- Block Public Access is applied automatically when you create or modify a resource-based policy, so
  policies granting public access are rejected.
- `put-resource-policy` accepts `--expected-revision-id` to update only if the current revision matches (use
  `NO_POLICY` to attach only when none exists), and `--confirm-remove-self-resource-access`.
- Denying the DynamoDB service-linked role actions used for global table replication breaks adding or
  removing replicas.
- An unconditional allow in an identity-based policy is not narrowed by conditions in a resource policy's allow
  (for example on `dynamodb:Attributes`); use an explicit `Deny` to restrict.

## 2. Deletion protection
```bash
aws dynamodb update-table --table-name orders --deletion-protection-enabled
aws dynamodb create-table ... --deletion-protection-enabled
```
Deletion protection is a table setting (`DeletionProtectionEnabled`, returned by `DescribeTable`) accepted by
both `CreateTable` and `UpdateTable`. Turn it on for critical tables and keep point-in-time recovery or backups
for recovery from item-level mistakes. The behaviour of `DeleteTable` on a protected table is described on the
table-basics documentation page, which was not read for this check.

## Verify
- [ ] Reporting role can Query from its account; `describe-table` shows `DeletionProtectionEnabled` true; a `delete-table` attempt on a non-production protected table was recorded and matches the documented behaviour.

## Checked
Checked 2026-10-24 against the DynamoDB guide pages on resource-based policies and the identity/resource policy
authorization page, plus the botocore model. Confirmed: supported resources, index coverage, 20 KB limit,
Block Public Access, same-account vs cross-account rules, `ExpectedRevisionId` / `NO_POLICY` behaviour,
`ConfirmRemoveSelfResourceAccess`, the global-table service-linked-role warning, and the
`DeletionProtectionEnabled` parameter on create and update. Removed the organisation-wide Deny example
(its `Resource: "*"` and `aws:PrincipalOrgID` use was not checked and could block service principals),
the "no role assumption" statement, the SCP suggestion and the CloudFormation property names. The `DeleteTable`
behaviour for protected tables was not confirmed, so the skill no longer states it.
Method: documentation only; no commands were run.
