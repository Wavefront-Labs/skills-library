---
id: computing-software.messaging-and-integration.prosody.mod-http-file-share
name: mod-http-file-share
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, file-upload, xep-0363, http, component, quota]
level: practitioner
status: docs-checked
description: "Set up mod_http_file_share in Prosody: upload component, http_host reuse, size limit 10 MiB, daily quota, expiry, allowed types and access control."
sources:
  - https://prosody.im/doc/modules/mod_http_file_share
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_http_file_share

XEP-0363 HTTP File Upload, available since Prosody 0.12.0. Add a component at the end of the config and restart:

```lua
Component "upload.example.org" "http_file_share"
```

It needs a certificate for that name. To avoid a separate DNS record and certificate set `http_host = "example.com"` (and optionally `modules_disabled = { "s2s"; }`). Behind a reverse proxy use `http_host` plus `http_external_url = "https://upload.example.com/"`. If the domain is not a subdomain of your VirtualHost, advertise it via `disco_items`.

| Setting | Default |
|---|---|
| `http_file_share_size_limit` | 10 MiB |
| `http_file_share_daily_quota` | 100 MiB per user per day |
| `http_file_share_global_quota` | unlimited |
| `http_file_share_expires_after` | 1 week (`"never"` disables) |
| `http_file_share_allowed_file_types` | `{}` (no restriction) |
| `http_file_share_access` | `{}` (any local user) |

```lua
http_file_share_size_limit = 16*1024*1024
http_file_share_expires_after = "31 days"
http_file_share_allowed_file_types = { "image/*" }
```

Verify: `prosodyctl shell http list upload.example.com` shows the `/file_share` URL.

## Checked

2026-11-04. Read the mod_http_file_share page: available from 0.12.0, the Component line, http_host and http_external_url single-domain and proxy setups, disco_items, the settings table defaults (10 MiB size limit, daily quota 10x the limit, unlimited global quota, 1 week expiry with "never", access and allowed types) and the prosodyctl shell http list command all match. Nothing removed. The page notes the expiry setting is a number of seconds in 0.12.x.

Method: documentation only; no commands were run.
