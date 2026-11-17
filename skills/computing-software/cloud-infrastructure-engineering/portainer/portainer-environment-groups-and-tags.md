---
id: computing-software.cloud-infrastructure-engineering.portainer.portainer-environment-groups-and-tags
name: portainer-environment-groups-and-tags
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [groups, tags, environments, organisation]
level: intro
status: docs-checked
description: "Organise Portainer environments with groups for access scoping and tags for searchable metadata."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/admin/environments/groups.md
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/admin/environments/tags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Groups organise environments, for example development, staging and production, and also define which environments are available to which users. Community Edition supports basic user and group assignments; more complex roles within groups need Business Edition.

Create a group from Environment-related, Groups, Add group. Fields are Name, an optional Description, Tags, and Associated environments (add or remove them from the table, then click Create).

Tags are metadata on environments, such as physical location, department or owner. Create a tag under Environment-related, Tags by entering a name and clicking Create tag. To tag an environment, open it from Environments, pick the tag in the Tags lookup and click Update environment. Tags show on the Portainer home page and you can search environments by tag.

You can also set a group or tags in the More settings section while adding an environment through the wizard, which saves a later edit.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. No wrong claims found; nothing removed.

Method: documentation only; no commands were run.
