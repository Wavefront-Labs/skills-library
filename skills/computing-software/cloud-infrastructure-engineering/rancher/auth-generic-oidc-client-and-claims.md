---
id: computing-software.cloud-infrastructure-engineering.rancher.auth-generic-oidc-client-and-claims
name: auth-generic-oidc-client-and-claims
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [oidc, generic-oidc, groups-claim, sub-claim, custom-claims, verify-auth, keycloak]
level: advanced
status: docs-checked
description: "Configure Generic OIDC in Rancher: client settings with verify-auth redirect URI, mappers, immutable sub claim, custom claim mapping."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/authentication-permissions-and-global-configuration/authentication-config/configure-generic-oidc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Generic OIDC lets users sign in with an account at any OIDC identity provider. Start in the IdP by creating a client: protocol `openid-connect`, access type `confidential`, and valid redirect URI `https://yourRancherHostURL/verify-auth`.

Then create mappers on that client:

- **Groups Mapper**: type Group Membership, token claim `groups`, added to user info only.
- **Client Audience**: type Audience, with an Included Client Audience, added to the access token.
- **Group Path**: type Group Membership, token claim `full_group_path`, full group path on, added to user info.

`groups` and `full_group_path` must be **JSON arrays**, for example `"groups":["admins","devs","qa"]`.

Warning from the page: Rancher uses the `sub` claim to form the PrincipalID, its unique identifier, so make `sub` unique and immutable.

In Rancher go to **Users & Authentication > Auth Provider > Generic OIDC**, fill in Client ID, Client Secret, optionally a key/certificate pair (required if the OIDC server uses HTTPS/SSL), and the Rancher URL, Issuer and endpoints, then **Enable**. A popup blocker can hide the IdP login window.

**Custom claim mapping** covers `name`, `email` and `groups` when your IdP uses non-standard names. A custom groups claim supplements the standard `groups` claim, or is the only source if there is none. Groups from a custom claim are not searchable; type the exact group name into the RBAC field.

## Checked

2026-11-09. Read the cited Configure Generic OIDC page in full and checked every claim against it (client settings, three mappers, JSON array note, sub claim warning, form fields, custom claims behaviour). Removed the "set to your client name" detail and the Keycloak-style remark, which the page does not state.

Method: documentation only; no commands were run.
