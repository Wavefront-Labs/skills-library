---
id: computing-software.ai-ml-engineering.open-webui.map-oauth-roles-and-groups
name: map-oauth-roles-and-groups
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [sso-oidc, oauth, role-management, group-management, claims, open-webui]
level: practitioner
status: docs-checked
description: "Map OIDC role and group claims to Open WebUI admin/user roles and groups with ENABLE_OAUTH_ROLE_MANAGEMENT and ENABLE_OAUTH_GROUP_MANAGEMENT."
sources:
  - https://docs.openwebui.com/features/authentication-access/auth/sso/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: drive Open WebUI roles and group membership from the identity provider on each login.

## Roles
```bash
ENABLE_OAUTH_ROLE_MANAGEMENT=true
OAUTH_ROLES_CLAIM=roles          # may be nested, e.g. user.roles
OAUTH_ALLOWED_ROLES=user,admin   # may log in as role user; "*" allows any
OAUTH_ADMIN_ROLES=admin          # become Open WebUI admin
OAUTH_ROLES_SEPARATOR=,          # optional: also split a string claim by this
```
Open WebUI reads the ID token claims merged with the userinfo response. If the claim carries roles matching neither list, login is refused with 403; the default role applies only when the claim is absent or empty. With Entra ID app roles, check `OAUTH_ALLOWED_ROLES` (default `user,admin`) and `OAUTH_ADMIN_ROLES` (default `admin`) against the values you assigned.

## Groups
```bash
ENABLE_OAUTH_GROUP_MANAGEMENT=true
OAUTH_GROUP_CLAIM=groups         # default groups; OAUTH_GROUPS_CLAIM is read first
ENABLE_OAUTH_GROUP_CREATION=true # JIT-create groups seen in claims (default false)
OAUTH_GROUP_DEFAULT_SHARE=true   # true | members | false, for JIT-created groups
```
Also relevant: `OAUTH_BLOCKED_GROUPS` (never created, added or removed).

## Behaviour to plan for
- Sync is strict: on each login the user is added to matching groups and removed from any Open WebUI group (even manually made) not in the claim. Only applies when the claim is present and non-empty; an absent or empty claim leaves memberships alone.
- Admins are not exempt from group sync.
- Role or group changes upstream take effect only after the user logs out and in again. When a login changes the role, other live WebSocket connections are ended.

## Gotchas
- Config values can be locked read-only in the Admin Panel unless `ENABLE_OAUTH_PERSISTENT_CONFIG=true`; edit env vars and restart otherwise.
- The token-exchange endpoint reads roles and groups from the presented access token (decoded without signature check) when userinfo lacks them; with restrictive `OAUTH_ALLOWED_ROLES` and no readable claim it returns 403.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page features/authentication-access/auth/sso (read in full): the role variables, their defaults and wildcard, ID token plus userinfo claim merge, the 403 rule and the default-role-only-when-absent rule from the Entra tip, the group variables and defaults, OAUTH_GROUPS_CLAIM read first, strict synchronisation with the absent-claim exception and OAUTH_BLOCKED_GROUPS, no admin exemption, the logout and login requirement and WebSocket ending, the read-only Admin Panel behaviour with ENABLE_OAUTH_PERSISTENT_CONFIG, and the token exchange claim reading and 403. Removed the Verify section, whose Groups page Preview tab step is not on the page.
Method: documentation only; no commands were run.
