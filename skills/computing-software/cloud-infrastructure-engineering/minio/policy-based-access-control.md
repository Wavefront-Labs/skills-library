---
id: computing-software.cloud-infrastructure-engineering.minio.policy-based-access-control
name: policy-based-access-control
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, policy-based-access-control, pbac, iam-policy, deny-overrides-allow, policy-document, tag-based-conditions, mc-admin-policy]
level: practitioner
status: docs-checked
description: "Write MinIO IAM policy documents with Effect, Action, Resource and Condition: deny overrides allow, the 20 KiB limit, tag conditions via ExistingObjectTag and key S3 actions."
sources: ["https://github.com/minio/docs/blob/main/source/administration/identity-access-management/policy-based-access-control.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO policy-based access control

MinIO PBAC mirrors AWS IAM policy syntax and behaviour. Policies are managed with `mc admin policy` and attached with `mc admin policy attach` to users or groups. Access is denied by default; each user gets only what is explicitly granted by assigned or inherited policies. **Deny overrides Allow** on the same action and resource, even if the Allow comes from a user policy and the Deny from a group.

## Policy document
```json
{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow", "Action": ["s3:<ActionName>"], "Resource": "arn:aws:s3:::*", "Condition": {} }
  ]
}
```
- `Resource` can restrict to a bucket or prefix; `arn:aws:s3:::data*` matches `data`, `data_private`, `data_internal`; `*` applies to all.
- Max size of one policy document: **20 KiB**. No limit on how many policies attach to a user or group.
- Since RELEASE.2022-10-02T19-29-29Z, conditions can limit access to objects with a given tag using `s3:ExistingObjectTag/<key>` for selected actions.

## Notable actions
`s3:*`, `s3:CreateBucket`, `s3:DeleteBucket`, `s3:ForceDeleteBucket` (needed to remove non-empty buckets with `x-minio-force-delete`), `s3:ListAllMyBuckets`, `s3:ListBucket`, `s3:GetObject` (extra condition keys `s3:x-amz-server-side-encryption`, `s3:x-amz-server-side-encryption-customer-algorithm`, `s3:ExistingObjectTag/<key>`, `s3:versionid`), `s3:DeleteObject`, `s3:RestoreObject`, plus `admin:*` for admin API.

Built-in policies: `computing-software.cloud-infrastructure-engineering.minio.builtin-policies`.

## Checked

2026-11-03. Confirmed against the MinIO docs source: the policy-based access control page: policy actions, attach command, evaluation behaviour. Removed or fixed: nothing.

Method: documentation only; no commands were run.
