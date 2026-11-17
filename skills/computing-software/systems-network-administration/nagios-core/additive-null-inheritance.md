---
id: computing-software.systems-network-administration.nagios-core.additive-null-inheritance
name: additive-null-inheritance
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, additive-inheritance, null-value, plus-prefix, implied-inheritance, templates, important-check-command]
level: advanced
status: docs-checked
description: "Nagios Core special inheritance values: null to cancel, + to append, ! for important check_command, and what services and escalations inherit implicitly."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/objectinheritance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Special inheritance values

- **`null`** as a string value cancels inheritance of that variable.
- **`+` prefix** on a local standard string value appends to the inherited value. `hostgroups +linux-servers,web-servers` over inherited `all-servers` gives `all-servers,linux-servers,web-servers`. Not for custom variables.
- **`!` prefix** on a service template's `check_command` marks it important so it overrides the command set on the service itself; mainly for distributed setups.

## Implied inheritance (no `use` needed)
- A service takes `contacts`, `contact_groups`, `notification_interval`, `notification_period` from its host if unset.
- Host and service escalations take `contact_groups`, `notification_interval`, and `escalation_period` (from the notification period) from the related object.
- An escalation whose `contact_groups` or `contacts` starts with `+` adds to the related object's values.

Basics in `computing-software.systems-network-administration.nagios-core.object-inheritance-templates`.

## Checked

2026-11-04. Confirmed against the Object Inheritance page: null cancels, + appends (standard string variables only), ! marks an important check_command, implied inheritance table and the escalation + rule. Removed an unconfirmed self-check line.

Method: documentation only; no commands were run.
