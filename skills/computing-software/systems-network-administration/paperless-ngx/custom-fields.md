---
id: computing-software.systems-network-administration.paperless-ngx.custom-fields
name: custom-fields
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, custom-fields, document-link, monetary, custom-field-query, data-types]
level: practitioner
status: docs-checked
description: "Create typed custom fields, know the available types and rules, and query them in the document list, API and workflows."
sources:
  - "https://docs.paperless-ngx.com/usage/"
  - "https://docs.paperless-ngx.com/api/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom fields

Create a field under Manage with a name and data type, then add it to documents from the Custom Fields menu on the document detail page. Nothing is stored until you press Save.

## Rules
- A field's data type cannot be changed once set.
- The same field name can appear only once per document.
- Only a document's owner can add or remove custom fields.

## Types
Text, Boolean, Date, URL, Integer, Number (float), Monetary (an ISO 4217 code plus exactly two decimals, such as USD12.30), Document Link (links other documents and creates the reverse link automatically) and Select (a predefined list).

## Using them
- Workflow assignment can add a field, with or without a value.
- Filename templates can read them with `get_cf_value`.
- The API upload accepts `custom_fields` as ids or an id-to-value object.
- Filter in the API with `custom_field_query`, for example `["due", "range", ["2024-08-01", "2024-09-01"]]`.
- Full-text search: `custom_fields.name:"Contract Number" custom_fields.value:1312`. Custom date fields do not support relative syntax such as `[now to 2 weeks]` there; use the list filters instead.

## Bulk
The bulk edit method `modify_custom_fields` adds or removes fields on many documents at once.

## Checked
2026-11-04. Compared with the Custom Fields section and Searching custom fields in usage, and the custom field recipes in the API page (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: creation under Manage, Save requirement, immutable data type, one instance per name, owner-only add/remove, all nine types including the Monetary format and Document Link reverse link, workflow assignment, get_cf_value, search syntax and the date note. Nothing removed.

Method: documentation only; no commands were run.
