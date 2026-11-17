---
id: computing-software.cybersecurity-defensive.zitadel.http-webhook-notification-provider
name: http-webhook-notification-provider
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, webhook, notifications, sms, email, http-provider]
level: advanced
status: docs-checked
description: "Deliver ZITADEL emails and SMS through your own service by creating and activating an HTTP provider through the admin API."
sources:
  - https://zitadel.com/docs/guides/manage/customize/notification-providers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An HTTP provider sends the message and its data as JSON to a webhook you define. You then deliver the message yourself or through any provider, with full control of content.

SMS flow: create the provider with the admin API, then activate it.

```bash
curl -L "https://${CUSTOM_DOMAIN}/admin/v1/sms/http" \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"endpoint": "http://relay.example.com/provider", "description": "provider description"}'
```

`endpoint` is the webhook that receives the data. The result contains the provider ID. Activate it with a call to `/admin/v1/sms/:id/_activate` using that ID and an empty JSON body `{}`.

Email uses the same pattern with `/admin/v1/email/http` for creation. You can configure multiple providers at once, but only the active one delivers.

The payload has three parts: `contextInfo` (why the message is sent: event type, which provider, the recipient), `templateData` (texts and format information for a template) and `args` (user data usable to customize the message).

## Checked

2026-11-08. Read the notification providers page in full; removed two unsupported advice lines and added the payload structure.

Method: documentation only; no commands were run.
