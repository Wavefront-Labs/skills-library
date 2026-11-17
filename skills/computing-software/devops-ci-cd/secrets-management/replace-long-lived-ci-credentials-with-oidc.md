---
id: computing-software.devops-ci-cd.secrets-management.replace-long-lived-ci-credentials-with-oidc
name: replace-long-lived-ci-credentials-with-oidc
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, long-lived-credentials, oidc-federation, workload-identity, assume-role-with-web-identity, credential-rotation, ci-secrets]
level: practitioner
status: gated
description: "Migrate CI pipelines off long-lived cloud keys to OIDC workload identity: inventory static secrets, configure AWS, Azure and GCP trust, scope subject claims, and revoke old keys."
sources:
  - https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect
  - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html
  - https://cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines
  - https://docs.gitlab.com/ee/ci/cloud_services/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Replacing long-lived CI credentials with OIDC

Static access keys in CI secrets get copied into logs, forks, laptops and third-party actions, and rarely rotate. OIDC federation gives each job a short-lived token (minutes to an hour) bound to repo, branch and environment.

## 1. Inventory
```bash
gh secret list --org ORG; for r in $(gh repo list ORG --json name -q '.[].name'); do gh secret list -R ORG/$r; done
aws iam list-access-keys --user-name ci-deployer; aws iam get-access-key-last-used --access-key-id AKIA...
```
Map each secret to: which pipelines use it, which cloud principal, what permissions, last used.

## 2. Create trust (per cloud)
Cloud-side resources below were not created here (gated: unconfirmed, no AWS/GCP/Azure account); the GitHub and GitLab claim formats were read from their docs.
**GitHub subject format changed:** repositories created after 2026-07-15 (and renamed or transferred ones, or those that opt in) use immutable subjects
`repo:OWNER@OWNER-ID/REPO@REPO-ID:environment:production`; older repositories keep `repo:org/app:environment:production`. Match whichever your repository emits
(GitHub docs, "Immutable subject claims"; not available on GHES). The AWS example below uses the older form.
**AWS**
```json
{"Effect":"Allow","Principal":{"Federated":"arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"},
 "Action":"sts:AssumeRoleWithWebIdentity",
 "Condition":{"StringEquals":{"token.actions.githubusercontent.com:aud":"sts.amazonaws.com",
   "token.actions.githubusercontent.com:sub":"repo:org/app:environment:production"}}}
```
**GCP**: workload identity pool + provider with `attribute.repository` mapping and `--attribute-condition="assertion.repository_owner=='org'"`, then grant `roles/iam.workloadIdentityUser` on the service account to `principalSet://.../attribute.repository/org/app`.
**Azure**: app registration or user-assigned managed identity > Federated credentials, subject `repo:org/app:environment:production`.
GitLab: `id_tokens: { AWS_TOKEN: { aud: sts.amazonaws.com } }` and subject `project_path:group/app:ref_type:branch:ref:main`.

## 3. Scope the subject tightly
- Prefer `environment:<name>` subjects and protect that environment (required reviewers, branch restrictions).
- Never `repo:org/*` or a `StringLike` with `*` on sub for deploy roles; pull requests from forks get their own subject (`pull_request`) - don't trust it for writes.
- Separate roles for plan (read-only) and apply (write).

## 4. Switch pipelines
```yaml
permissions: { id-token: write, contents: read }
steps:
  - uses: aws-actions/configure-aws-credentials@v6
    with: { role-to-assume: arn:aws:iam::123456789012:role/gh-deploy-prod, aws-region: eu-west-2 }
```
Run both paths briefly if needed, then delete the secret from CI.

## 5. Revoke and prevent regression
- Deactivate, wait, then delete old keys (`aws iam update-access-key --status Inactive`); watch CloudTrail for use by forgotten jobs.
- SCP/organization policy denying `iam:CreateAccessKey` for CI users; GCP org policy `iam.disableServiceAccountKeyCreation`.
- Secret scanning for cloud keys in repos.

## Where OIDC doesn't reach
Third-party SaaS without federation: store in a vault with short TTLs (Vault dynamic secrets, cloud secret manager) fetched via OIDC, and rotate on a schedule.

## Verify
- [ ] No cloud access keys remain in CI secret stores; old IAM users have no active keys.
- [ ] A workflow from another branch or fork fails to assume the production role.
