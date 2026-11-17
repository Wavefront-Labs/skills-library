---
id: computing-software.cloud-infrastructure-engineering.aws.github-actions-oidc-federation-to-aws
name: github-actions-oidc-federation-to-aws
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iam, sts, assume-role-with-web-identity, github-actions-oidc, oidc-provider, ci-cd, keyless]
level: practitioner
status: docs-checked
description: "Replace CI access keys with OIDC federation: IAM OIDC provider for GitHub Actions, trust policy sub/aud conditions per repo, branch and environment, and the workflow config."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html", "https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services", "https://github.com/aws-actions/configure-aws-credentials"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitHub Actions OIDC federation to AWS

**Goal:** no long-lived `AWS_ACCESS_KEY_ID` secrets in CI. Each workflow run gets short-lived
credentials via `AssumeRoleWithWebIdentity`, scoped to a repo/branch/environment.

## 1. OIDC provider (once per account)
```bash
aws iam create-open-id-connect-provider --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com
```
Per the IAM guide, AWS verifies the provider's JWKS endpoint TLS certificate against its library of trusted root CAs, and uses the thumbprints configured on the IdP only as a fallback (certificate not signed by a trusted CA, certificate cannot be retrieved, or TLS 1.3 is required). A provider must have at least one and at most five thumbprints. When you create a provider in the console, IAM retrieves the top intermediate CA thumbprint for you.

## 2. Role trust policy: the security-critical part
```json
{"Version": "2012-10-17", "Statement": [{
  "Effect": "Allow",
  "Principal": {"Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"},
  "Action": "sts:AssumeRoleWithWebIdentity",
  "Condition": {
    "StringEquals": {"token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
                     "token.actions.githubusercontent.com:sub": "repo:ORG-NAME/REPO-NAME:environment:ENVIRONMENT-NAME"}}}]}
```
GitHub's AWS guide shows `sub` values `repo:ORG/REPO:ref:refs/heads/BRANCH` (branch) and
`repo:ORG/REPO:environment:ENVIRONMENT-NAME`; for a workflow that uses an environment, `sub` must reference the environment name. Its examples use `StringEquals` for an exact match and a `repo:ORG/REPO:*` wildcard (with `StringLike`) to allow any ref in one repository. Pin `sub` to the narrowest value that works: a broad wildcard lets every workflow in that scope assume the role. Combine `environment:` with GitHub environment protection rules for production.

## 3. Workflow
```yaml
permissions:
  id-token: write
  contents: read
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v6.3.0   # version shown in the action README; pin the one you review
        with:
          role-to-assume: arn:aws:iam::<ACCOUNT_ID>:role/gha-deploy-my-service
          aws-region: eu-west-1
          role-session-name: gha-${{ github.run_id }}
      - run: aws sts get-caller-identity
```
- `id-token: write` lets the job request the OIDC token (GitHub: it does not grant write access to any resource). Without it the action cannot fetch a token.
- `aws-region` is always required; `role-session-name` defaults to `GitHubActions`.
- `role-duration-seconds` (action input) defaults to 1 hour (3600) and accepts 900 to 43200 seconds; the role's own maximum session duration also applies.

## Gotchas
- `Not authorized to perform sts:AssumeRoleWithWebIdentity`: compare the token's `sub` and `aud` with the trust policy exactly.
- AWS suggests reviewing CloudTrail `AssumeRoleWithWebIdentity` events when investigating a provider problem.

## Verify
- [ ] A run on the allowed branch or environment assumes the role; the same workflow from another ref is denied.
- [ ] No AWS access keys remain in repo/org secrets (`aws iam list-access-keys` for any CI users, then delete the users).

## Checked
Confirmed on the IAM guide page (thumbprint behaviour and limits, CloudTrail note), the GitHub Docs AWS OIDC page (sub formats, environment rule, `id-token: write`, StringEquals/StringLike examples) and the configure-aws-credentials README (inputs, defaults, current version). CLI commands checked against the botocore model.
Removed: the `repo:ORG/REPO:pull_request` sub format, the GitLab/Bitbucket/CircleCI/Terraform Cloud/IRSA section, and claims about fork PRs, which are not on the cited pages.
Method: docs-only read of cited pages, 2026-11-08
