---
id: computing-software.cloud-infrastructure-engineering.portainer.configure-oauth-authentication
name: configure-oauth-authentication
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [authentication, oauth, sso, team-membership, entra-id]
level: practitioner
status: docs-checked
description: "Configure OAuth login in Portainer, including SSO, hiding internal auth, automatic provisioning and claim-based team membership."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/admin/settings/authentication/oauth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Go to Settings, Authentication, choose OAuth, and enter the credentials your OAuth provider issued.

Key options:

- Use SSO: the provider will not force a credentials prompt when the user already has a logged-in session.
- Hide internal authentication prompt: removes the internal login form. With external authentication on, only the initial admin can log in with internal auth.
- Automatic user provisioning: users that exist at the provider are created in Portainer, optionally placed in a default team. If off, create users manually.
- Automatic team membership: match users to Portainer teams by a claim name. Claim values map to team names, or you can link a claim to teams by regex under Statically assigned teams. You can also set a Default team.
- Automatic admin assignment for specified groups is available.

When using Microsoft Entra ID (Azure AD) as provider, use the group Object Id value for group matching rather than the display name.

Because team leaders are disabled when teams are synced from an external provider, manage membership at the provider.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. No wrong claims found; nothing removed.

Method: documentation only; no commands were run.
