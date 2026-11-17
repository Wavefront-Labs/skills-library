---
id: computing-software.messaging-and-integration.ntfy.webhooks-get-publish
name: webhooks-get-publish
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, webhooks, get, trigger, query-parameters]
level: intro
status: docs-checked
description: "Publish to ntfy with a plain GET to /publish, /send or /trigger using query parameters, for webhook senders that cannot POST."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Webhooks (publish via GET)

For services that can only call a URL, use `/publish` under the topic. Aliases: `/send` and `/trigger`.

```
https://ntfy.sh/mytopic/publish?message=Hello&priority=high&tags=warning,skull
```

- With no arguments the message is `triggered`.
- Every header-equivalent option can be passed as a URL-encoded query parameter (`message`, `title`, `priority`, `tags`, `click`, `delay`, `email` and so on). Query parameter names must be lowercase; aliases listed in the publish-parameter-aliases skill also work.
- Clients with limited HTTP support can also use `GET /<topic>/<sequence_id>/clear` (alias `/read`) and `GET /<topic>/<sequence_id>/delete`.

## Gotchas

- With `?auth=` your credentials are part of the URL; see the publish-authentication skill for the encoding.
- URL-encode special characters in message text.

## Authenticated webhooks

Add the `auth` query parameter with the base64 value described in the publish-authentication skill.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Webhooks (publish via GET): /publish, /send, /trigger, default triggered, parameters as query args; clear and delete GET forms). Removed: the logging gotcha and the Verify step.
Method: documentation only; no commands were run.
