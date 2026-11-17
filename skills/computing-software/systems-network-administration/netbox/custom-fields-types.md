---
id: computing-software.systems-network-administration.netbox.custom-fields-types
name: custom-fields-types
category: computing-software
field: systems-network-administration
product: netbox
tags: [custom-fields, cf-prefix, custom-field-data]
level: practitioner
status: docs-checked
description: "Add extra attributes to models with typed custom fields."
sources: ["https://netboxlabs.com/docs/netbox/customization/custom-fields/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom fields

Goal: store attributes that do not belong in the core schema.

Custom fields are stored as JSON alongside each object, so retrieval needs no complex queries. Create them under Customization > Custom Fields.

**Types:** text, long text (Markdown), integer, decimal (4 decimal places), boolean, date (ISO 8601), date and time, URL, JSON, selection, multiple selection, object, multiple object (the object types use `object_type`).

**Naming.** `name` is database-friendly: only alphanumerics and underscores (for example `tps_report`). A separate label can be human-friendly.

**Options.** Mark a field required to force a value on create and save. A default may be supplied; use "true" or "false" for boolean defaults.

**Assign** each field to one or more object types. It then appears in the web UI and REST API. Not all models support custom fields.

**Behaviour change in v4.6.8.** Empty values are no longer pre-provisioned. Creating a field without a default writes nothing to existing objects, so the key is absent from `custom_field_data` until a value is set. Read it with `obj.cf['field_name']`. A default is written to every existing object when created.

**Checklist**

1. Pick the right type.
2. Use `obj.cf[...]` in scripts.
3. Remember defaults backfill.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Custom fields page: the list of field types (decimal 4 places, ISO 8601 dates), naming rule, required/default behaviour, v4.6.8 change with obj.cf['field_name'], object_type for object fields. Removed: The claim that custom fields are queried with a cf_ prefix (not on this page).

Method: documentation only; no commands were run.
