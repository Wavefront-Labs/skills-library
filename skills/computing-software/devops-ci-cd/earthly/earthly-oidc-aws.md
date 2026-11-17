---
id: computing-software.devops-ci-cd.earthly.earthly-oidc-aws
name: earthly-oidc-aws
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, oidc, aws, iam, run-aws, run-with-aws-oidc, trust-policy, sts]
level: advanced
status: docs-checked
description: "Let Earthly builds assume an AWS IAM role through OIDC with RUN --aws --oidc: provider URL, audience, trust policy conditions and a sample Earthfile."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/cloud/oidc.md
  - https://github.com/earthly/earthly/blob/main/docs/earthfile/earthfile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OIDC authentication to AWS from Earthly builds

Goal: access AWS in a build without storing credentials locally or in CI. Only AWS is supported at the moment.

## Setup in AWS
1. Add an IAM OIDC provider: provider URL `https://api.earthly.dev`, audience `sts.amazonaws.com`.
2. Create (or reuse) an IAM role with limited permissions and a trust policy:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Federated": "<oidc-provider-name>" },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "api.earthly.dev:aud": "sts.amazonaws.com",
          "api.earthly.dev:sub": "<earthly-org>/<earthly-project>"
        }
      }
    }
  ]
}
```
`<oidc-provider-name>` is the provider ARN from step 1. The org/project pair comes from the Earthfile or build execution; the user needs read-secrets access in that project.

Alternative conditions:
- all members of the org: `"StringLike": { "api.earthly.dev:sub": "<earthly-org>/*" }`
- one user: `"StringEquals": { "api.earthly.dev:email": "<user-email>" }` (the email of the Earthly account)

## Use in an Earthfile
```Dockerfile
VERSION --run-with-aws --run-with-aws-oidc 0.8

PROJECT <your-org>/<your-project>

aws:
    FROM amazon/aws-cli
    LET OIDC="role-arn=arn:aws:iam::1234567890:role/your-oidc-role,session-name=my-session,region=us-east-1"
    RUN --aws --oidc=$OIDC aws s3 ls
```
The oidc-spec keys are `session-name` (RUN commands with the same name share one temporary token), `role-arn`, `region` (global endpoint if omitted) and `session-duration` (default and AWS minimum 15 minutes). `--oidc` requires `--aws` and is experimental.

## Checked

2026-11-07. Read docs/cloud/oidc.md in full, and the RUN --aws/--oidc section of earthfile.md (about lines 359-386) rather than the whole page. Provider URL, audience, trust policy, oidc-spec keys, session duration and region behaviour match. Corrected: added earthfile.md to sources because the oidc-spec key table lives there.
Method: documentation only; no commands were run.
