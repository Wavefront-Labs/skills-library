---
id: computing-software.web-development.ghost.ghost-admin-api-create-and-update-members
name: ghost-admin-api-create-and-update-members
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, members, labels, newsletters, subscribers]
level: practitioner
status: docs-checked
description: "Create and update Ghost members via the Admin API: email is the only required field, plus name, note, labels and newsletters."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/members/creating-a-member.mdx
  - https://github.com/TryGhost/docs/blob/main/admin-api/members/updating-a-member.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add or change members from a script.

Create: `POST /admin/members/` with body `{"members":[{"email":"jamie@example.com"}]}`. At minimum an email is required and the result is a free member.

Additional writable fields:
- `name`: the member's name.
- `note`: notes on the member.
- `labels`: member labels.
- `newsletters`: the newsletters this member is subscribed to.

Example: `{"members":[{"email":"jamie@example.com","name":"Jamie","labels":[{"name":"VIP","slug":"vip"}],"newsletters":[{"id":"<newsletter id>"}]}]}`.

Update: `PUT /admin/members/{id}/`. All writable fields can be changed. The docs recommend fetching the latest data with GET first, then sending the change, for example `{"members":[{"name":"Jamie Doe"}]}`.

Verify: GET the member and check the labels and newsletter subscriptions match what you sent.

## Checked

2026-11-04. Confirmed: POST and PUT paths, email as the only required field, the free-member result, writable fields name, note, labels and newsletters, and the GET-before-update recommendation (creating and updating a member pages). Removed: labels shown as plain strings (the page shows label objects); the bulk-import, duplicate-error, note-field and default-newsletter-behaviour paragraphs, which no page states.

Method: documentation only; no commands were run.
