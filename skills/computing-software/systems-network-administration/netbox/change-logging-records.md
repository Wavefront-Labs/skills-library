---
id: computing-software.systems-network-administration.netbox.change-logging-records
name: change-logging-records
category: computing-software
field: systems-network-administration
product: netbox
tags: [change-log, object-changes, changelog-message]
level: practitioner
status: docs-checked
description: "Read object-change records, correlate by request ID and add changelog messages."
sources: ["https://netboxlabs.com/docs/netbox/features/change-logging/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Change logging

Goal: audit who changed what and why.

Whenever an object is created, updated or deleted, NetBox saves a serialized copy taken before and after the change, along with the time and the user. The JSON resembles REST API output but has no nested representations, so a tenant field holds the tenant's primary key.

**Request correlation.** Each request gets a UUID attached to every change record it creates. Bulk-editing three sites creates three records that share one request ID, so you can find everything one action touched.

**Access**

- Read-only endpoint: `/api/extras/object-changes/`.
- Export as CSV from the web UI.

**User messages.** A user may record an arbitrary message of up to 200 characters. In the UI the optional "Changelog message" field appears at the bottom of create forms, edit forms and delete confirmations. The REST API accepts the same message.

**Related features.** Journaling lets humans keep notes on any primary or organizational model, separate from automatic change records. Retention is controlled by a configuration setting.

**Checklist**

1. Ask users to fill the message field.
2. Query by request ID to group changes.
3. Use journals for narrative notes.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Change logging page: before/after serialization, request UUID, /api/extras/object-changes/, 200-character changelog message. Removed: Nothing.

Method: documentation only; no commands were run.
