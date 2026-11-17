---
id: computing-software.systems-network-administration.netbox.webhook-jinja-templates
name: webhook-jinja-templates
category: computing-software
field: systems-network-administration
product: netbox
tags: [webhooks, body-template, jinja2]
level: practitioner
status: docs-checked
description: "Build URLs, headers and bodies from event context."
sources: ["https://netboxlabs.com/docs/netbox/integrations/webhooks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Webhooks

Goal: send customized HTTP requests to remote systems when objects change.

Webhooks are configured through event rules. Jinja2 templating is supported in the `url`, `additional_headers` and `body_template` fields.

**Slack example from the docs**

- Object type: IPAM > IP address
- HTTP method: POST
- URL: your Slack incoming webhook URL
- HTTP content type: `application/json`
- Body template:

```
{"text": "IP address {{ data['address'] }} was created by {{ request.user }}!"}
```

**Template context**

- `event`: created, updated or deleted
- `timestamp`: ISO 8601
- `object_type`: `app_label.model_name`
- `request`: with `id` (UUID), `method`, `path`, `path_info`, `GET`, `user`
- `data`: the object's current detailed representation, typically equal to its REST API form
- `snapshots`: minimal `prechange` and `postchange` states
- `object_change_ids`: change log record IDs for the event

**Security.** Webhooks accept user-submitted code to generate the URL, headers and payload, which may pose risks. Grant permission to create or modify webhooks only to trusted users.

**Checklist**

1. Use only listed context variables.
2. Match content type to the body.
3. Restrict who edits webhooks.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Webhooks page: Jinja2 fields, Slack example, template context variables (event, timestamp, object_type, request, data, snapshots, object_change_ids), security warning. Removed: Nothing.

Method: documentation only; no commands were run.
