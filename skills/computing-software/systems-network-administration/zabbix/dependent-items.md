---
id: computing-software.systems-network-administration.zabbix.dependent-items
name: dependent-items
category: computing-software
field: systems-network-administration
product: zabbix
tags: [dependent-item, master-item, preprocessing, bulk-collection, dependent, master, item]
level: practitioner
status: docs-checked
description: "Collect once and split into many metrics using a master item plus dependent items with preprocessing."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/dependent_items
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A dependent item gets its value from a master item instead of polling. One query on the master populates many dependent items at once: a new master value automatically populates the dependent items.

Rules from the docs:
- The master item must exist first. Any item type, including another dependent item, can be a master, so you can add levels to extract smaller parts.
- A dependent item cannot have a different update interval than the master item; a new master value populates it.
- Use preprocessing on the dependent item (for example JSONPath) to pull out the needed part. Without preprocessing it receives the master value unchanged.
- Dependencies are allowed only within the same host or template. An item prototype may depend on another item prototype or a regular item of the same host.
- A dependent item on a host whose master comes from a template is not exported to XML.

Where it runs: the server, or the proxy if the host is proxied. Preprocessing is handled by the preprocessing manager with worker threads; values from pollers and trappers pass through it before reaching the history cache.

Configuration: create the master item, then create the dependent with Type = Dependent item, a key, the Master item, and the Type of information that fits the extracted data.

Typical use: an HTTP agent item returns one JSON document and several dependent items each extract a field with a JSONPath step. Deleting a master item also deletes its dependent items.

## Checked

2026-11-09. Confirmed against the Zabbix manual page Dependent items (current): bulk collection from one query, update interval rule, preprocessing manager and worker threads, server or proxy performing preprocessing, any item type as master, same host or template limitation, item prototype rule, XML export limitation, configuration fields, master deletion. Removed the list of master item types and the use-case examples the page does not state.

Method: documentation only; no commands were run.
