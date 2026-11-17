---
id: computing-software.data-engineering.prefect.cloud-webhooks
name: cloud-webhooks
category: computing-software
field: data-engineering
product: prefect
tags: [webhooks, jinja, cloud, events, curl]
level: practitioner
status: docs-checked
description: "Create a Prefect Cloud webhook with a Jinja2 template that turns an HTTP POST into an event, then automate on it and debug failures."
sources:
  - https://docs.prefect.io/v3/how-to-guides/cloud/create-a-webhook
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn an external HTTP POST into a Prefect event.

Workflow:
1. In the Cloud UI open Webhooks, then Create Webhook; give a name and a Jinja2 template.
2. Cloud issues a unique URL: `https://api.prefect.cloud/hooks/YOUR_UNIQUE_WEBHOOK_ID`.
3. POST to it from the external system.
4. Find the event in the Event Feed, open it and click Automate to pre-fill a trigger.
5. Click Next and choose actions such as running a deployment or sending a notification.

Template: read body fields as `body.field_name` and headers as `headers['Header-Name']`.

```json
{
    "event": "model-update",
    "resource": {
        "prefect.resource.id": "product.models.{{ body.model_id}}",
        "prefect.resource.name": "{{ body.friendly_name }}",
        "run_count": "{{body.run_count}}"
    }
}
```

```bash
curl -X POST https://api.prefect.cloud/hooks/YOUR_UNIQUE_WEBHOOK_ID \
  -d "model_id=my_model_123" \
  -d "friendly_name=My Awesome Model" \
  -d "run_count=15"
```

Troubleshooting: look for `prefect-cloud.webhook.failed` events, which include request details and template rendering errors. Check the URL, HTTP method, headers and body, and that the template reads fields correctly.

The guide does not cover CLI commands, authentication or limits.

## Checked

2026-11-09. Confirmed: Create a webhook page (docs.prefect.io/v3/how-to-guides/cloud/create-a-webhook): UI steps, Jinja2 template, curl example, Event Feed, Automate button, prefect-cloud.webhook.failed troubleshooting. Nothing removed.

Method: documentation only; no commands were run.
