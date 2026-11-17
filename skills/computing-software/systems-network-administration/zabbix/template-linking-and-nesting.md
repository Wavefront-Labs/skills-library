---
id: computing-software.systems-network-administration.zabbix.template-linking-and-nesting
name: template-linking-and-nesting
category: computing-software
field: systems-network-administration
product: zabbix
tags: [templates, linking, nesting, unlink, uniqueness, template]
level: practitioner
status: docs-checked
description: "Link and nest templates safely: what gets inherited, uniqueness rules, and Unlink versus Unlink and clear."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/templates/linking
  - https://www.zabbix.com/documentation/current/en/manual/config/templates/nesting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Linking applies a template's entities to a host: items, triggers, graphs, low-level discovery rules, web scenarios and dashboards.

Uniqueness criteria decide what is updated rather than duplicated: items by key, triggers by name and expression, custom graphs by name and items. Existing identical entities on the host become template entities and lose host-level customisations. Host-only entities are untouched. Template entities are prefixed with the template name in lists.

Gotchas:
- Linking several templates with items of the same key to one host fails. Triggers and graphs using those items fail too.
- For external, HTTP agent, simple, SSH and Telnet checks the host interface is optional. If the host had no interface when you linked, the items stay without one even after you add an interface. Unlink the template and link it again to assign it.
- To keep item history, use Unlink, not Unlink and clear. Unlink removes only the association; Unlink and clear also removes the inherited entities.
- The predefined templates are for reference; they may poll too often or have too many items, so tune them before production use.

Nesting: link T1 and T2 to T3 and T3 gains their entities, not vice versa. Hosts linked to T3 inherit everything. Nested entities include items, triggers, graphs, LLD rules and web scenarios but exclude dashboards from the template form, although linked template dashboards are still inherited by hosts.

Bulk change: Data collection > Hosts, select hosts, Mass update > Link templates, with Replace, Unlink and Clear when unlinking options.

## Checked

2026-11-09. Confirmed against the Linking/unlinking and Nesting pages: linked entity types, uniqueness criteria, same-key failure, optional host interface and relink fix, Unlink versus Unlink and clear, predefined template caution, nesting behaviour and dashboards exception, Mass update options. Linking page read through the editing section only.
Method: documentation only; no commands were run.
