---
id: computing-software.data-engineering.metabase.jwt-sso
name: jwt-sso
category: computing-software
field: data-engineering
product: metabase
tags: [jwt, sso, jwt-group-sync, identity-provider-uri, group-mappings, return-to]
level: advanced
status: docs-checked
description: "Set up Metabase JWT single sign-on: Pro/Enterprise settings, shared signing key, the /auth/sso redirect flow, group mapping modes, MB_JWT env vars and lockout traps."
sources:
  - https://www.metabase.com/docs/latest/people-and-groups/authenticating-with-jwt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Availability: Pro and Enterprise only.

Setup: Admin, Settings, Authentication, JWT, then "Save and enable".
- JWT Identity Provider URI: where Metabase redirects logins.
- String used by the JWT signing key: shared between Metabase and your auth app ("Set up key" generates or accepts one).
- Optional attribute names for email, first name, last name, group assignment, and tenant (default `@tenant`). Extra attributes sync on each login.

Flow: unauthenticated users hit `/auth/sso`, are redirected to your IdP, which sends them back to `/auth/sso` with `jwt` and `return_to`. Metabase verifies the token, logs them in and redirects to `return_to`. Use POST with a JSON body for modular embeds, so the JWT stays out of the URL.

Group mapping: Automatic (matches JWT group names to Metabase groups, the default), Manual, or Off. The JWT carries `groups: ["group_name"]` under the key named by the group attribute. Switching Manual to Automatic deletes mappings, and removing a mapping can remove members or delete the group irreversibly.

Environment variables: `MB_JWT_ATTRIBUTE_GROUPS`, `MB_JWT_GROUP_SYNC` (off by default) and `MB_JWT_GROUP_MAPPINGS` (JSON of JWT group name to Metabase group ID; All Users is 1, Administrators is 2). Setting the sync or mappings variable makes the UI read-only.

Provisioning: on by default, creating or reactivating accounts at login; when off, users without accounts cannot log in. SSO accounts have no passwords.

Gotcha: turning off password authentication affects admins too, so keep it on to avoid lockout. The page does not state the signing algorithm or required claims.

## Checked
2026-11-03. Confirmed against the Metabase docs page People and groups, Authenticating with JWT: Pro/Enterprise availability, /auth/sso flow with jwt and return_to, POST for modular embeds, setup fields, attribute settings and the @tenant default, group mapping modes and destructive effects, MB_JWT_* variables and group IDs 1 and 2, provisioning, password-login lockout warning. Nothing removed.
Method: documentation only; no commands were run.
