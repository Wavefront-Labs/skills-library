---
id: computing-software.collaboration-platform-administration.vikunja.config-service-options
name: config-service-options
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, service-section, jwt-ttl, service-secret, feature-toggles, unix-socket]
level: practitioner
status: docs-checked
description: "Reference for Vikunja's service.* options: secret and token lifetimes, listen interface and Unix socket, public URL, feature toggles and timezone."
sources:
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Selected `service.*` options and defaults:
- `secret`: signs JWTs and other crypto. Default is a random secret generated at each startup, so restarts invalidate all issued tokens; set a fixed value. `JWTSecret` is deprecated.
- `jwtttl` 259200 s (3 days); `jwtttllong` 2592000 s (30 days, "remember me"); `jwtttlshort` 600 s (short tokens used with refresh tokens).
- `interface` `:3456`; `unixsocket` and `unixsocketmode` (octal needs the `0o` prefix, e.g. `0o660`).
- `publicurl`: required when `cors.enable` is true.
- `maxitemsperpage` 50; `timezone` `GMT` (tz database names only, no offsets); `motd` shown by `/info`.
- Toggles, all default true: `enablecaldav`, `enablelinksharing`, `enableregistration`, `enabletaskattachments`, `enabletaskcomments`, `enabletotp`, `enableemailreminders`, `enableuserdeletion`, `allowiconchanges`.
- `enablepublicteams` false; `enableopenidteamusersearch` false; `bcryptrounds` 11; `maxavatarsize` 1024.
- `customlogourl` and `customlogourldark` for branding; `demomode` false.
- `testingtoken`: if not empty, enables `/test/{table}` endpoints that put any content in the database; the docs say never use it unless you know exactly what you are doing.

## Checked

2026-11-04: every option and default checked against config-raw.json (service section).

Method: documentation only; no commands were run.
