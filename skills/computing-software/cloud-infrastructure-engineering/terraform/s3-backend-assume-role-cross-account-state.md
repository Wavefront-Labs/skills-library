---
id: computing-software.cloud-infrastructure-engineering.terraform.s3-backend-assume-role-cross-account-state
name: s3-backend-assume-role-cross-account-state
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, s3-backend-assume-role, cross-account-state, s3-backend, assume-role, aws]
level: practitioner
status: docs-checked
description: "Keep state in a central AWS account with the S3 backend assume_role block, while the AWS provider deploys into workload accounts, with the IAM and bucket policy it needs."
sources: ["https://developer.hashicorp.com/terraform/language/backend/s3", "https://developer.hashicorp.com/terraform/language/backend"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 backend with `assume_role` (cross-account state)

## Pattern
HashiCorp's multi-account pattern: an administrative account holds the S3 bucket with the
state files; environment accounts hold the managed infrastructure and an IAM role that
Terraform can assume.
- **State account** owns the bucket (and the KMS key if you use one).
- **Workload accounts** host resources; the AWS provider assumes a deploy role there.
- Backend I/O (reading and writing state in S3) is performed directly as the identity
  in the administrative account, or as the role in the backend's own `assume_role`.

```hcl
terraform {
  backend "s3" {
    bucket       = "example-tfstate"
    key          = "workloads/payments/prod.tfstate"
    region       = "eu-west-1"
    encrypt      = true
    kms_key_id   = "<KMS_KEY_ARN>"
    use_lockfile = true
    assume_role = {
      role_arn     = "arn:aws:iam::STATE-ACCOUNT-ID:role/tfstate-rw"
      session_name = "tf-payments-prod"
      external_id  = "optional"
    }
  }
}
provider "aws" {
  region = "eu-west-1"
  assume_role = {
    role_arn = "arn:aws:iam::WORKLOAD-ACCOUNT-ID:role/deploy"
  }
}
```
`assume_role` takes an object; `role_arn` is the only required key. `duration` (between
15m and 12h), `external_id`, `policy`, `policy_arns`, `session_name`, `source_identity`,
`tags` and `transitive_tag_keys` are optional. If you give several `assume_role` values the
roles are assumed in order.

## State role policy (state account)
Per HashiCorp, without workspaces the principal needs `s3:ListBucket` on the bucket
(at minimum able to list the path where state is stored), and `s3:GetObject` and
`s3:PutObject` on the state key. `s3:DeleteObject` is not needed on the state file because
Terraform does not delete it. With `use_lockfile`, `s3:GetObject`, `s3:PutObject` and
`s3:DeleteObject` are needed on `<key>.tflock`. With workspaces it also needs
`s3:DeleteObject` on `<workspace_key_prefix>/*/<key>` (default prefix `env:`). If you set
`kms_key_id` it also needs `kms:Encrypt`, `kms:Decrypt` and `kms:GenerateDataKey` on that key.
```json
{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow", "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::example-tfstate",
      "Condition": {"StringEquals": {"s3:prefix": "workloads/payments/prod.tfstate"}} },
    { "Effect": "Allow", "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": ["arn:aws:s3:::example-tfstate/workloads/payments/prod.tfstate"] },
    { "Effect": "Allow", "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": ["arn:aws:s3:::example-tfstate/workloads/payments/prod.tfstate.tflock"] }
  ]
}
```
To restrict who can modify or read each state, scope access per state object; if locking is
enabled the `.tflock` object must be included in the access controls. Reading state also
needs controlling, because state is sensitive.

## Gotchas
- Backend and provider credentials are independent: management operations go through the
  provider's `assume_role`, while state reads and writes use the backend's credentials.
- Backend blocks cannot refer to variables, locals or data sources. Supply
  per-environment values such as the role ARN with `-backend-config` (partial
  configuration).
- Values passed with `-backend-config` or hardcoded are written in plain text to the
  `.terraform` directory and into plan files; prefer environment variables for
  credentials.
- Non-default workspace states live under `<workspace_key_prefix>/<workspace_name>/<key>`;
  the policy must cover that path.
- Enable bucket versioning for recovery from accidental deletion (HashiCorp recommends it).

## Checked
Date: 2026-11-07
Read in full: the S3 backend page (all sections, including Permissions Required, Assume Role Configuration, Multi-account AWS Architecture, Protecting Access to Workspace State) and the backend overview page (limitations, credentials, partial configuration).
Confirmed: the `assume_role` keys, duration range and ordering, permission lists, `.tflock` handling, KMS permissions, `workspace_key_prefix` default and path, backend block limitations, plain-text warning, versioning recommendation. Provider `assume_role = { role_arn = ... }` form is the one shown on the page's multi-account example.
Removed (not on the pages): "since Terraform 1.6 ... top-level `role_arn` deprecated", `DeleteObject` on the whole prefix, the claim that `AccessDenied` on init usually means a KMS key policy problem, the real-looking account IDs and KMS ARN (now placeholders), and all Verify steps. The old policy fragment was not valid JSON and was rewritten from the page's policy.
Method: documentation only; no commands were run.
