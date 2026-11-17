---
id: computing-software.data-engineering.metabase.collection-permissions
name: collection-permissions
category: computing-software
field: data-engineering
product: metabase
tags: [collection-permissions, curate, personal-collections, sub-collections, inheritance]
level: practitioner
status: docs-checked
description: "Set Metabase collection permissions: Curate, View and No access, additive group inheritance, sub-collection toggle, dashboard card access and personal collection rules."
sources:
  - https://www.metabase.com/docs/latest/permissions/collections
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Levels: Curate (view, edit, move, delete, pin items, create subcollections, manage events), View (see items and timelines), and No access (the collection is hidden).

Scope: collection permissions apply only to viewing and curating existing questions, models and dashboards. Editing a query or creating a question also needs data permissions. A Blocked data permission hides questions even from users with Curate access.

Dashboards: users need access to every collection that holds a card on the dashboard.

Inheritance:
- Additive across groups; the most permissive setting wins, so Curate for All Users gives every user Curate.
- Changes do not reach existing subcollections unless you toggle "Also change sub-collections".
- New subcollections inherit the parent's access.
- Users can reach a deep collection without access to its parents, and it appears at the top level they can reach.

Personal collections: every user can always save there; their permissions are fixed. Admins can view and edit all users' personal collections.

Other gotchas:
- "Our analytics" and personal collections cannot be archived.
- Do not use collection permissions for Library, Data; use data permissions.
- Only admins can edit collection permissions.
- View access includes each item's query definition, including SQL of native questions and via the API, even without Create queries permission; withhold collection access to hide a query.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Claims matched the page; added the page's note that View access exposes query definitions. Otherwise unchanged.
