---
id: computing-software.rpa-and-low-code.n8n.understand-instance-roles
name: understand-instance-roles
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, roles, owner, admin, member, chat-user, permissions]
level: practitioner
status: docs-checked
description: "Know the four built-in n8n instance roles Owner, Admin, Member and Chat user, what each can do, and what changing a user to Chat user removes."
sources:
  - https://docs.n8n.io/administer/manage-users-and-access/understand-instance-roles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: pick the right instance role. Every user has one. Instance roles apply across the instance; project roles (RBAC) apply per project. Custom instance roles give granular permissions without full Admin.

Availability: **Admin** and **Chat user** need n8n Cloud Pro/Enterprise or self-hosted Enterprise. Chat user also requires the Chat feature.

## Permissions (Owner / Admin / Member / Chat user)
- Manage own email and password: all four.
- Manage own workflows; view, create and use tags: Owner, Admin, Member.
- Delete tags: Owner, Admin.
- View and share all workflows; view, edit and share all credentials; set up and use source control; create projects; view all projects; add and remove users: Owner and Admin only.
- Access the n8n Cloud console: Owner only.

## Advice
Owners should create a second **Member** account for building. Owners see and edit everything, and n8n cannot show who created a workflow, so you risk overriding others' work.

## Chat user
Can send Chat messages, create/edit/delete own Chat agents, run shared workflows and agents. Cannot create/view/edit workflows or credentials, create projects, view projects they do not belong to, or create API keys. n8n opens Chat after sign-in.

Changing a user to Chat user: removes them from shared projects (blocked if sole project admin: assign another admin first), makes their personal project read-only, and deletes their API keys. Changing back restores personal project ownership but not lost projects or keys.

## Checked
Method: docs-checked 2026-11-09 against the n8n "Understand instance roles" page (docs.n8n.io, read in full).
Nothing removed; availability, the permission table and Chat user effects match the page.
