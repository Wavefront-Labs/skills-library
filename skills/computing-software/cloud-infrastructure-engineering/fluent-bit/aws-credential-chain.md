---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.aws-credential-chain
name: aws-credential-chain
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, aws, credentials, role-arn, irsa, imds, iam]
level: practitioner
status: docs-checked
description: "Understand the order Fluent Bit AWS plugins use to find credentials and how role_arn assumes a role."
sources: ["https://docs.fluentbit.io/manual/administration/aws-credentials"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AWS credential chain

Plugins that talk to AWS fetch credentials from these providers in order. Only the first provider that supplies credentials is used.

1. **Environment variables**: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, optionally `AWS_SESSION_TOKEN`.
2. **Shared config and credentials files**: `$AWS_CONFIG_FILE` or `$HOME/.aws/config`, and `$AWS_SHARED_CREDENTIALS_FILE` or `$HOME/.aws/credentials`, for the profile in `$AWS_PROFILE` or `$AWS_DEFAULT_PROFILE`, else `default`. Only `credential_process` (config file, Linux only) and `aws_access_key_id`, `aws_secret_access_key`, `aws_session_token` (credentials file) are supported.
3. **EKS web identity token (OIDC)**: a signed token for a Kubernetes service account.
4. **ECS HTTP credentials endpoint**: the ECS task role.
5. **EC2 instance profile (IMDS)**: the instance profile role.
6. **AWS Greengrass**: a localhost token exchange endpoint, read through `AWS_CONTAINER_CREDENTIALS_FULL_URI`.

EKS Pod Identity credentials are also supported, fetched from a pod identity endpoint.

All AWS plugins additionally take `role_arn` (Elasticsearch uses `AWS_ROLE_ARN`). If set, the fetched credentials are used to assume that role.

```yaml
pipeline:
  outputs:
    - name: s3
      match: '*'
      bucket: my-bucket
      region: us-east-1
      role_arn: arn:aws:iam::<ACCOUNT_ID>:role/fluent-bit
```

Only the first provider that supplies credentials is used, so access keys in the environment are used before any role-based provider. For the EC2 instance profile, IMDSv2 is used by default from Fluent Bit 1.8.8; earlier versions require IMDSv1 enabled on EC2.

## Checked

2026-11-03. Confirmed on the Fluent Bit AWS credentials page: provider order, environment variables, shared file locations and supported settings, EKS web identity, ECS, Pod Identity, IMDS and IMDSv2, Greengrass, role_arn and AWS_ROLE_ARN. Removed: an unsourced troubleshooting claim; the example account ID is now a placeholder.

Method: documentation only; no commands were run.
