---
id: computing-software.ai-ml-engineering.open-webui.design-groups-and-resource-access-grants
name: design-groups-and-resource-access-grants
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [rbac, groups, nested-groups, access-grants, sharing, default-models, open-webui]
level: practitioner
status: docs-checked
description: "Structure Open WebUI groups (nested, permission vs sharing), share models and knowledge with read or write grants, and audit access with Preview."
sources:
  - https://docs.openwebui.com/features/authentication-access/rbac/groups
  - https://docs.openwebui.com/features/authentication-access/rbac/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: organise users into groups and control who can read or write each resource.

## Create and nest groups
Admin Panel > Users > Groups. Fields: name, description, parent group, default models, permissions, members. Drag a group onto another to nest it (or onto **Move to top level**). Subgroup members inherit the parent's permissions and access to every shared resource, all the way up. Loops are rejected by the server. Deleting a group lifts its subgroups one level and deletes its permissions, memberships and access grants.

Groups can also come from sync: with `ENABLE_OAUTH_GROUP_MANAGEMENT` memberships follow OAuth claims, and `ENABLE_OAUTH_GROUP_CREATION` auto-creates missing groups (they start at top level; you can then place them under a parent).

## Who can share to this group
`DEFAULT_GROUP_SHARE_PERMISSION` sets the default for new groups (Members). Options: **Anyone**, **Members** (only members, direct or via subgroups, see it in sharing menus), **No one** (hidden from non-admins).

## Recommended pattern
- Permission Groups (e.g. `[Perms] Web Search`): share setting **No one**, carry the toggles.
- Sharing Groups (e.g. `Marketing`): share setting Members/Anyone, ALL permissions off. Permissions are additive (True wins, no deny), so a group with Web Search on would override a later global switch-off.

## Default models per group
General tab > Default models replaces the instance Selected Models for members. Deepest group wins; at equal depth the group created first wins; a user's own "Set as default" still comes first. Hidden or inaccessible models are dropped.

## Share a resource
Set a model/knowledge base/prompt/tool/skill to **Private**, then **Add Access** for groups or users with Read or Write. Read = view and use. Write = owner-equivalent: update, delete and re-share (limited by the sharer's own sharing permissions). **Public** is one extra grant (read for every signed-in user, wildcard `*` principal); a Write row on a Public resource lets that group edit it while everyone can use it. Stored grants have resource, principal (group or user) and permission `read`/`write`.

Private means owner-only for workspace items (admins see them only if `BYPASS_ADMIN_ACCESS_CONTROL` is on, the default, or are granted). External tool servers, MCP servers, Open Terminal connections and arena models have no owner: private = admin-only until granted.

## Verify
Admin-only Preview Access: eye icon on a user row in Admin Panel > Users, or the group editor's Preview tab. API: `GET /api/v1/users/{user_id}/preview`, `GET /api/v1/groups/id/{id}/preview`.

## Gotchas
- Changes apply instantly; open tabs reconnect and reload permissions, models, tools, skills, channels.
- Member counts show direct members only; the Inherited tab shows subgroup people.
- Models with attached knowledge bases only see those KBs.

## Checked
2026-11-04. Confirmed against the Open WebUI docs pages features/authentication-access/rbac/groups and rbac/index (both read in full): group fields, nesting and drag and drop, loop rejection, deletion behaviour, OAuth group sync variables, DEFAULT_GROUP_SHARE_PERMISSION and its three options, the permission versus sharing group pattern and additive permissions, default models resolution, Read and Write grant semantics, Public as a wildcard grant, what Private means per resource type, Preview Access and its two API paths, and the knowledge scoping note. Nothing removed.
Method: documentation only; no commands were run.
