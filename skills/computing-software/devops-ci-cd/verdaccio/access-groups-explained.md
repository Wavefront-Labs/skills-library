---
id: computing-software.devops-ci-cd.verdaccio.access-groups-explained
name: access-groups-explained
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [groups, authenticated, anonymous, all, authenticated-group, anonymous-group, htpasswd-groups]
level: practitioner
status: docs-checked
description: "What $all, $anonymous, $authenticated and user or group names mean in Verdaccio access rules, which groups each user gets, and the deprecated @all aliases."
sources:
  - https://verdaccio.org/docs/packages/
  - https://verdaccio.org/docs/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every value in `access`, `publish`, `unpublish` and `stage` is a list of groups; a request passes when the user belongs to at least one.

| Group | Members |
|---|---|
| `$all` | everyone, logged in or not |
| `$anonymous` | only visitors not logged in |
| `$authenticated` | any logged-in user |
| a group name (`admin`) | users the auth plugin reports as members |
| a user name (`alice`) | with htpasswd every user is also a group of their own |

Resulting group lists:
- not logged in: `$all`, `$anonymous`
- alice (htpasswd): `$all`, `$authenticated`, `alice`
- plugin returns dev, qa: `$all`, `$authenticated`, `dev`, `qa`

Gotchas:
- `$all` is not "all logged-in users"; to require a login use `$authenticated`.
- `$anonymous` excludes logged-in users, rarely what you want.
- `@all`, `@authenticated`, `@anonymous`, `all` are deprecated aliases; use `$`.
- htpasswd does not implement `allow_access`, `allow_publish` and `allow_unpublish` (the authentication page lists all three, the package access page names only the first two); Verdaccio applies defaults. A custom plugin that implements them decides for itself.
- Since npm 7.10, `always-auth` has no effect.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Package Access (packages) and Authentication. Confirmed: the group table, the resulting group lists, the three gotchas, the deprecated @ aliases and the always-auth note. Removed or corrected: nothing removed. The two pages differ slightly: the package access page says htpasswd does not handle allow_access and allow_publish, the authentication page lists allow_access, allow_publish and allow_unpublish; the skill now says so.

Method: documentation only; no commands were run.
