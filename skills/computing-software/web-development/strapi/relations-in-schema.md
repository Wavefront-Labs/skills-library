---
id: computing-software.web-development.strapi.relations-in-schema
name: relations-in-schema
category: computing-software
field: web-development
product: strapi
tags: [strapi, relations, inversedby, mappedby, onetoone, manytoone, schema]
level: practitioner
status: docs-checked
description: "Declare Strapi relations in schema.json: relation kinds, target, and inversedBy/mappedBy on the owning and inverse sides."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/models.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Relations in the schema

Attribute with `type: 'relation'` plus:

- `relation`: `oneToOne`, `oneToMany`, `manyToOne` or `manyToMany`
- `target`: target content-type
- `mappedBy` / `inversedBy` (optional): in bidirectional relations the owning side declares `inversedBy`, the inversed side declares `mappedBy`.

One-to-one is unidirectional (only one side can query the other) or bidirectional.

Bidirectional one-to-one, article side:

```json
attributes: {
  category: {
    type: 'relation',
    relation: 'oneToOne',
    target: 'category',
    inversedBy: 'article',
  },
},
```

Category side:

```json
attributes: {
  article: {
    type: 'relation',
    relation: 'oneToOne',
    target: 'article',
    mappedBy: 'category',
  },
},
```

One-to-many is always bidirectional, usually defined with its many-to-one counterpart. Example on the "many" side:

```json
owner: {
  type: 'relation',
  relation: 'manyToOne',
  target: 'api::person.person',
  inversedBy: 'plants',
},
```

To change links at request time see `computing-software.web-development.strapi.relations-connect-disconnect-set`.

## Checked

Checked 2026-11-04 against the Strapi Models page (relations table, one-to-one, one-to-many and many-to-one examples). Nothing removed.

Method: documentation only; no commands were run.
