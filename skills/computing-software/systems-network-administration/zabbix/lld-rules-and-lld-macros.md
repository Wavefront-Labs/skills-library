---
id: computing-software.systems-network-administration.zabbix.lld-rules-and-lld-macros
name: lld-rules-and-lld-macros
category: computing-software
field: systems-network-administration
product: zabbix
tags: [lld, low-level-discovery, lld-macros, jsonpath, vfs-fs-discovery, discovery, low-level]
level: practitioner
status: docs-checked
description: "Build a low-level discovery rule that returns JSON, maps custom LLD macros with JSONPath and tunes update interval."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/discovery/low_level_discovery
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Low-level discovery (LLD) finds entities such as file systems or network interfaces and creates items, triggers and graphs from prototypes. The rule's data must be a JSON array of objects, each one an entity, for example net.if.discovery returning [{"{#IFNAME}": "lo"}, {"{#IFNAME}": "eth0"}].

The rule form has five tabs in data-flow order: Discovery rule, Preprocessing, LLD macros, Filters, Overrides.

- Type can be a regular check or a dependent item on a master item; a rule cannot depend on another discovery rule.
- Key is up to 2048 characters, such as vfs.fs.discovery. vfs.fs.get is an alternative.
- Update interval: use a short value while testing, then 30 minutes or more since file systems rarely change. A new rule is checked within 60 seconds unless it has a custom interval with interval 0. Execute now runs it at once.
- Keys already in {#MACRO} form are usable directly. For JSON without them (vfs.fs.get), define LLD macros on the LLD macros tab, each mapped by JSONPath to a field. Values come from the result after preprocessing. Use bracket notation for special characters.

Delete lost resources and Disable lost resources set how soon entities no longer discovered are removed or disabled. Disable should exceed the update interval; Delete should exceed Disable. Manually disabled resources are never re-enabled or deleted by LLD.

Notes: several rules can use the same discovery item via the Alias agent parameter (vfs.fs.discovery[foo]). Rules can also create hosts and nest.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (discovery/low_level_discovery): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: the discovery JSON size-limit sentence (not on the page).

Method: documentation only; no commands were run.
