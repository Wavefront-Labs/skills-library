---
id: computing-software.cloud-infrastructure-engineering.graylog.roles-sharing-and-teams
name: roles-sharing-and-teams
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [roles, sharing, teams, permissions, rbac]
level: practitioner
status: docs-checked
description: "Graylog permissions need both a role and sharing of the entity; Reader or Admin base roles; create teams manually or sync them."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/permission_management.html
  - https://go2docs.graylog.org/current/setting_up_graylog/manage_teams.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# roles sharing and teams

A user needs two things for an entity: a **role** granting access to that entity type, and the entity **shared** with them.

- Every user has the Reader or Admin role; new users default to Reader.
- Roles can be assigned to users directly or through teams.
- With an identity source, group sync (Enterprise) populates teams. Without one, create teams manually.

Create a team at **System > Users and Teams > Teams Overview > Create team**: Name and Description, assign users, assign roles, Create team. Administrators only; teams are an Enterprise feature. Click Assign User after choosing users. Teams created through an identity provider cannot be edited in Graylog; change membership and roles in the provider.

Roles describe capabilities (Reader/Viewer, Manager, Creator types) and do not grant access to entities. Sharing does, at three levels: Viewer, Manager, and Owner (Manager plus the ability to share). Sharing is required only for non-Admin users; Admins see every entity. A new Reader with nothing shared has no access to Graylog resources.

Default collections can be assigned to a team only when editing it; shareable entities created by members then land in those collections.

## Checked

Method: docs-checked 2026-11-09 against https://go2docs.graylog.org/current/setting_up_graylog/permission_management.html and https://go2docs.graylog.org/current/setting_up_graylog/manage_teams.htm (both read in full). Dropped the unsourced Cluster Configuration Reader role sentence.
