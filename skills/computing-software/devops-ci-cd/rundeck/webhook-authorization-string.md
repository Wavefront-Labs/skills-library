---
id: computing-software.devops-ci-cd.rundeck.webhook-authorization-string
name: webhook-authorization-string
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, webhooks, authorization-header, webhook-user, api-40]
level: practitioner
status: docs-checked
description: "Secure a Rundeck webhook with an HTTP Authorization string, call it with curl, regenerate it, and avoid the webhook user pitfalls."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/webhooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Webhook administration (released in 4.0) is under `Webhooks` in the project. Webhooks can also be managed through the Webhook API or the rd CLI. Each webhook is processed by a Webhook Event plugin (built-in handlers include Run Job and Log Events; several others are commercial).

Add an Authorization string:
1. Create or edit the webhook and tick *Use Authorization Header*.
2. Save. A box shows the generated string. It is shown only once; copy it before leaving the page.
3. Send it as an `Authorization` header:

```bash
curl --request POST 'http://your.rundeck.domain:4440/api/40/webhook/<webhook-token>' \
  --header 'Authorization: <the-authorization-string>' \
  --header 'Content-Type: application/json' \
  --data-raw '{"messages": {"field1": "value1"}}'
```

To rotate, click **Regenerate** on the webhook; the new value shows after saving.

Gotchas:
- The `Webhook User` cannot be changed after creation; the field becomes read only.
- The user must have logged into Rundeck at least once, otherwise saving fails with a user-not-found validation error.

## Checked

2026-11-04: administration, authorization string behaviour, curl form, regenerate and the two Webhook User tips confirmed against the Webhooks page.
Method: documentation only; no commands were run.
