---
id: computing-software.cloud-infrastructure-engineering.terraform.bootstrap-root-modules-for-state-and-ci-identity
name: bootstrap-root-modules-for-state-and-ci-identity
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, bootstrap-root, state-bucket, chicken-and-egg, oidc-role, backend-migration, local-state]
level: practitioner
status: docs-checked
description: "Bootstrap the resources Terraform itself needs: state bucket and lock table, CI OIDC identity and roles, created by a small bootstrap root with local state then migrated."
sources:
  - https://developer.hashicorp.com/terraform/language/backend/s3
  - https://developer.hashicorp.com/terraform/cli/commands/init#backend-initialization
  - https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Bootstrap root modules for state and CI identity

Terraform needs a state backend and a CI identity before it can manage anything else. Something has to create them - a small **bootstrap** root module, run rarely, by a human with admin rights.

## What goes in bootstrap
- State storage: S3 bucket or Azure storage account/container or GCS bucket. For S3 the backend page strongly recommends enabling Bucket Versioning for state recovery after accidental deletion or human error; encryption and a public access block are sensible additions (design guidance).
- Locking: `use_lockfile = true` on the S3 backend (defaults to false; needs `s3:GetObject`, `s3:PutObject` and `s3:DeleteObject` on the `.tflock` object). DynamoDB locking (`dynamodb_table`) is deprecated and will be removed in a future minor version, so do not build a new table.
- CI identity: OIDC provider (`https://token.actions.githubusercontent.com`, audience `sts.amazonaws.com` with the official action) and deploy roles whose trust policy checks the `token.actions.githubusercontent.com:sub` condition key, scoped to repo or environment (`repo:ORG/REPO:environment:NAME`); separate plan (read-only) and apply roles. Workflows need `id-token: write`.
- Optionally KMS key for state encryption and an audit trail on the bucket.
Keep it minimal; everything else belongs in normal roots run by CI.

## Two-step pattern
```hcl
# bootstrap/main.tf
resource "aws_s3_bucket" "state" { bucket = "acme-tfstate-${var.account_name}" }
resource "aws_s3_bucket_versioning" "state" {
  bucket = aws_s3_bucket.state.id
  versioning_configuration { status = "Enabled" }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "state" {
  bucket = aws_s3_bucket.state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}
resource "aws_s3_bucket_public_access_block" "state" {
  bucket = aws_s3_bucket.state.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}
resource "aws_iam_openid_connect_provider" "github" {
  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
}
```
1. Apply with **local state** (no backend block): `terraform init && terraform apply`.
2. Add a backend block pointing at the bucket it just created, then migrate:
```hcl
terraform {
  backend "s3" {
    bucket = "acme-tfstate-prod"
    key = "bootstrap/terraform.tfstate"
    region = "eu-west-2"
    use_lockfile = true
  }
}
```
```bash
terraform init -migrate-state      # attempts to copy existing state to the new backend (may prompt)
rm terraform.tfstate terraform.tfstate.backup   # after confirming the remote copy
```
Now bootstrap manages its own bucket. Protect against accidental destruction: `lifecycle { prevent_destroy = true }` on the bucket and key.

## Multi-account
- Run bootstrap per account (a module called with different providers), or centralise state in a dedicated "terraform" account with cross-account roles.

## Operating
- Bootstrap changes are rare and high-impact: run manually with break-glass credentials, reviewed PR, two people.
- Document the recovery: if the bucket is lost, versioned state is lost too - enable replication or backups of the state bucket.
- Store bootstrap outputs (role ARNs, bucket names) where CI config reads them.

## Verify
- [ ] Bootstrap's own state is remote; `terraform plan` in bootstrap shows no changes.
- [ ] CI can assume the plan role from PRs and the apply role only from the protected environment (the GitHub page recommends protection rules on environments used in OIDC policies).

## Checked
2026-11-08. Confirmed against the Terraform S3 backend page (versioning warning, use_lockfile default and permissions, deprecated DynamoDB locking), the terraform init page (-migrate-state copies existing state and may prompt) and the GitHub OIDC-in-AWS page (provider URL, audience, sub condition, environment sub format, id-token: write). Removed: the Terraform 1.10+ version gate, the TLS-only policy item, and the Control Tower / AFT / landing zone claim (not on the cited pages). Resource-block examples are illustrative.
Method: documentation only; no commands were run.
