---
id: computing-software.cloud-infrastructure-engineering.azure.flexible-federated-identity-credentials-and-claims-matching
name: flexible-federated-identity-credentials-and-claims-matching
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, workload-identity-federation, flexible-federated-credential, claims-matching-expression, github-oidc-subject, federated-credential-limit]
level: advanced
status: gated
description: "Beat the 20 federated-credential limit: flexible federated identity credentials with claims matching expressions, and customising GitHub's OIDC subject claim."
sources: ["https://learn.microsoft.com/entra/workload-id/workload-identities-flexible-federated-identity-credentials", "https://learn.microsoft.com/graph/api/resources/federatedidentitycredentials-overview", "https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flexible federated identity credentials

**Goal:** one credential that trusts "any branch/environment matching a pattern" instead of one exact-subject
credential per branch, PR and environment.

## Why
A federated identity credential (FIC) normally needs an exact `subject` (e.g. `repo:contoso/api:environment:prod`).
An app or managed identity allows only **20** FICs, which runs out with many repos/branches/environments.

## Flexible FIC (claims matching expression)
Supported for specific issuers (the Learn page has GitHub, GitLab and Terraform Cloud tabs) - check the current
docs for GA status and supported issuers. Created via Graph (gated: unconfirmed, source is paywalled or blocked):
```bash
az rest --method POST --url "https://graph.microsoft.com/beta/applications/<appObjectId>/federatedIdentityCredentials" \
  --body '{
    "name": "github-contoso-release-branches",
    "issuer": "https://token.actions.githubusercontent.com",
    "audiences": ["api://AzureADTokenExchange"],
    "claimsMatchingExpression": {
      "value": "claims['"'"'sub'"'"'] matches '"'"'repo:contoso/*:ref:refs/heads/release/*'"'"'",
      "languageVersion": 1 } }'
```
Expression language supports `eq`, `matches` (wildcard `*`) and `and`; use it for a bounded pattern, not `*` alone.

## Alternative: customise GitHub's subject
GitHub lets an org or repo change the `sub` claim template; see GitHub's OIDC hardening docs for the API and claim keys. Update the FIC subject at the same time or every login fails.

## Security
- Wildcards widen trust: `repo:contoso/*` trusts every repo in the org - anyone who can create a repo can deploy.
  Scope to environment names protected by required reviewers instead.
- Pair with GitHub environment protection rules and branch protection; the claim is only as trustworthy as those.

## Verify
- [ ] A workflow on a matching branch logs in; a non-matching branch fails; FIC count per app stays well under 20.

## Checked
2026-10-28. Confirmed on the flexible federated identity credentials and Graph overview pages: the limit of 20 federated identity credentials per application or user-assigned managed identity, `claimsMatchingExpression` with `matches` (wildcard `*`), `eq` and `and`, issuer `https://token.actions.githubusercontent.com`, audience `api://AzureADTokenExchange`.
Gated: the exact Graph endpoint and API version for creating the credential (graph.microsoft.com returns 401 to scripts), marked in the text.
Removed (not confirmed): the `gh api` OIDC customization call and keys, the AADSTS error code, and the claim that only app registrations are supported.

Method: documentation only; no commands were run.
