---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.short-lived-credentials-vault-dynamic-secrets-and-oidc
name: short-lived-credentials-vault-dynamic-secrets-and-oidc
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, secrets-in-iac, dynamic-secrets, oidc-federation, secret-rotation]
level: advanced
status: docs-checked
description: "Replace static cloud keys in pipelines with GitHub Actions OIDC federation and HashiCorp Vault AWS dynamic secrets, including the Ansible hashi_vault collection."
sources: ["https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect", "https://developer.hashicorp.com/vault/docs/secrets/aws", "https://docs.ansible.com/ansible/latest/collections/community/hashi_vault/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Short-lived credentials: OIDC and Vault dynamic secrets

Static access keys in CI secrets leak and rarely rotate. Prefer identities that expire quickly.

## OIDC federation (CI to cloud)
From the GitHub Actions OIDC documentation:
- After you set up a trust connection with an OIDC-capable cloud provider, a workflow requests a short-lived access token directly from the provider, so you do not store long-lived cloud credentials as GitHub secrets.
- The token the cloud provider issues is valid only for a single job and then expires, so credentials rotate per run.
- The cloud provider validates the claims in the GitHub-issued token before issuing its token. Example claims: `iss` is `https://token.actions.githubusercontent.com`, and `sub` such as `repo:octo-org/octo-repo:environment:prod` (job environment) or `repo:my-org/my-repo:ref:refs/heads/main` (branch).
- Write the cloud-side trust condition on `sub` as narrowly as you can (repository and environment or ref) so that only the intended workflow can assume the production role. (Practitioner inference from the claim structure.)
- The docs note repositories created after 15 July 2026 use an immutable default `sub` format that includes owner and repository IDs, so check the OpenID Connect reference for the format your repository uses before writing conditions.

## Vault AWS secrets engine
Vault's AWS secrets engine generates AWS credentials on demand from roles; they are time-based and revoked when the Vault lease expires. Four credential types:
- `iam_user`: Vault creates an IAM user per lease, attaches the role's policies (and a permissions boundary if set), returns an access key and secret key with no session token, and deletes the user at TTL expiry.
- `assumed_role`: calls sts:AssumeRole and returns access key, secret key and session token.
- `federation_token`: calls sts:GetFederationToken with a supplied policy document.
- `session_token`: calls sts:GetSessionToken.
Reading `aws/creds/<role>` generates a new credential on each invocation and returns a lease ID and duration.

Static roles map a Vault role one-to-one to an IAM user whose credentials Vault rotates on a configurable period, in contrast to dynamic secrets.

## Ansible
The `community.hashi_vault` collection (requires ansible-core 2.17 or newer in the version documented) includes `vault_login`, `vault_read` and `vault_write` modules and lookups, KV v1/v2 modules, database role and connection modules including static-role credential rotation, and a PKI certificate module. Use `no_log: true` on tasks that handle credentials.

## Gotchas
- IAM credentials are eventually consistent with other AWS services. Vault's docs say a pipeline may need a delay of 5-10 seconds or more after fetching IAM user credentials; STS-based credentials are usable as soon as they are generated.
- Size the lease or TTL to the longest job plus margin, otherwise authentication can fail mid-run. (Practitioner guidance.)
- `vault write -f aws/config/rotate-root` rotates the credentials Vault itself uses to talk to AWS.

## Verify
- [ ] No long-lived cloud keys remain in CI secret stores; runs show federated or leased identities.

## Checked
Method: docs-checked 2026-11-09 against the GitHub Actions OIDC about page, the Vault AWS secrets engine page, and the community.hashi_vault collection index.
Removed as unconfirmed: the aws-actions workflow and IAM trust policy JSON (aud value), Azure/GCP/GitLab equivalents, Vault JWT/OIDC auth setup for CI, the Ansible JWT lookup sample, the Terraform vault_aws_access_credentials remark, and the CloudTrail session-naming advice.
