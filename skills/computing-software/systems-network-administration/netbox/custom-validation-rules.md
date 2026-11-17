---
id: computing-software.systems-network-administration.netbox.custom-validation-rules
name: custom-validation-rules
category: computing-software
field: systems-network-administration
product: netbox
tags: [custom-validators, custom-validation, min-length]
level: advanced
status: docs-checked
description: "Enforce naming and data rules with CUSTOM_VALIDATORS."
sources: ["https://netboxlabs.com/docs/netbox/customization/custom-validation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom validation

Goal: enforce local rules beyond NetBox's built-in checks.

Rules are a mapping of attributes to constraints, for example:

```json
{"name": {"min_length": 5, "max_length": 30}}
```

This runs after NetBox's own validation.

**Types:** `min`, `max` (numeric), `min_length`, `max_length`, `regex` (strings), `required`, `prohibited`, `eq`, `neq`. These supplement built-in validation and cannot override it: prohibiting a field NetBox requires will not work.

**Custom logic.** Subclass `CustomValidator`, override `validate()` and call `fail()`:

```python
from extras.validators import CustomValidator

class MyValidator(CustomValidator):
    def validate(self, instance, request):
        if instance.status == 'active' and not instance.description:
            self.fail("Active sites must have a description set!", field='status')
```

If `field` is given, the message appears on that field.

**Assign** in `CUSTOM_VALIDATORS`, keyed by model such as `dcim.site`. Three styles: plain JSON mapping, dotted path to a class, or direct class reference. Plain data is the most portable.

**Checklist**

1. Prefer plain JSON rules.
2. Use `fail()` with a field.
3. Key by `app.model`.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: Custom validation page: rule types, CustomValidator.validate()/fail() with field, CUSTOM_VALIDATORS keyed by model. Removed: Nothing.

Method: documentation only; no commands were run.
