---
id: computing-software.cloud-infrastructure-engineering.aws.iam-policy-design
name: iam-policy-design
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iam, iam-policy-design, policy-documents, abac, attribute-based-access-control, tag-based-access, resource-policies, bucket-policy, kms-key-policy, managed-policies, inline-policies, policy-size-limits, service-authorization-reference, policy-as-code, access-analyzer, check-no-new-access, check-access-not-granted, cfn-policy-validator, least-privilege, principaltag, resourcetag, requesttag, tagkeys]
level: advanced
status: docs-checked
description: "Author AWS IAM policy documents that stay least-privilege at scale: ABAC with tags, resource-policy patterns, size and version limits, and policy-as-code checks in CI."
sources: ["https://docs.aws.amazon.com/general/latest/gr/iam-service.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_variables.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-generation.html", "https://github.com/boto/botocore/blob/develop/botocore/data/accessanalyzer/2019-11-01/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS IAM policy design: writing the documents themselves

**Goal:** policy JSON that a reviewer can read, that grows by adding tags rather than
statements, that fits inside AWS's size limits, and that CI refuses to merge if it widens
access. Evaluation logic, roles vs users and SCP guardrails are covered in
`computing-software.cloud-infrastructure-engineering.aws.iam-policies-and-roles`; this
skill is the authoring craft that sits on top.

## 1. Derive actions from the Service Authorization Reference, not from guesses
For each service, the reference lists every action, its access level, the resource types it accepts and the
condition keys it supports. Design from that table:
- Group statements by resource type, one `Sid` each (`ReadAppBucketObjects`,
  `DecryptWithAppKey`). Sids make Access Analyzer findings and CloudTrail debugging legible.
- Actions that do not support resource-level permissions must use `"Resource": "*"`; put them in their own
  statement so a reviewer can see exactly which grants are unscoped.
- Treat actions that change permissions (`iam:*` writes, `s3:PutBucketPolicy`, `kms:PutKeyPolicy`,
  `lambda:AddPermission`) as privilege escalation and review them separately.

## 2. ABAC: let tags carry the scope
Instead of one statement per project ARN, match principal tags to resource tags:
```json
{
  "Sid": "ProjectScopedEc2",
  "Effect": "Allow",
  "Action": ["ec2:StartInstances", "ec2:StopInstances", "ec2:RebootInstances"],
  "Resource": "arn:aws:ec2:*:<ACCOUNT_ID>:instance/*",
  "Condition": {"StringEquals": {"aws:ResourceTag/project": "${aws:PrincipalTag/project}"}}
}
```
To make ABAC safe you also need:
- **Creation-time tagging:** allow create only when `aws:RequestTag/project` equals the
  principal's tag, and restrict `aws:TagKeys` to an allowed list.
- **Tag immutability:** deny the service's tagging actions (for EC2, `ec2:CreateTags` / `ec2:DeleteTags`) on the
  `project` key unless the principal is an admin, or users simply re-tag resources into their scope.
- Session tags from your identity provider so `PrincipalTag` is set centrally.
- Not every service and action supports `aws:ResourceTag`: check the reference per
  action; fall back to ARN scoping where it is missing.
If a tag referenced through a policy variable is not present in the request, the variable has no value and
`StringEquals` does not match (so an allow does nothing); inverted operators such as `StringNotEquals` do match.

## 3. Resource-policy patterns
- **S3 bucket policy:** deny `aws:SecureTransport = false`; deny principals outside
  `aws:PrincipalOrgID` (the key exists only for principals that belong to an organization).
- **Service principals** (`sns.amazonaws.com`, `events.amazonaws.com`): pair with
  `aws:SourceArn` and `aws:SourceAccount`. The global condition keys page puts `aws:SourceAccount` and
  `aws:PrincipalAccount` on its sensitive-keys list, and says wildcards have no valid use for `aws:SourceAccount`.
- Key policies (KMS) and CloudFront access: follow each service's own guide for the required statements; they are
  not restated here.

## 4. Fit the limits
Quotas from the IAM service quotas table (confirm there before relying on them):
- Customer managed policy: 6,144 characters; IAM does not count white space. Up to 5 versions are stored per
  managed policy; beyond that an existing version must be overwritten (removed) before saving another.
- Inline policies: aggregate per entity of 2,048 characters for a user, 10,240 for a role and 5,120 for a group
  (white space not counted).
- Managed policies attached: per role 20 by default (adjustable, up to 25); per user 10 by default (up to 20);
  per group 10 (not adjustable).
- Role trust policy: 2,048 characters by default, adjustable up to 8,192.
When you hit a limit, wildcard within a coherent family (`s3:GetObject*`) or move to ABAC,
never collapse to `service:*`.
Prefer **customer managed** policies (versioned, reusable, rollback via
`set-default-policy-version`) over inline, except for one-off grants tightly bound to a single role.

## 5. Policy as code
- `aws accessanalyzer validate-policy --policy-type IDENTITY_POLICY --policy-document file://p.json`
  returns findings of type `ERROR`, `SECURITY_WARNING`, `SUGGESTION` or `WARNING`.
- `check-no-new-access` compares a candidate policy (`--new-policy-document`) against an existing one
  (`--existing-policy-document`) and reports whether the candidate grants new access; `check-access-not-granted`
  takes a policy and an `--access` list (for example `iam:PassRole`) to assert those permissions are not granted.
- Run these in CI against rendered policy documents (for example the JSON your IaC tool produces).

## Gotchas
- `"Resource": "arn:aws:s3:::bucket"` vs `"arn:aws:s3:::bucket/*"`: bucket-level actions such as `ListBucket` use the
  bucket ARN, object actions use the `/*` form; missing one is a common S3 denial.
- `${aws:username}` is not present for IAM role requests, so use `${aws:PrincipalTag/...}` for roles; `aws:userid` for
  an assumed role is `role-id:session-name`.
- A condition key the request does not carry makes `StringEquals` false but `...IfExists` true: choose deliberately.

## Verify
- [ ] Every statement has a Sid and a scoped Resource, or sits in a clearly labelled `*`-only statement.
- [ ] ABAC grants are backed by RequestTag/TagKeys on create and a deny on retagging.
- [ ] `validate-policy` returns no security warnings; `check-access-not-granted` passes for your sensitive-action list in CI.
- [ ] No managed policy is within 10% of the 6,144-character limit without a plan.

## Checked
Checked 2026-10-24 against the IAM General Reference quotas table, the IAM User Guide quotas, global condition keys
and policy variables pages, the Access Analyzer policy generation page and the botocore Access Analyzer model.
Corrected: managed policies per role were stated as 10 raisable to 20 (the table says 20 default, up to 25; per
user 10 up to 20) and the trust policy limit as raisable to 4,096 (the maximum is 8,192). Confirmed: 6,144 and
white space not counted, 5 policy versions, inline aggregate sizes, per-group 10, finding types, the
check operations and parameter names, `aws:SourceAccount` wildcard note, `aws:username` absence for roles,
`aws:userid` format for assumed roles, and missing-variable matching behaviour. Removed unchecked statements: the
five access-level category names, the KMS default-statement lock-out advice and `kms:ViaService` /
`kms:EncryptionContext` detail, the CloudFront OAC pattern, the `ArnLike` vs `StringLike` case-sensitivity
note, the `cfn-policy-validator` and Terraform plan-check tooling, and the per-call billing remark.
Method: documentation only; no commands were run.
