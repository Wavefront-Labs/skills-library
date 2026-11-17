---
id: computing-software.systems-network-administration.zabbix.preprocessing-pipeline
name: preprocessing-pipeline
category: computing-software
field: systems-network-administration
product: zabbix
tags: [preprocessing, custom-on-fail, unsupported-items, transformations, transformation, steps]
level: practitioner
status: docs-checked
description: "Transform item values before storage with ordered preprocessing steps and choose error handling per step."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/preprocessing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Preprocessing runs on the server, or on the proxy for proxied hosts, before a value is saved. Steps are set on the item's Preprocessing tab and execute in the configured order.

Key facts:
- All incoming values are treated as strings. Conversion to the item's type of information happens at the end of the pipeline, though some steps convert earlier.
- If a step fails the item becomes unsupported, unless you tick Custom on fail and choose Discard value, Set value to, or Set error to. With Discard value or Set value to, the item stays supported.
- Step types on the page are grouped as text, structured data (XML XPath, JSON Path, CSV to JSON, XML to JSON), SNMP, arithmetic (Custom multiplier), change, numeral systems, custom scripts (JavaScript), validation, throttling and Prometheus.
- A failed Regular expression step (no match) makes the item unsupported.
- Change and throttling steps remember the previous value. After a server or proxy restart, or an edit to the steps, that memory resets: the next Simple change or Change per second value is ignored, and the next Discard unchanged value is never discarded.

Test your preprocessing steps before relying on them; the docs describe a testing facility for this.

## Checked

2026-11-09. Confirmed against the Item value preprocessing page: server or proxy execution, ordered steps, unsupported on failure, Custom on fail options, strings-first conversion, transformation groups, the Change and Throttling reset behaviour, and the regular expression no-match failure. Removed: the Custom multiplier fraction-trimming claim (0.9 becomes 0) and the K, M, G prefix remark, which the page does not state (the details page was not read).
Method: documentation only; no commands were run.
