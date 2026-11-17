---
id: computing-software.devops-ci-cd.semaphore-ui.project-alerts-and-teams
name: project-alerts-and-teams
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [alerts, project-alerts, rbac, roles, team, semaphore-ui]
level: practitioner
status: docs-checked
description: "Configure per-project alerts and understand Owner, Manager, Task Runner and Guest roles."
sources:
  - https://semaphoreui.com/docs/user-guide/alerts
  - https://semaphoreui.com/docs/user-guide/team
  - https://semaphoreui.com/docs/user-guide/task-templates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Project alerts and team roles

Goal: route notifications and set least-privilege access.

Alerts tab: Server channels card (switch on Send alerts of this project to server channels, optionally a per-project Telegram Chat ID) and Project alerts. Press New Alert and set Name (unique in the project), Type (Telegram, Slack, Email, Microsoft Teams, Rocket.Chat, DingTalk, Gotify) and the type's fields. Templates and schedules pick which alerts they use; Test all sends a test through every server channel and enabled alert.

Roles (Teams section, Members tab):
- Owner: everything, including roles and members. Keep two owners; only an admin can remove the last one.
- Manager: almost everything, creates and runs workflows, but cannot delete the project or change Owners.
- Task Runner: runs any template, runs and approves workflows, read-only on other resources.
- Guest: read-only (Can read project).

Enterprise Extended RBAC (v2.17+) adds custom roles with finer permissions on specific templates, without changing the built-in roles.

Template creation needs Manager or higher; starting a task needs Task Runner or higher.

Gotchas:
- A template with a custom alert list does not use server channels.
- Server-level administrators can access every project.

Verify: press Test all on the Alerts tab and confirm a test message reaches each enabled destination.

## Checked

2026-11-07. Read in full, from markdown sources in the semaphore-docs repository (no snippet files included): user-guide/alerts.md, user-guide/team.md and user-guide/task-templates/README.md. Confirmed: the Alerts tab layout, the send-to-server-channels switch and per-project Telegram Chat ID, the seven alert types and unique name, Test all, the four built-in roles with their limits, the last-owner rule, Enterprise Extended RBAC from v2.17, the custom-alert-set behaviour, admins reaching every project, and Manager-or-higher template creation. Removed: the Task Runner template-editing Verify step, which the pages do not state.
Method: documentation only; no commands were run.
