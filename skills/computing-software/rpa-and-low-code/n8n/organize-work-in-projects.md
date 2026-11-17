---
id: computing-software.rpa-and-low-code.n8n.organize-work-in-projects
name: organize-work-in-projects
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, projects, rbac, move-workflows, personal-credentials, members]
level: practitioner
status: docs-checked
description: "Manage n8n projects: create, add or remove members, delete with transfer, move workflows and credentials (which revokes sharing) and personal credentials in team projects."
sources:
  - https://docs.n8n.io/administer/manage-users-and-access/set-permissions-and-roles-rbac/organize-work-in-projects
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: group workflows and credentials and give users different roles per project. RBAC availability: Cloud all plans; self-hosted Registered Community, Business, Enterprise; project and role counts vary by plan.

## Operations
- Create: instance owners and admins only; fill settings, **Save**.
- Add member (project admins): project, **Project settings**, **Project members**, search by username or email, check the role, **Save**. Remove: three-dot menu, **Remove user**, **Save**.
- Delete: **Project settings**, **Delete project**, then either transfer workflows and credentials to another project or delete them (confirmed).
- Move: owners of a workflow or credential can move it to other users or projects they can access. Moving removes all existing sharing, which may break workflows that relied on it. When moving a workflow whose credentials you may share, you can share them too; n8n notes ones that cannot move. Confirm that workflows may stop working if the target lacks the credentials, then **Confirm move to new project**.

## Personal credentials in team projects
Members can pick their own credentials in any workflow in a team project; the selector groups **Available to you** and **Available in** the project. Only the owner and people they share with directly can run or publish with it. Share it with the project for everyone.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/administer/manage-users-and-access/set-permissions-and-roles-rbac/organize-work-in-projects

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
