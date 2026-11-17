---
id: computing-software.collaboration-platform-administration.vikunja.oidc-claims-and-userinfo
name: oidc-claims-and-userinfo
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, oidc-claims, preferred-username, forceuserinfo, random-username, userinfo-endpoint]
level: advanced
status: docs-checked
description: "Which ID token claims Vikunja needs from an OIDC provider, the userinfo fallback and forceuserinfo, and why users get random usernames."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/openid.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Claims Vikunja reads:
- `email` (required, scope `email`): user creation fails if it is missing and the userinfo lookup also fails.
- `name` (optional, `profile`): display name.
- `preferred_username` (optional, `profile`): username.
- `picture` (optional, `profile`): avatar; must be a URL that returns an image.
- `vikunja_groups`: team assignment (see the team sync skill).

If `email`, `name`, `preferred_username` or `picture` is absent from the ID token, Vikunja queries the `userinfo` endpoint. Set `forceuserinfo: true` to always use userinfo, which helps with providers like Casdoor whose token and userinfo data are inconsistent.

Username order: `preferred_username` from the ID token, then from userinfo, then `nickname` from userinfo, otherwise a random username is generated. Random-looking usernames mean the provider omits `preferred_username`; make the profile scope include it (some providers, such as Synology SSO, do not by default).

Accounts are created on first OIDC login. There is no SCIM or bulk import, so a user cannot be assigned to a task or team before first login.

## Checked

2026-11-04: claims table, userinfo fallback, `forceuserinfo`, username order and troubleshooting notes checked against the OpenID page.

Method: documentation only; no commands were run.
