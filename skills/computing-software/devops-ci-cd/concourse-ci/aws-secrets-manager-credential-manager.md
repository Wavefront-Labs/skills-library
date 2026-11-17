---
id: computing-software.devops-ci-cd.concourse-ci.aws-secrets-manager-credential-manager
name: aws-secrets-manager-credential-manager
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [aws, secrets-manager, credential-manager, iam, health-check, rate-limits, scaling]
level: practitioner
status: docs-checked
description: "Configure AWS Secrets Manager credentials: IAM policy with the __concourse-health-check secret, plaintext storage, and watching for rate limiting via /api/v1/info/creds."
sources:
  - https://concourse-ci.org/docs/operation/creds/aws-secrets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Env vars on the web node: `CONCOURSE_AWS_SECRETSMANAGER_REGION`, `..._ACCESS_KEY`, `..._SECRET_KEY`, and optionally `..._SESSION_TOKEN`. With an instance IAM role only the region is needed.

**IAM policy.** `secretsmanager:ListSecrets` on `*`; `secretsmanager:GetSecretValue` and `secretsmanager:DescribeSecret` on `arn:aws:secretsmanager:*:*:secret:/concourse/*` and on `arn:aws:secretsmanager:*:*:secret:__concourse-health-check-??????`. The health check secret is required for the health check to work. For a single pipeline, narrow the first resource to `/concourse/TEAM_NAME/*` and `/concourse/TEAM_NAME/PIPELINE_NAME/*`.

**Lookup** matches the SSM manager: pipeline path then team path, both under `/concourse`. Customise with `CONCOURSE_AWS_SECRETSMANAGER_TEAM_SECRET_TEMPLATE`, `..._PIPELINE_SECRET_TEMPLATE` and `..._SHARED_SECRET_TEMPLATE`.

**Storing secrets.** Use the "other type of secret" option with the plaintext entry; otherwise secrets are interpolated as JSON. Secret names must match the lookup templates exactly, including the leading `/`.

**Scaling.** A cluster with many resources can generate heavy traffic and be rate-limited by AWS. With permission to read `__concourse-health-check`, you can measure the error rate by polling `/api/v1/info/creds` as a Concourse admin. To mitigate, use credential caching and retries.

## Checked

2026-11-04. Env vars, IAM policy, storage advice and scaling note confirmed on the AWS Secrets Manager credential manager page.

Method: documentation only; no commands were run.
