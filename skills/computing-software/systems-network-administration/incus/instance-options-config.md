---
id: computing-software.systems-network-administration.incus.instance-options-config
name: instance-options-config
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, config-set, config-show, config-edit, instance-options, properties, live-update, rest-api]
level: practitioner
status: docs-checked
description: "Set, show and edit Incus instance options and properties with incus config set/show/edit and the equivalent PATCH/PUT API calls; live-update caveats."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/instances_configure.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instance options and properties

Options:
```
incus config set my-container limits.memory=8GiB
incus config show my-container --expanded
incus config edit my-container
```
- API: `PATCH /1.0/instances/<name>` with a `config` field; `PUT` with the full configuration for edit; `GET` to read.
- Some options apply live; others need a restart. The reference marks this as "Live update".
- Options can also be given at creation time.

Properties (root level, not under `config`):
```
incus config set <name> <key>=<value> --property
incus config get <name> <key> --property
incus config unset <name> <key> --property
```
- API: PATCH to set; to unset, PUT the whole configuration without the property.
- Read-only properties appear in output; edits to them are ignored.

Store reusable settings in profiles.

## Checked

2026-11-09. Confirmed against the Incus How to configure instances page: config set/show --expanded/edit, PATCH/PUT/GET calls, live update note, creation-time options, --property set/get/unset, property unset via PUT, read-only properties ignored, profiles. Nothing removed.
Method: documentation only; no commands were run.
