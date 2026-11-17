---
id: computing-software.cybersecurity-defensive.wazuh.decoder-dynamic-fields
name: decoder-dynamic-fields
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [dynamic-fields, static-fields, decoder-order-size, order-tag, nested-fields]
level: advanced
status: docs-checked
description: "Use dynamic fields in Wazuh decoders via the order tag: dotted names nest JSON, the 14 static fields, the eight-field cap, the 64 field limit."
sources:
  - https://documentation.wazuh.com/current/user-manual/ruleset/decoders/dynamic-fields.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dynamic fields are extracted from log data during decoding; their number and names vary per message.

Naming: names listed in a decoder's `<order>` tag become JSON fields. Dots create nested objects, so `audit.auid` becomes `auid` under `audit`. Example: an auditd decoder with `<order>audit.auid,audit.session,audit.op</order>` yields `audit.auid`, `audit.session` and `audit.op` in the alert JSON.

Static fields (predefined): `user`, `srcuser`, `srcip`, `dstip`, `srcport`, `dstport`, `protocol`, `action`, `id`, `url`, `data`, `extra_data`, `status`, `system_name`. Only eight static fields can be populated at once. When more are present, Wazuh prioritises `user`, `srcip`, `dstip`, `srcport`, `dstport`, `protocol`, `action` and `id`.

Limit: a single `<order>` tag can extract up to 64 fields by default. Raise it with `analysisd.decoder_order_size` in `local_internal_options.conf`, copying the setting from `internal_options.conf`.

Gotcha: do not edit `internal_options.conf` directly, because upgrades overwrite it and the change is lost.

## Checked

2026-11-08: confirmed against the Wazuh docs page Dynamic fields (read in full): the 14 static fields, the eight-field limit and prioritised fields, dotted names becoming nested JSON, the auditd example, the 64-field default for decoder_order_size and the local_internal_options.conf procedure. Removed the unsupported design tip.
Method: documentation only; no commands were run.
