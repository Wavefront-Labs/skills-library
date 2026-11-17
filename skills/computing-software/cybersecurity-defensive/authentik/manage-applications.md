---
id: computing-software.cybersecurity-defensive.authentik.manage-applications
name: manage-applications
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, applications, providers, launch-url, backchannel-providers, hide-application]
level: practitioner
status: docs-checked
description: "Create authentik application and provider pairs, restrict access with bindings, hide apps, use launch URLs, add backchannel providers."
sources:
  - https://docs.goauthentik.io/add-secure-apps/applications/manage_apps/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

## Create an application and provider
**Applications > Applications > New Application** (the drop-down offers **with New Provider...** or **with Existing Provider...**). Wizard steps: Application (name, optional group, policy engine mode, UI settings), Choose a Provider, Configure the Provider (name, authorization flow, extras), Configure Bindings (optional), then Review and **Create Application**.

## Access control
With no bindings every user has access. Bind policies, groups or users from the application's **Policy / Group / User Bindings** tab (**Create or bind...**). Policy engine mode `All` requires every binding to pass; `Any` at least one. Use a policy when access depends on time, region, request data or user attributes.

## Hide and launch
- **Hide from Application Dashboard** hides the tile only; users still have access and can authorize when login starts from the app. Before 2026.5 the trick was Launch URL `blank://blank`; such apps migrate automatically.
- Direct link: `https://authentik.company/application/launch/<slug>/` (logged-in users are redirected; others authenticate first).

## Backchannel providers
They add protocols beside the main SSO provider: SCIM, LDAP, Google Workspace, Microsoft Entra ID or SSF. Create under **Applications > Providers > Create**, then edit the application and add it in **Backchannel Providers**. The application's access restrictions apply to all its backchannel providers.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
