---
id: computing-software.systems-network-administration.netbox.data-validation-field-choices
name: data-validation-field-choices
category: computing-software
field: systems-network-administration
product: netbox
tags: [custom-validators, field-choices, data-validation]
level: advanced
status: docs-checked
description: "Use CUSTOM_VALIDATORS and FIELD_CHOICES to enforce rules and extend choice sets."
sources: ["https://netboxlabs.com/docs/netbox/configuration/data-validation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Data validation parameters

Goal: enforce naming rules and adjust static choice fields in configuration.

**CUSTOM_VALIDATORS** maps models to validators. Entries may be a dictionary of field rules or a dotted path to a validator class:
```
CUSTOM_VALIDATORS = {
    "dcim.Site": [
        {"name": {"min_length": 5, "max_length": 30}},
        "my_plugin.validators.Validator1"
    ],
    "dcim.Device": ["my_plugin.validators.Validator1"]
}
```
Model identifiers are case-insensitive (`dcim.site` equals `dcim.Site`).

**FIELD_CHOICES** maps `app.Model.field` to choices. Each choice is a tuple of database value, label and color. Replace the stock choices:
```
FIELD_CHOICES = {
    'dcim.Site.status': (
        ('foo', 'Foo', 'red'),
        ('bar', 'Bar', 'green'),
    )
}
```
Append instead by adding a plus sign: `'dcim.Site.status+'`. A choice can also be a dictionary with `value` and `label` required, plus `color` and a description shown as a subtitle.


The dictionary form of a choice allows a description shown as a subtitle beneath the option, in addition to value, label and color.

Both parameters live in `configuration.py`, so changes take effect after the NetBox services are restarted.

**Checklist**

1. Use `+` to append.
2. Keep database values stable.
3. Test validators on a staging copy.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Data validation page: CUSTOM_VALIDATORS example, case-insensitive model names, FIELD_CHOICES tuple format, plus-sign append, dictionary format introduced in v4.7. Removed: Nothing.

Method: documentation only; no commands were run.
