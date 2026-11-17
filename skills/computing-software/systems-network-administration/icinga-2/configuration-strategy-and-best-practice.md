---
id: computing-software.systems-network-administration.icinga-2.configuration-strategy-and-best-practice
name: configuration-strategy-and-best-practice
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, best-practice, apply-rules, templates, icinga-director, config-management]
level: practitioner
status: docs-checked
description: "Choose an Icinga 2 configuration strategy and when to prefer apply rules, templates, groups and custom variables over per-object definitions."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/04-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# configuration strategy and best practice
Ways to create objects: Icinga Director, an editor, a configuration management tool (Puppet, Chef, Ansible), or a custom exporter from a CMDB or inventory.

Decision questions from the docs:
- Hosts share a common group of services, or only a small set of users gets notifications for everything? Use apply rules.
- Need specific configuration per host/service, or your generator already knows the host-service relationship? Use object-level attributes such as `host_name`.

Layout ideas: tree by location/hostgroup/attribute, flat `hosts.conf` and `services.conf` for rule-based config, one file per host plus global groups and users, or one big generated file (called probably a bad idea for maintaining changes). Whatever you pick, `icinga2.conf` must include it.

Checks:
- Set describing attributes as `vars` custom variables for later assign/ignore rules or export.
- Put hosts in hostgroups and services in servicegroups and use them in apply rules.
- Use templates for generic attributes.
- Apply rules may overlap, so keep them in a central place (services.conf, notifications.conf) rather than deep in the tree.
- Every plugin used as check, notification or event command needs a Command definition.

For distributed setups decide up front what lives on the master (synced to other nodes) versus local configuration such as health checks.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/04-configuration/. No commands were run.
