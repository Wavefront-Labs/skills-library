---
id: computing-software.devops-ci-cd.verdaccio.server-tuning-and-hidden-logs
name: server-tuning-and-hidden-logs
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [server-settings, keepalive, max-body-size, server-block, legacyauthcache, dotfiles, hidepinglogs, user-agent]
level: practitioner
status: docs-checked
description: "The server block of config.yaml: keepAliveTimeout, legacyAuthCache, dotfiles, hideStaticLogs, hidePingLogs, plus max_body_size and user_agent."
sources:
  - https://verdaccio.org/docs/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
server:
  keepAliveTimeout: 60
  legacyAuthCache:        # 6.10.0+, off by default
    enabled: true
    ttlMs: 15000
    maxEntries: 1000
  dotfiles: ignore        # 7.x
  hideStaticLogs: true    # 7.x
  hidePingLogs: true      # 7.x
max_body_size: 10mb
user_agent: false
```
- `keepAliveTimeout` (seconds): `0` behaves like Node before 8.0.0; try it if 60 is not enough (issue 301 workaround).
- `legacyAuthCache` caches successful legacy bearer-token checks; changed or revoked credentials stay valid until the entry expires.
- `dotfiles` (7.x): `ignore` answers 404 (default), `deny` 403, `allow` passes through.
- `hideStaticLogs` hides `/-/static/*`; `hidePingLogs` hides successful `/-/ping` only (>=400 still logged). `DEBUG=verdaccio:middleware:log` shows them regardless.
- `max_body_size` default is 10mb; raise it on "request entity too large".
- `user_agent`: disabled by default (client UA passed to remote); `true`, `false` or a custom string.

## Checked

2026-11-04. Confirmed against the Configuration page (keepAliveTimeout and issue 301 workaround, legacyAuthCache fields and 6.10.0, dotfiles values, hideStaticLogs, hidePingLogs, max_body_size, user_agent). Removed: the closing Verify tip.
Method: documentation only; no commands were run.
