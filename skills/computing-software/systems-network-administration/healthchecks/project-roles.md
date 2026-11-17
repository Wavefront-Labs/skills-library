---
id: computing-software.systems-network-administration.healthchecks.project-roles
name: project-roles
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, project-roles, team-access, owner-manager-member, read-only-role]
level: practitioner
status: docs-checked
description: "Healthchecks project team roles and permissions: owner, manager, team member and read-only, and how to invite members or leave a team."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/projects_teams.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Roles:
- Owner: created the project. Can transfer it to another account, manage billing and remove the project.
- Manager: all Team Member permissions plus inviting and removing team members. Cannot change or remove the owner or manage billing.
- Team Member: create, edit and delete checks; create and delete integrations; rename the project; view or regenerate API keys. Cannot invite members, change the owner, manage billing or remove the project.
- Read-only: view checks, details, ping logs and integrations. Cannot modify anything and cannot access API keys.

Invite members from the project's Settings page, Team Access section.

Every role except Owner can leave the team from Account Settings.

Each project has its own API keys and team (see api-authentication).

Reports cover all projects you own or belong to (see email-reports).

## Checked

2026-11-04. Confirmed against the Healthchecks Projects and Teams page: the Owner, Team Member, Manager and Read-only roles and their permissions, inviting from the project Settings page, leaving a team from Account Settings, and reports covering all accessible projects. Removed a recommendation about stakeholders that the page does not make. The Owner permissions are inferred from the lists of what Team Members cannot do.

Method: documentation only; no commands were run.
