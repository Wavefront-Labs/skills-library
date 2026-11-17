---
id: computing-software.devops-ci-cd.github-actions.oidc-federation-for-cloud-auth
name: oidc-federation-for-cloud-auth
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, oidc, openid-connect, workload-identity-federation, id-token-write, keyless-auth, aws, iam-role, assume-role-with-web-identity, configure-aws-credentials, azure, federated-credential, azure-login, gcp, google-github-actions-auth, workload-identity-pool, sub-claim, trust-policy, environment-protection, token.actions.githubusercontent.com, short-lived-credentials, no-static-keys, vault-jwt]
level: advanced
status: docs-checked
description: "Replace stored cloud keys with GitHub Actions OIDC: id-token permission, AWS/Azure/GCP trust setup, scoping the sub claim to repo+environment, and debugging token claims."
sources: ["https://docs.github.com/en/actions/concepts/security/openid-connect", "https://docs.github.com/en/actions/reference/security/oidc","https://github.com/aws-actions/configure-aws-credentials", "https://github.com/google-github-actions/auth", "https://github.com/Azure/login"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OIDC federation for cloud auth

**Goal:** deploy jobs get short-lived cloud credentials minted per run, scoped to one repo
and one environment, with **no** cloud keys stored as GitHub secrets.

## 1. How it works (one paragraph)
With `permissions: id-token: write`, the job can request a signed JWT from
`https://token.actions.githubusercontent.com`. The cloud provider is configured to trust
that issuer and to accept only tokens whose claims (`sub`, `aud`, `repository`,
`environment`, `job_workflow_ref`…) match a policy. The login action swaps the JWT for
temporary credentials (the AWS action's `role-duration-seconds` defaults to 3600 s). Nothing long-lived exists to leak.

## 2. The workflow side
```yaml
permissions:
  id-token: write     # required to request the JWT
  contents: read      # set explicitly: declaring permissions drops all unlisted ones
jobs:
  deploy:
    environment: production          # puts "environment:production" into the sub claim
    runs-on: ubuntu-latest
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::<ACCOUNT_ID>:role/gha-deploy-prod
          aws-region: eu-west-1
      - run: aws sts get-caller-identity
```
Gotcha: setting `permissions:` at all resets unlisted scopes to `none` — forgetting
`contents: read` breaks `actions/checkout` in private repos.

## 3. Subject claim formats — the part people get wrong
Default `sub` shapes:
- `repo:<org>/<repo>:environment:<env>` — when the job declares `environment:`
- `repo:<org>/<repo>:ref:refs/heads/main` — branch push, no environment
- `repo:<org>/<repo>:pull_request` — PR events
- `repo:<org>/<repo>:ref:refs/tags/v1.2.3`

Repositories created on github.com on or after 15 July 2026 (and older ones that opt in or are
renamed) emit an immutable `sub` that appends numeric IDs: `repo:<org>@<ORG_ID>/<repo>@<REPO_ID>:ref:refs/heads/main`.
A trust policy written in the name-only form then fails with `Not authorized to perform
sts:AssumeRoleWithWebIdentity`; copy the exact `sub` from the run's token (per the
configure-aws-credentials README).

Trust **environment** subjects for deploys: environments can require reviewers and
restrict branches, so the cloud trust inherits those protections. Trusting
`repo:<org>/<repo>:*` lets any branch or PR workflow assume the role — the classic mistake.
Orgs can customise the `sub` template (see the OIDC reference page) to include `job_workflow_ref`,
so a trust policy can require a specific reusable workflow. Changing the `sub` format changes
every trust policy, so plan the migration.

## 4. Provider setup
**AWS** — IAM OIDC provider for `token.actions.githubusercontent.com`, audience
`sts.amazonaws.com`; role trust policy:
```json
{"Effect":"Allow","Principal":{"Federated":"arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"},
 "Action":"sts:AssumeRoleWithWebIdentity",
 "Condition":{"StringEquals":{
   "token.actions.githubusercontent.com:aud":"sts.amazonaws.com",
   "token.actions.githubusercontent.com:sub":"repo:<org>/<repo>:environment:production"}}}
```
Use `StringEquals` on `sub`; `StringLike` with `*` only when you mean it.

**Azure** — App registration or user-assigned managed identity → *Federated credentials*
→ GitHub Actions scenario with org/repo/entity (environment). Workflow:
`azure/login@v2` with `client-id`, `tenant-id`, `subscription-id` (IDs, not secrets).
Azure federated credential subjects are matched case-sensitively (per the Azure/login
troubleshooting section): use the exact casing from the run's `sub`, and expect one credential
per environment/branch.

**GCP** — Workload Identity Pool + OIDC provider with an `attribute-condition`
such as `assertion.repository_owner == '<org>'` (the google-github-actions/auth README says to
always add one to restrict entry into the pool), map `attribute.repository`, grant `roles/iam.workloadIdentityUser` on a service account
to `principalSet://.../attribute.repository/<org>/<repo>`; workflow:
`google-github-actions/auth@v2` with `workload_identity_provider` and `service_account`
(or direct WIF without a service account).

**Vault / others** — JWT auth method with `bound_claims` on `repository` and `environment`.

## 5. Debugging
- Inspect the claims of a real token (see "Inspecting the token" in the configure-aws-credentials README)
  only on a throwaway branch; the token is a live credential for its lifetime.
- `Not authorized to perform sts:AssumeRoleWithWebIdentity` usually means a `sub`/`aud` mismatch,
  including a name-only `sub` against an immutable one.
- Failure to obtain a token usually means the job lacks `id-token: write`.

## Uncertainty
Action major versions evolve; confirm current provider docs. Not executed against live clouds here.

## Verify
- [ ] No `AWS_SECRET_ACCESS_KEY` / service-account JSON / client secrets remain in repo or org secrets.
- [ ] Deploy roles trust only `...:environment:<env>` (or a pinned `job_workflow_ref`), never `repo:*`.
- [ ] A PR workflow attempting to assume the prod role fails.
- [ ] `aud` is pinned in the trust condition.
- [ ] Cloud audit logs show the session name/claims tied to the run (repo, run id).

## Checked
2026-10-31. Confirmed in the GitHub OIDC concepts page, aws-actions/configure-aws-credentials,
google-github-actions/auth and Azure/login READMEs: `id-token: write`, the `sub` shapes, 3600 s default AWS
duration, `repository_owner` attribute condition, case-sensitive Azure subjects, immutable `sub` format.
Removed: Azure wildcard/preview matching claim, GCP "required" wording, the curl token-decode command, the fork-PR
and error-string claims, the "9 times out of 10" figure.
Method: documentation only; no commands were run.
