---
id: computing-software.systems-network-administration.paperless-ngx.share-links
name: share-links
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, share-links, email-sharing, bundle, public-link, smtp]
level: practitioner
status: docs-checked
description: "Share documents outside Paperless-ngx with expiring public share links, bundled ZIP links and email, and what to watch behind a proxy."
sources:
  - "https://docs.paperless-ngx.com/usage/"
  - "https://docs.paperless-ngx.com/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharing documents

Internally, share by granting other users permissions on the document. Externally you have share links, email, and email or webhook workflow actions.

## Share links
Created and managed under the Send button on the document detail screen, or from the bulk editor.
- Public: no login required. Links have the form `{paperless-url}/share/{randomly-generated-slug}`.
- Optional expiration time. After a link expires or is deleted, users are redirected to the regular login.
- Only document owners can create share links, and the user needs the ShareLink permission (add, delete or view share links).
- From the bulk editor you can create a share link bundle for a selection: Paperless-ngx prepares a ZIP archive in the background and exposes a single share link. The "Manage share link bundles" dialog lets you monitor progress, retry failed bundles or delete links.
- `PAPERLESS_SHARE_LINK_BUNDLE_CLEANUP_CRON` controls removal of expired bundles and their ZIP archives (default `0 2 * * *`; `disable` stops automatic cleanup).

If your instance is behind a reverse proxy, you may want an exception that bypasses any authentication layer so links are truly publicly accessible. Do so with caution.

## Email
Once an SMTP server is configured, the Send button on the document detail page includes an Email option. The same settings power the Email workflow action and password reset:
```bash
PAPERLESS_EMAIL_HOST=<SMTP_HOST>
PAPERLESS_EMAIL_PORT=<PORT>
PAPERLESS_EMAIL_HOST_USER=<USER>
PAPERLESS_EMAIL_HOST_PASSWORD=<PASSWORD>
PAPERLESS_EMAIL_FROM=<FROM_ADDRESS>
PAPERLESS_EMAIL_USE_TLS=true
```
Defaults: host `localhost`, port 25, TLS and SSL false, from address equal to `PAPERLESS_EMAIL_HOST_USER`.

Password reset also needs `PAPERLESS_URL` (and/or its corresponding settings) to be set.

## Checked
Date: 2026-11-07
Pages read in full: usage (docs/usage.md), configuration (docs/configuration.md).
Corrections: replaced "exempt the share path" with the usage tip wording (no path pattern is named); replaced invented example values (a hostname and port 587) with placeholders; added the bundle cleanup setting.
Method: documentation only; no commands were run.
