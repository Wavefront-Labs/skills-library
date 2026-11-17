---
id: computing-software.cybersecurity-defensive.pomerium.impersonate-user-console
name: impersonate-user-console
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [impersonation, enterprise-console, unimpersonate, troubleshoot-access, policy-testing]
level: practitioner
status: docs-checked
description: "Temporarily sign in to Pomerium Enterprise Console as another user to troubleshoot access errors or test policies, and how to end it."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/impersonation.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Administrators can sign in as another user or group in their organisation. The admin receives the impersonated user's access and authorization policies.

Use cases: troubleshooting access errors by seeing what the user sees; making changes for a user who is away; testing policies, routes and settings by previewing others' permissions.

In the Console GUI:
1. Select the **Logout** icon.
2. Select **Impersonate**.
3. In the **Session** dropdown pick the target user.
4. Select **Impersonate**.

To end it, select **Unimpersonate**.

For machine impersonation use a service account with a User ID; see create-service-account and service-account-auth-headers. A service account works only in the Namespace where it was created, including child Namespaces.

## Checked

2026-11-04. Confirmed against the User Impersonation page: use cases, Console steps (Logout icon, Impersonate, Session dropdown, Unimpersonate), service account namespace scope. Nothing removed.

Method: documentation only; no commands were run.
