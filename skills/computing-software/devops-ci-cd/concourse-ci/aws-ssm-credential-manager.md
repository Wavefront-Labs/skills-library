---
id: computing-software.devops-ci-cd.concourse-ci.aws-ssm-credential-manager
name: aws-ssm-credential-manager
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [aws, ssm, parameter-store, credential-manager, iam, kms, session-token, instance-profile]
level: practitioner
status: docs-checked
description: "Configure AWS SSM Parameter Store as the credential manager: region and keys, session token, instance profile, the IAM and KMS permissions needed, lookup paths and templates."
sources:
  - https://concourse-ci.org/docs/operation/creds/aws-ssm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable on the web node with `CONCOURSE_AWS_SSM_REGION`, `CONCOURSE_AWS_SSM_ACCESS_KEY` and `CONCOURSE_AWS_SSM_SECRET_KEY`. For short-lived credentials add `CONCOURSE_AWS_SSM_SESSION_TOKEN`. If the web node has an IAM role (instance profile), credentials come from the EC2 metadata service and only the region is needed.

**IAM permissions** (the page gives JSON and Terraform/OpenTofu forms). Three statements: `kms:ListAliases` and `kms:ListKeys` on `*`; `ssm:GetParameter` and `ssm:GetParametersByPath` on `arn:aws:ssm:::parameter/concourse/*`; and `kms:Decrypt` and `kms:DescribeKey` on the KMS key. To restrict to a pipeline, replace the parameter resource with `parameter/concourse/TEAM_NAME/*` and `parameter/concourse/TEAM_NAME/PIPELINE_NAME/*`.

**Lookup.** `((foo_param))` is tried at `/concourse/TEAM_NAME/PIPELINE_NAME/foo_param` and then `/concourse/TEAM_NAME/foo_param`. One-off tasks only use the team path.

Customise with:
- `CONCOURSE_AWS_SSM_SHARED_PATH` for credentials common to all teams
- `CONCOURSE_AWS_SSM_TEAM_SECRET_TEMPLATE` (default `/concourse/{{.Team}}/{{.Secret}}`)
- `CONCOURSE_AWS_SSM_PIPELINE_SECRET_TEMPLATE` (default `/concourse/{{.Team}}/{{.Pipeline}}/{{.Secret}}`)

With templates `/{{.Team}}/concourse/{{.Secret}}`, `/{{.Team}}/concourse/{{.Pipeline}}/{{.Secret}}` and shared path `/common/{{.Secret}}`, `((password))` for `myteam`/`mypipeline` resolves `/myteam/concourse/mypipeline/password`, then `/myteam/concourse/password`, then `/common/password`.

## Checked

2026-11-04. Env vars, IAM statements and lookup order confirmed on the AWS SSM credential manager page.

Method: documentation only; no commands were run.
