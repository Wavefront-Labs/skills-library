---
id: computing-software.cloud-infrastructure-engineering.terraform.github-actions-oidc-to-aws
name: github-actions-oidc-to-aws
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, github-oidc-aws, aws-oidc, oidc, github-actions, assume-role]
level: practitioner
status: docs-checked
description: "Give GitHub Actions short-lived AWS credentials for Terraform via OIDC: IAM OIDC provider, trust policy scoped by sub claim, and separate plan and apply roles."
sources: ["https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services", "https://github.com/aws-actions/configure-aws-credentials", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/r/iam_openid_connect_provider.html.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitHub Actions OIDC to AWS

## AWS side (Terraform, in a bootstrap stack)
```hcl
resource "aws_iam_openid_connect_provider" "github" {
  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
}
data "aws_iam_policy_document" "plan_trust" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }
    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:corp/payments-infra:ref:refs/heads/*"]   # add the sub your PR jobs emit (inspect a token)
    }
  }
}
resource "aws_iam_role" "tf_plan" {
  name               = "gha-payments-plan"
  assume_role_policy = data.aws_iam_policy_document.plan_trust.json
}
```
Apply role: same, but `sub` = `repo:corp/payments-infra:environment:prod` so only jobs
in the `prod` environment can assume it; add protection rules to that environment. A
thumbprint is no longer necessary; if one is specified it is ignored.

## Workflow
```yaml
permissions:
  id-token: write        # required for OIDC
  contents: read
jobs:
  apply:
    environment: prod
    steps:
      - uses: actions/checkout@v6
      - uses: aws-actions/configure-aws-credentials@v6
        with:
          role-to-assume: arn:aws:iam::<ACCOUNT_ID>:role/gha-payments-apply
          aws-region: eu-west-1
      # install Terraform with your preferred method here
      - run: terraform init -input=false && terraform apply -input=false -auto-approve tfplan
```
By default the action exports `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and
`AWS_SESSION_TOKEN` as environment variables (`output-env-credentials`).

## Gotchas
- The `sub` claim depends on the workflow: branch runs look like
  `repo:ORG/REPO:ref:refs/heads/BRANCH`, and a job that uses an environment must be matched
  with `repo:ORG/REPO:environment:NAME`. Inspect a real token to see what your jobs emit.
- Repositories created on or after 15 July 2026 (and older ones that opted in or were
  renamed) emit an immutable `sub` with numeric IDs, `repo:ORG@ORG_ID/REPO@REPO_ID:...`. A
  trust policy in the legacy name-only form then fails with `Not authorized to perform
  sts:AssumeRoleWithWebIdentity`; the examples above use the legacy form.
- Never use `StringLike` with `repo:corp/*` on an apply role. Avoid `ForAllValues:` operators
  in Allow statements: they pass when the claim is absent or misspelled.
- The assumed-role session defaults to 1 hour; `role-duration-seconds` accepts 900 to 43200 seconds.

## Verify
- [ ] No long-lived AWS keys in repository secrets.
- [ ] A PR job cannot assume the apply role (AccessDenied in a test).

## Checked
2026-10-28. Confirmed against GitHub's "Configuring OpenID Connect in Amazon Web Services" page, the aws-actions/configure-aws-credentials README and the `aws_iam_openid_connect_provider` doc: issuer URL and `sts.amazonaws.com` audience, `sts:AssumeRoleWithWebIdentity` with a Federated principal, `aud` and `sub` condition keys, environment sub form, `id-token: write`, thumbprint ignored, `output-env-credentials` variables, `role-duration-seconds` default and range, `ForAllValues:` warning, immutable sub claim for repositories created from 15 July 2026, `client_id_list` and `url` arguments.
Corrected: action version (`@v4` in the skill; the README uses `@v6`), the claim that a thumbprint is validated through a trust store, the placeholder account ID.
Removed: the `pull_request` and tag `sub` forms, the setup-terraform step, "provider and S3 backend pick up the credentials", and the max-session-duration claim (not in the fetched pages).
Method: documentation only; no commands were run.
