---
id: computing-software.data-engineering.prefect.events-and-resources
name: events-and-resources
category: computing-software
field: data-engineering
product: prefect
tags: [events, follows, resource, related-resources, event-ordering]
level: practitioner
status: docs-checked
description: "Prefect event specification fields, event naming grammar, resource identifiers and related resources, and ordering with follows."
sources:
  - https://docs.prefect.io/v3/concepts/events
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: emit and reason about Prefect events.

Event fields: `occurred` (string, required), `event` (name, required), `resource` (object, required), `related` (array, optional), `payload` (object, optional), `id` (client-provided, required), `follows` (id of an earlier event, optional).

Names are arbitrary but should describe a resource and an action, for example `prefect.block.write-method.called` or `prefect-cloud.user.logged-in`.

Resources are dot-delimited identifiers such as `prefect.flow-run.e3755d32-cec5-42ca-9bcd-af236e308ba6` or `acme.user.kiki.elt_script_1`. They can carry labels used in aggregation, such as `prefect.resource.id`. Related resources use `prefect.resource.role` (for example `automation`).

Ordering: arrival time cannot give order, so set `follows` on the later event to the earlier event's `id`.
- Helps disambiguate events within a second or two; use it only in the same causal chain.
- `emit_event` sets the relationship automatically when the events occurred within five minutes of each other.
- Matters most for automation triggers using `after` and `expect`.

Responding: from an event detail page use the automate button; the default trigger fires on each event with a matching resource id. Advanced conditions use custom event triggers. Manage via CLI, the Terraform provider or the API.

The page gives no event size, rate or retention limits.

## Checked
2026-11-08. Confirmed against the Events concept page: the event specification fields and required flags, naming grammar and examples, resource examples and labels, related resources with prefect.resource.role, follows ordering rules, the five minute emit_event window, and the automate button. Nothing removed.
Method: documentation only; no commands were run.
