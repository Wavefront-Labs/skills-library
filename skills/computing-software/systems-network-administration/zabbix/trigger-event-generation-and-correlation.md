---
id: computing-software.systems-network-administration.zabbix.trigger-event-generation-and-correlation
name: trigger-event-generation-and-correlation
category: computing-software
field: systems-network-administration
product: zabbix
tags: [problem-event-generation, multiple-problems, tag-matching, ok-event-closes, multiple, correlation]
level: advanced
status: docs-checked
description: "Create multiple problems from one trigger and close them individually with tag-matched OK events."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/triggers/trigger
  - https://www.zabbix.com/documentation/current/en/manual/events/tagging
  - https://www.zabbix.com/documentation/current/en/manual/events/event_correlation/trigger
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Problem event generation mode has two settings:
- Single: a single event is generated when the trigger goes into the Problem state for the first time.
- Multiple: an event is generated upon every Problem evaluation of the trigger.

OK event closes has two settings:
- All problems: all problems of this trigger.
- All problems if tag values match: only those trigger problems with matching event tag values. This requires a Tag for matching, an event tag name.

Together they let one trigger track many independent conditions. The docs' log example: a log item (such as log[/var/log/syslog]), a trigger with PROBLEM event generation mode Multiple, and a tag whose value is extracted from the log line with a macro function such as service:{{ITEM.VALUE<N>}.regsub()}; then set OK event closes to All problems if tag values match and name the tag for matching. Each matching log line opens its own problem, and a later OK event closes only the problem with the same tag value. Such triggers are normally used for log monitoring, trap processing and similar.

Pitfall from the docs: indexed macros such as {ITEM.VALUE1} always refer to the trigger Expression, not the Recovery expression. If the recovery expression is based on a different item and the problem item's value changes by recovery time, the events get different tags and are not correlated.

Triggers can have trigger-level tags on the Tags tab. Problems inherit tags from the whole chain: templates, hosts, items or web scenarios, and triggers. Identical name and value pairs (after macro resolution) merge into one. A trigger does not inherit and display host-level tags in its own form.

Trigger tags support user macros, LLD macros (in trigger prototypes) and item-value macros. In trigger prototypes an LLD macro in a tag such as scope:{#FSNAME} gives every discovered trigger its own tag.

Multiple mode raises an event for every Problem evaluation, so test with realistic data volumes.

## Checked

2026-11-09. Confirmed against the trigger configuration page (event generation mode, OK event closes, Tag for matching, trigger tags tab), the Tagging page (inheritance, merging, macro support, LLD example) and the Trigger-based event correlation page (log example, indexed macro pitfall). The /manual/config/tagging source returned 404 and was replaced. Read the correlation page's configuration part only; its later cases were not read. Removed: the escalations claim.
Method: documentation only; no commands were run.
