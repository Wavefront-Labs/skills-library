---
id: computing-software.cloud-infrastructure-engineering.terraform.aws-provider-assume-role-profiles-and-env-credentials
name: aws-provider-assume-role-profiles-and-env-credentials
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, aws-assume-role, aws-profile, env-credentials, aws-credentials, sso, oidc, provider-authentication]
level: practitioner
status: docs-checked
description: "Authenticate the AWS provider: credential chain, env-var credentials, named profiles, assume_role (and with web identity), keeping secrets out of HCL."
sources: ["https://registry.terraform.io/providers/hashicorp/aws/latest/docs#authentication-and-configuration", "https://registry.terraform.io/providers/hashicorp/aws/latest/docs#assuming-an-iam-role", "https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS provider credentials

## Precedence (highest first)
1. Parameters in the provider configuration (`access_key`/`secret_key` — don't).
2. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`).
3. Shared credentials files.
4. Shared configuration files (select a named profile with `profile` or `AWS_PROFILE`).
5. Container credentials (ECS or CodeBuild task role).
6. Instance profile credentials (EC2 metadata service).
The provider docs say this order matches the AWS CLI and the AWS SDK for Go v2.
Web identity (`AWS_ROLE_ARN` + `AWS_WEB_IDENTITY_TOKEN_FILE`) is configured through
environment variables or a named profile; EKS IRSA sets those variables. An external
`credential_process` must be configured in a named profile. If you give `assume_role`,
the provider assumes that role using the credentials it found.

## Environment credentials (CI)
```bash
export AWS_REGION=eu-west-1
eval "$(aws configure export-credentials --profile ci --format env)"   # or from OIDC action
terraform plan
```
Keep secrets out of code; credentials supplied as environment variables are not written
into plan files by Terraform.

## Profiles (humans)
```hcl
provider "aws" {
  region  = "eu-west-1"
  profile = var.aws_profile          # null in CI, "acme-prod-admin" locally
}
```
The provider (and the S3 backend) also read `profile` from `AWS_PROFILE`; prefer the
environment variable over hard-coding `profile` so CI and humans share code.

## assume_role
```hcl
provider "aws" {
  region = "eu-west-1"
  assume_role {
    role_arn     = "arn:aws:iam::${var.account_id}:role/terraform-deployer"
    session_name = "terraform-${terraform.workspace}"
    duration     = "1h"    # 15 minutes up to the role's maximum session duration
  }
}
```
Variants: `assume_role_with_web_identity { role_arn, session_name, web_identity_token_file }`
(only one such block is allowed); role chaining by listing several `assume_role` blocks,
assumed in order; or put the role in a named profile.
Block values take precedence over `AWS_ROLE_ARN` / `AWS_WEB_IDENTITY_TOKEN_FILE`.

## Debugging
```bash
aws sts get-caller-identity                   # who the base chain resolves to
TF_LOG=DEBUG terraform plan 2>&1 | grep -i "credential\|assume"
```
Add `data "aws_caller_identity" "current" {}` and an output/precondition on
`account_id` to catch wrong-account runs.

## Gotchas
- Environment-variable keys rank above shared-file profiles in the precedence list, so
  exported keys can override `AWS_PROFILE`.
- `duration` must be between 15 minutes and the role's maximum session duration.
- S3 backend auth is configured separately (its own `profile`, `assume_role` and
  `assume_role_with_web_identity` arguments); with a workspace-specific `assume_role` in
  the provider, state operations still run as the backend's own credentials.

## Verify
- [ ] A precondition asserting `data.aws_caller_identity.current.account_id == var.account_id` passes.
- [ ] No `access_key` or `secret_key` appears in any `.tf` file.

## Checked
- 2026-10-28. Confirmed against the AWS provider documentation (authentication order, `assume_role`, `assume_role_with_web_identity`, role chaining, `duration` range, `session_name`, `credential_process` in a named profile, `AWS_ROLE_ARN` / `AWS_WEB_IDENTITY_TOKEN_FILE`, EKS IRSA and ECS task roles), the AWS CLI environment-variable page (`AWS_PROFILE`, `AWS_SESSION_TOKEN`, `AWS_ROLE_ARN`, `AWS_WEB_IDENTITY_TOKEN_FILE`) and the Terraform S3 backend page (own `profile`, `assume_role` and web identity arguments; backend operations use the backend's credentials).
- Removed: SSO and `aws sso login` claims, `source_profile`, the assume_role `tags` argument, the GitHub Action reference and the `ValidationError` name (not in the fetched docs).
Method: documentation only; no commands were run.
