---
id: computing-software.cloud-infrastructure-engineering.terraform.oss-and-cos-state-backends
name: oss-and-cos-state-backends
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, oss-backend, cos-backend, alibaba-cloud, tencent-cloud, remote-state]
level: practitioner
status: docs-checked
description: "Configure the oss (Alibaba Cloud OSS + Tablestore locking) and cos (Tencent Cloud COS) state backends: arguments, locking, auth and workspace key layout."
sources: ["https://developer.hashicorp.com/terraform/language/backend/oss", "https://developer.hashicorp.com/terraform/language/backend/cos"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `oss` and `cos` backends

## Alibaba Cloud OSS
```hcl
terraform {
  backend "oss" {
    bucket              = "corp-tfstate"
    prefix              = "network/prod"          # path prefix inside bucket
    key                 = "terraform.tfstate"
    region              = "cn-hangzhou"
    encrypt             = true                    # server-side encryption
    acl                 = "private"
    tablestore_endpoint = "https://tf-lock.cn-hangzhou.ots.aliyuncs.com"
    tablestore_table    = "terraform_lock"        # enables locking
  }
}
```
- Locking is enabled by setting `tablestore_table` to an existing Tablestore table whose
  primary key is named `LockID` with type String. `tablestore_endpoint` (and
  `tablestore_instance_name` for VPC endpoints) locate the instance.
- Auth: `access_key`/`secret_key` (environment variables `ALICLOUD_ACCESS_KEY` and
  `ALICLOUD_SECRET_KEY`, or the recommended `ALIBABA_CLOUD_ACCESS_KEY_ID` and
  `ALIBABA_CLOUD_ACCESS_KEY_SECRET`), `security_token`, `profile` + `shared_credentials_file`,
  `assume_role_role_arn` / `assume_role_session_name` (the nested `assume_role` block is
  deprecated since 1.1.0), or an ECS RAM role (`ecs_role_name`).
- `prefix` defaults to `env:` and `key` to `terraform.tfstate`. The docs do not spell out the
  object layout for non-default workspaces; check the bucket after `terraform workspace new`.

## Tencent Cloud COS
```hcl
terraform {
  backend "cos" {
    region  = "ap-guangzhou"
    bucket  = "tfstate-1250000000"     # bucket name includes the APPID suffix
    prefix  = "terraform/state"
    key     = "terraform.tfstate"
    encrypt = true
    acl     = "private"
  }
}
```
- Locking is supported with no extra table. It needs permission to create, delete and
  describe tags on the tag key `tencentcloud-terraform-lock`, plus put, get and delete on
  the bucket prefix.
- Auth: `secret_id`/`secret_key` (`TENCENTCLOUD_SECRET_ID` / `TENCENTCLOUD_SECRET_KEY`),
  `security_token`, an `assume_role` block (`role_arn`, `session_name`, `session_duration`),
  shared credentials (`shared_credentials_dir`, `profile`), or `cam_role_name` for a CVM
  CAM role.
- Create the bucket first; the docs' example bucket name ends with the Tencent APPID
  (`bucket-for-terraform-state-1258798060`).

## Shared practices
- Enable bucket versioning for state recovery (the COS page highly recommends object
  versioning); restrict bucket access to the CI role.
- Put credentials in env vars or `-backend-config` files, not in the backend block.
- Migrating in/out: `terraform init -migrate-state` after editing the backend block.

## Verify
- [ ] Two concurrent `terraform plan` runs: the second reports a lock error.
- [ ] State object visible at the expected prefix/key; versioning on.

## Checked
2026-10-28. Confirmed against the Terraform oss and cos backend pages: arguments and defaults (`prefix` default `env:`, `key`), Tablestore locking and the `LockID` String key, auth options and environment variables, the 1.1.0 deprecation of the nested OSS `assume_role` block, COS tag-based locking permissions, COS auth options, APPID-suffixed example bucket names, versioning recommendation, credentials-in-plan-files warning, `-migrate-state` (listed in the v1.x compatibility promises).
Corrected: COS locking (it uses tags on `tencentcloud-terraform-lock`, not a lock object); OSS assume-role argument names.
Removed: the `<prefix>/env:/<workspace>/<key>` layout and the `NoSuchBucket` error text (not in the fetched pages).
Method: documentation only; no commands were run.
