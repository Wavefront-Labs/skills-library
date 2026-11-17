---
id: computing-software.web-development.directus.field-validation-conditions
name: field-validation-conditions
category: computing-software
field: web-development
product: directus
tags: [field-validation, field-conditions, conditional-fields, relational-triggers]
level: practitioner
status: docs-checked
description: "Add Directus field validation rules and conditions, show fields conditionally, and understand client then server validation and relational triggers."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/01.data-model/2.fields.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Validation** (field config > Validation): write rules and a custom message. Two stages run on submit: first client-side in the Studio, then on the Server, which re-runs the rules plus permission checks. These are Directus validations, not database constraints.

**Conditions** change a field based on other fields in the item: read-only, hidden, required, plus interface options.

Show a field conditionally:
1. Set `hidden` to true in the field settings.
2. Add a condition with a rule checking another field's value.
3. In that condition set hidden to false.

**Relational triggers** (relational fields) decide what happens when related values are deselected or deleted: set to `null`, set to default, or cascade/prevent the deletion.

**Display** options can include conditional styles (colors, icons, text) when data meets criteria.

Other field config sections: Schema, Field (read-only, required, note, name translations), Interface, Display.

## Checked

2026-11-04: confirmed against the Directus docs Fields page (Validation, Conditions, Relationships, Display, Field sections). Removed the verify line, which claimed direct API writes are rejected; the page only describes Studio then Server validation.

Method: documentation only; no commands were run.
