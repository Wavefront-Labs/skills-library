---
id: computing-software.cybersecurity-defensive.zitadel.organizations-and-multi-tenancy
name: organizations-and-multi-tenancy
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, organizations, multi-tenancy, registration, b2b]
level: practitioner
status: docs-checked
description: "Model tenants as ZITADEL organizations, create them in the console, enable self-service organization registration, and set the default organization."
sources:
  - https://zitadel.com/docs/guides/manage/console/organizations-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An organization is the vessel for users and projects, comparable to a tenant in a SaaS system or an organizational unit in a directory. Several organizations live in one instance, users and data are isolated between them, and organizations can delegate rights to each other. In a B2B case an organization usually stands for a business partner with its own branding, access settings or federated login providers.

Create one from the organizations dropdown in the console with New organization. You choose between making your current user the organization manager, which adds a membership to your account, or creating a fresh account to manage it.

For customer-driven sign-up, ZITADEL ships a registration form at `https://$CUSTOM-DOMAIN/ui/login/register/org`. The customer enters an organization name and contact details.

On the default settings page (`${CUSTOM_DOMAIN}/ui/console/orgs`) you can designate a default organization.

Projects live inside organizations. Use project grants to let another organization assign your project's roles to its own users, rather than duplicating users or giving partners administrator rights in your organization.

## Checked

2026-11-08. Read in full: the organizations page. All claims confirmed.

Method: documentation only; no commands were run.
