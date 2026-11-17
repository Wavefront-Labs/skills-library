---
id: computing-software.messaging-and-integration.ntfy.web-push-config
name: web-push-config
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, web-push, vapid, web-push-public-key, pwa]
level: advanced
status: docs-checked
description: "Enable Web Push on a self-hosted ntfy server: generate keys with ntfy webpush keys and set the web-push-* options."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/pwa.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web Push on the server

Web Push must be configured for background notifications and the PWA to work on a self-hosted server.

```
ntfy webpush keys
```

prints a key pair. Then set:

```yaml
web-push-public-key: "..."
web-push-private-key: "..."
web-push-file: "/var/cache/ntfy/webpush.db"
web-push-email-address: "admin@example.com"
```

Other keys: `web-push-startup-queries`, `web-push-expiry-warning-duration` (default `55d`), `web-push-expiry-duration` (default `60d`).

## Gotchas

- Background web push requires HTTPS with a valid certificate.
- Do not set `web-push-file` together with `database-url`.
- Web Push works only for the same server that hosts the web app, not for topics on another server.
- Persist `web-push-file` across restarts; if it is lost, web apps that are not open stop receiving pushes until opened again.
- Changing the keypair is not recommended: clients cannot re-subscribe until the user clears the notification permission.

## Checked

2026-11-04. Confirmed against the ntfy config page (Web Push: ntfy webpush keys, web-push-* options, 55d/60d defaults, HTTPS, same-server limit) and PWA page. Added: persistence and key-change cautions. Removed: the Verify step.
Method: documentation only; no commands were run.
