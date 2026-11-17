---
id: computing-software.systems-network-administration.home-assistant.webhook-trigger
name: webhook-trigger
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [webhook, allowed-methods, local-only]
level: advanced
status: draft
description: "Start a Home Assistant automation from an HTTP request with a webhook trigger, restrict allowed methods and local_only, and follow webhook security rules."
sources:
  - https://www.home-assistant.io/docs/automation/trigger/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: let another system start an automation by calling a URL.

```yaml
automation:
  trigger_variables:
    webhook_id_variable: "template_webhook_id"
  triggers:
    - trigger: webhook
      webhook_id: "some_hook_id"
      allowed_methods:
        - POST
        - PUT
      local_only: true
    - trigger: webhook
      webhook_id: "{{ webhook_id_variable }}"
      allowed_methods:
        - POST
```

Call it:

```shell
curl -X POST -d 'key=value&key2=value2' http://your-home-assistant:8123/api/webhook/some_hook_id
```

JSON body:

```bash
curl -X POST -H "Content-Type: application/json" -d '{ "key": "value" }' http://your-home-assistant:8123/api/webhook/some_hook_id
```

Security rules from the docs. Webhook endpoints need no authentication beyond knowing the ID, so:

- Do not use webhooks for destructive or safety-relevant actions, such as unlocking a lock or opening a garage door.
- Treat the webhook ID like a password: unique, non-guessable, secret.
- Never copy IDs from public sources, including blueprints. Create your own.
- Keep `local_only` enabled unless internet access is required.

The webhook ID may be a template when it is built from `trigger_variables`, as the second trigger above shows. Request data is available to templates through the trigger data (see the trigger-data skill).
