---
id: computing-software.cybersecurity-defensive.identity-access-management.workload-identity-federation
name: workload-identity-federation
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [entra-id, workload-identity-federation, oidc-federation, github-actions, federated-credentials, secretless, managed-identity, oidc-federation-trust-subject-claims]
level: advanced
status: docs-checked
description: "Remove long-lived cloud secrets from CI/CD and external workloads with workload identity federation: Entra federated credentials, AWS and GCP OIDC trust, and tight subject claims."
sources: ["https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation", "https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect", "https://cloud.google.com/iam/docs/workload-identity-federation"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Workload identity federation

**Goal:** pipelines and workloads outside a cloud (GitHub Actions, GitLab, Kubernetes,
another cloud) get short-lived cloud credentials by presenting an OIDC token from their own
platform, so no client secrets or access keys are stored anywhere.

## How it works
1. The external platform issues a signed OIDC token describing the workload (issuer,
   subject such as `repo:org/app:environment:prod`, audience).
2. The cloud trusts that issuer for a specific identity, with conditions on subject/claims.
3. The workload exchanges the token for short-lived cloud credentials.

## Microsoft Entra
App registration or user-assigned managed identity > Federated credentials:
- Configure the issuer URL of the external platform, the subject (GitHub's `sub` claim has the form `repo:<org>/<repo>:environment:<name>`) and an audience, per the Entra workload identity federation page.
- Keep claim conditions narrow.

## GCP
Workload identity pool + provider with attribute mapping and an **attribute condition** (a CEL expression
that checks assertion attributes; credentials that fail it are rejected), then grant the service account the
Workload Identity User role (`roles/iam.workloadIdentityUser`) for the pool principal.

## Security rules
- Pin the subject to repo **and** branch or environment; GitHub environments with required
  reviewers protect production deploy identities.
- Never use wildcards like `repo:example-org/*` for privileged roles; any repo in the org
  (including forks' workflows in some configurations) could deploy.
- Least-privilege roles per pipeline; separate identities per environment.
- Log and alert on token exchanges from unexpected subjects (the cloud provider's audit logs).

## Gotchas
- Pull request workflows from forks: ensure they cannot reach environments with federated
  credentials.
- Custom claims and subject formats differ per platform version; check the actual token
  (debug by printing claims in a test workflow, not the token itself).

## Verify
Pipeline deploys without any stored cloud secret; a workflow from another branch/repo fails
to obtain credentials; old secrets are deleted from the CI store and the app registration.

## Checked

2026-10-28. Confirmed: GitHub OIDC page (token `sub` format `repo:<org>/<repo>:environment:<name>`); Google Cloud workload identity federation page (attribute conditions as CEL expressions, `roles/iam.workloadIdentityUser`, token exchange flow); Microsoft Entra workload identity federation page (federated credentials concept). Removed: the AWS section and trust policy (AWS pages not fetched), `AssumeRoleWithWebIdentity`, `id-token: write`, `azure/login`, `api://AzureADTokenExchange`, the AKS subject string, the `assertion.repository` example and the flexible-credentials sentence.
Method: documentation only; no commands were run.
