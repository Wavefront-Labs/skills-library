---
id: computing-software.cloud-infrastructure-engineering.azure.federated-credentials-on-user-assigned-managed-identities
name: federated-credentials-on-user-assigned-managed-identities
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, workload-identity-federation, uami-federated-credential, managed-identity-federation, federated-credentials, oidc-issuer]
level: practitioner
status: docs-checked
description: "Manage federated identity credentials on user-assigned managed identities: issuer/subject/audience rules, limits, IaC, supported regions and when to use an app registration instead."
sources: ["https://learn.microsoft.com/entra/workload-id/workload-identity-federation-create-trust-user-assigned-managed-identity", "https://learn.microsoft.com/entra/workload-id/workload-identity-federation-considerations", "https://learn.microsoft.com/entra/workload-id/workload-identity-federation", "https://learn.microsoft.com/entra/workload-id/workload-identity-federation-create-trust"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Federated credentials on user-assigned managed identities

**Goal:** external workloads (CI, Kubernetes, other clouds) exchange their own OIDC tokens for
Entra tokens of a UAMI, without app registrations or secrets.

## Credential fields
| Field | Rule |
|---|---|
| `issuer` | URL of the external IdP, required; must match the token's `iss` claim exactly (leading or trailing whitespace blocks the exchange) and comply with OIDC Discovery, because Entra uses it to fetch the signing keys; max 600 characters |
| `subject` | Required; must match the token's `sub` claim exactly; no fixed format per IdP; no wildcards; max 600 characters |
| `audiences` | Exactly one value, normally `api://AzureADTokenExchange`; max 600 characters |
| name | 3-120 characters: alphanumeric, dash or underscore, first character alphanumeric; immutable |
The `issuer` and `subject` combination must be unique on the identity. Max **20** federated credentials per user-assigned managed identity (or app). Only issuers whose tokens are signed with RS256 are supported. A wrong `subject` is accepted at creation and only fails at token exchange, silently. Allow several minutes for a new or changed credential to propagate in a region; creating credentials is not supported for identities in some regions (the considerations article lists them, currently Malaysia South).

## Create
```bash
az identity federated-credential create -g rg-id -n k8s-payments \
  --identity-name id-payments \
  --issuer <oidc-issuer-url> \
  --subject system:serviceaccount:payments:payments-sa \
  --audiences api://AzureADTokenExchange
az identity federated-credential list -g rg-id --identity-name id-payments
```
Kubernetes subjects have the form `system:serviceaccount:<namespace>:<service-account>`; GitHub Actions subjects look like `repo:octo-org/octo-repo:environment:Production` and must match the workflow configuration exactly. `show` and `delete` also exist; list, get and delete are not available through templates.

## Templates and automation
Create federated credentials under the same parent identity **sequentially**: by default child credentials are created in parallel, which triggers concurrency detection and fails the deployment. Credentials under different identities can be created in parallel. Terraform AzureRM 3.40.0 and later creates multiple credentials sequentially.

## UAMI vs app registration
Both can hold federated credentials with the same field rules and 20-credential limit. Flexible federated identity credentials (claims-matching expressions, preview) are documented for app registrations. Anyone who can register apps and add a secret or certificate can add a federated credential to an app; if "Users can register applications" is No, an Application Administrator or Application Owner must do it.

## Gotchas
- Subject and issuer mismatches fail silently at exchange time: compare the decoded external token to the credential.
- Workloads whose issuer cannot be reached for key discovery cannot federate; publish the OIDC discovery document and keys at the issuer URL.

## Verify
- [ ] A token exchange for the identity succeeds.
- [ ] The federated credential count per identity is tracked against the 20 limit.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/entra-docs `docs/workload-id` (workload-identity-federation, -considerations, -create-trust, -create-trust-user-assigned-managed-identity and the shared federated-credential configuration considerations include; main branch, repo pushed 2026-10-23).
- Confirmed: 20-credential limit; field rules and character limits; single audience; no wildcards; name rule; issuer/subject uniqueness; RS256 only; propagation delay; unsupported region list; `az identity federated-credential create/list/show/delete`; sequential creation under one parent and the Terraform 3.40.0 note; app-registration permissions.
- Removed as unconfirmed: the Bicep resource API version and `@batchSize` advice, the raw token-exchange curl, the client credential class names, GKE issuer URL, case-sensitivity wording, the trailing-slash wording, the UAMI recreate warning and the claim that UAMIs cannot be multi-tenant or lack app roles.
Method: documentation only; no commands were run.
