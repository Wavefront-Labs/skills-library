---
id: computing-software.cybersecurity-defensive.keycloak.organizations-create-and-manage
name: organizations-create-and-manage
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, organizations, members, alias, domains]
level: practitioner
status: docs-checked
description: "Create and manage Keycloak organizations: unique name and alias, domains, attributes, members, groups and linked identity providers."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/organizations/managing-organization.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# organizations create and manage
To use organizations, enable the feature for the realm: *Realm Settings*, toggle *Organizations* On, *Save*. An *Organizations* section then appears in the menu; use *Create Organization*.

Organization settings:
- **Name**: friendly name, unique within the realm.
- **Alias**: internal identifier, unique within the realm; ASCII spaces, control characters and backslashes are not allowed, `*` alone is reserved (it can occur within an alias such as `acme*corp`), `/` and `:` are allowed. If not set, Keycloak tries to use the name.
- **Redirect URL** (deprecated): when sending invitations specify a `client_id` instead; the URL is used only for invitations without a custom client and must be a valid redirect URI of the account client, otherwise users go to the account console.
- **Domains**: zero or more domains; a domain cannot be shared by different organizations in a realm. With no domain, members are not validated against domain restrictions during authentication and profile validation.
- **Description**.

After creating one you manage its attributes, members, groups and identity providers (managed and unmanaged members are described in the docs).

Disabling (toggle *Enabled* off): the organization stays manageable but its members cannot authenticate to the realm, including through linked identity providers; the providers themselves stay enabled and only the links become inactive. Unmanaged members can still authenticate as realm users, but tokens hold no metadata about the disabled organization.

Deleting: all data associated with the organization is deleted, including any managed member. Unmanaged users and identity providers remain; providers are unlinked from the deleted organization only.

## Checked
2026-11-03. Confirmed against server_admin/topics/organizations/managing-organization.adoc. Fixed: enabling is a realm setting toggle, and deleting an organization does delete managed members. Removed (not on the page): customer/business-unit planning advice, the login-flow gotcha, and the invitation/organization-claim Verify step.
Method: documentation only; no commands were run.
