---
id: computing-software.web-development.strapi.webhooks-config-security
name: webhooks-config-security
category: computing-software
field: web-development
product: strapi
tags: [strapi, webhooks, defaultheaders, hmac, signature, replay]
level: advanced
status: docs-checked
description: "Configure Strapi webhook default headers in config/server and secure receivers with tokens and HMAC signature checks."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/webhooks.md
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/configurations/server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Webhooks

Webhooks send HTTP callbacks (typically POST) to other applications when content changes. They do not work for the User content-type; use lifecycle hooks for that.

## Default headers
In `./config/server`:

```js
module.exports = {
  webhooks: {
    defaultHeaders: {
      Authorization: `Bearer ${process.env.WEBHOOK_TOKEN}`,
    },
  },
};
```

Headers set on an individual webhook take precedence over `defaultHeaders`. Setting them in the admin panel must be done per webhook; `defaultHeaders` applies to all.

## Receiver verification
Webhook URLs are usually public, so authenticate and sign:
- Generate a shared secret in environment variables.
- Sender computes an HMAC (e.g. SHA-256) over the raw body plus a timestamp.
- Send signature and timestamp in headers (e.g. `X-Webhook-Signature`, `X-Webhook-Timestamp`).
- Receiver recomputes and compares with a constant-time check.
- Reject invalid signatures or timestamps that are too old (replay).

## Related server options
- `webhooks.deduplicateReleaseWebhooks`: skips individual `entry.publish`/`entry.unpublish` requests during a release publish when the webhook also subscribes to `releases.publish`.
- `webhooks.populateRelations` was removed in Strapi 5.

## Checked

Checked 2026-11-04 against the Strapi Webhooks page (User content-type note, default headers, security, verifying signatures) and the Server configuration page (`webhooks.defaultHeaders`, `webhooks.deduplicateReleaseWebhooks`, `webhooks.populateRelations`). Nothing removed.

Method: documentation only; no commands were run.
