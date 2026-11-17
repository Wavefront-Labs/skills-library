---
id: computing-software.cloud-infrastructure-engineering.terraform.ssm-parameter-store-securestring
name: ssm-parameter-store-securestring
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, ssm-securestring, ssm-parameter-lookup, aws-provider, secrets-management, write-only]
level: practitioner
status: docs-checked
description: "Manage and read SSM Parameter Store SecureString values with Terraform without leaking them: value_wo and value_wo_version, ephemeral reads, key_id and state exposure."
sources: ["https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/r/ssm_parameter.html.markdown", "https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/ephemeral-resources/ssm_parameter.html.markdown", "https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSM Parameter Store SecureString

## Creating without the value in state
```hcl
resource "aws_ssm_parameter" "db_password" {
  name             = "/payments/prod/db_password"
  type             = "SecureString"
  key_id           = aws_kms_key.app.arn
  value_wo         = ephemeral.random_password.db.result
  value_wo_version = 1                 # change to trigger an update of value_wo
}
```
From the `aws_ssm_parameter` resource page:
- Exactly one of `value`, `value_wo` or `insecure_value` is required. Write-only values are never stored in state;
  `value_wo` requires `value_wo_version`, and changing that number triggers an update.
- Write-only arguments need Terraform 1.11.0 or later.
- `key_id` is the KMS key ID or ARN used to encrypt a SecureString.
- `type` is `String`, `StringList` or `SecureString`.
- The page warns that the unencrypted value of a SecureString set with `value` is stored in the raw state as plain
  text (`value` is always marked sensitive in plan output; `insecure_value` never is).
- `overwrite` defaults to false on create and true on later operations once Terraform manages the resource.
- `tier` is `Standard`, `Advanced` or `Intelligent-Tiering` (region default if unset); downgrading Advanced to
  Standard recreates the resource.

## Reading
The `aws_ssm_parameter` ephemeral resource retrieves a parameter including its value without writing it to state.
It takes `arn` (required), optional `region` and `with_decryption` (default true), and exports `name`, `type`,
`value`, `version` and `with_decryption`. The page flags ephemeral resources as a new feature that may evolve.
For metadata only, use the `aws_ssm_parameter` data source.

## Checked
2026-11-01. Confirmed on the provider's resource and ephemeral-resource documentation (source markdown in
hashicorp/terraform-provider-aws). Removed: placeholder-with-ignore_changes pattern, ephemeral version minimums,
KMS cross-account claims, size limits, overwrite deprecation (the page does not deprecate it), history advice.
Method: documentation only; no commands were run.
