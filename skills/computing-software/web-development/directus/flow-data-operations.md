---
id: computing-software.web-development.directus.flow-data-operations
name: flow-data-operations
category: computing-software
field: web-development
product: directus
tags: [flow-create-data, flow-read-data, flow-update-data, flow-delete-data]
level: practitioner
status: docs-checked
description: "Use the Directus flow Create, Read, Update and Delete Data operations: permissions scope, emit events, IDs versus query, and the appended payloads."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/06.flows/4.operations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All four operations have **Collection**, **Permissions** (scope of permissions the operation runs with) and **Emit Events** (toggle whether the event is emitted).

- **Create Data**: payload defines the item(s). Appends an array of created IDs.
- **Read Data**: select by IDs or a Query using filter rules. Appends an array of items read.
- **Update Data**: select by IDs or Query. Payload formats: one object applied to the selected items; one object with keys and data to update multiple items to the same values; or an array of objects including primary keys to set different values. Appends the updated items.
- **Delete Data**: IDs or Query. Appends an array of deleted IDs.

Gotchas:
- Payload requirements match the Items API reference.

## Checked

2026-11-04: confirmed against the Directus docs Operations page (Create, Read, Update, Delete Data): options, ID or query selection, update payload formats, appended payloads. Removed the event re-trigger gotcha, the narrowest-scope advice and the verify line, none of which the page states.

Method: documentation only; no commands were run.
