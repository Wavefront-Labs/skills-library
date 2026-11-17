---
id: computing-software.web-development.directus.flow-event-hook-trigger
name: flow-event-hook-trigger
category: computing-software
field: web-development
product: directus
tags: [flow-event-hook, filter-blocking, action-non-blocking, cancel-transaction]
level: practitioner
status: docs-checked
description: "Configure a Directus flow event hook trigger as blocking filter or non-blocking action, replace the payload via Response Body, and cancel transactions."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/06.flows/3.triggers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Event hook triggers fire on platform events and mirror custom API hooks. Event data is nested in `$trigger`.

Options: **Type**, **Scope** (which events), **Collections**, and **Response Body** (filter only).

- **Filter (Blocking)**: pauses the transaction, copies the `payload` into the flow, lets the whole flow run, optionally replaces the payload, then resumes the database transaction. On `items.created` the item has no ID yet.
- **Action (Non-Blocking)**: the event commits without waiting; faster, but cannot validate or transform. A payload copy is still in `$trigger`.

Response Body (filters): Data of Last Operation (`$last`), All Data (whole chain), or Other (an `<operationKey>`). With none configured the payload is unmodified but you can still cancel.

To cancel the transaction: throw an error in a Run Script operation, or end the flow on a failure path (a condition ending on its reject path also cancels).

Gotcha: creating several items in one request runs the flow once per item, each with one item in the payload.

## Checked

2026-11-04: confirmed against the Directus docs Triggers page (Event Hook section): options, filter and action behaviour, items.created note, Response Body choices, cancelling transactions, one run per item. Removed the unsupported verify line.

Method: documentation only; no commands were run.
