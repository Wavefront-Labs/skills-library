---
id: computing-software.systems-network-administration.nagios-core.object-types-overview
name: object-types-overview
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, object-configuration, object-types, cfg-file, cfg-dir, sample-config, config-overview]
level: intro
status: docs-checked
description: "The Nagios Core object types (hosts, services, groups, contacts, commands, time periods, escalations, dependencies), how they relate and where they are loaded from."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/configobject.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object configuration overview

Objects are all the elements in monitoring and notification logic.

## Types
- **Hosts** and **services** (a host has one or more services); **host groups** and **service groups** collect them.
- **Contacts** and **contact groups**: who is notified, and how.
- **Commands**: programs run for checks, notifications, event handlers.
- **Time periods**: when checks run and contacts may be notified.
- **Escalations** and **dependencies** (notification and execution).

## Relationships
- Hosts can have `parents`, used by reachability logic.
- Services and hosts name contacts or contact groups to notify.

## Where they live
Defined in one or more files/directories named in `nagios.cfg` by `cfg_file=` and `cfg_dir=`. A quickstart install puts sample object files in `/usr/local/nagios/etc/objects/`; use them to see how inheritance works. Objects use a template format (see `computing-software.systems-network-administration.nagios-core.object-inheritance-templates`).

The page does not describe load ordering within a directory.

## Checked

2026-11-04. Confirmed against the Object Configuration Overview page (object types, cfg_file and cfg_dir, quickstart sample directory, template format, host parents for reachability, timeperiods and commands). Removed the invented sample file names and the unconfirmed nagios -v totals self-check.

Method: documentation only; no commands were run.
