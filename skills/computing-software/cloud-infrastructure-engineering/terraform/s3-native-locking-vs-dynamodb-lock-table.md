---
id: computing-software.cloud-infrastructure-engineering.terraform.s3-native-locking-vs-dynamodb-lock-table
name: s3-native-locking-vs-dynamodb-lock-table
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, s3-backend, dynamodb-lock-table, conditional-writes, use-lockfile, state-locking]
level: practitioner
status: docs-checked
description: "Choose and migrate between S3 native lockfiles (use_lockfile) and the DynamoDB lock table: IAM, stale digest, and a safe transition, with Terraform vs OpenTofu differences."
sources: ["https://developer.hashicorp.com/terraform/language/backend/s3", "https://opentofu.org/docs/language/settings/backends/s3/", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# S3 lockfile vs DynamoDB lock table

## The two mechanisms
| | DynamoDB table | S3 lockfile |
|---|---|---|
| Setting | `dynamodb_table = "<TABLE_NAME>"` | `use_lockfile = true` (default false) |
| Mechanism | table with a `LockID` partition key (type String); a digest of the state is stored under a key suffixed `-md5` | `<key>.tflock` object in the state bucket; S3 conditional writes (`If-None-Match`) stop an overwrite of an existing key |
| Terraform docs | deprecated, will be removed in a future minor version | recommended |
| OpenTofu docs | fully supported, no plans to deprecate | fully supported, no plans to deprecate |

Choose per the tool you run: on Terraform plan to leave DynamoDB; on OpenTofu either
is supported and the docs say pick whichever fits your infrastructure.

## IAM
- DynamoDB locking: `dynamodb:GetItem`, `dynamodb:PutItem`, `dynamodb:DeleteItem` on the table.
- S3 state: `s3:GetObject` and `s3:PutObject` on the state key.
- With `use_lockfile`: `s3:GetObject`, `s3:PutObject` and `s3:DeleteObject` on the
  lock file `<key>.tflock` (and, for workspaces, on the workspace-prefixed paths).

## Native lockfile setup
```hcl
terraform {
  backend "s3" {
    bucket       = "<BUCKET>"
    key          = "prod/network.tfstate"
    region       = "<REGION>"
    use_lockfile = true
  }
}
```

## Migrating
1. Set **both** `use_lockfile = true` and `dynamodb_table`. Terraform allows both for
   migration; OpenTofu takes the S3 lock first, then the DynamoDB lock, and counts the
   lock as held only when both succeed, so runners on old and new config exclude each other.
2. Re-run `init` with `-reconfigure` where the backend settings changed.
3. After a baking period with no issues, remove `dynamodb_table`.

## Stale digest
OpenTofu stores a digest of the state in DynamoDB for consistency checks. After you
move to S3-only locking, that digest goes stale. If you return to DynamoDB locking, the
old digest has to be cleaned up manually. S3 lockfiles have no digest item.

## Workspaces
Non-default workspaces are stored at `<workspace_key_prefix>/<workspace>/<key>`; the
default prefix is `env:`.

## Verify
- [ ] While a run holds the lock, the `<key>.tflock` object exists in the bucket.
- [ ] After cut-over, no runner still sets `dynamodb_table`.

## Checked
2026-10-31. Confirmed against the Terraform S3 backend page (`use_lockfile` default
false, DynamoDB locking deprecated and both settable together, `LockID` String
partition key, IAM actions, `.tflock`, `workspace_key_prefix` default `env:`), the
OpenTofu S3 backend page (no plans to deprecate either, order of lock acquisition,
`-md5` digest and stale-digest note) and the AWS conditional-writes page
(`If-None-Match`). Removed: Terraform/OpenTofu version numbers for lockfile support,
the lock-table HCL, billing mode, the quoted checksum error text and its fix, and the
bucket-policy and Object Lock gotchas, none of which the pages confirm.
Method: documentation only; no commands were run.
