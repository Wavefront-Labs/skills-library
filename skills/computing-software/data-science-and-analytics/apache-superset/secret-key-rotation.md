---
id: computing-software.data-science-and-analytics.apache-superset.secret-key-rotation
name: secret-key-rotation
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [secret-key, rotation, re-encrypt-secrets, encryption, previous-secret-key]
level: advanced
status: docs-checked
description: "Generate and rotate the Superset SECRET_KEY: openssl generation, PREVIOUS_SECRET_KEY, re-encrypt-secrets and the related JWT secrets."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/configuring-superset.mdx
  - https://github.com/apache/superset/blob/master/docs/admin_docs/security/securing_superset.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set a strong `SECRET_KEY` and rotate it without losing encrypted metadata.

Superset requires a user-specified `SECRET_KEY` to start (since 2.1.0). It signs session cookies and is key material for encrypting sensitive values stored in the metadata database such as database passwords. Generate one:

```bash
openssl rand -base64 42
```

Set `SECRET_KEY` in `superset_config.py` or use the `SUPERSET_SECRET_KEY` environment variable. Never reuse a key across environments or instances: a shared key lets a signed session cookie work on every instance, which can lead to authentication bypass.

Rotation:
1. Put the current key in `superset_config.py` as `PREVIOUS_SECRET_KEY` and the new key as `SECRET_KEY`. To read the current key, run `superset shell` (inside the container with Docker) and print `current_app.config["SECRET_KEY"]`.
2. Run:

```bash
superset re-encrypt-secrets
```

The security guide recommends rotating the key quarterly and after any security incident, keeping it in a secrets manager rather than `superset_config.py` or version control, and following the configuration guide's rotation procedure precisely to avoid locking yourself out.

Other secrets to inventory and rotate on the same cadence: `GUEST_TOKEN_JWT_SECRET` (embedded dashboard guest tokens) and `WEBSOCKET_JWT_SECRET`. Rotating either invalidates outstanding tokens of that type. For the websocket secret, set the outgoing value as `PREVIOUS_JWT_SECRET` on the websocket server so it keeps verifying old cookies, then remove it once they have aged out. After a suspected compromise rotate all of them.

## Checked

2026-11-08. Confirmed against the Configuring Superset page (SECRET_KEY sections, read in full) and the Securing Superset page (SECRET_KEY management, Appendix B and C, checked by search and reading). Removed: "remove PREVIOUS_SECRET_KEY after it completes", the claim that imports are re-encrypted with the current key, `PREVIOUS_JWT_SECRET` for the guest-token secret (the page ties it to the websocket secret only), and "every web server and worker" wording.
Method: documentation only; no commands were run.
