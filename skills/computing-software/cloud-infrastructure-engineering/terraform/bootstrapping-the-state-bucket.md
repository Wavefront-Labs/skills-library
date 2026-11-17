---
id: computing-software.cloud-infrastructure-engineering.terraform.bootstrapping-the-state-bucket
name: bootstrapping-the-state-bucket
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, state-bucket-bootstrap, backend-bootstrap, s3-backend, remote-state, migrate-state]
level: practitioner
status: docs-checked
description: "Solve the chicken-and-egg of creating the S3 state bucket with Terraform: create it with local state, add the s3 backend block, then run init to migrate state into it."
sources: ["https://developer.hashicorp.com/terraform/language/backend#initialization", "https://developer.hashicorp.com/terraform/cli/commands/init", "https://developer.hashicorp.com/terraform/language/backend/s3"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Bootstrapping the state bucket

The S3 backend page assumes the bucket already exists ("This assumes we have a bucket
created called mybucket"). So the bucket has to be created some other way first. One way
is to create it with Terraform using the default local backend, then switch that
configuration to the s3 backend and migrate its state into the bucket.

## Sequence
1. Write the bucket resource(s) in a configuration with **no** `backend` block. Terraform
   uses the `local` backend by default, which stores state as a local file.
2. Run `terraform init` and `terraform apply`.
3. Add a backend block pointing at the new bucket (`bucket` and `key` and `region` are
   required by the S3 backend; `key` is the path of the state object in the bucket):
```hcl
terraform {
  backend "s3" {
    bucket = "mybucket"
    key    = "path/to/my/key"
    region = "us-east-1"
  }
}
```
4. Run `terraform init` again. Changing backend configuration requires re-running init;
   Terraform detects the change and asks whether to migrate existing state to the new
   configuration. Answer yes to copy the local state into the bucket. Before migrating the
   backend docs "strongly recommend manually backing up your state" by copying
   `terraform.tfstate` elsewhere.

## Bucket settings the S3 backend page calls out
- The page warns that it is highly recommended to enable Bucket Versioning on the bucket
  so state can be recovered after accidental deletions and human error.
- Optional backend arguments: `encrypt` (server-side encryption of the state and lock
  files), `kms_key_id` (a KMS key ARN; Terraform then needs `kms:Encrypt`, `kms:Decrypt`
  and `kms:GenerateDataKey` on it), `acl`.
- Locking is opt-in: `use_lockfile` (default false) locks via S3. DynamoDB-based locking
  is deprecated; the page says it will be removed in a future minor version.
- Do not hard-code credentials in the backend block or pass them with `-backend-config`:
  they would be written to `.terraform` and to plan files. Use environment variables.
- Backend blocks cannot refer to variables, locals or data source attributes, and a
  configuration can have only one backend block.

## Checked
Date: 2026-11-07

Read in full (stripped text): "Backend block configuration overview" (initialization, change configuration, remove backend sections) and the S3 backend page up to the Assume Role section plus the `bucket`, `key`, `acl`, `encrypt` and `kms_key_id` argument lines; the AWS-assume-role and remaining optional argument sections were not read. The `terraform init` page was read earlier in this batch for `-migrate-state` (see the backend-to-backend skill). No code tabs present.

Trimmed as unconfirmed (the cited pages do not cover the AWS provider resources or other tools): the `aws_s3_bucket`, versioning, encryption and public-access-block resources, `prevent_destroy`, the `rm terraform.tfstate` step, the CloudFormation/Bicep/gcloud and HCP Terraform "Option B", the Terragrunt `remote_state` "Option C", bucket-naming, CI permission and "first apply has no lock" gotchas, and both Verify items. Description narrowed to S3.

Method: documentation only; no commands were run.
