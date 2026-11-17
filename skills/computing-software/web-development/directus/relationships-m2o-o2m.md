---
id: computing-software.web-development.directus.relationships-m2o-o2m
name: relationships-m2o-o2m
category: computing-software
field: web-development
product: directus
tags: [relationship-m2o, relationship-o2m, alias-relation-field, reverse-navigation]
level: practitioner
status: docs-checked
description: "Model Many to One and One to Many relationships in Directus and add the O2M alias field so editors can navigate from the one side."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/01.data-model/5.relationships.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Many to One (M2O)**: a field on the "many" collection stores the primary key of the "one" collection. Examples: many cities to one country, orders to a customer, books to a publisher.

Gotcha: an M2O field does not by itself let editors navigate from the related collection back to its items.

**One to Many (O2M)**: one item is linked to multiple items in another collection. To navigate from the related collection, it needs an O2M field. Creating the O2M interface on an existing M2O relationship creates an `Alias` field, which is purely virtual and adds no database column, but gives an item-page interface to access the related items.

## Checked

2026-11-04: confirmed against the Directus docs Relationships page (Many to One and One to Many sections). Removed the invented step list, the display-template step and the verify line; reworded the O2M side to follow the page, which words the side of the M2O ambiguously.

Method: documentation only; no commands were run.
