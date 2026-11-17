---
id: computing-software.systems-network-administration.netbox.event-rules-conditions
name: event-rules-conditions
category: computing-software
field: systems-network-administration
product: netbox
tags: [event-rules, conditional-logic, redis-queue]
level: practitioner
status: docs-checked
description: "Trigger scripts, webhooks or notifications on object changes with JSON conditions."
sources: ["https://netboxlabs.com/docs/netbox/features/event-rules/", "https://netboxlabs.com/docs/netbox/installation/4a-gunicorn/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Event rules

Goal: react automatically to changes inside NetBox.

Event rules can execute a custom script, send a webhook, or generate user notifications. Example from the docs: start monitoring a device when its operational status becomes active and stop for any other status, using a webhook.

**Requirements.** Each rule must be associated with at least one NetBox object type and at least one event (create, update or delete).

**Conditions.** A rule may carry JSON conditional logic that decides whether an event fires for a specific object:

```json
{
  "and": [
    {"attr": "status.value", "value": "active"}
  ]
}
```

Here the rule triggers only for objects whose status is active. The syntax is the same conditional logic documented in the reference section.

**Processing.** When a change is detected, resulting events are placed into a Redis queue. The user's request completes without waiting for outgoing events; the `rqworker` process then extracts events from the queue. The current queue and any failed events can be inspected under System > Background Tasks. In the standard install the worker runs as the `netbox-rq` service.

**Checklist**

1. Pick object types and events.
2. Add conditions to avoid noisy triggers.
3. Confirm the worker service is running.

## Checked

Method: docs-checked 2026-11-09 against the NetBox Event Rules feature page and the Gunicorn installation page (both read in full).
