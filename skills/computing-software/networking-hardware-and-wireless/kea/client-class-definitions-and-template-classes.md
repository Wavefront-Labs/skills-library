---
id: computing-software.networking-hardware-and-wireless.kea.client-class-definitions-and-template-classes
name: client-class-definitions-and-template-classes
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, client-classes, template-test, spawn, vendor-class, only-in-additional-list]
level: advanced
status: docs-checked
description: "Define Kea client classes with test and template-test, built-in VENDOR_CLASS_, SPAWN_, HA_ and BOOTP classes, and additional-list evaluation."
sources:
  - https://kea.readthedocs.io/en/latest/arm/classify.html
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# client class definitions and template classes
A class in `client-classes` has a mandatory unique `name` and optional `test`, `template-test`, `option-data`, `option-def` and `only-in-additional-list` (replaces the deprecated `only-if-required`).

Built-in classes need no definition: a DHCPv4 vendor class identifier (option 60) or DHCPv6 vendor class (16) becomes `VENDOR_CLASS_<content>`, e.g. `VENDOR_CLASS_docsis3.0` (DHCPv6 uses only the first vendor class data field). Others: `HA_` prefix from the HA hook, `SPAWN_` for template classes, `BOOTP`, `SKIP_DDNS`.

Template classes: `template-test` yields a string; the spawned class is `SPAWN_<template-class-name>_<value>`. `test` and `template-test` are mutually exclusive in one class. Both the spawned class and the template class are associated with the packet, and `option-data` in a template class goes to the spawned class. Use `ifelse` in `template-test` to spawn classes only when needed.

```json
{ "name": "Client-ID", "template-test": "substring(option[61].hex,0,3)" }
```

Additional classification limits a class to a pool, subnet or shared network: list it in `evaluate-additional-classes` and set `only-in-additional-list` true so its test runs only then. Since 2.7.4 an additional class with no test is always added. Lifetimes set in such a class have no effect because evaluation follows lease assignment. Since 3.3.0 invalid characters in generated class names (vendor and spawned) are escaped with `%` plus two hex digits, and a configured name containing an invalid character logs a warning.

## Checked
2026-11-04. Confirmed against the Kea Administrator Reference Manual (Client Classification chapter and DHCPv4 chapter). Removed: the claim that an option in a spawned class beats the template's, and the claim that no class is made for an empty value.
Method: documentation only; no commands were run.
