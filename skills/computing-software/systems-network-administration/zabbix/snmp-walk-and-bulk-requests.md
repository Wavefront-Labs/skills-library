---
id: computing-software.systems-network-administration.zabbix.snmp-walk-and-bulk-requests
name: snmp-walk-and-bulk-requests
category: computing-software
field: systems-network-administration
product: zabbix
tags: [snmp-walk, getbulk, master-item, dependent-items, max-repetitions, walk, bulk]
level: advanced
status: docs-checked
description: "Collect many OIDs in one SNMP request with walk[] and feed dependent items, understanding timeout and retry behaviour."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/snmp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The walk[OID1,OID2,...] item retrieves subtrees using native SNMP GetBulkRequest PDUs (SNMP v2 and v3 only), asynchronously. Example: walk[1.3.6.1.2.1.2.2.1.2,1.3.6.1.2.1.2.2.1.3]. A GetBulk executes several GetNext operations in one response, which cuts round trips for both regular items and SNMP discovery.

Pattern: make the walk[] item the master item, then create dependent items that parse the result with SNMP walk value or SNMP walk to JSON preprocessing. One poll feeds many metrics. The preprocessing step "SNMP walk to JSON" is also usable for SNMP OID discovery.

Behaviour to remember:
- Up to five retries occur for bulk items if a packet is lost.
- The timeout in the item form covers the whole session. If the timeout hits, the request is retried with the timeout reset, so 3 seconds can mean a 15 second wait for an unreachable device. Keep the timeout low.
- If only some OIDs return, the item becomes unsupported with "Only partial data received".
- Max repetition (interface setting, default 10) applies to walk[] and discovery[].

Do not confuse native bulk requests with the interface option Use combined requests, Zabbix's own batching of legacy items. Combined processing batches at most 128 variable bindings per get, and walks with GetNext (v1) or GetBulk (v2 and v3) with max-repetitions of at most 128. Asynchronous get[] and walk[] items avoid combined-request pitfalls.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (config/items/itemtypes/snmp): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
