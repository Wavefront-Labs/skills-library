---
id: computing-software.devops-ci-cd.gitlab-ci.gitlab-oidc-to-aws
name: gitlab-oidc-to-aws
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, gitlab-oidc-aws, assume-role-web-identity-gitlab, aws-iam-oidc-provider, id-tokens-aws]
level: advanced
status: docs-checked
description: "Authenticate GitLab CI jobs to AWS without stored keys: IAM OIDC provider for GitLab, role trust on sub/aud claims, id_tokens, and assume-role-with-web-identity."
sources: ["https://docs.gitlab.com/ci/cloud_services/aws/", "https://docs.gitlab.com/ci/secrets/id_token_authentication/", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/cloud_services/aws/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitLab ID tokens to AWS

## 1. AWS side
Create GitLab as an IAM OIDC identity provider in AWS:
- **Provider URL**: your GitLab address, for example `https://gitlab.com`; it must be publicly accessible (a workaround for a non-public instance exists in the GitLab docs, with security warnings).
- **Audience**: the logical name of the service the token is for. The GitLab docs say this typically matches the audience in your IAM provider, often `sts.amazonaws.com` or the GitLab URL, and call the GitLab URL "semantically misleading" because the audience should name the service that accepts the token. Whatever you choose must equal the job's `id_tokens` `aud`.

Create a web identity role with a custom trust policy. Example from the docs (GitLab.com), pinning group, project and branch:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Federated": "arn:aws:iam::AWS_ACCOUNT:oidc-provider/gitlab.com" },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "gitlab.com:sub": "project_path:mygroup/myproject:ref_type:branch:ref:main",
        "gitlab.com:namespace_id": "12345",
        "gitlab.com:project_id": "67890"
      }
    }
  }]
}
```
Condition keys: `sub` and `aud` work everywhere. On GitLab.com AWS also supports `namespace_id`, `project_id`, `user_id`, `user_login`, `user_email`, `user_access_level`, `ref_protected`, `pipeline_source` and `runner_environment`; on GitLab Self-Managed and Dedicated only `sub` and `aud`. `project_id` is stable across renames and transfers, so combine it with `sub`; do not rely on `user_login` or `user_email` alone because users can change them. The default `sub` is `project_path:{group}/{project}:ref_type:{type}:ref:{branch_name}`.
Using `StringEquals` with a wildcard value is a documented cause of authorisation errors: use `StringLike` when a condition contains `*`.

## 2. Job (from the docs)
```yaml
assume role:
  id_tokens:
    GITLAB_OIDC_TOKEN:
      aud: https://gitlab.example.com     # must match the audience configured in AWS
  script:
    - >
      aws_sts_output=$(aws sts assume-role-with-web-identity
      --role-arn ${ROLE_ARN}
      --role-session-name "GitLabRunner-${CI_PROJECT_ID}-${CI_PIPELINE_ID}"
      --web-identity-token ${GITLAB_OIDC_TOKEN}
      --duration-seconds 3600
      --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]'
      --output text)
    - export $(printf "AWS_ACCESS_KEY_ID=%s AWS_SECRET_ACCESS_KEY=%s AWS_SESSION_TOKEN=%s" $aws_sts_output)
    - aws sts get-caller-identity
```
`ROLE_ARN` is the role from step 1. Attach a permissions policy to the role for the AWS services the job needs.

## 3. Errors
- `Not authorized to perform sts:AssumeRoleWithWebIdentity`: project not configured for OIDC, role restricted from this branch or tag, or `StringEquals` used with a wildcard.
- `Could not connect to openid configuration of provider`: the issuer's certificate chain is out of order or has duplicate or extra certificates; the chain must run domain, intermediate, root.
- `Couldn't retrieve verification key from your identity provider`: the `.well-known` URL and `jwks_uri` are not reachable from the public internet, a firewall blocks them, API latency exceeds 5 seconds, or STS makes too many requests to them.

## Verify
- [ ] `aws sts get-caller-identity` shows the assumed role on the allowed branch; a pipeline on another branch is denied.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/cloud_services/aws/_index.md and doc/ci/secrets/id_token_authentication.md: IAM OIDC provider fields (provider URL, audience, with the docs' note that `sts.amazonaws.com` is the semantically correct audience), the `gitlab.com` condition keys (`sub`, `aud`, `namespace_id`, `project_id`, `user_id`, `user_login`, `user_email`, `user_access_level`, `ref_protected`, `pipeline_source`, `runner_environment`) available only on GitLab.com, `sub` and `aud` only for Self-Managed and Dedicated, the default `sub` format, the `assume-role-with-web-identity` job from the docs, and the three troubleshooting causes. Removed the SDK web-identity token file shortcut, the jq credential parsing, the `InvalidIdentityToken` provider-URL explanation, token-claim advice not in the docs, and the placeholder account and region values.

Method: documentation only; no commands were run.
