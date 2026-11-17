---
id: computing-software.cybersecurity-defensive.zitadel.projects-applications-and-roles
name: projects-applications-and-roles
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, projects, applications, roles, default-project]
level: practitioner
status: docs-checked
description: "Group applications and roles in a ZITADEL project, understand role keys, and avoid changing the built-in default project."
sources:
  - https://zitadel.com/docs/guides/manage/console/projects-overview
  - https://zitadel.com/docs/guides/manage/console/applications-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A project is the security context for one software solution. It holds applications and roles. In the documentation's example, a point-of-sale platform is one project; its administration web portal, iOS app and Android app are applications inside it, and `admin`, `cashier` and `viewer` are roles shared by all of them.

A role has a Key, a Display Name and a Group. Only the key matters for role assignment, and it must be unique within the project. The key is what you read in code. The display name is for humans. The group lets you assign several roles at once in the console.

ZITADEL offers five application types, among them Web, Native, User Agent and API. Web, Native and User Agent involve user interaction; API is for machine-to-machine use. A server-side rendered app, including a NextJS app that runs server code, is a Web application and can hold a client secret.

New instances contain a Default Project named ZITADEL in the first organization. It protects the Management Console and APIs. Do not change its settings or host your own applications in it, because that can alter ZITADEL's own behavior. Create your own project under Projects with Create New Project.

## Checked

2026-11-08. Read in full: the projects page and the applications page. All claims confirmed.

Method: documentation only; no commands were run.
