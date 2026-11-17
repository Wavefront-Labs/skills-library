---
id: computing-software.cloud-infrastructure-engineering.aws.tag-on-create-with-request-tag-conditions
name: tag-on-create-with-request-tag-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, tagging, tag-on-create, request-tag, tag-keys-condition, createaction, abac]
level: advanced
status: docs-checked
description: "Control tags at resource creation with aws:RequestTag and aws:TagKeys conditions, and allow EC2 tagging only during create via ec2:CreateAction."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/access_tags.html#access_tags_control-requests", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/supported-iam-actions-tagging.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tag-on-create with RequestTag conditions

## 1. Condition keys
- `aws:RequestTag/<key>`: which tag key-value pairs may be passed in a request that tags a resource.
- `aws:TagKeys`: which tag keys may (or must) appear in the request.
- `aws:ResourceTag/<key>`: tags already on the resource (ABAC for later actions). Some services support only a service-specific version of this key.
- `ec2:CreateAction`: used on `ec2:CreateTags` to tie tagging permission to the create action.
- Services must support tag-based control: check the ABAC column in "AWS services that work with IAM".

## 2. EC2: letting users tag during creation
To tag at creation users need the create action (for example `ec2:RunInstances` or `ec2:CreateVolume`) and explicit `ec2:CreateTags`. If tags are in the request, EC2 does an extra authorization on `ec2:CreateTags`; without that permission the request fails. `ec2:CreateTags` is only evaluated when tags are supplied (and also for tags in a launch template).
```json
{"Effect": "Allow", "Action": "ec2:CreateTags",
 "Resource": "arn:aws:ec2:us-east-1:111122223333:*/*",
 "Condition": {"StringEquals": {"ec2:CreateAction": "RunInstances"}}}
```
With this, users can tag at launch but cannot call `ec2:CreateTags` on existing resources. Use `"CreateVolume"` for volumes (AWS shows a separate policy per create action).

## 3. Controlling which tags are allowed
From the EC2 page, applicable to create actions and to `ec2:CreateTags` / `ec2:DeleteTags`:
- Specific key and value: `"StringEquals": {"aws:RequestTag/cost-center": "cc123"}`.
- A key must be present (any value): `"StringLike": {"aws:RequestTag/purpose": "*"}`.
- Only certain keys allowed if any tags are sent: `"ForAllValues:StringEquals": {"aws:TagKeys": ["environment","cost-center"]}`.
- At least one of certain keys must be present: `"ForAnyValue:StringEquals": {"aws:TagKeys": ["environment","webserver"]}`.
To force tags at creation you must use `aws:RequestTag`, or `aws:TagKeys` with `ForAnyValue`, on the create action itself, because `ec2:CreateTags` is not evaluated when no tags are sent.

IAM example for Secrets Manager (`secretsmanager:CreateSecret`, `secretsmanager:TagResource`): `"Null": {"aws:TagKeys": "false"}` plus `ForAllValues:StringEquals` on `aws:TagKeys` for `environment` and `cost-center` permits only those keys; the Null condition makes the statement false when the request has no tags.

## 4. Case sensitivity
Condition key names are not case-sensitive, values are. `aws:ResourceTag/TagKey1` matches a tag key `TagKey1` or `tagkey1`, but not both. Services may allow tag keys that differ only by case (`stack` and `Stack`). To enforce key casing, use `aws:TagKeys` with the exact key as a value, or use Organizations tag policies.

## Gotchas
- Do not control `iam:PassRole` by tagging the role and using `aws:ResourceTag`; AWS warns it is unreliable.
- Test your create call paths (console, CLI, IaC): they must send the tags in the create request for these conditions to see them.

## Method
Rewritten from the IAM and EC2 pages cited. The SCP example page returned no readable text, so the SCP, console second-call behaviour, `RunInstances` multi-ARN scoping and per-service support claims were removed.

## Checked
Checked 2026-11-08 against the IAM page "Controlling access to AWS resources using tags" and the EC2 page "Grant permission to tag Amazon EC2 resources during creation". The Organizations SCP tagging examples page was unreadable and is no longer cited.
Method: docs-only read of cited pages, 2026-11-08
