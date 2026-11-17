---
id: computing-software.collaboration-platform-administration.matrix-synapse.user-admin-api-shadow-ban-and-ratelimit-override
name: user-admin-api-shadow-ban-and-ratelimit-override
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, admin-api, users, shadow-ban, ratelimit, override-ratelimit, messages-per-second, burst-count, moderation]
level: practitioner
status: docs-checked
description: "Moderate abusive Synapse users with the shadow_ban admin endpoint, and set, read or remove per-user rate limit overrides with messages_per_second and burst_count."
sources:
  - https://element-hq.github.io/synapse/latest/admin_api/user_admin_api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two per-user controls in the user admin API, both for local users only (the `user_id` is the full MXID, such as `@user:server.com`) and both needing an admin `access_token`.

**Shadow-banning.** A shadow-banned user gets successful responses to client-server API requests, but their events are not propagated into rooms. The idea is that the abuser takes longer to notice and switch accounts. The docs call it a last resort: it may cause confusing or broken client behaviour, the user receives no notification, and the user cannot contact anyone on the server. Banning or kicking is usually more appropriate.

```
POST /_synapse/admin/v1/users/<user_id>/shadow_ban
DELETE /_synapse/admin/v1/users/<user_id>/shadow_ban
```

POST bans and DELETE reverses it; both return an empty JSON dict.

**Rate limit overrides.** Override or disable rate limiting for one user. An override replaces the rate and burst count of the `rc_message` limiter (sending events and related actions such as creating rooms or updating the profile); it does not change other limiters such as `rc_invites` or `rc_joins`, except that `messages_per_second` of 0 disables all rate limiting for the user:

```
GET    /_synapse/admin/v1/users/<user_id>/override_ratelimit
POST   /_synapse/admin/v1/users/<user_id>/override_ratelimit
DELETE /_synapse/admin/v1/users/<user_id>/override_ratelimit
```

POST takes optional positive integers `messages_per_second` (actions per second) and `burst_count` (actions before limiting), both defaulting to 0. Setting both to 0 disables rate limiting for that user. GET returns the current pair; if no custom limit is set it returns `{}` and the global limits apply. DELETE removes the override and returns `{}`; this does not disable rate limiting.

Remember that deactivating an account does not remove its rate limit override, so delete it explicitly when cleaning up.

## Checked

Method: docs-checked 2026-11-09 against docs/admin_api/user_admin_api.md (Synapse develop branch, raw markdown; shadow-ban and ratelimit override sections read in full).
