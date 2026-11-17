---
id: computing-software.cloud-infrastructure-engineering.portainer.docker-resource-access-control
name: docker-resource-access-control
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [access-control, ownership, labels, docker, swarm]
level: practitioner
status: docs-checked
description: "Control who can see Docker and Swarm resources deployed through Portainer, and grant access to external resources with labels."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/advanced/access-control.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All Docker and Swarm resources except images deployed through Portainer carry access control settings, which you set at deploy time or later. Resources created by a stack or service inherit the parent's access.

Three modes:

- Administrators only: only Portainer administrators see the resource and anything it creates (containers, services, volumes, networks, secrets).
- All users: access control disabled, every Portainer user has access.
- Restricted: choose specific teams and users.

Resources deployed outside Portainer are marked `external` and you have limited control. By default they are administrator-only. You can open them up with labels, for example:

- `io.portainer.accesscontrol.public`: all users; takes precedence over team and user assignments.
- `io.portainer.accesscontrol.teams=dev,prod`: restricted to those teams.
- `io.portainer.accesscontrol.users=bob,adam`: restricted to those users; can be combined with the teams label.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Added the users label; removed unconfirmed advice about team existence and migration.

Method: documentation only; no commands were run.
