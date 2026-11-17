---
id: computing-software.systems-network-administration.zabbix.tags-and-event-tags
name: tags-and-event-tags
category: computing-software
field: systems-network-administration
product: zabbix
tags: [tags, event-tags, problem-tags, action-conditions, service-mapping, event, tagging]
level: practitioner
status: docs-checked
description: "Use tags on templates, hosts, items and triggers to label problems for filtering, notifications, correlation and services."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/events/tagging
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A tag is a name with an optional value, such as mysql, target:mysql or service:jira. Tags can be set on templates, hosts, items, web scenarios, triggers, services, template items and triggers, and host, item and trigger prototypes.

A problem event inherits tags from the whole chain: templates, hosts, items or web scenarios, and triggers. Identical tag:value combinations (after macros resolve) are merged. The same name with different values (component:memory and component:storage), or a name with and without a value (database and database:postgresql), are not duplicates.

What tags are used for, per the docs:
- Filter Monitoring > Latest data (for example item tag component:cpu) and mark problems in Monitoring > Problems.
- Action conditions: send notifications only for events with matching tags, such as scope:security versus scope:availability.
- Event correlation based on tags, including closing problems individually with tag-matched OK events.
- Show tags in notifications with the {EVENT.TAGS} macro ({EVENT.TAGSJSON} gives a JSON array).
- Map problems to services by service problem tags, and match services to SLAs and service actions by service tags.
- Extract data into tag values from item values, for example tag-name:{{ITEM.VALUE<N>}.regsub()}. A tag name or value over 255 characters after macro resolution is truncated to 255.
- LLD trigger prototypes with a macro in the tag, such as scope:{#FSNAME}.
- Template tags so every trigger from a template carries the tag.
- Maintenance periods can suppress problems with defined tags, and user group tags limit which problems a group can view.

Guidance: choose a small consistent vocabulary of tag names (scope, component, service, target) across templates so filters and action conditions stay simple.

## Checked

2026-11-09. Confirmed against the Events and resolution > Tagging page: entity list, inheritance and merging, duplicates rule, use cases, macro support, 255-character truncation. The cited /manual/config/tagging URL returns 404, so the source was replaced with /manual/events/tagging. Removed: the unsupported claim that tag name matching in conditions is case-sensitive.
Method: documentation only; no commands were run.
