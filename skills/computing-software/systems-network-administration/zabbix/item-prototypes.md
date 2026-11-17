---
id: computing-software.systems-network-administration.zabbix.item-prototypes
name: item-prototypes
category: computing-software
field: systems-network-administration
product: zabbix
tags: [item-prototypes, trigger-prototypes, create-enabled, discover, lld-macro-in-key, prototype, item, lld]
level: practitioner
status: docs-checked
description: "Define item prototypes with mandatory LLD macros in the key and use Create enabled and Discover attributes."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/discovery/low_level_discovery/item_prototypes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
After creating a discovery rule, open its items and click Create item prototype. Prototypes become real items for each discovered entity.

Rules:
- An LLD macro is mandatory in the item key so each discovered item is unique, for example vfs.fs.size[{#FSNAME},free]. When the key has no parameters, put the macro inside brackets: v_[{#MACRO}].
- LLD macros and user macros work in prototype fields and preprocessing parameters. Regex and XPath preprocessing parameters get context-specific escaping of LLD macros.
- In update intervals a single macro must fill the whole field; multiple macros or macros mixed with text are not supported.

Prototype-specific attributes:
- Create enabled: unticked means items are created disabled.
- Discover: ticked by default; unticked means the item is not added to discovered entities unless an override changes it.

From the three-dot menu you can create a trigger prototype, list its trigger prototypes, or create a dependent item. Mass update works across prototypes.

Create several item prototypes, one for each metric you are interested in per discovered entity.

## Checked

2026-11-09. Confirmed against the Zabbix manual page Item prototypes (current): Create item prototype entry point, mandatory LLD macro in the key, v_[{#MACRO}] form, macro support and escaping in preprocessing, single-macro update interval rule, Create enabled and Discover attributes, three-dot menu entries, mass update. Removed the unsupported advice on user macros with LLD context in thresholds.

Method: documentation only; no commands were run.
