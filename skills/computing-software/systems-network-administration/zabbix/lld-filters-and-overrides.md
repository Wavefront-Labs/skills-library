---
id: computing-software.systems-network-administration.zabbix.lld-filters-and-overrides
name: lld-filters-and-overrides
category: computing-software
field: systems-network-administration
product: zabbix
tags: [lld-filters, overrides, pcre, prototypes, lost-resources, filter, override, discovery]
level: advanced
status: docs-checked
description: "Restrict discovered entities with LLD filters and tailor prototypes per entity with ordered overrides."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/discovery/low_level_discovery
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Filters (rule level) decide which entities get real items, triggers and graphs. Each filter is an LLD macro plus an operator: matches, does not match (both PCRE, or a global regular expression), exists, does not exist. Calculation types: And, Or, And/Or (And across different macros, Or for the same macro), Custom expression (all filters must appear, up to 255 symbols).

If a macro in a filter is missing from the response, the entity is ignored unless a does not exist condition is set for it.

Example: macro {#FSNAME} with ^C|^D|^E keeps only C:, D: and E:. Use {#FSTYPE} (for example ^ext|^reiserfs) for types, and {#FSDRIVETYPE} on Windows for drive types. Test patterns with grep -E first.

Warning from the docs: a typo in the regex can cause deletion of thousands of configuration elements, historical values and events across many hosts. Combine with a sensible Delete lost resources period, and avoid Immediately.

Overrides modify prototypes or their attributes for entities that meet given criteria. They live in a drag-and-drop list and run in order. Each has:
- If filter matches: Continue overrides or Stop processing.
- Filters, evaluated after the rule filters.
- Operations on an object type: Item, Trigger, Graph, Host or Discovery prototype, with a condition on the object name.

Typical use: keep a trigger prototype only for certain mount points, or change severity or create-enabled state for one entity.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (discovery/low_level_discovery): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
