---
id: computing-software.cloud-infrastructure-engineering.aws.iam-policy-variables-in-arns-and-conditions
name: iam-policy-variables-in-arns-and-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iam, policy-variables, aws-username-variable, principaltag-variable, per-user-prefix, iam-policy-design, least-privilege]
level: practitioner
status: docs-checked
description: "Write one IAM policy that scopes every principal to its own resources with policy variables (aws:username, aws:PrincipalTag, sts:RoleSessionName) in ARNs and conditions."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_variables.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_aws_my-sec-creds-self-manage.html", "https://github.com/boto/botocore/blob/develop/botocore/data/iam/2010-05-08/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IAM policy variables: one policy, per-principal scope

**Goal:** replace N near-identical policies ("alice can use `users/alice/`", "bob can use
`users/bob/`") with one policy whose `Resource` or `Condition` contains `${...}` variables
that IAM fills in from the request context at evaluation time.

## 1. Prerequisites
- Variables only work with `"Version": "2012-10-17"` (introduced in that version). Without the `Version` element,
  or with an earlier version, `${aws:username}` is treated as a literal string.
- Variables are allowed in the `Resource` element (only in the resource portion of the ARN, after the fifth colon,
  not in the service or account parts) and in `Condition` **values** for string operators (`StringEquals`,
  `StringLike`, `StringNotLike`) and ARN operators (`ArnEquals`, `ArnLike`). They cannot be used with `Numeric`,
  `Date`, `Boolean`, `Binary`, `IP Address` or `Null` operators.
- Any single-valued condition key can be a variable; multivalued keys cannot. Key names are case-insensitive.
- Variables work in identity-based policies, resource policies, SCPs, session policies and VPC endpoint
  policies, and in identity policies used as permissions boundaries.

## 2. The variables that matter
| Variable | Present when | Typical use |
|---|---|---|
| `${aws:username}` | IAM **users** only: not present for roles, federated sessions or root | S3 home folders, `iam:*AccessKey*` on self |
| `${aws:userid}` | always; for an assumed role it is `ROLEID:session-name`, for an IAM user the unique ID | stable ID that survives user rename |
| `${aws:PrincipalTag/team}` | principal has that tag (user, role, or session tag) | ABAC: team-scoped prefixes and resources |
| `${aws:PrincipalAccount}`, `${aws:PrincipalOrgID}` | account always; org ID only for organization members | resource policies shared org-wide |
| `${aws:SourceIdentity}` | after a source identity is set during `AssumeRole`; persists through role chaining | per-human scope |
| `${s3:prefix}` | S3 list requests | finer scoping |
Missing variables: when the context key has no value, `StringEquals` / `StringLike` do not match and the statement
does not take effect (an Allow grants nothing), while inverted operators such as `StringNotEquals` do match. A
`Resource` or `NotResource` containing a variable with no value matches no resource. Provide a default with a comma
and single quotes: `${aws:PrincipalTag/team, 'none'}` resolves to `none` instead.

## 3. Pattern: S3 home directories
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {"Sid": "ListOwnPrefix", "Effect": "Allow", "Action": "s3:ListBucket",
     "Resource": "arn:aws:s3:::corp-home",
     "Condition": {"StringLike": {"s3:prefix": ["users/${aws:username}/*", "users/${aws:username}"]}}},
    {"Sid": "RWOwnObjects", "Effect": "Allow",
     "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
     "Resource": "arn:aws:s3:::corp-home/users/${aws:username}/*"}
  ]
}
```
For roles (Identity Center, federated users), `aws:username` is absent, so build the prefix from a principal
tag passed as a session tag, for example `${aws:PrincipalTag/userName}`.

## 4. Pattern: self-service credentials
The AWS self-service credentials example scopes each statement to the caller's own user ARN:
```json
{"Effect": "Allow",
 "Action": ["iam:CreateAccessKey", "iam:DeleteAccessKey", "iam:ListAccessKeys",
            "iam:UpdateAccessKey", "iam:ChangePassword"],
 "Resource": ["arn:aws:iam::*:user/${aws:username}"]}
```
MFA device actions (`iam:EnableMFADevice`, `iam:ListMFADevices`, `iam:ResyncMFADevice`, `iam:DeactivateMFADevice`)
use the same user ARN, and `iam:CreateVirtualMFADevice` uses `arn:aws:iam::*:mfa/*` in the AWS example.

## 5. Pattern: team-scoped resources (ABAC with variables)
```json
{"Effect": "Allow", "Action": ["secretsmanager:GetSecretValue"],
 "Resource": "arn:aws:secretsmanager:eu-west-1:111122223333:secret:${aws:PrincipalTag/team}/*"}
```
Combine with a condition that the principal tag is set:
`"Condition": {"Null": {"aws:PrincipalTag/team": "false"}}` (a `Null` test on the key, not a variable).

## 6. Escaping and special characters
- Literal `*`, `?` and `$` inside a string: write `${*}`, `${?}`, `${$}`.
- S3 keys are case-sensitive; `${aws:username}` keeps the user's case, so `Alice` and a `users/alice/` folder will
  not match.

## 7. Test it
```bash
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::111122223333:user/alice \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::corp-home/users/alice/a.txt arn:aws:s3:::corp-home/users/bob/a.txt
```
Expect `allowed` for alice's key and `implicitDeny` for bob's. For role sessions, pass
`--context-entries` with `ContextKeyName=aws:PrincipalTag/team,ContextKeyValues=data,ContextKeyType=string`.

## Gotchas
- `${aws:username}` is absent for roles, so a policy written for users and attached to a
  role grants nothing; this is the commonest "it works for me but not in CI" bug.
- A principal that can change the tags a policy keys off (for example through `iam:TagUser` on itself or
  `sts:TagSession`) can rewrite its own scope; restrict who can set those tags.

## Verify
- [ ] `Version` is `2012-10-17` on every policy using variables.
- [ ] Simulator shows allow on own prefix, implicit deny on another principal's prefix.
- [ ] A role session without the tag resolves to the default value and gets no access.
- [ ] Principals cannot modify the tags the policy keys off.

## Checked
Checked 2026-10-24 against the IAM User Guide pages "IAM policy elements: Variables and tags", global
condition keys and the self-service credentials example, plus the botocore IAM model. Corrected: the old text
said variables work in "Principal-free parts of resource policies" and are not allowed in `Action`; the page
limits them to the `Resource` ARN resource portion and to condition values with string and ARN operators. The
old table row for `${sts:RoleSessionName}` and `${ec2:SourceInstanceARN}` was removed (not on the checked pages),
as were the tag-policy regex suggestion, the claim that `validate-policy` flags variables, and the
awkward-wildcard example for role session names. Confirmed: version requirement, default value syntax, special
variables `${*}`, `${?}`, `${$}`, behaviour of variables without a value, `aws:username` absence for roles,
`aws:userid` formats, `aws:SourceIdentity` persistence, and the simulator `--context-entries` shape.
Method: documentation only; no commands were run.
