---
id: computing-software.cybersecurity-defensive.pomerium.create-service-account
name: create-service-account
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [service-accounts, machine-to-machine, user-id, expiration, namespace-scope]
level: practitioner
status: docs-checked
description: "Create a Pomerium service account in the Enterprise Console or Zero, save its JWT once, and grant it access through a policy User criterion."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/service-accounts.md
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/impersonation.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Service accounts authenticate machine-to-machine calls between services protected by Pomerium. They are an Enterprise and Zero feature.

**Enterprise Console**
1. Confirm you are in the right Namespace; a service account only works in the Namespace it was created in, including child Namespaces.
2. Service Accounts dashboard, **+ ADD SERVICE ACCOUNT**.
3. Enter a unique **User ID** or select an existing user to impersonate. Including the Namespace name in the ID helps. Optionally set an expiration.
4. **Submit**, then save the JWT shown.

**Zero**: Service Accounts dashboard, **+ New Service Account**, enter a unique User ID (or an existing user's), optional expiration, **Save**, then store the JWT.

The JWT cannot be viewed again, so save it securely.

The User ID matches the `User` criterion in policies. Accounts can exist only for Pomerium or impersonate directory users from your IdP.

Grant access: create or edit a policy (for example Policies, NEW POLICY, Builder, ADD ALLOW BLOCK, criterion User, pick the service account), then apply it to a route. See service-account-auth-headers to use the token.

## Checked

2026-11-04. Confirmed against the Service Accounts and User Impersonation pages: Enterprise and Zero steps, namespace scope, User ID field, expiration, JWT shown once, User criterion, and the policy builder steps. Nothing removed.

Method: documentation only; no commands were run.
